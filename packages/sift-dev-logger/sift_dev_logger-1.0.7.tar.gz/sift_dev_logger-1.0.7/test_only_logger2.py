from sift_dev_logger import getLogger

def test_second_logger():
    logger = getLogger("test")
    logger.info("Hello, world from inside the second logger!")