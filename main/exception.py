class PageDoesNotExist(Exception):
    def __init__(self, message):
        super(PageDoesNotExist, self).__init__(message)


class MissingData(Exception):
    def __init__(self, message=None):
        super(MissingData, self).__init__(message)
