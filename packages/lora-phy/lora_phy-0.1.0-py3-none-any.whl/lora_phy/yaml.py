from .tx import LoRaTransmitter
from .rx import LoRaReceiver

def load_yaml_config(file_path: str) -> tuple[LoRaTransmitter, LoRaReceiver]:
    """
    Load a YAML configuration file and return the transmitter and receiver objects.

    Parameters
    ----------
    file_path : str
        Path to the YAML configuration file.
    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("Parsing YAML config files requires the 'pyyaml' package. "
                          "Please install it with 'pip install pyyaml'") from e
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    rf_freq = float(config["fc"])
    sample_rate = float(config["fs"])
    spreading_factor = int(config["lora_sf"])
    bandwidth = float(config["lora_bw"])
    coding_rate = int(config["lora_cr"]) if "lora_cr" in config else 4
    has_header = bool(config["lora_has_header"]) if "lora_has_header" in config else True
    tx = LoRaTransmitter(spreading_factor, bandwidth, sample_rate, has_header=has_header, coding_rate=coding_rate)
    rx = LoRaReceiver(rf_freq, spreading_factor, bandwidth, sample_rate, has_header=has_header, implicit_header_coding_rate=coding_rate)
    return tx, rx
