import logging

logger = logging.getLogger("files_to_folders")

logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', 
        datefmt='%Y-%m-%d:%H:%M:%S', 
        filename='files_to_folders.log', 
        encoding='utf-8',
        level=logging.ERROR,
    )
