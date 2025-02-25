# -*- coding: utf-8 -*-
# @Time    : 2022-08-12 19:22
# @Author  : zbmain

import sentry_sdk

import winwin

sentry_sdk.init(
    dsn=winwin.support.sentry_dsn(),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

test_arr = [1]
test_arr[1]
