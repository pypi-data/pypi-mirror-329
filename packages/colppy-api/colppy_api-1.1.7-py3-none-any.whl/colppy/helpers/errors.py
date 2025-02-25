from colppy.helpers.logger import logger


class ColppyError(Exception):
    def __init__(self, response):
        self._response = response

    def is_error(self) -> Exception or None: # type: ignore
        if self._response['result']['estado'] != 0:
            logger.error(f"Error: {self._response['result']['mensaje']}")
            return Exception(self._response['result']['mensaje'])
        if not self._response['response']['success']:
            logger.error(f"Error: {self._response['service']['provision']} - {self._response['response']['message']}")
            return Exception(self._response['response']['message'])
        return None
