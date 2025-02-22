from enum import Enum


class ConsumerType(str, Enum):
    DIRECT = "DIRECT"
    COMPRESSOR = "COMPRESSOR"
    PUMP = "PUMP"
    COMPRESSOR_SYSTEM = "COMPRESSOR_SYSTEM"
    PUMP_SYSTEM = "PUMP_SYSTEM"
    TABULATED = "TABULATED"
    GENERATOR_SET_SIMPLE = "GENERATOR_SET_SIMPLE"
