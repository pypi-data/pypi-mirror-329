import logging

from .base import AWG
from .enums import WaveformType, FrequencyUnit, AmplitudeUnit


class SiglentSDG1000X(AWG):
    def __init__(self, ip_address):
        super().__init__(ip_address)
        logging.debug("SiglentSDG1000X instance created.")

    def set_waveform(self, channel, waveform_type: WaveformType):
        """Sets the waveform type for the specified channel."""
        # Siglent uses a slightly different command structure
        try:
            self.write(f"C{channel}:BSWV WVTP,{waveform_type.value}")
            logging.debug(f"Channel {channel} waveform set to {waveform_type.value}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} waveform to {waveform_type.value}: {e}")
            raise

    def set_frequency(self, channel, frequency: float, unit: FrequencyUnit = FrequencyUnit.HZ):
        """Sets the frequency for the specified channel."""
        try:
            # Siglent uses a slightly different command structure
            converted_frequency = frequency
            if unit == FrequencyUnit.KHZ:
                converted_frequency = frequency * 1000
            elif unit == FrequencyUnit.MHZ:
                converted_frequency = frequency * 1000000

            self.write(f"C{channel}:BSWV FRQ,{converted_frequency}")
            logging.debug(f"Channel {channel} frequency set to {frequency}{unit.value} (converted to {converted_frequency} Hz)")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} frequency to {frequency}{unit.value}: {e}")
            raise

    def set_amplitude(self, channel, amplitude: float, unit: AmplitudeUnit = AmplitudeUnit.VPP):
        """Sets the amplitude for the specified channel."""
        try:
            # Siglent uses a slightly different command structure
            self.write(f"C{channel}:BSWV AMP,{amplitude}")
            logging.debug(f"Channel {channel} amplitude set to {amplitude}")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} amplitude to {amplitude}{unit.value}: {e}")
            raise

    def set_offset(self, channel, offset_voltage: float):
        """Sets the offset voltage for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV OFST,{offset_voltage}")
            logging.debug(f"Channel {channel} offset voltage set to {offset_voltage} Vdc")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} offset voltage to {offset_voltage} Vdc: {e}")
            raise

    def set_phase(self, channel, phase: float):
        """Sets the phase for the specified channel."""
        try:
            self.write(f"C{channel}:BSWV PHSE,{phase}")
            logging.debug(f"Channel {channel} phase set to {phase}°")
        except Exception as e:
            logging.error(f"Failed to set channel {channel} phase to {phase}°: {e}")
            raise

    def sync_phase(self):
        """Sets the phase synchronization of the two channels."""
        try:
            self.write(f"EQPHASE")
            logging.debug(f"Phases of both the channels have been synchronized")
        except Exception as e:
            logging.error(f"Failed to synchronize phase: {e}")
            raise
