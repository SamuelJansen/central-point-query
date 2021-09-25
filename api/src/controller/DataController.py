from python_framework import Controller, ControllerMethod, HttpStatus

from dto import DataDto

@Controller(url = '/data', tag='Data', description='Data controller')
class DataController:

    @ControllerMethod(url = '/',
        requestClass = [DataDto.DataRequestDto],
        responseClass = [DataDto.DataResponseDto])
    def post(self, dto):
        return self.service.data.createNewData(dto), HttpStatus.CREATED
