__author__ = 'assaf'


class DeployFailedException(Exception):
    def __init__(self, error_message):
        super(DeployFailedException, self).__init__(
            "Deploy failed. {0}".format(error_message))