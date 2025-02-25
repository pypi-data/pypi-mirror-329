class MyProphet:

    def visualization(self):
        """
        Prophet 모델의 예측 결과를 시각화합니다.

        - Matplotlib를 사용하여 예측 결과 및 추세/계절성을 그래프로 출력.
        """
        self.initializing()
        # 예측 결과 출력
        print(self.df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # 예측 결과 시각화 (Matplotlib 사용)
        fig = self.model.plot(self.df_forecast)
        # 추세 및 계절성 시각화
        fig2 = self.model.plot_components(self.df_forecast)
        plt.show()  # 시각화 창 띄우기

    def export(self, to="html") -> Optional[str]:
        """
        예측 결과를 시각화하여 다양한 형식으로 내보냅니다.

        매개변수:
            refresh (bool): 데이터를 새로 생성할지 여부.
            to (str): 내보낼 형식 ('html', 'png', 'file').

        반환값:
            Optional[str]: HTML 문자열로 반환하거나 PNG/HTML 파일로 저장합니다.

        예외:
            Exception: 지원되지 않는 형식의 경우 예외 발생.
        """
        self.initializing()
        # Plotly를 사용한 시각화
        fig = go.Figure()

        # 실제 데이터
        fig.add_trace(go.Scatter(x=self.df_real['ds'], y=self.df_real['y'], mode='markers', name='실제주가'))
        # 예측 데이터
        fig.add_trace(go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat'], mode='lines', name='예측치'))

        # 상한/하한 구간
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_upper'], fill=None, mode='lines', name='상한'))
        fig.add_trace(
            go.Scatter(x=self.df_forecast['ds'], y=self.df_forecast['yhat_lower'], fill='tonexty', mode='lines', name='하한'))

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis = dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis = dict(
                tickformat=".0f",  # 소수점 없이 원래 숫자 표시
            ),
            showlegend=False,
        )

        if to == 'html':
            # 그래프 HTML로 변환 (string 형식으로 저장)
            graph_html = plot(fig, output_type='div')
            return graph_html
        elif to == 'png':
            # 그래프를 PNG 파일로 저장
            fig.write_image(f"myprophet_{self.ticker}.png")
            return None
        elif to == 'file':
            # 그래프를 HTML 파일로 저장
            plot(fig, filename=f'myprophet_{self.ticker}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

class CorpProphet(MyProphet):
    @staticmethod
    def prophet_ranking(refresh=False, top: Union[int, str] = 'all') -> OrderedDict:
        """
        Prophet 데이터를 기반으로 기업 순위를 계산합니다.

        매개변수:
            refresh (bool): 데이터를 새로 가져올지 여부.
            top (Union[int, str], optional): 상위 기업 개수. 'all'이면 전체 반환. 기본값은 'all'.

        반환값:
            OrderedDict: Prophet 점수를 기준으로 정렬된 기업 순위.
        """
        print("**** Start Compiling scores and sorting... ****")
        redis_name = 'prophet_ranking'

        print(
            f"redisname: '{redis_name}' / refresh : {refresh} / expire_time : {expire_time / 3600}h")

        def fetch_prophet_ranking() -> dict:
            data = {}
            c = tsa.CorpProphet('005930')
            for code in myredis.Corps.list_all_codes():
                try:
                    c.code = code
                except ValueError:
                    mylogger.error(f'prophet ranking error : {code}')
                    continue
                score = c.generate_latest_data(refresh=refresh).score
                print(f'{code} compiled : {score}')
                data[code] = score
            return data

        data_dict = myredis.Base.fetch_and_cache_data(redis_name, refresh, fetch_prophet_ranking, timer=expire_time)

        ranking = OrderedDict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))

        if top == 'all':
            return ranking
        else:
            if isinstance(top, int):
                return OrderedDict(list(ranking.items())[:top])
            else:
                raise ValueError("top 인자는 'all' 이나 int형 이어야 합니다.")


def test_export(self):
    #print(self.prophet.export_to(to='str'))
    #self.prophet.export_to(to='png')
    #self.prophet.export_to(to='htmlfile')
    self.prophet.export(to='show')
    self.prophet.ticker = self.test_tickers[2]
    self.prophet.export(to='show')

def test_visualization(self):
    self.prophet.visualization()
    self.prophet.ticker = self.test_tickers[2]
    self.prophet.visualization()