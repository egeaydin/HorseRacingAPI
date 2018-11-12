class PageDoesNotExist(Exception):
    def __init__(self, message):

        message = 'Could not find the race! Please make sure race is available on TJK.org. Url: {0}'.format(message)
        super(PageDoesNotExist, self).__init__(message)


class MissingData(Exception):
    def __init__(self, message=None):
        super(MissingData, self).__init__(message)
