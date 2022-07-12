import subprocess
from pathlib import Path
import logging
BUILD_COMMAND = "dts devel build --workdir {dir} -H {hostname}.local -f"
logging.basicConfig(level=logging.INFO)


def build_template_ros_core(hostname: str, directory: Path, log: Path) -> None:
    logging.info(f"BUILD template for hostname [{hostname}], directory [{directory}]")
    with open(log.absolute(), 'w') as file:
        file.write("Log for {}".format(hostname))
        file.flush()
        if not directory.is_absolute():
            logging.error(f"BUILD [{str(directory.absolute())}] is not absolute:")
            raise ValueError(f"[{str(directory.absolute())}] is not absolute:")
        subprocess.Popen(BUILD_COMMAND.format(
            hostname=hostname,
            dir=str(directory.absolute())
        ).split(), stdout=file, stderr=file)


if __name__ == '__main__':
    build_template_ros_core("autobotglazunov", Path("/tests/template-ros-core"))
