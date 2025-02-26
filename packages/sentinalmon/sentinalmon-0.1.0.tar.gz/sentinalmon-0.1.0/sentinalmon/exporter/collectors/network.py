import socket

import psutil
from psutil._common import snetio, snicaddr

from sentinalmon.collectors import BaseMetricCollector
from sentinalmon.models.metrics import NetworkInterfaceMetric, NetworkMetric


class NetworkMetricCollector(BaseMetricCollector[NetworkMetric]):
    def __init__(self, interval: int = 1):
        super().__init__(interval)
        self.nics = psutil.net_if_addrs()

    @staticmethod
    def _get_ipv4(addresses: list[snicaddr]) -> str | None:
        for addr in addresses:
            if addr.family == socket.AF_INET:
                return addr.address

    def _get_mac(self, addresses: list[snicaddr]) -> str | None:
        if self.system == "Linux":
            for addr in addresses:
                if addr.family == socket.AF_PACKET:
                    return addr.address
        else:
            for addr in addresses:
                if addr.family == socket.AF_LINK:
                    return addr.address

    def _calc_rx_speed(self, start: snetio, end: snetio) -> int:
        return int((end.bytes_recv - start.bytes_recv) / self.interval)

    def _calc_tx_speed(self, start: snetio, end: snetio) -> int:
        return int((end.bytes_sent - start.bytes_sent) / self.interval)

    @staticmethod
    def _calc_packet_loss(start: snetio, end: snetio) -> float:
        packets_sent_diff = end.packets_sent - start.packets_sent
        packets_recv_diff = end.packets_recv - start.packets_recv
        packets_sent_loss_diff = end.packets_sent - start.packets_sent
        packets_recv_lost_diff = end.packets_recv - start.packets_recv
        lost_packets = packets_sent_loss_diff + packets_recv_lost_diff
        total_packets = packets_sent_diff + packets_recv_diff
        if total_packets == 0:
            return 0.0
        return max(0.0, (lost_packets / total_packets) * 100)

    def _collect_network_interfaces(self):
        nics = psutil.net_if_addrs()
        nic_metrics = []
        nics_io_counters_start = psutil.net_io_counters(pernic=True)
        self._stop_event.wait(timeout=self.interval)
        nics_io_counters_end = psutil.net_io_counters(pernic=True)
        for key in nics:
            nic_metrics.append(
                NetworkInterfaceMetric(
                    interface_name=key,
                    ip_address=self._get_ipv4(nics[key]),
                    mac_address=self._get_mac(nics[key]),
                    total_rx=nics_io_counters_end[key].bytes_recv,
                    total_tx=nics_io_counters_end[key].bytes_sent,
                    rx_speed=self._calc_rx_speed(
                        nics_io_counters_start[key], nics_io_counters_end[key]
                    ),
                    tx_speed=self._calc_rx_speed(
                        nics_io_counters_start[key], nics_io_counters_end[key]
                    ),
                    packet_lost_percent=self._calc_packet_loss(
                        nics_io_counters_start[key], nics_io_counters_end[key]
                    ),
                )
            )
        return nic_metrics

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            nic_metrics = self._collect_network_interfaces()
            total_rx, total_tx, rx_speed, tx_speed = 0, 0, 0, 0
            for nic in nic_metrics:
                total_rx += nic.total_rx
                total_tx += nic.total_tx
                rx_speed += nic.rx_speed
                tx_speed += nic.tx_speed
            network_metric = NetworkMetric(
                total_rx=total_rx,
                total_tx=total_tx,
                rx_speed=rx_speed,
                tx_speed=tx_speed,
                nics=nic_metrics,
            )
            with self._thread_lock:
                self.metric = network_metric
                self._metric_ready.set()
