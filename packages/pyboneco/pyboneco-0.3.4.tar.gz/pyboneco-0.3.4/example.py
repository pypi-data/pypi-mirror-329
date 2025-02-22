import asyncio
import json
import logging

from pyboneco import BonecoAuth, BonecoClient, BonecoAuthState

logging.basicConfig(level=logging.INFO)


async def actions(auth: BonecoAuth):
    boneco_client = BonecoClient(auth)
    try:
        await boneco_client.connect()
        name = await boneco_client.get_device_name()
        print(f"User's device name is {name}")
        data = json.dumps(auth.save())
        print(f"Device json data: {data}")
        info = await boneco_client.get_device_info()
        print(f"Device info: {vars(info)}")
        state = await boneco_client.get_state()
        print(f"Device state: {vars(state)}")
    except Exception as e:
        print(e)
    finally:
        await boneco_client.disconnect()


def auth_state_callback(auth: BonecoAuth) -> None:
    print(
        f"Got new auth state: current={auth.current_state}, level={auth.current_auth_level}"
    )
    if auth.current_state == BonecoAuthState.CONFIRM_WAITING:
        print("Press button on device to confirm pairing")


async def find_device(address: str):
    scanned = await BonecoClient.find_boneco_devices()
    chosen = next((x for x in scanned.keys() if x.address == address), None)
    return chosen, scanned[chosen]


async def pair():
    scanned = await BonecoClient.find_boneco_devices()
    devices = list(scanned.keys())
    devices_text = "\n".join(
        [
            f"{n}) {value} (Pairing active = {scanned[value].pairing_active})"
            for n, value in enumerate(devices, start=1)
        ]
    )
    print(f"Scan results: \n{devices_text}\n")
    number = input(f"Choose device to pair [1-{len(scanned)}]: ")
    device = devices[int(number) - 1]
    advertisement = scanned[device]
    pairing_active = advertisement.pairing_active
    print(
        f'Chosen device "{device.name}" with address "{device.address}". Pairing active = {pairing_active}'
    )
    while not pairing_active:
        print("Put the device in pairing mode and press Enter")
        input()
        device, advertisement = await find_device(device.address)
        pairing_active = device and advertisement.pairing_active

    auth_data = BonecoAuth(device)
    auth_data.set_auth_state_callback(auth_state_callback)

    await actions(auth_data)


async def connect():
    print("Enter device json data")
    data = json.loads(input())
    device, advertisement = await find_device(data["address"])
    auth_data = BonecoAuth(device, data["key"])
    await actions(auth_data)


async def menu():
    while True:
        choosed = input(
            "\nChoose between (1) pairing new device and (2) connecting existing device: "
        )
        match choosed:
            case "1":
                await pair()
                break
            case "2":
                await connect()
                break
            case _:
                print("Not supported")
    print("Press Enter for exit")
    input()


if __name__ == "__main__":
    asyncio.run(menu())
