# -*- coding: utf-8 -*-
# @Time    : 2022-09-07 09:15
# @Author  : zbmain
import logging

if __name__ == '__main__':
    logging.basicConfig(
        filename="run.log",
        filemode="a",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s",
        level=logging.INFO
    )
    logging.info('test')
