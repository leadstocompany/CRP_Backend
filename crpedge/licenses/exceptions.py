from rest_framework.exceptions import APIException


class LicenseError(APIException):
    status_code = 400
    default_detail = "There was a problem with the license."
    default_code = "license_error"

    def __init__(self, detail=None, code=None):
        super().__init__(detail or self.default_detail, code or self.default_code)
