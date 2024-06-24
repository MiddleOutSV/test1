import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Streamlit 앱 설정
st.title('주식 시가 총액 크기 비교')

# 사용자 입력 받기
tickers = st.text_input('주식 티커를 콤마로 구분하여 입력하세요', 'AAPL,MSFT,GOOGL,AMZN,TSLA')

# 주식 데이터를 가져오고 시가 총액 계산
def get_market_caps(tickers):
    market_caps = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            market_cap = stock.info['marketCap']
            if market_cap:
                market_caps[ticker] = market_cap
            else:
                st.warning(f'{ticker}의 시가 총액 정보를 가져올 수 없습니다.')
        except Exception as e:
            st.error(f'{ticker}의 데이터를 가져오는 중 오류가 발생했습니다: {e}')
    return market_caps

if tickers:
    tickers = [ticker.strip().upper() for ticker in tickers.split(',')]
    market_caps = get_market_caps(tickers)

    # 시가 총액 시각화
    if market_caps:
        fig, ax = plt.subplots()
        sizes = [market_caps[ticker] for ticker in tickers if ticker in market_caps]
        labels = [ticker for ticker in tickers if ticker in market_caps]

        # 시가 총액 순으로 정렬
        sorted_indices = np.argsort(sizes)[::-1]
        sizes = [sizes[i] for i in sorted_indices]
        labels = [labels[i] for i in sorted_indices]

        max_size = max(sizes)
        max_circle_diameter = plt.gcf().get_size_inches()[0] * plt.gcf().dpi / 5  # 화면 전체 크기의 5분의 1

        scaled_sizes = [(size / max_size) * max_circle_diameter**2 for size in sizes]
        colors = [plt.cm.tab20(i / len(scaled_sizes)) for i in range(len(scaled_sizes))]

        # 가로선상에 위치 설정
        gap = 1.2  # 각 원 사이의 간격 조정
        x_positions = np.arange(len(scaled_sizes)) * gap
        y_position = [0] * len(scaled_sizes)
        
        # 원 그리기
        for x, y, size, color, label in zip(x_positions, y_position, scaled_sizes, colors, labels):
            circle = plt.Circle((x, y), np.sqrt(size / np.pi), color=color, alpha=0.5)
            ax.add_artist(circle)
            ax.text(x, y, label, horizontalalignment='center', verticalalignment='center')

        ax.set_aspect('equal', 'box')
        plt.axis('off')
        st.pyplot(fig)
    else:
        st.info('유효한 티커를 입력하세요.')
else:
    st.info('주식 티커를 입력하세요.')
