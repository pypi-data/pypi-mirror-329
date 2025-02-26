import json
import threading
from datetime import UTC, datetime

import requests
import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic.v1.json import pydantic_encoder

from sentinalmon.collectors.base import InstanceCollectors
from sentinalmon.master.collectors import RemoteMetricCollector
from sentinalmon.models import (
    CpuMetric,
    ExporterInstance,
    NetworkMetric,
    RamMetric,
    StorageMetric,
)
from sentinalmon.models.server import HealthResponse, MetricType, RegistrationResponse


class Master:
    HEALTH_CHECK_INTERVAL = 15
    HEALTH_CHECK_TIMEOUT = 5
    DEFAULT_HOST = "0.0.0.0"
    DEFAULT_PORT = 8001

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT) -> None:
        self.app = FastAPI()
        self.router = APIRouter()
        self.setup_routes()
        self.app.include_router(self.router)
        self.server = uvicorn.Server(uvicorn.Config(self.app, host=host, port=port))
        self.instances: dict[str, ExporterInstance] = {}
        self.collectors: dict[ExporterInstance, InstanceCollectors] = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self.liveliness = threading.Thread(target=self.unregister)

    def setup_routes(self):
        @self.router.post("/register", response_model=RegistrationResponse)
        def register_instance(instance: ExporterInstance):
            try:
                if instance.id in self.instances:
                    return {
                        "status": "success",
                        "message": f"Machine {instance.hostname} already registered",
                    }

                collectors = InstanceCollectors(
                    cpu=RemoteMetricCollector[CpuMetric](instance, CpuMetric),
                    memory=RemoteMetricCollector[RamMetric](instance, RamMetric),
                    storage=RemoteMetricCollector[StorageMetric](
                        instance, StorageMetric
                    ),
                    network=RemoteMetricCollector[NetworkMetric](
                        instance, NetworkMetric
                    ),
                )
                collectors.start()

                with self._lock:
                    self.collectors[instance] = collectors
                    self.instances[instance.id] = instance
                print(f"Machine {instance.hostname} registered successfully")
                return {
                    "status": "success",
                    "message": f"Machine {instance.hostname} registered successfully",
                }
            except Exception as e:
                print(f"Error registering instance: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

        @self.router.get("/instances/")
        def get_instances() -> list[ExporterInstance]:
            return list(self.instances.values())

        @self.router.get("/instances/{instance}")
        def get_instance(instance: str) -> ExporterInstance:
            if instance not in self.instances:
                raise HTTPException(status_code=404, detail="Instance not exists")
            return json.loads(
                json.dumps(self.instances[instance], default=pydantic_encoder)
            )

        async def get_instance_by_id(instance_id: str):
            if instance_id not in self.instances:
                raise HTTPException(status_code=404, detail="Instance not found")
            return self.instances[instance_id]

        @self.router.get("/instances/{instance_id}/metrics")
        def get_instance_metrics(
            instance: ExporterInstance = Depends(get_instance_by_id),
        ) -> dict[str, CpuMetric | RamMetric | StorageMetric | NetworkMetric] | None:
            return self.collectors[instance].get_metrics()

        @self.router.get("/instances/{instance}/metrics/{metric_type}")
        def get_instance_metric(
            instance: str, metric_type: MetricType
        ) -> CpuMetric | RamMetric | StorageMetric | NetworkMetric | None:
            if instance not in self.instances:
                raise HTTPException(status_code=404, detail="Instance not exists")
            return getattr(
                self.collectors[self.instances[instance]], metric_type
            ).get_metrics()

        @self.router.get("/health", response_model=HealthResponse)
        def health_check() -> HealthResponse:
            return HealthResponse(
                status="ok", timestamp=datetime.now(UTC), version="1.0.0"
            )

    def is_instance_health(self, instance: ExporterInstance) -> bool:
        """Check if an instance is healthy"""
        try:
            url = f"http://{instance.ip_addr}:{instance.port}/health"
            response = requests.get(url, timeout=self.HEALTH_CHECK_TIMEOUT)
            data = response.json()
            return data.get("status") == "ok"
        except requests.RequestException:
            return False

    def unregister(self) -> None:
        """
        Unregister monitored instances from the system when they are determined to be
        unhealthy or offline. This function continuously checks the health status of
        instances using their health endpoint and removes them from the monitoring
        systems if they are not healthy or unreachable.
        """
        while not self._stop_event.is_set():
            with self._lock:
                # Copy instances, to prevent changing dict during iteration
                instances = [instance for instance in self.instances.values()]
                for instance in instances:
                    if not self.is_instance_health(instance):
                        print(f"Unregister instance {instance.hostname} is offline")
                        self.collectors.pop(instance).stop()
                        self.instances.pop(instance.id)
                self._stop_event.wait(timeout=self.HEALTH_CHECK_INTERVAL)

    def start(self) -> None:
        """
        Starts the service, initializing liveliness checks and running the
        server. It ensures the liveliness monitor is activated and begins
        the server's execution loop. Handles clean shutdown in case of a
        KeyboardInterrupt signal.

        :return: None
        """
        self.liveliness.start()
        try:
            self.server.run()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """
        Stops the current operational processes by signaling the stop event, joining threads
        that are alive, stopping active collectors, and shutting down the server.

        This method ensures that all resources, including threads and collectors, are
        properly stopped and cleaned up to avoid potential memory leaks or inconsistent states.

        :param self: Refers to the instance of the class the method belongs to.
        :return: None
        """
        # Stop liveliness monitor thread
        self._stop_event.set()

        if self.liveliness.is_alive():
            self.liveliness.join()

        # Stop running collectors
        for collector in self.collectors.values():
            collector.stop()

        # Stop uvicorn server process
        self.server.should_exit = True
        print("Shutdown complete")
