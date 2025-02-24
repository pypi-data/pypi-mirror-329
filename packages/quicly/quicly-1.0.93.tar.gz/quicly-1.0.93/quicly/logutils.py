import logging


class QxLogging(object):
  DEFAULT_LEVEL = 'DEBUG'
  DEFAULT_FORMAT = '[%(asctime)s] [%(name)s] %(message)s'

  def __init__(self, name: str = None):
    self._logger = self.get_logger(name)

  @property
  def logger(self) -> logging.Logger:
    return self._logger

  @staticmethod
  def get_logger(name: str):
    return logging.getLogger(name)

  @staticmethod
  def disable(name: str):
    QxLogging.get_logger(name).disabled = True


logging.basicConfig(level=QxLogging.DEFAULT_LEVEL, format=QxLogging.DEFAULT_FORMAT)
