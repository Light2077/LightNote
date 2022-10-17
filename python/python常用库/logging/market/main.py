import log

from flower import iris, violet
from fruit import apple, orange
import logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    iris.show()
    violet.show()
    apple.show()
    orange.show()
    logger.error('asdfasdf')
    1 / 0
    
