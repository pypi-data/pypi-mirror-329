import asyncio
import json
import socket
from datetime import UTC, datetime

import httpx
import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic.dataclasses import dataclass
from pydantic.v1.json import pydantic_encoder

from sentinalmon.collectors.base import InstanceCollectors
from sentinalmon.exporter.collectors import (
    CpuMetricCollector,
    MemoryMetricCollector,
    NetworkMetricCollector,
    StorageMetricCollector,
)
from sentinalmon.models import ExporterInstance
from sentinalmon.models.server import HealthResponse, MetricType, RegistrationStatus


@dataclass
class ServerConfig:
    ip_addr: str
    port: int


class Exporter:
    REGISTRATION_TIMEOUT = 5
    REGISTRATION_RETRY_DELAY = 5
    REGISTRATION_MAX_RETRY_DELAY = 60
    MASTER_HEALTH_CHECK_INTERVAL = 5

    def __init__(
        self,
        master: ServerConfig,
        host="0.0.0.0",
        port=8000,
        hostname: str | None = None,
    ):
        self.host = host
        self.port = port
        self.hostname = hostname if hostname else socket.gethostname()
        self.master = master

        self.app = FastAPI()
        self.router = APIRouter()
        self.setup_routes()
        self.app.include_router(self.router)
        self.server = uvicorn.Server(uvicorn.Config(self.app, host=host, port=port))
        self.collectors = InstanceCollectors(
            cpu=CpuMetricCollector(),
            memory=MemoryMetricCollector(),
            storage=StorageMetricCollector(),
            network=NetworkMetricCollector(),
        )

        self.registration_status = RegistrationStatus.UNREGISTERED
        self._stop_registration = asyncio.Event()
        self._registration_task: asyncio.Task | None = None

    async def register_with_master(self) -> bool:
        me = ExporterInstance(ip_addr=self.host, port=self.port, hostname=self.hostname)
        url = f"http://{self.master.ip_addr}:{self.master.port}/register"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=json.loads(json.dumps(me, default=pydantic_encoder)),
                    timeout=self.REGISTRATION_TIMEOUT,
                )
                result = response.json()
                if response.status_code == 200:
                    if result.get("status") == "success":
                        print("Successfully registered with master server")
                        return True
                    else:
                        print(f"Registration failed: {result.get('message')}")
                        return False
                else:
                    print(f"Registration failed with status {response.status_code}")
                    return False

        except (httpx.RequestError, asyncio.TimeoutError) as e:
            print(f"Failed to connect to master: {str(e)}")
            return False

    async def check_master_health(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                url = f"http://{self.master.ip_addr}:{self.master.port}/health"
                response = await client.get(url, timeout=5.0)
                if response.status_code != 200:
                    return False
        except (httpx.RequestError, asyncio.TimeoutError) as e:
            print(f"Lost connection to master server: {str(e)}")
            return False
        return True

    async def registration_loop(self):
        retry_delay = self.REGISTRATION_RETRY_DELAY
        while not self._stop_registration.is_set():
            self.registration_status = RegistrationStatus.ATTEMPTING

            # Attempt to register
            if await self.register_with_master():
                print("Registered successfully with the master")
                self.registration_status = RegistrationStatus.REGISTERED
                retry_delay = (
                    self.REGISTRATION_RETRY_DELAY
                )  # Reset delay after registration

                # Start health check loop
                while not self._stop_registration.is_set():
                    if not await self.check_master_health():
                        break
                    else:
                        await asyncio.sleep(self.MASTER_HEALTH_CHECK_INTERVAL)

                self.registration_status = RegistrationStatus.UNREGISTERED
            else:  # Failed registration
                self.registration_status = RegistrationStatus.FAILED
                # Increment retry delay
                retry_delay = min(
                    retry_delay + self.REGISTRATION_RETRY_DELAY,
                    self.REGISTRATION_MAX_RETRY_DELAY,
                )

            # Wait before next attempt
            try:
                await asyncio.wait_for(
                    self._stop_registration.wait(), timeout=retry_delay
                )
            except asyncio.TimeoutError:
                continue

    def setup_routes(self):
        @self.app.on_event("startup")
        async def startup_event() -> None:
            self._stop_registration.clear()
            self._registration_task = asyncio.create_task(self.registration_loop())

        @self.app.on_event("shutdown")
        async def shutdown_event() -> None:
            # Stop registration loop
            if self._registration_task:
                self._stop_registration.set()
                await self._registration_task

        @self.router.get("/metric/{metric_type}")
        def get_metric(metric_type: MetricType):
            collector = getattr(self.collectors, metric_type)
            return collector.get_metrics()

        @self.router.get("/health", response_model=HealthResponse)
        def health_check() -> HealthResponse:
            return HealthResponse(
                status="ok", timestamp=datetime.now(UTC), version="1.0.0"
            )

    def start(self):
        try:
            self.collectors.start()
            self.server.run()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.server.should_exit = True
        self.collectors.stop()
