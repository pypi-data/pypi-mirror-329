import logging
import colorlog


def configure_moth_logger(level=logging.DEBUG):
    # Create a handler for the console
    handler = colorlog.StreamHandler()

    # Define a colorful formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(name)s [%(levelname)s]: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # Assign the formatter to the handler
    handler.setFormatter(formatter)

    # Create the logger
    logger = colorlog.getLogger('moth')
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False
    logger.addHandler(handler)