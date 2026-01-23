from pathlib import Path
import time
from maa.controller import AdbController
from maa.toolkit import Toolkit
from maa.tasker import Tasker, LoggingLevelEnum
from maa.resource import Resource

def main():
    user_path = Path(".")
    Toolkit.init_option(user_path)

    Tasker.set_stdout_level(LoggingLevelEnum.Warn)

    resource = Resource()
    resource_detail = resource.post_bundle(user_path / "assets" / "resource").wait()
    if not resource_detail.succeeded:
        print(f"Failed to load resource: {resource_detail}")
        return

    devices = Toolkit.find_adb_devices()
    if not devices:
        print("No devices found")
        return

    device = devices[0]
    print(f"Using device: {device}")
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        input_methods=device.input_methods,
        config=device.config,
    )
    controller.post_connection().wait()

    tasker = Tasker()
    tasker.bind(resource,controller)

    while True:
        start_time = time.time()
        task_detail = tasker.post_task("Challenge").wait().get()
        print(f"Task detail: {task_detail}")
        time.sleep(3)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
