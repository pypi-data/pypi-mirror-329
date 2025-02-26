from urllib.parse import urljoin

import requests

from sentinalmon.models.metrics import InstanceMetric
from sentinalmon.models.server import ExporterInstance


class MasterClient:
    def __init__(self, host: str, port: int = 8001):
        self._host = host
        self._port = port
        self.session = requests.Session()

    @property
    def _base_url(self):
        return f"http://{self._host}:{self._port}"

    def _url(self, endpoint: str) -> str:
        return urljoin(self._base_url, endpoint)

    def _get(self, end_point: str, **kwargs):
        response = self.session.get(self._url(end_point), **kwargs)
        response.raise_for_status()
        return response

    def _post(self, end_point: str, **kwargs):
        response = self.session.get(self._url(end_point), **kwargs)
        response.raise_for_status()
        return response

    def get_instances(self) -> list[ExporterInstance] | None:
        try:
            response = self._get("/instances/")
            result = list()
            for instance in response.json():
                result.append(ExporterInstance(**instance))
            return result
        except requests.RequestException:
            return None

    def get_instance(self, instance_id) -> ExporterInstance | None:
        try:
            response = self._get(f"/instances/{instance_id}")
            return ExporterInstance(**response.json())
        except requests.RequestException:
            return None

    def get_hostname(self, instance_id):
        try:
            response = self._get(f"/instances/{instance_id}")
            return response.json()["hostname"]
        except requests.RequestException:
            return None

    def get_metrics(self, instance_id) -> InstanceMetric | None:
        try:
            response = self._get(f"/instances/{instance_id}/metrics")
            return InstanceMetric(**response.json())
        except requests.RequestException:
            return None
