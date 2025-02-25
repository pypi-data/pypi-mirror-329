from __future__ import annotations

import logging

import vxi11

from .enums import WaveformType, AmplitudeUnit, FrequencyUnit


class AWG:
    ip_addr: str
    device: vxi11.Instrument | None

    def __init__(self: AWG, ip_addr: str):
        self.ip_addr = ip_addr
        self.device = None
        try:
            self.device = vxi11.Instrument(ip_addr)
            self.device.clear()
            logging.debug(f"Connected to AWG at {ip_addr}")
        except Exception as e:
            logging.error(f"Failed to connect to AWG at {ip_addr}: {e}")
            raise

    def write(self, command):
        try:
            self.device.write(command)
            logging.debug(f"Sent command: {command}")
        except Exception as e:
            logging.error(f"Failed to write command: {e}")
            raise

    def query(self, command):
        try:
            response = self.device.ask(command)
            logging.debug(f"Sent query: {command}, Received: {response}")
            return response
        except Exception as e:
            logging.error(f"Failed to query command: {e}")
            raise

    def close(self):
        try:
            self.device.close()
            logging.debug("Disconnected from AWG")
        except Exception as e:
            logging.error(f"Failed to disconnect from AWG: {e}")

    def set_output(self, channel, state: bool):
        state_str = "ON" if state else "OFF"
        self.write(f"OUTP{channel}:STAT {state_str}")

    def get_id(self) -> str:
        return self.query("*IDN?")
