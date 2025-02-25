import argparse
import datetime
import importlib.resources
import io
import json
import logging
import logging.config
import os
import pathlib
import platform
import random
import ssl
import stat
import sys
import time
import uuid

from attrs import asdict
import backoff
from rich import print_json

from invariant_client import auth, display, zip_util
from invariant_client import pysdk
from invariant_client.aws_pruner_integration import use_aws_pruner
from invariant_client.bindings.invariant_instance_client.models.snapshot_report_data import SnapshotReportData
from invariant_client.display import OutputFormat
from invariant_client.version import VersionClient


logger = logging.getLogger(__name__)


CREDS_FILE_PATH = pathlib.Path.cwd()
try:
    CREDS_FILE_PATH = pathlib.Path.home()
except RuntimeError:
    pass
finally:
    CREDS_FILE_PATH = CREDS_FILE_PATH.joinpath('.invariant_creds')


class UploadTerminationError(Exception):
    """An exception that is raised when a snapshot upload is terminated."""

    def __init__(self, *args, retry_after: int):
        super().__init__(self, *args)
        self.retry_after = retry_after


def parse_args():
    parser = argparse.ArgumentParser(
        prog='invariant',
        description='Invariant analyzes network snapshots',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title='available commands',
        description='Run [command] --help for more information.',
        dest='command')
    command_login       = subparsers.add_parser(
        'login',
        description='Authenticate by opening a link in your browser. Saves credentials to ~/.invariant_creds.',
        help="Authenticate by opening a link in your browser. Saves credentials to ~/.invariant_creds.")
    command_run         = subparsers.add_parser(
        'run',
        description='Analyze the current directory.',
        help="Analyze the current directory.")
    command_show        = subparsers.add_parser(
        'show',
        description='Examine Invariant analysis results.',
        help="Examine Invariant analysis results.")
    # command_solution    = subparsers.add_parser(
    #     'show_solution',
    #     description='Display a suggested patch result.',
    #     help="Display a suggested patch result.")
    command_snapshots   = subparsers.add_parser(
        'snapshots',
        description='List prior snapshot analysis results.',
        help="List prior snapshot analysis results.")

    def add_debug(parser: argparse.ArgumentParser):
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help='Enable detailed logging.',
        )
    add_debug(command_login)
    add_debug(command_run)
    add_debug(command_snapshots)
    add_debug(command_show)

    def add_common_arguments(parser: argparse.ArgumentParser, allow_tsv: bool = True, allow_condensed: bool = True):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--json',
            dest='json',
            action='store_true',
            help='Output data as JSON.',
        )
        group.add_argument(
            '--fast-json',
            dest='fast_json',
            action='store_true',
            help='Output data as JSON (unformatted).',
        )

        if allow_tsv:
            group.add_argument(
                '--tsv',
                dest='tsv',
                action='store_true',
                help='Output data as TSV.',
            )

        if allow_condensed:
            group.add_argument(
                '--condensed',
                dest='condensed',
                action='store_true',
                help='Output only snapshot ID and outcome.',
            )

    add_common_arguments(command_run, allow_tsv=False)
    add_common_arguments(command_snapshots, allow_condensed=False)
    add_common_arguments(command_show)

    command_run.add_argument(
        '--compare-to',
        dest='compare_to',
        help='Compare this snapshot to another by its git ref. Ref must refer to the primary git repository.',
    )

    command_run.add_argument(
        '--target',
        dest='target',
        help='An Invariant project root directory. Default is current directory.',
    )

    command_run.add_argument(
        '--network',
        dest='network',
        help='The name of the network being evaluated.',
    )

    command_run.add_argument(
        '--role',
        dest='role',
        help='The network role being evaluated, e.g. "live", "intended".',
    )

    # AWS Pruner:
    # The pruner will run if invariant/aws_pruner.yaml exists in the snapshot directory.
    # The user can disable the pruner with --no-aws-pruner or enabled: False in the config.
    # The user can set --aws-pruner-preview=<dir> to write the pruned snapshot to a directory. It can be combined with --no-aws-pruner or enabled: False .
    # The pruner will write the pruned snapshot to a tempdir and not modify the original.
    command_run.add_argument(
        '--no-aws-pruner',
        dest='no_aws_pruner',
        action='store_true',
        help='Do not use the AWS pruner.'
    )

    command_run.add_argument(
        '--aws-pruner-debug-out',
        nargs='?',
        dest='aws_pruner_output_directory',
        const='./aws_pruner_debug',  # Value when --aws-pruner-debug-out is present but has no value
        default=None,  # Value when --aws-pruner-debug-out is NOT present
        help='Specify a directory to write the pruned snapshot for preview purposes. Default is ./aws_pruner_debug/ . Performs a dry-run if --no-aws-pruner is set or the pruner is disabled in aws_pruner.yaml .'
    )

    command_snapshots.add_argument(
        '--network',
        dest='network',
        help='Filter snapshots by network.',
    )

    command_snapshots.add_argument(
        '--role',
        dest='role',
        help='Filter by network role being evaluated, e.g. "live", "intended".',
    )

    command_show.add_argument(
        'file_name',
        nargs="?",
        help='The snapshot file to examine.'
    )

    command_show.add_argument(
        '--snapshot',
        dest='snapshot_name',
        help='The snapshot to examine. If unset, environment variable INVARIANT_SNAPSHOT is used.'
    )

    command_run.add_argument(
        '--no-upload-limit',
        dest='no_upload_limit',
        action='store_true',
        help='Disable the 40MB upload limit for snapshots.',
    )

    # command_solution.add_argument(
    #     'snapshot_name',
    #     help='The snapshot to examine.'
    # )

    # command_solution.add_argument(
    #     'solution_name',
    #     help='The solution to examine.'
    # )

    parser.add_argument(
        '--version',
        dest='version',
        action='store_true',
        help="Display the client and server version.")

    args = parser.parse_args()

    command = getattr(args, 'command')
    if not command and not args.version:
        parser.print_help()
        exit(0)

    return args


def serialize(inst, field, value):
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def configure_logging(debug: bool):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "incremental": True,
                "loggers": {
                    "multipart.multipart": {"level": "INFO"},
                },
            }
        )
    try:
        import rich.console
        import rich.logging
        root_logger = logging.getLogger()
        rich_handler = rich.logging.RichHandler(
            rich_tracebacks=True,
            omit_repeated_times=False,
            tracebacks_show_locals=True,
            tracebacks_suppress=[],
            show_time=False,
            show_path=False,
            console=rich.console.Console(stderr=True),
        )
        root_logger.addHandler(rich_handler)
    except ImportError:
        pass

    
def EntryPoint():
    args = parse_args()

    if args.version:
        command = None
        format = None
    else:
        command = getattr(args, 'command')
        format = OutputFormat.TABULATE
        if getattr(args, 'json', False):
            format = OutputFormat.JSON
        elif getattr(args, 'fast_json', False):
            format = OutputFormat.FAST_JSON
        elif getattr(args, 'tsv', False):
            format = OutputFormat.TSV
        elif getattr(args, 'condensed', False):
            format = OutputFormat.CONDENSED
        
    debug = getattr(args, 'debug', False)
    configure_logging(debug)
    
    try:
        EntryPoint_inner(args, command, format, debug)
    except Exception as e:
        if debug:
            raise e
        print('Error: %s' % e, file=sys.stderr)
        exit(1)


def EntryPoint_inner(args, command, format, debug):
    settings: pysdk.Settings = {
        'format': format,
        'debug': debug,
    }

    env = dict(os.environ)
    invariant_domain = env.get('INVARIANT_DOMAIN', 'https://prod.invariant.tech')
    env_snapshot = env.get('INVARIANT_SNAPSHOT', None)

    creds = None

    if args.version:
        with importlib.resources.path(__package__, 'VERSION') as data_path:
            with open(data_path, 'r') as f:
                print(f"client: {f.read().strip()}")
        print(f"server: {VersionClient(invariant_domain, ssl.create_default_context()).get_version()}")
        return

    if command == 'login':
        # TODO warn before logging in if an API token is present (possibly check if it works?)
        workflow = auth.BrowserLoginFlow(invariant_domain, ssl.create_default_context())
        link = workflow.start()
        print("Open this link in your browser to log in:")
        print(link)
        try:
            end_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
            # time.sleep(10)  # poor man's websocket
            time.sleep(6)  # poor man's websocket
            # TODO consider a nice animated "waiting" message for interactive terminal
            while not creds and end_time > datetime.datetime.now():
                result = workflow.poll_await_browser_creds()
                if isinstance(result, pysdk.AccessCredential):
                    creds = result
                    break
                elif isinstance(result, int):
                    time.sleep(result)
                else:
                    time.sleep(2)
            if not creds:
                print("Timed out.", file=sys.stderr)
                exit(1)
            with open(CREDS_FILE_PATH, 'w') as f:
                f.write(creds.to_json())
            CREDS_FILE_PATH.chmod(
                stat.S_IRUSR |
                stat.S_IWUSR
            )
            sdk = pysdk.Invariant(
                creds=creds,
                settings=settings,
                base_url=invariant_domain)
            status = sdk.status()
            print(f"Logged in as {status.user.email} (tenant={creds.organization_name}).")
        except KeyboardInterrupt as e:
            print("Exiting...", file=sys.stderr)
            exit(1)

        exit(0)
    
    # Load credentials or error
    try:
        creds = pysdk.AccessCredential.from_env(env, base_url=invariant_domain)
        if not creds:
            try:
                creds = pysdk.AccessCredential.from_file(CREDS_FILE_PATH, base_url=invariant_domain)
            except FileNotFoundError:
                # Expected
                creds = None
            if not creds:
                print("Please run 'invariant login' to authenticate.", file=sys.stderr)
                exit(1)

    except pysdk.AuthorizationException as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please run 'invariant login' to authenticate.", file=sys.stderr)
        if debug:
            raise e
        exit(1)
    except pysdk.RemoteError as e:
        print(f"Error: {e}", file=sys.stderr)
        if debug:
            raise e
        exit(1)

    sdk = pysdk.Invariant(
        creds=creds,
        settings=settings,
        base_url=invariant_domain)

    if command == "run":
        target = getattr(args, 'target') or '.'
        network = getattr(args, 'network') or ''
        role = getattr(args, 'role') or ''

        bytes = None
        if pathlib.Path(target).is_file():
            with open(target, "rb") as f:
                bytes = io.BytesIO(f.read())
        elif pathlib.Path(target).is_dir():
            if not pathlib.Path(target, 'configs').is_dir() and not pathlib.Path(target, 'aws_configs').is_dir():
                print(f"Invalid directory. Expected subdirectories 'configs' or 'aws_configs' to be present. See https://docs.invariant.tech/Reference/Snapshots for instructions.", file=sys.stderr)
                exit(1)
            home_dir = ''
            if platform.system() == 'Windows':
                home_dir = pathlib.Path(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'])
            else:
                home_dir = os.environ['HOME']
            if pathlib.Path(target).absolute() == pathlib.Path(home_dir).absolute():
                print("Upload aborted. Cowardly refusing to upload your home directory.")
                exit(1)
            bytes = io.BytesIO()
            BYTES_LIMIT = 40000000
            if getattr(args, 'no_upload_limit', False):
                BYTES_LIMIT = 0
            zip_util.zip_dir(target, bytes, BYTES_LIMIT)  # Write a zip file into 'bytes'
        else:
            print("Unacceptable target", file=sys.stderr)
            print(str(target), file=sys.stderr)
            exit(1)
        compare_to = getattr(args, 'compare_to')

        # Optionally process the snapshot using the pruner
        if getattr(args, 'aws_pruner_output_directory') or not getattr(args, 'no_aws_pruner'):
            pruner_debug_target = pathlib.Path(target, getattr(args, 'aws_pruner_output_directory')) if getattr(args, 'aws_pruner_output_directory') else None
            bytes = use_aws_pruner(bytes, getattr(args, 'no_aws_pruner'), pruner_debug_target)

        try:
            exec_uuid = upload_snapshot(sdk, bytes, compare_to, network, role, format)
        except KeyboardInterrupt as e:
            print("Exiting...", file=sys.stderr)
            exit(1)

        if format == OutputFormat.TABULATE:
            print("Analysis complete.")
        response = sdk.snapshot_detail(exec_uuid)
        # pprint.pprint(asdict(response), width=200)
        if format == OutputFormat.JSON or format == OutputFormat.FAST_JSON:
            response_json = json.dumps(response.to_dict(), sort_keys=True)
            try:
                print_json(response_json)
            except:
                print(response_json)
        elif format == OutputFormat.CONDENSED:
            if response.status['state'] != 'COMPLETE':
                if response.summary['errors'] > 0:
                    errors_locator = response.report.reports.errors
                    errors_response = sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, format)
            display.snapshot_condensed_status(response)
        else:
            display.snapshot_status(response)
            if response.status['state'] == 'COMPLETE':
                display.snapshot_halted(response)
                print('')
                summary = sdk.snapshot_detail_text(str(exec_uuid), json_mode=False)
                if summary.text:
                    print(summary.text)
                else:
                    display.snapshot_summary_table(response, format)

                print(f"\nRun 'invariant show <file>' to examine any file.")

                if response.summary['errors'] > 0:
                    print(f"\n{response.summary['errors']} {'error' if response.summary['errors'] == 1 else 'errors'} found.")
                    errors_locator = response.report.reports.errors
                    errors_response = sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, format)

            else:
                if response.summary['errors'] > 0:
                    errors_locator = response.report.reports.errors
                    errors_response = sdk.snapshot_file(errors_locator)
                    display.snapshot_errors(errors_response, format)

    elif command == "snapshots":
        network = getattr(args, 'network') or None
        role = getattr(args, 'role') or None
        snapshots = sdk.list_snapshots(
            filter_net=network,
            filter_role=role)
        snapshots_dict = {report.uuid: {"report": asdict(report, value_serializer=serialize), "extras": None} for report in snapshots.reports}
        for extras in snapshots.with_extras:
            record = snapshots_dict.get(extras.report_uuid, None)
            if not record:
                continue
            record["extras"] = asdict(extras, value_serializer=serialize)
        snapshots = list(snapshots_dict.values())
        if format == OutputFormat.JSON:
            print_json(data=snapshots, default=vars)
        elif format == OutputFormat.FAST_JSON:
            print(json.dumps(snapshots, default=vars))
        else:
            report_table = []
            skip_extras = ["errors_lines", "report_uuid", "additional_properties"]
            if network is not None:
                skip_extras.append("network_name")
            for row in snapshots:
                out = {k: v for k, v in row["report"].items() if k not in ["reports", "organization_uuid", "network_uuid", "metadata", "additional_properties"]}
                out.update({k: v for k, v in row["extras"].items() if k not in skip_extras})
                report_table.append(out)
            display.print_frame(report_table, format)

    elif command == "show":
        snapshot_name = args.snapshot_name
        if not snapshot_name:
            snapshot_name = env_snapshot
        if not snapshot_name:
            # NOTE: API Token users should explicitly set --snapshot or INVARIANT_SNAPSHOT
            last_snapshot = sdk.list_snapshots(filter_session=True, limit=1)
            if not last_snapshot or len(last_snapshot.reports) == 0:
                raise ValueError(f"Use --snapshot <name> argument or INVARIANT_SNAPSHOT environment variable to select a snapshot.")
            snapshot_name = last_snapshot.reports[0].uuid

        try:
            exec_uuid = uuid.UUID(snapshot_name, version=4)
        except ValueError as e:
            raise ValueError(f"Expected {snapshot_name} to be a UUID like f5b4e387-e336-499e-b3a0-d6186c590572.") from e

        if args.file_name is not None:
            # Access a specific file
            try:
                file = uuid.UUID(args.file_name, version=4)
            except ValueError:
                # OK if the file is the file key (e.g. errors)
                file = args.file_name
            if not isinstance(file, uuid.UUID):
                # Resolve non-UUID file to UUID
                response = sdk.snapshot_detail(exec_uuid)
                reports = response.report.reports
                try:
                    file_locator: str = getattr(reports, file)
                except AttributeError as e:
                    if not isinstance(reports, SnapshotReportData):
                        raise ValueError(f"Report {file} not found for snapshot {exec_uuid}.") from e
                    try:
                        file_locator: str = reports.files[file]
                    except KeyError as e:
                        raise ValueError(f"Report {file} not found for snapshot {exec_uuid}.") from e

            if format == OutputFormat.JSON or format == OutputFormat.FAST_JSON:
                file_data = sdk.snapshot_file(file_locator)
                if format == OutputFormat.JSON:
                    print_json(file_data.to_json(orient='records'))
                elif format == OutputFormat.FAST_JSON:
                    print(file_data.to_json(orient='records'))

            elif format == OutputFormat.TSV:
                file_data = sdk.snapshot_file(file_locator)
                display.print_frame(file_data, format)
            else:
                file_data = sdk.snapshot_file(file_locator)
                display.print_frame(file_data, format)
                # print("Set --traces to display all example traces")
                print("Set --json to get JSON")
                print("See 'show --help' for more options")

        else:
            # Display the process summary for the snapshot
            if format == OutputFormat.TABULATE:
                print(f"Snapshot {exec_uuid}")
            elif format == OutputFormat.CONDENSED:
                print(f"snapshot: {exec_uuid}")
            response = sdk.snapshot_detail(str(exec_uuid))
            if format == OutputFormat.TABULATE:
                display.snapshot_status(response)
            if format == OutputFormat.CONDENSED:
                if response.status['state'] != 'COMPLETE':
                    if response.summary['errors'] > 0:
                        errors_locator = response.report.reports.errors
                        errors_response = sdk.snapshot_file(errors_locator)
                        display.snapshot_errors(errors_response, format)
                display.snapshot_condensed_status(response)
            elif response.status['state'] == 'COMPLETE':
                if format == OutputFormat.TABULATE:
                    display.snapshot_halted(response)
                    print('')
                    summary = sdk.snapshot_detail_text(str(exec_uuid), json_mode=False)
                    if summary.text:
                        print(summary.text)
                    else:
                        display.snapshot_summary_table(response, format)
                elif format == OutputFormat.JSON or format == OutputFormat.FAST_JSON:
                    summary = sdk.snapshot_detail_text(str(exec_uuid), json_mode=True)
                    if summary.json:
                        if format == OutputFormat.JSON:
                            try:
                                print_json(summary.json)
                            except:
                                print(summary.json)
                        elif format == OutputFormat.FAST_JSON:
                            print(summary.json)
                    else:
                        display.snapshot_summary_table(response, format)
                else:
                    display.snapshot_summary_table(response, format)
                if format == OutputFormat.TABULATE:
                    print(f"\nRun 'invariant show <file>' to examine any file.")

                    if response.summary['errors'] > 0:
                        print(f"\n{response.summary['errors']} {'error' if response.summary['errors'] == 1 else 'errors'} found.", file=sys.stderr)
                        errors_locator = response.report.reports.errors
                        errors_response = sdk.snapshot_file(errors_locator)
                        display.snapshot_errors(errors_response, format)
            elif response.summary['errors'] > 0:
                errors_locator = response.report.reports.errors
                errors_response = sdk.snapshot_file(errors_locator)
                display.snapshot_errors(errors_response, format)

    elif command == "show_solution":
        sdk.show_solution(
            snapshot=args.snapshot_name,
            solution=args.solution_name)

    else:
        print(f"Unknown command {command}", file=sys.stderr)


DEFAULT_RETRY_SECONDS = 3


@backoff.on_exception(
        backoff.runtime,
        UploadTerminationError,
        value=lambda e: e.retry_after + random.uniform(0, e.retry_after),
        jitter=None,
        logger=None,
        on_backoff=lambda _: logger.warning('Upload was remotely terminated, retrying...'),
        max_tries=3)
def upload_snapshot(sdk: pysdk.Invariant, bytes: io.BytesIO, compare_to: str, network: str, role: str, format: OutputFormat) -> str:
    if format == OutputFormat.TABULATE:
        print("Uploading snapshot...")
    exec_uuid = sdk.upload_snapshot(
        source=bytes,
        network=network,
        role=role,
        compare_to=compare_to)
    exec_uuid = exec_uuid.exec_uuid
    end_time = datetime.datetime.now() + datetime.timedelta(weeks=1)
    if format == OutputFormat.TABULATE:
        print(f"Processing... ({exec_uuid})")
    elif format == OutputFormat.CONDENSED:
        print(f"snapshot: {exec_uuid}")
    while datetime.datetime.now() < end_time:
        response = sdk.upload_is_running(exec_uuid)
        if response.terminated:
            raise UploadTerminationError(f"Upload was remotely terminated, try again later", retry_after=response.retry_after_seconds or DEFAULT_RETRY_SECONDS)
        if not response.is_running:
            break

        # TODO send some RetryAfter header to control this
        # TODO separately, exponential back-off on error
        time.sleep(4)
    if not response:
        print("Timed out.", file=sys.stderr)
        exit(1)
    return exec_uuid