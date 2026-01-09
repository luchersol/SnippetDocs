import logging

class ColorHandler(logging.StreamHandler):
    COLORS = {
        "DEBUG": "\033[36m",    # cyan
        "INFO": "\033[32m",     # green
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",    # red
        "CRITICAL": "\033[41m", # fondo rojo
    }
    RESET = "\033[0m"

    def emit(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{color} [{record.levelname}] {record.msg}{self.RESET}"
        super().emit(record)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(ColorHandler())