class CorpCompile:
    @staticmethod
    def caching_corp_compile_topn(refresh: bool, top=40):
        """
        상위 N개의 기업에 대해 CorpCompileData를 수집합니다..

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
            top (int, optional): 상위 기업 개수. 기본값은 40.
        """
        ranking_topn = CorpCompile.prophet_ranking(refresh=False, top=top)
        mylogger.info(ranking_topn)
        corp_compile = CorpCompile('005930')
        print(f"*** CorpCompile redis cashing top{top} items ***")
        for i, (code, _) in enumerate(ranking_topn.items()):
            corp_compile.code = code
            print(f"{i + 1}. {code}")
            corp_compile_data = corp_compile.get(refresh=refresh)
            print(corp_compile_data)

    @staticmethod
    def caching_mi_compile_all(refresh: bool):
        """
        모든 MI(Market Index)에 대해 MICompileData를 캐싱합니다..

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
        """
        mi_compile = MICompile('WTI')
        print(f"*** MICompileData caching Market Index items ***")
        for mi_type in MIs._fields:
            mi_compile.mi_type = mi_type
            print(f"{mi_type}")
            mi_compile_data = mi_compile.get(refresh=refresh)
            print(mi_compile_data)


def test_caching_corp_compile_topn(self):
    compile.CorpCompile.caching_corp_compile_topn(refresh=True, top=1)