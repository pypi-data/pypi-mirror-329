import unittest
import pprint

from analyser_hj3415.analyser import compile, MIs
from db_hj3415 import myredis


class CorpCompileTests(unittest.TestCase):
    def setUp(self):
        self.test_codes = myredis.Corps.list_all_codes()
        self.compile = compile.CorpCompile('005930')

    def tearDown(self):
        pass

    def test_get_one(self):
        pprint.pprint(self.compile.get(refresh=True), compact=True)
        pprint.pprint(self.compile.get(refresh=False), compact=True)

    def test_get_all(self):
        for code in self.test_codes[:2]:
            self.compile.code = code
            pprint.pprint(self.compile.get(refresh=True), compact=True)

    def test_red_ranking(self):
        # 이전이랑 다른 기대수익률세팅이라 리프레시함
        print(compile.CorpCompile.red_ranking(expect_earn=0.10, refresh=False))
        print(myredis.Base.get_ttl('red_ranking'))
        # 강제리프레시
        print(compile.CorpCompile.red_ranking(refresh=True))
        print(myredis.Base.get_ttl('red_ranking'))
        # 이전과 같은 기대수익률로 레디스캐시사용함.
        print(compile.CorpCompile.red_ranking(refresh=False))


class MICompileTests(unittest.TestCase):
    def setUp(self):
        self.mi_types = list(MIs._fields)
        self.compile = compile.MICompile('WTI')

    def tearDown(self):
        pass

    def test_get_one(self):
        pprint.pprint(self.compile.get(refresh=True), compact=True)
        pprint.pprint(self.compile.get(refresh=False), compact=True)

    def test_get_all(self):
        for mi_type in self.mi_types:
            self.compile.mi_type = mi_type
            pprint.pprint(self.compile.get(refresh=False), compact=True)