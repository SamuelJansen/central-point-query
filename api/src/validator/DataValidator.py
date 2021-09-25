from python_helper import Constant
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from dto.DataDto import DataRequestDto
from model.Data import Data

@Validator()
class DataValidator:

    @ValidatorMethod(requestClass=[DataRequestDto])
    def validatePostRequestDto(self, dto):
        self.notExistsByKey(dto.key)

    @ValidatorMethod(requestClass=[DataRequestDto])
    def validatePutRequestDto(self, dto):
        self.existsByKey(dto.key)

    @ValidatorMethod(requestClass=str)
    def notExistsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if self.service.data.existsByKey(key) :
            raise GlobalException(message=f'Data already exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def existsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if not self.service.data.existsByKey(key) :
            raise GlobalException(message=f'''Data does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.NOT_FOUND)

    @ValidatorMethod(requestClass=[[Data], [str]])
    def validateExistsAllByKeyList(self, featureList, featureKeyList) :
        for key in featureKeyList :
            for feature in featureList :
                if not feature.key in featureKeyList :
                    raise GlobalException(message=f'''Data does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.BAD_REQUEST)
