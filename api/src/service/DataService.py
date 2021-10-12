from python_helper import Constant as c
from python_helper import EnvironmentHelper, ObjectHelper, RandomHelper, StringHelper, log
from python_framework import Service, ServiceMethod, EnumItem

from DataDto import DataRequestDto
from Data import Data

@Service()
class DataService :

    @ServiceMethod(requestClass=[DataRequestDto])
    def createNewData(self, dto) :
        self.validator.data.validatePostRequestDto(dto)
        model = Data(
            key=dto.key,
            label=dto.label,
            url=dto.url,
            type=dto.type
        )
        self.client.featureManager.createNewSample(dto.key, dto.label)
        sampleAsFeatureKey = f'{dto.type}-{dto.key}'
        self.client.featureManager.createNewFeature(sampleAsFeatureKey, dto.label)
        self.client.featureManager.updateSample(dto.type, sampleAsFeatureKey)
        self.repository.data.save(model)
        return self.mapper.data.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[str])
    def existsByKey(self, key):
        return self.repository.data.existsByKey(key)
