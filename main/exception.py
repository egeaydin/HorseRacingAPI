from rest_framework.exceptions import APIException


class PageDoesNotExist(APIException):
    status_code = 400
    default_detail = 'Could not find the race! Please make sure race is available on TJK.org.'
    default_code = 'race_does_not_exists'

    def __init__(self, message, url=''):
        if len(message) > 0:
            message = '{0}, {1}'.format(self.default_detail, message)
        else:
            message = self.default_detail

        if url:
            self.generated_url = url
        super(PageDoesNotExist, self).__init__(message)

    @property
    def full_details(self):
        return {'message': self.detail,
                'generated_url': self.generated_url,
                'status_code': self.status_code}


class MissingData(Exception):
    def __init__(self, message=None):
        super(MissingData, self).__init__(message)
