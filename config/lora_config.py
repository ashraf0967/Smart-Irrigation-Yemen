# config/lora_config.py
import os
from dotenv import load_dotenv

load_dotenv()

LORA_CONFIG = {
    'FREQUENCY': int(os.getenv('LORA_FREQUENCY', 433000000)),
    'BANDWIDTH': int(os.getenv('LORA_BANDWIDTH', 125000)),
    'SF': int(os.getenv('LORA_SF', 12)),
    'CR': int(os.getenv('LORA_CR', 5)),
    'PREAMBLE': int(os.getenv('LORA_PREAMBLE', 8)),
    'SYNC_WORD': int(os.getenv('LORA_SYNC_WORD', 0x12)),
    'TX_POWER': int(os.getenv('LORA_TX_POWER', 17))
}