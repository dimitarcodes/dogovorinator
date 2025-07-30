# logger.py
import logging

class DogovLogger:
    _instance = None

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            # Create and configure logger
            logger = logging.getLogger("DogovLogger")
            logger.setLevel(logging.DEBUG)

            # Create handlers (console + file, optional)
            if not logger.hasHandlers():
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)

                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                datefmt="%m-%d %H:%M:%S")
                ch.setFormatter(formatter)

                logger.addHandler(ch)

            cls._instance = logger

        return cls._instance
