# SentinalMon
SentinalMon is a system monitoring tool built with Python that allows you to track and visualize real-time performance metrics across multiple machines in your network.

### Features
- Multi-machine Monitoring: Monitor multiple systems from a central interface
- Real-time Metrics: Track system performance with live updates
- Rich Visualization: Terminal-based UI with intuitive dashboards
- Distributed Architecture: Master-agent model for scalable monitoring

### Metrics Tracked
- **CPU**: Usage percentage, core-specific metrics, clock speeds, and temperature
- **Memory**: RAM and swap usage with detailed statistics
- **Storage**: Disk I/O, read/write speeds, IOPS, and partition usage
- **Network**: Interface statistics, bandwidth usage, and packet metrics

### Architecture
SentinalMon uses a distributed architecture with three main components:

- **Exporter:** Runs on each machine you want to monitor, collecting system metrics
- **Master:** Central server that aggregates data from all exporters
- **Client:** Terminal UI that connects to the master to display metrics

## Installation
### PyPi
```bash
pip install sentinalmon
```
### Repository clone
```Bash
# Clone the repository
git clone https://github.com/bdizen/sentinalmon.git
cd sentinalmon

# Install using Poetry

poetry install

# Enter poetry virtual environment

poetry shell
```
## Usage
### Starting the Master Server

```Bash
poetry run pcmonitor master --host 0.0.0.0 --port 8001

```
### Running an Exporter on a Machine to Monitor
```Bash
poetry run pcmonitor exporter --master-host <master-ip> --master-port 8001 --host 0.0.0.0 --port 8000
```
### Launching the Client UI

Bash
poetry run pcmonitor client --master-host <master-ip> --master-port 8001
### Client UI Navigation
- Use the Tab key to switch between metric views (CPU, Memory, Storage, Network)
- Press i to open the instance selector
- Select a machine to monitor from the list
- Press Escape to return to the instance selector
### Requirements
- Python 3.10+
- Dependencies:
  - psutil: System metrics collection
  - textual: Terminal UI framework
  - typer: Command-line interface
  - httpx/requests: HTTP client libraries
  - fastapi/uvicorn: API server
  - Additional dependencies for authentication and security
### Development
SentinalMon uses Poetry for dependency management and includes several development tools:


```Bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run flake8
poetry run pylint sentinalmon

# Generate dependency graph
poetry run pydeps sentinalmon
```
### Acknowledgments
- Built with Textual for the TUI
- System metrics provided by psutil

**Note: This project is under active development.**