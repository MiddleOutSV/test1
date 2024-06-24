import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import random

def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['marketCap']

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def visualize_market_caps(tickers, market_caps):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    max_cap = max(market_caps)
    max_radius = 0.4  # 최대 원의 반지름
    
    x_position = 0
    for ticker, cap in zip(tickers, market_caps):
        radius = (cap / max_cap) * max_radius
        circle = Circle((x_position, 0), radius, fill=True, alpha=0.6)
        ax.add_patch(circle)
        ax.text(x_position, -max_radius - 0.05, ticker, ha='center')
        x_position += 2 * max_radius + 0.1  # 원 사이의 간격
    
    ax.set_xlim(-max_radius, x_position - max_radius)
    ax.set_ylim(-max_radius - 0.2, max_radius)
    ax.set_aspect('equal')  # 원이 찌그러지지 않도록 비율 설정
    ax.axis('off')
    
    plt.title('주식 시가 총액 크기 비교')
    st.pyplot(fig)

st.title('주식 시가총액 비교 시각화')

tickers_input = st.text_input('ticker 심볼들을 쉼표로 구분하여 입력하세요 (예: AAPL,MSFT,GOOGL):')

if tickers_input:
    tickers = [ticker.strip() for ticker in tickers_input.split(',')]
    visualize_market_caps(tickers)
