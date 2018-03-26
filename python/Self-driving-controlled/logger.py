import logging

class Log:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.fh = logging.FileHandler('log\\Red_Rover.log')
        self.fh.setLevel(logging.DEBUG)

        self.ch = logging.Streamhandler()
        ch.setLevel(logging.ERROR)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def debugger(self, txt):
        self.logger.debug("Debugging %s", % txt)

    def attempt(self, txt):
        self.logger.info("Attempting to %s", % txt)

    def finished(self, txt):
        self.logger.info("finished %s", % txt)

    def warn(self, txt, **kwargs):
        self.logger.warning("Warning: %s", % txt, **kwargs)

    def err(self, txt, **kwargs):
        self.logger.error("Error: %s", % txt, **kwargs)
