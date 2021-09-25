from python_framework import Enum, EnumItem

@Enum()
class DataTypeEnumeration :
    IMAGES = EnumItem()
    MOVIES = EnumItem()
    INVALID = EnumItem()

DataType = DataTypeEnumeration()
