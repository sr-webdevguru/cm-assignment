from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 400
    default_detail = "Not Found"

    def __init__(self, detail, code=400):
        self.detail = detail + " not found"
        self.status_code = code
