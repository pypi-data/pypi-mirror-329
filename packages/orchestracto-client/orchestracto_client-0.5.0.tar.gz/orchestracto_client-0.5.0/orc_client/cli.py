import argparse
import datetime
import json
import os
import sys
from typing import Any

import yaml

from orc_client.client import OrcClient


def print_struct_data_json_indent(data: dict[str, Any]):
    print(json.dumps(data, indent=2))


def print_struct_data_json(data: dict[str, Any]):
    print(json.dumps(data))


def print_struct_data_yaml(data: dict[str, Any]):
    print(yaml.safe_dump(data))


def print_unstruct_data(*args: Any):
    print(*args)


class CannotReadWorkflowFromUserSource(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--format", default="yaml", choices=["json", "json_indent", "yaml"],
        help="Output format for structured data"
    )

    subparsers = parser.add_subparsers(dest="component")

    workflow_parser = subparsers.add_parser("workflow", help="Workflow management.")
    run_parser = subparsers.add_parser("run", help="Run management.")

    run_command = run_parser.add_subparsers(dest="command")

    create_run_parser = run_command.add_parser("create", help="Create a new run.")
    create_run_parser.add_argument("--wf-path", help="Path of workflow.", required=True)
    create_run_parser.add_argument("--label", action="append", help="Label for run.")
    create_run_parser.add_argument("--from-stdin", action="store_true",
                                          help="Read workflow from stdin in yaml format.")
    create_run_parser.add_argument("--from-file", help="Read workflow from yaml file.")

    stop_run_parser = run_command.add_parser("stop", help="Stop a run.")
    stop_run_parser.add_argument("--run-id", help="ID of run.", required=True)
    stop_run_parser.add_argument("--wf-path", help="Path of workflow.", required=True)

    get_run_parser = run_command.add_parser("get", help="Get a run.")
    get_run_parser.add_argument("--run-id", help="ID of run.", required=True)
    get_run_parser.add_argument("--wf-path", help="Path of workflow.", required=True)

    get_logs_parser = run_command.add_parser("get-logs", help="Get run's logs.")
    get_logs_parser.add_argument("--run-id", help="ID of run.", required=True)
    get_logs_parser.add_argument("--wf-path", help="Path of workflow.", required=True)
    get_logs_parser.add_argument("--step-id", help="ID of step.")

    restart_run_parser = run_command.add_parser("restart", help="Restart a run.")
    restart_run_parser.add_argument("--run-id", help="ID of run.", required=True)
    restart_run_parser.add_argument("--wf-path", help="Path of workflow.", required=True)
    restart_run_parser.add_argument("--restart-all", action="store_true", help="Restart all steps, including successful ones.")
    restart_run_parser.add_argument("--restart-step", action="append", help="Step (step_id) to restart.")

    workflow_command = workflow_parser.add_subparsers(dest="command")

    update_workflow_parser = workflow_command.add_parser("update", help="Update a workflow.")
    update_workflow_parser.add_argument("--wf-path", help="Path of workflow.", required=True)
    update_workflow_parser.add_argument("--do-not-create-secret-delegations", action="store_true", help="Do not create secret delegations.")
    update_workflow_parser.add_argument("--from-stdin", action="store_true", help="Read workflow from stdin in yaml format.")
    update_workflow_parser.add_argument("--from-file", help="Read workflow from yaml file.")
    update_workflow_parser.add_argument("--input-format", choices=["yaml", "json"], default="yaml",
                                        help="Input format for workflow.")

    validate_workflow_parser = workflow_command.add_parser("validate", help="Validate a workflow.")
    validate_workflow_parser.add_argument("--from-stdin", action="store_true", help="Read workflow from stdin in yaml format.")
    validate_workflow_parser.add_argument("--from-file", help="Read workflow from yaml file.")
    validate_workflow_parser.add_argument("--input-format", choices=["yaml", "json"], default="yaml",
                                        help="Input format for workflow.")

    get_runs_parser = workflow_command.add_parser("get-runs", help="Get workflow runs.")
    get_runs_parser.add_argument("--wf-path", help="Path of workflow.", required=True)
    get_runs_parser.add_argument("--limit", help="Number of runs to get.")
    get_runs_parser.add_argument("--start-dt", help="Start datetime (filter by created_at)")
    get_runs_parser.add_argument("--end-dt", help="End datetime (filter by created_at)")
    get_runs_parser.add_argument("--label", action="append", help="Label of run.")

    try:
        import orc_sdk
    except ImportError:
        pass
    else:
        from orc_sdk.processor import configure_arg_parser

        sdk_parser = subparsers.add_parser("sdk",  help="SDK processor.")
        sdk_parser = configure_arg_parser(sdk_parser)

    args = parser.parse_args()

    match args.format:
        case "json":
            print_struct_data = print_struct_data_json
        case "json_indent":
            print_struct_data = print_struct_data_json_indent
        case "yaml":
            print_struct_data = print_struct_data_yaml
        case _:
            raise ValueError(f"Unknown format: {args.format}")

    if "ORC_URL" not in os.environ:
        yt_proxy = os.environ.get("YT_PROXY")
        if yt_proxy is None:
            raise ValueError("Either ORC_URL or YT_PROXY environment variable should be set")
        orc_url = "https://orc." + yt_proxy.removeprefix("https://").removeprefix("http://")
    else:
        orc_url = os.environ["ORC_URL"]

    orc_client = OrcClient(orc_url=orc_url, yt_token=os.environ["YT_TOKEN"])

    def _get_workflow_dict(args: argparse.Namespace, allow_none: bool = False, input_format: str = "yaml") -> dict[str, Any]:
        workflow_dict: dict[str, Any] | None = None

        match input_format:
            case "yaml":
                load_data = yaml.safe_load
            case "json":
                load_data = json.loads
            case _:
                raise ValueError(f"Unknown input format: {input_format}")

        if args.from_stdin:
            data = sys.stdin.read()
            workflow_dict = load_data(data)
        elif args.from_file:
            with open(args.from_file, "r") as f:
                workflow_dict = load_data(f)
        else:
            if not allow_none:
                raise CannotReadWorkflowFromUserSource("Workflow source is not specified")
        return workflow_dict

    match args.component:
        case "run":
            match args.command:
                case "create":
                    workflow_dict = _get_workflow_dict(args, allow_none=True)
                    run_id = orc_client.create_run(workflow_path=args.wf_path, workflow=workflow_dict, labels=args.label)
                    print_struct_data({"run_id": run_id})
                case "stop":
                    orc_client.stop_run(run_id=args.run_id, workflow_path=args.wf_path)
                case "get":
                    info = orc_client.get_run(run_id=args.run_id, workflow_path=args.wf_path)
                    print_struct_data(info)
                case "get-logs":
                    logs = orc_client.get_logs(run_id=args.run_id, workflow_path=args.wf_path, step_id=args.step_id)
                    print_unstruct_data(logs["workflow_execution_log"])
                case "restart":
                    run_id = orc_client.restart_run(
                        run_id=args.run_id, workflow_path=args.wf_path,
                        restart_all=args.restart_all, restart_steps=args.restart_step,
                    )
                    print_struct_data({"run_id": run_id})
        case "workflow":
            match args.command:
                case "update":
                    workflow_dict = _get_workflow_dict(args, allow_none=True)
                    orc_client.update_workflow(
                        workflow_path=args.wf_path, workflow=workflow_dict,
                        create_secret_delegations=not args.do_not_create_secret_delegations,
                    )
                case "validate":
                    workflow_dict = _get_workflow_dict(args)
                    validation_resp = orc_client.validate_workflow(workflow_dict)
                    print_struct_data(validation_resp)
                case "get-runs":
                    start_dt = datetime.datetime.fromisoformat(args.start_dt) if args.start_dt else None
                    end_dt = datetime.datetime.fromisoformat(args.end_dt) if args.end_dt else None
                    runs = orc_client.get_runs(
                        workflow_path=args.wf_path, limit=args.limit,
                        start_dt=start_dt, end_dt=end_dt,
                        labels=args.label,
                    )
                    print_struct_data(runs["runs"])

        case "sdk":
            import orc_sdk.processor
            orc_sdk.processor.process_args(args)

if __name__ == "__main__":
    main()
