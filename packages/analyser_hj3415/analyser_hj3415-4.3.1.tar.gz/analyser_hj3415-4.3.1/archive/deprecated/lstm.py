class MyLstm:
    def export(self, refresh=False, to="html", num=5) -> Optional[str]:
        """
        과거 및 예측된 주가 데이터를 기반으로 시각화를 생성하고 저장합니다.

        매개변수:
            refresh (bool): 데이터 새로고침 여부. 기본값은 False.
            to (str): 그래프 출력 형식 ('hrml', 'png', 'file'). 기본값은 'html'.
            num (int): 예측 모델 수. 기본값은 5.

        반환값:
            Optional[str]: HTML 형식의 그래프 문자열(`to='html'`인 경우).
            None: PNG 또는 HTML 파일로 저장된 경우.

        예외:
            Exception: 잘못된 `to` 값이 주어졌을 때 발생.
        """
        def prepare_past_data(past_days) -> tuple:
            # 데이터 준비
            raw_data_copied = self.raw_data.reset_index()
            data = raw_data_copied[['Date', 'Close']][-past_days:].reset_index(drop=True)

            # 'Date'와 'Close' 열 추출
            past_dates = pd.to_datetime(data['Date'])
            past_prices = data['Close']

            # 'past_prices'가 Series인지 확인
            if isinstance(past_prices, pd.DataFrame):
                past_prices = past_prices.squeeze()

            # 'Close' 열의 데이터 타입 변경
            past_prices = past_prices.astype(float)
            return past_dates, past_prices

        def prepare_future_data(refresh_in, num_in) -> tuple:
            future_data, lstm_grade = self.get_final_predictions(refresh=refresh_in, num=num_in)

            # 예측 데이터 준비
            future_dates = pd.to_datetime(list(future_data.keys()))

            future_prices = pd.Series(future_data.values(), index=range(len(future_data.values()))).astype(float)
            return future_dates, future_prices

        self.initializing()
        past_dates, past_prices = prepare_past_data(past_days=120)
        future_dates, future_prices = prepare_future_data(refresh_in=refresh, num_in=num)

        # 그래프 생성
        fig = go.Figure()

        # 실제 데이터 추가
        fig.add_trace(go.Scatter(
            x=past_dates,
            y=past_prices,
            mode='markers',
            name='실제주가'
        ))

        # 예측 데이터 추가
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_prices,
            mode='lines+markers',
            name='예측치(30일)'
        ))

        # 레이아웃 업데이트
        fig.update_layout(
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis=dict(
                tickformat='%Y/%m',
            ),
            yaxis=dict(
                tickformat=".0f",
            ),
            showlegend=True,
        )

        mylogger.debug(f"past_dates({len(past_dates)}) - {past_dates}")
        mylogger.debug(f"past_prices({len(past_prices)} - {past_prices}")
        mylogger.debug(f"future_dates({len(future_dates)}) - {future_dates}")
        mylogger.debug(f"future_prices({len(future_prices)}) - {future_prices}")

        fig.update_layout(
            # title=f'{self.code} {self.name} 주가 예측 그래프(prophet)',
            xaxis_title='일자',
            yaxis_title='주가(원)',
            xaxis=dict(
                tickformat='%Y/%m',  # X축을 '연/월' 형식으로 표시
            ),
            yaxis=dict(
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
            fig.write_image(f"myLSTM_{self.ticker}.png")
            return None
        elif to == 'file':
            # 그래프를 HTML로 저장
            plot(fig, filename=f'myLSTM_{self.ticker}.html', auto_open=False)
            return None
        else:
            Exception("to 인자가 맞지 않습니다.")

    def visualization(self, refresh=True):
        """
        실제 주가와 예측 주가를 시각화합니다.

        매개변수:
            refresh (bool): 예측 데이터를 새로고침할지 여부. 기본값은 True.

        반환값:
            None: 시각화를 출력합니다.
        """
        self.initializing()
        future_data, _ = self.get_final_predictions(refresh=refresh)
        mylogger.debug(f'future_data : {future_data}')
        future_dates = pd.to_datetime(list(future_data.keys()))
        mylogger.debug(f'future_dates : {future_dates}')
        future_prices = pd.Series(future_data.values(), index=range(len(future_data.values()))).astype(float)
        mylogger.debug(f'future_prices : {future_prices}')

        # 시각화1
        plt.figure(figsize=(10, 6))

        # 실제 주가
        plt.plot(self.raw_data.index, self.raw_data['Close'], label='Actual Price')

        # 미래 주가 예측
        plt.plot(future_dates, future_prices, label='Future Predicted Price', linestyle='--')

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.title(f'{self.ticker} Stock Price Prediction with LSTM')
        plt.show()

        """# 시각화2
        plt.figure(figsize=(10, 6))
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], self.lstm_data.data_2d[self.lstm_data.train_size + 60:], label='Actual Price')
        plt.plot(self.raw_data.index[self.lstm_data.train_size + 60:], lstm_grade.mean_test_predictions_2d, label='Predicted Price')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.title('Stock Price Prediction with LSTM Ensemble')
        plt.show()"""



def test_export(my_lstm_fixture):
    lstm, _, _, _ = my_lstm_fixture
    html_str = lstm.export(refresh=False, to='html')
    print(html_str)
    lstm.export(refresh=False, to='file')
    lstm.export(refresh=True, to='png', num=1)


def test_visualization(my_lstm_fixture):
    lstm, _, _, _ = my_lstm_fixture
    lstm.visualization(refresh=False)