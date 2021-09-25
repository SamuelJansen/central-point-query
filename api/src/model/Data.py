from python_framework import SqlAlchemyProxy as sap
from python_framework import ConverterStatic
from ModelAssociation import MODEL, DATA

from enumeration.DataType import DataType
from constant import DataConstant

class Data(MODEL):
    __tablename__ = DATA

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(128), unique=True, nullable=False)
    type = sap.Column(sap.String(128), default=DataConstant.DEFAULT_DATA_TYPE)
    url = sap.Column(sap.String(2048))
    label = sap.Column(sap.String(128))

    def __init__(self,
        id = None,
        key = None,
        url = None,
        type = None,
        label = None
    ):
        self.id = id
        self.key = key
        self.url = url
        self.type = DataType.map(ConverterStatic.getValueOrDefault(type, DataConstant.DEFAULT_DATA_TYPE))
        self.label = label

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, label={self.label}, type={self.type})'
