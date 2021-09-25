from python_framework import Mapper, MapperMethod

from dto import DataDto
from model import Data

@Mapper()
class DataMapper:

    @MapperMethod(requestClass=[[DataDto.DataRequestDto]], responseClass=[[Data.Data]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        for model in modelList :
            self.mapper.call.mapModelWeekDay(model)
        return modelList

    @MapperMethod(requestClass=[[Data.Data]], responseClass=[[DataDto.DataResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList) :
        return dtoList

    @MapperMethod(requestClass=[DataDto.DataRequestDto], responseClass=[Data.Data])
    def fromRequestDtoToModel(self, dto, model) :
        self.mapper.call.mapModelWeekDay(model)
        return model

    @MapperMethod(requestClass=[Data.Data], responseClass=[DataDto.DataResponseDto])
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @MapperMethod()
    def mapModelWeekDay(self, model) :
        model.weekDay = self.service.call.getWeekDayByModel(model)
