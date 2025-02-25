import logging
import os
import unittest

import winwin


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass
        print('winwin ver:%s' % winwin.__version__)
        print('winwin env:%s' % winwin.support.env_file)
        winwin.utils.func_util.warning_ignored()
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger().addHandler(console)
        logging.basicConfig(level=logging.DEBUG)

    def test_oss(self):
        print(winwin.managers.oss.oss_file2DF('oss://qmgy-private-hz-dev/algo/zhaobin/tmp/tmp.csv'))
        print(winwin.managers.oss.oss_file2DF('oss://qmgy-private-hz-dev/algo/zhaobin/tmp/京东详情采集-限云采集.xlsx'))
        winwin.managers.oss.oss_get_object_cache('algo/zhaobin/tmp/csv.txt')
        winwin.managers.oss.oss_upload_object('.cache/csv.txt', 'algo/zhaobin/tmp/tmp/')
        winwin.managers.oss.oss_get_object_cache('oss://qmgy-private-hz-dev/algo/zhaobin/tmp/csv.txt')
        winwin.managers.oss.oss_get_object_topath('algo/zhaobin/tmp/tmp.csv', '.cache/new.csv')

    def test_odps(self):
        sql_query = '''SELECT * FROM zhidou_hz.algo_cls2bcat_map WHERE ds='20220812' LIMIT 2'''
        sql_filepath = winwin.env.CACHE_PROJECT_HOME + '/tmp.csv'
        winwin.managers.odps.odps_download_with_sql(sql_query, sql_filepath)

    def test_escape(self):
        print(winwin.utils.str_util.escape('123/321/456"213'))

    def test_arr(self):
        print(winwin.utils.list_util.extend([1, 2, 3], [1]))

    def test_queue(self):
        import queue
        q = queue.Queue(10)
        for i in range(10):
            q.put(i)
        print(q.get(), q.get(), q.get(), q.get())

        from collections import deque
        stack = deque()
        for i in range(10):
            stack.append(i)
        print(stack.pop(), stack.popleft())
        print(stack)

    def test_nebula(self):
        nebula_client = winwin.managers.nebula.Client(winwin.support.nebula_connect('NEBULA_URI'))
        winwin.managers.nebula.print_resp(nebula_client.show_spaces())

    def test_resource(self):
        resource_conf = os.path.join(winwin.env.PROJECT_HOME, 'resource.yaml')
        resource_info = winwin.managers.resource.upgrade(resource_conf)
        print(resource_info)

    def test_utils(self):
        from winwin.utils.func_util import pd_util
        print(pd_util.check_null('x'))
        from winwin.utils.pd_util import check_null
        print(check_null('x'))


if __name__ == '__main__':
    unittest.main()
