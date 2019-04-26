# -*- coding: utf-8 -*-
import logging.handlers


class LogSetting():
    """로거 세팅 클래스
        LogSetting.LEVEL = logging.INFO # INFO 이상만 로그를 작성
    """
    LEVEL = logging.INFO
    # LEVEL = logging.DEBUG
    FILENAME = "./logs/crawl.log"
    MAX_BYTES = 10 * 1024 * 1024
    BACKUP_COUNT = 10
    FORMAT = "%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s"


def Logger(name):
    """[파일 로그 클래스]
    Arguments:
        param name {[str]} -- [로그 이름]
    Returns:
        [type] -- [로거 인스턴스]
    logger = Logger(__name__)
    logger.info('info 입니다')
    """
    # 로거 & 포매터 & 핸들러 생성
    logger = logging.getLogger(name)
    # 로거 레벨 설정
    logger.setLevel(LogSetting.LEVEL)

    formatter = logging.Formatter(LogSetting.FORMAT)
    streamHandler = logging.StreamHandler()
    fileHandler = logging.handlers.RotatingFileHandler(
        filename=LogSetting.FILENAME,
        maxBytes=LogSetting.MAX_BYTES,
        backupCount=LogSetting.BACKUP_COUNT)

    # 핸들러 & 포매터 결합
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 로거 & 핸들러 결합
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    return logger


if __name__ == "__main__":
    # from cafe_kakao.utils import log_util
    # log_util.LogSetting.FILENAME = "./logs/test.log"
    # log = log_util.Logger(__name__)
    # log.info("OMGthis is %s", __name__)
    pass
