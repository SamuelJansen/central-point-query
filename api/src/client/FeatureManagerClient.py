from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Client, ClientMethod, HttpStatus, GlobalException, FlaskManager

import json
import requests

from config import FeatureManagerClientConfig

SAMPLE_DATA_URL = f'{FeatureManagerClientConfig.BASE_URL}/samples/'
FEATURE_DATA_URL = f'{FeatureManagerClientConfig.BASE_URL}/features/'
BASIC_HEADERS = basicHeaders = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Authorization': f'Bearer {FeatureManagerClientConfig.AUTHORIZATION}'
}

CLIENT_DID_NOT_SENT_ANY_MESSAGE = 'Client did not sent any message'
ERROR_AT_CLIENT_CALL_MESSAGE = 'Error at client call'

@Client()
class FeatureManagerClient :

    @ClientMethod(requestClass=[str, str])
    def createNewSample(self, key, label):
        body = {
          'label': label,
          'featureDataList': []
        }
        response = None
        try:
            response = requests.post(SAMPLE_DATA_URL + key, headers=basicHeaders, json=body)
        except Exception as exception:
            self.raiseException(response, exception)
        self.raiseExceptionIfNeeded(response)
        return self.getCompleteResponseAsJson(response)

    @ClientMethod(requestClass=[str, str])
    def updateSample(self, key, featureKey):
        body = {
          'featureDataList': [{'featureKey': featureKey}]
        }
        response = None
        try:
            response = requests.put(SAMPLE_DATA_URL + key, headers=basicHeaders, json=body)
        except Exception as exception:
            self.raiseException(response, exception)
        self.raiseExceptionIfNeeded(response)
        return self.getCompleteResponseAsJson(response)

    @ClientMethod(requestClass=[str, str])
    def createNewFeature(self, key, label):
        body = {
          'label': label
        }
        try:
            response = requests.post(FEATURE_DATA_URL + key, headers=basicHeaders, json=body)
        except Exception as exception:
            self.raiseException(response, exception)
        self.raiseExceptionIfNeeded(response)
        return self.getCompleteResponseAsJson(response)

    def raiseException(self, response, exception):
        if ObjectHelper.isNone(response):
            # FlaskManager.getGlobalException(exception, resourceInstance, resourceInstanceMethod, api=None)
            raise GlobalException(
                logMessage = f'{ERROR_AT_CLIENT_CALL_MESSAGE}{c.DOT_SPACE_CAUSE}{CLIENT_DID_NOT_SENT_ANY_MESSAGE if ObjectHelper.isNone(exception) or StringHelper.isBlank(exception) else str(exception)}'
            )
        else:
            #
            raise GlobalException(
                message = self.getErrorMessage(response, exception=exception),
                status = HttpStatus.map(response.status_code),
                logMessage = ERROR_AT_CLIENT_CALL_MESSAGE
            )

    def raiseExceptionIfNeeded(self, response):
        if ObjectHelper.isNone(response):
            raise GlobalException(logMessage = self.getErrorMessage(response))
        if 399 < response.status_code :
            raise GlobalException(
                message = self.getErrorMessage(response),
                status = HttpStatus.map(response.status_code),
                logMessage = ERROR_AT_CLIENT_CALL_MESSAGE
            )

    def getCompleteResponseAsJson(self, response, fallbackStatus=HttpStatus.INTERNAL_SERVER_ERROR):
        responseBody, responseStatus = None, None
        try :
            responseBody, responseStatus = response.json(), HttpStatus.map(HttpStatus.NOT_FOUND if ObjectHelper.isNone(response.status_code) else response.status_code)
        except Exception as exception :
            tempStatus = None
            responseBody, responseStatus = None, HttpStatus.map(fallbackStatus)
            log.failure(self.getCompleteResponseAsJson, 'Not possible to parse response as json', exception=exception, muteStackTrace=True)
        return responseBody, responseStatus

    def getErrorMessage(self, response, exception=None):
        errorMessage = CLIENT_DID_NOT_SENT_ANY_MESSAGE
        try :
            possibleErrorMessage = response.json().get('message', response.json().get('error')).strip()
            if ObjectHelper.isNotNone(possibleErrorMessage) and StringHelper.isNotBlank(possibleErrorMessage):
                errorMessage = possibleErrorMessage
            else:
                log.prettyPython(self.getErrorMessage, 'Client response', response.json(), logLevel=log.DEBUG)
        except Exception as innerException :
            log.warning(self.getErrorMessage, 'Not possible to get error message from response', exception=innerException)
        exceptionPortion = ERROR_AT_CLIENT_CALL_MESSAGE if ObjectHelper.isNone(exception) or StringHelper.isBlank(exception) else str(exception)
        return f'{exceptionPortion}{c.DOT_SPACE_CAUSE}{errorMessage}'
