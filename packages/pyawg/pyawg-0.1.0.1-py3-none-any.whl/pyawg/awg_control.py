from .base import AWG
from .rigol import RigolDG1000Z
from .siglent import SiglentSDG1000X
import logging

def awg_control(ip_address: str) -> AWG:
    """
    Factory function to create AWG instances based on device identification.
    """
    try:
        # Create a generic AWG instance to identify the device
        temp_awg = AWG(ip_address)
        device_id = temp_awg.get_id()
        temp_awg.close()  # Close the temporary connection

        if "RIGOL" in device_id.upper():
            return RigolDG1000Z(ip_address)
        elif "SIGLENT" in device_id.upper():
            return SiglentSDG1000X(ip_address)
        else:
            raise ValueError(f"Unsupported AWG device: {device_id}")
    except Exception as e:
        logging.error(f"Failed to identify AWG at {ip_address}: {e}")
        raise