import os

__author__ = 'assaf'

class BlException(Exception):
    pass


class DeployError(BlException):
    def __init__(self, error_message, exception=None):
        msg = "Deploy failed: {0}".format(error_message)
        if exception is not None and isinstance(exception, Exception):
            msg += "{0}InnerException: {1}".format(os.linesep, exception)

        super(DeployError, self).__init__(msg)


class DockerManagerNotAvailableError(BlException):
    def __init__(self):
        super(DockerManagerNotAvailableError, self).__init__("No Docker Manager servers are configured. C'mon...")


class DockerServerNotAvailableError(BlException):
    def __init__(self):
        super(DockerServerNotAvailableError, self).__init__("No Docker Server is configured. WTF...")