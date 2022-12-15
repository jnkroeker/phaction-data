#!/Users/johnkroeker/Desktop/phaction_scripts/bin/python

# ^ modify above to path displayed as the result of executing 'which python' in you venv
# the above points to the python in the venv created in ~/Desktop/phaction_resources/ on your laptop
# remember to always source the venv before executing this script (`source ~/Desktop/phaction_scripts/bin/activate`)

import argparse
import asyncio 
import logging
import requests
import json
import re
import sys
import time

from binascii import hexlify
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice
from typing import Dict, Any, List, Callable, Optional, Tuple

from rich.logging import RichHandler
from rich import traceback

GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"
GOPRO_BASE_URL = "http://10.5.5.9:8080"

logger: logging.Logger = logging.getLogger("tutorial_logger")
sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
sh.setFormatter(stream_formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    msg = context.get("exception", context["message"])

async def connect_ble(args: argparse.Namespace, notification_handler: Callable[[int, bytes], None]) -> BleakClient :

    asyncio.get_event_loop().set_exception_handler(exception_handler)

    try:
        print("scanning for 5 seconds, please wait...")

        devices = await BleakScanner.discover(return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr))

        matched_devices: List[BleakDevice] = []

        token = re.compile(r"GoPro [A-Z0-9]{4}")

        for d, a in devices.values():
            if d.name != "Unknown" and d.name is not None:
                if token.match(d.name):
                    matched_devices = [d]

        print(f"Found {len(matched_devices)} matching devices.")

        device = matched_devices[0]

        client = BleakClient(device)
        await client.connect(timeout=15)
        
        print("BLE Connected!")

        try:
            await client.pair()
        except NotImplementedError:
            # This is expected on Mac
            pass

        print("pairing complete")

        for service in client.services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        # print(char.properties)
                        await client.start_notify(char, notification_handler)

        print("done enabling notifications")

        return client

    except Exception as e:

        raise Exception(f"Couldn't establish BLE connection")


async def enable_wifi(args: argparse.Namespace) ->  None: #Tuple[str, str, BleakClient]:

    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from, and read from
    COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
    COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
    WIFI_AP_SSID_UUID = GOPRO_BASE_UUID.format("0002")
    WIFI_AP_PASSWORD_UUID = GOPRO_BASE_UUID.format("0003")

    client: BleakClient

    def notification_handler(handle: int, data: bytes) -> None:
        # print(f'Received response at {handle=}: {hexlify(data, ":")!r}')

        print(client.services.characteristics[handle].uuid)

        # If this is the correct handle and the status is success, the command was a success
        if client.services.characteristics[handle].uuid == COMMAND_RSP_UUID and data[2] == 0x00:
            print("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            print("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(args, notification_handler)

    # event.clear()
    # await client.write_gatt_char(
    #     COMMAND_REQ_UUID, bytearray([0x06, 0x40, 0x04, 0x00, 0x00, 0x00, 0x01]), response=True
    # )
    # await event.wait()  # Wait to receive the notification response
    # await client.disconnect()

    # Write to command request BleUUID to put the camera to sleep
    # logger.info("Putting the camera to sleep")
    # event.clear()
    # await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x01, 0x05]), response=True)
    # await event.wait()  # Wait to receive the notification response
    # await client.disconnect()

    # Read from WiFi AP SSID BleUUID
    print("Reading the WiFi AP SSID")
    ssid = (await client.read_gatt_char(WIFI_AP_SSID_UUID)).decode()
    print(f"SSID is {ssid}")

    # Read from WiFi AP Password BleUUID
    print("Reading the WiFi AP password")
    password = (await client.read_gatt_char(WIFI_AP_PASSWORD_UUID)).decode()
    print(f"Password is {password}")

    # Write to the Command Request BleUUID to enable WiFi
    print("Enabling the WiFi AP")
    # event.clear()
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x03, 0x17, 0x01, 0x01]), response=True)
    await event.wait()  # Wait to receive the notification response
    print("WiFi AP is enabled")

    # return ssid, password, client

def get_media_list() -> Dict[str, Any]:
    # Build the HTTP GET request
    url = GOPRO_BASE_URL + "/gopro/media/list"
    print(f"Getting the media list: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")

    return response.json()

async def main(args: argparse.Namespace) -> None:

    *_, client = await enable_wifi(args)

    get_media_list()

    await client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(main(args))