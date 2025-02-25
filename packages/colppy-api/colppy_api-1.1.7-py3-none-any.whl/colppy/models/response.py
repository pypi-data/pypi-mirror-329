from colppy.helpers.errors import ColppyError

class Response:
    def __init__(self, model, http_response):
        self._model = model
        self._response = http_response

    def get_items(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['data']:
                return [self._model(**item) for item in self._response['response']['data']]
        return []