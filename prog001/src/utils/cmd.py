import os
import docker

AVAHI_SOCKET = "/var/run/avahi-daemon/socket"


def send_start_command(hostname: str):
    client = docker.from_env()
    env = {
        "VEHICLE_NAME": hostname,
        "ROS_MASTER": hostname,
        "DUCKIEBOT_NAME": hostname,
        "ROS_MASTER_URI": f"http://{hostname}.local:11311",
        "HOSTNAME": hostname,
    }

    volumes = {}
    if os.path.exists(AVAHI_SOCKET):
        volumes[AVAHI_SOCKET] = {"bind": AVAHI_SOCKET, "mode": "rw"}

    cmd = "dt-launcher-start"

    params = {
        "image": "light5551/dt-ros-api:latest",
        "name": f"start_command_{hostname}",
        "environment": env,
        "stdin_open": True,
        "tty": True,
        "detach": True,
        "privileged": True,
        "remove": True,
        "stream": True,
        "command": cmd,
        "volumes": volumes,
        "network_mode": "host",
        "ports": {}
    }

    print(params)
    l = client.containers.run(**params)
    print(l.logs())


if __name__ == '__main__':
    send_start_command("autobotpi4")
    # ("autobotglazunov")
    # ("autobotpi4")
