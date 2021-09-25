from python_framework import ConverterStatic

from enumeration.DataType import DataType
from constant import DataConstant

class DataRequestDto:
    def __init__(self,
        key = None,
        url = None,
        type = None,
        label = None
    ):
        self.key = key
        self.url = url
        self.type = DataType.map(ConverterStatic.getValueOrDefault(type, DataConstant.DEFAULT_DATA_TYPE))
        self.label = label

class DataResponseDto:
    def __init__(self,
        key = None,
        url = None,
        type = None,
        label = None
    ):
        self.key = key
        self.url = url
        self.type = DataType.map(type)
        self.label = label
