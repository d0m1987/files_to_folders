import logging

logger = logging.getLogger("files_to_folders")

ERROR_LOG_FILENAME = 'files_to_folders.log'

logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', 
        datefmt='%Y-%m-%d:%H:%M:%S', 
        filename=ERROR_LOG_FILENAME, 
        encoding='utf-8',
        level=logging.ERROR,
    )
