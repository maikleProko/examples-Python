import subprocess
import logging
logging.basicConfig(level=logging.INFO)

SOFT_STOP_COMMAND = "docker -H {hostname}.local stop -t 2 dts-run-template-ros-core"
HARD_STOP_COMMAND = "docker -H {hostname}.local restart -t 1 duckiebot-interface"


def soft_stop(hostname: str) -> None:
    logging.info(f"SOFT STOP bot with hostname [{hostname}]")
    subprocess.run(SOFT_STOP_COMMAND.format(
        hostname=hostname
    ).split())


def hard_stop(hostname: str) -> None:
    logging.info(f"HARD STOP bot with hostname [{hostname}]")
    print(HARD_STOP_COMMAND.format(
        hostname=hostname
    ))
    subprocess.Popen(SOFT_STOP_COMMAND.format(
        hostname=hostname
    ).split())
    subprocess.Popen(HARD_STOP_COMMAND.format(
        hostname=hostname
    ).split())
