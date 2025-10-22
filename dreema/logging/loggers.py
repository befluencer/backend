from .setup import Setup

class Logger:
    _instances = {}  # filename → Setup instance

    @classmethod
    def logger(cls, filename):
        if filename not in cls._instances:
            cls._instances[filename] = Setup(file=filename)
        return cls._instances[filename]

    @staticmethod
    def success(message: str, filename='system'):
        log = Logger.logger(filename)
        log.write('success', message=message)

    @staticmethod
    def info(message: str, filename='system'):
        log = Logger.logger(filename)
        log.write('info', message=message)
    
    @staticmethod
    def debug(message: str, filename='system'):
        log = Logger.logger(filename)
        log.write('debug', message=message)

    @staticmethod
    def error(message: str, filename='system'):
        log = Logger.logger(filename)
        log.write('error', message=message)