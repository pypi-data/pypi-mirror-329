import pyaudio
import asyncio


CHUNK_SIZE = 1024


class AudioProcessor:
    def __init__(self):
        self.wave_data = bytearray()
        self.read_offset = 0

    async def read(self, chunk_size):
        while self.read_offset + chunk_size > len(self.wave_data):
            await asyncio.sleep(0.01)
        new_offset = self.read_offset + chunk_size
        data = self.wave_data[self.read_offset : new_offset]
        self.read_offset = new_offset
        return data

    def write_audio(self, data):
        self.wave_data.extend(data)
        return


def get_devices_list(input=True) -> list[tuple[str, int]]:
    pa = pyaudio.PyAudio()
    devices = []
    for i in range(pa.get_device_count()):
        if (
            pa.get_device_info_by_index(i)[
                "maxInputChannels" if input else "maxOutputChannels"
            ]
            > 0
        ):
            devices.append((pa.get_device_info_by_index(i)["name"], i))
    return devices


def get_device_by_name(device_name: str) -> int:
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        if pa.get_device_info_by_index(i)["name"] == device_name:
            return i
    raise ValueError(f'Could not find device with name "{device_name}"')


def get_device_info_by_index(index: int) -> dict:
    pa = pyaudio.PyAudio()
    return pa.get_device_info_by_index(index)


def get_stream(
    input_device_index: int,
    rate: int,
    stream_callback: callable,
    format: int = pyaudio.paFloat32,
    channels: int = 1,
    input: bool = True,
    frames_per_buffer: int = CHUNK_SIZE,
):
    return pyaudio.PyAudio().open(
        format=format,
        channels=channels,
        rate=rate,
        input=input,
        frames_per_buffer=frames_per_buffer,
        input_device_index=input_device_index,
        stream_callback=stream_callback,
    )
