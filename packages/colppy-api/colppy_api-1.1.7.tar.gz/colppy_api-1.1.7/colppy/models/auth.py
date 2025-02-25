from colppy.helpers.errors import ColppyError


class LoginRequest:
    def __init__(self, auth_user, auth_password, params_user, params_password):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._params_password = params_password

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Usuario",
                "operacion": "iniciar_sesion"
            },
            "parameters": {
                "usuario": self._params_user,
                "password": self._params_password
            }
        }


class LoginResponse:
    def __init__(self, response):
        self._response = response

    def get_token(self):
        if not ColppyError(self._response).is_error():
            return self._response['response']['data']['claveSesion']
        return None


class LogoutRequest:
    def __init__(self, auth_user, auth_password, params_user, token):
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Usuario",
                "operacion": "cerrar_sesion"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                }
            }
        }


class LogoutResponse:
    def __init__(self, response):
        self._response = response

    def get_logout(self):
        if not ColppyError(self._response).is_error():
            return self._response['response']['success']
        return False
