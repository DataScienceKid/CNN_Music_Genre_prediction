import logging
import sys

from classes.driver.cnn_driver import CNNDriver


class CnnMain:
    if __name__ == "__main__":
        result = -1
        args = sys.args
        print(args)
        
        try:
            driver = CNNDriver()
            result = driver.processor(args)
            sys.exit(result)
        
        except Exception:
            logging.error("Error running Main class", exc_info = True)
            sys.exit(result)
