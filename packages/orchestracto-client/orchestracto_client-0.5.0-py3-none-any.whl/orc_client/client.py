import dataclasses
import datetime
from typing import Any

import requests


@dataclasses.dataclass
class OrcClient:
    orc_url: str = dataclasses.field()
    yt_token: str = dataclasses.field(repr=False)

    def _make_request(
            self, method: str, url: str,
            params: dict[str, Any] | None = None, json_data: dict[str, Any] | None = None) -> requests.Response:
        return requests.request(
            method=method, url=f"{self.orc_url}/{url}",
            headers={"Authorization": f"OAuth {self.yt_token}"},
            params=params, json=json_data,
            timeout=30,
        )

    def create_run(
            self, workflow_path: str, params: dict[str, Any] | None = None,
            workflow: dict[str, Any] | None = None, labels: dict[str, str] | None = None,
    ) -> str:
        req_data = {
            "workflow_path": workflow_path,
        }
        if params is not None:
            req_data.update({"params": params})
        if labels is not None:
            req_data.update({"labels": labels})
        if workflow is not None:
            req_data.update({"workflow": workflow})

        resp = self._make_request(
            "POST", "api/v1/create_run",
            json_data=req_data,
        )
        resp.raise_for_status()
        return resp.json()["run_id"]

    def restart_run(
            self, run_id: str, workflow_path: str,
            restart_all: bool, restart_steps: list[str] | None = None,
    ) -> str:
        req_data = {
            "workflow_path": workflow_path,
            "run_id": run_id,
            "restart_all": restart_all,
        }
        if restart_steps is not None:
            req_data.update({"restart_steps": restart_steps})
        resp = self._make_request(
            "POST", "api/v1/restart_run",
            json_data=req_data,
        )
        resp.raise_for_status()
        return resp.json()["run_id"]

    def stop_run(self, run_id: str, workflow_path: str) -> None:
        req_data = {
            "workflow_path": workflow_path,
            "run_id": run_id,
        }

        resp = self._make_request(
            "POST", "api/v1/stop_run",
            json_data=req_data,
        )
        resp.raise_for_status()

    def get_run(self, workflow_path: str, run_id: str) -> dict[str, Any]:
        resp = self._make_request(
            "GET", "api/v1/get_run",
            params={"workflow_path": workflow_path, "run_id": run_id},
        )
        resp.raise_for_status()
        return resp.json()

    def get_runs(
            self, workflow_path: str, limit: int | None = None,
            start_dt: datetime.datetime | None = None, end_dt: datetime.datetime | None = None,
            labels: list[str] | None = None,
    ) -> dict[str, Any]:
        params = {"workflow_path": workflow_path}

        if start_dt is not None:
            params["start_dt"] = start_dt.isoformat()

        if end_dt is not None:
            params["end_dt"] = end_dt.isoformat()

        if limit is not None:
            params["limit"] = limit

        if labels:
            params["labels"] = ",".join(labels)

        resp = self._make_request(
            "GET", "api/v1/get_runs",
            params=params,
        )
        resp.raise_for_status()
        return resp.json()

    def get_logs(self, workflow_path: str, run_id: str, step_id: str | None = None) -> dict[str, Any]:
        resp = self._make_request(
            "GET", "api/v1/get_logs",
            params={"workflow_path": workflow_path, "run_id": run_id, "step_id": step_id},
        )
        resp.raise_for_status()
        return resp.json()

    def update_workflow(
            self, workflow_path: str, workflow: dict[str, Any] | None = None,
            create_secret_delegations: bool = True,
    ):
        req_data = {
            "workflow_path": workflow_path,
            "create_secret_delegations": create_secret_delegations,
        }
        if workflow is not None:
            req_data.update({"workflow": workflow})

        resp = self._make_request(
            "POST", "api/v1/update_workflow",
            json_data=req_data,
        )
        resp.raise_for_status()

    def validate_workflow(self, workflow: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._make_request(
            "POST", "api/v1/validate_workflow",
            json_data=workflow,
        )
        resp.raise_for_status()
        return resp.json()
