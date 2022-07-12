from pathlib import Path
import subprocess
import logging
# RUN_COMMAND = "dts devel run -M -s -f --workdir {dir} -H {hostname}.local --"
# from utils.cmd import send_start_command
logging.basicConfig(level=logging.INFO)

# RUN_COMMAND = "dts duckiebot demo --demo_name lane_following --duckiebot_name {hostname} --package_name duckietown_demos --image duckietown/template-ros-core:latest-arm32v7"
RUN_COMMAND = "dts devel run --workdir {dir} -M -s -f -H {hostname} --"


def run_template_ros_core(hostname: str, directory: Path, log: Path) -> None:
    logging.info(f"RUN template for hostname [{hostname}], directory [{directory}]")
    with open(log.absolute(), 'w') as file:
        file.write("Log for {}".format(hostname))
        file.flush()
        subprocess.Popen(RUN_COMMAND.format(
            dir=str(directory.absolute()),
            hostname=hostname
        ).split(), stdout=file, stderr=file)
    # send_start_command(hostname)


if __name__ == '__main__':
    run_template_ros_core("autobotglazunov")  # ,
