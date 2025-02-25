import logging

from .base import AWG
from .enums import WaveformType, FrequencyUnit, AmplitudeUnit


class RigolDG1000Z(AWG):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        logging.debug("RigolDG1000Z instance created.")

    def set_waveform(self, channel, waveform_type: WaveformType):
        """Sets the waveform type for the specified channel."""
        try:
            self.write(f"SOUR{channel}:FUNC {waveform_type.value}")
            logging.debug(f"Channel {channel} waveform set to {waveform_type.value}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} waveform to {waveform_type.value}: {e}")
            raise

    def set_frequency(self, channel, frequency: float, unit: FrequencyUnit = FrequencyUnit.HZ):
        """Sets the frequency for the specified channel."""
        try:
            self.write(f"SOUR{channel}:FREQ {frequency}{unit.value}")
            logging.debug(f"Channel {channel} frequency set to {frequency}{unit.value}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} frequency to {frequency}{unit.value}: {e}")
            raise

    def set_amplitude(self, channel, amplitude: float, unit: AmplitudeUnit = AmplitudeUnit.VPP):
        """Sets the amplitude for the specified channel."""
        try:
            self.write(f"SOUR{channel}:VOLT {amplitude}{unit.value}")
            logging.debug(f"Channel {channel} amplitude set to {amplitude}{unit.value}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} amplitude to {amplitude}{unit.value}: {e}")
            raise
