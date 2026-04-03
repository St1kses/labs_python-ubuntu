import os
import signal
import subprocess
def get_pids_listening_on_port(port: int) -> list[int]:
    result = subprocess.run(
        ["lsof", "-ti", f":{port}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    pids: list[int] = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return pids
def kill_processes_on_port(port: int) -> int:
    killed = 0
    for pid in get_pids_listening_on_port(port):
        try:
            os.kill(pid, signal.SIGTERM)
            killed += 1
        except ProcessLookupError:
            continue
    return killed
def ensure_port_free(port: int) -> None:
    while get_pids_listening_on_port(port):
        kill_processes_on_port(port)
