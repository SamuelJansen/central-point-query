from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getSetting('feature-manager-api.base-url')
AUTHORIZATION = globalsInstance.getSetting('feature-manager-api.authorization')
