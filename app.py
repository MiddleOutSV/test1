import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import random

def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['marketCap']

def visualize_market_caps(tickers):
    market_caps = []
    for ticker in tickers:
        try:
            market_cap = get_market_cap(ticker)
            market_caps.append((ticker, market_cap))
        except:
            st.warning(f"Could not fetch data for {ticker}")
    
    market_caps.sort(key=lambda x: x[1], reverse=True)
    
    fig, ax = plt.subplots(figsize=(10, 2))
    max_size = fig.get_size_inches()[0] * fig.dpi * 0.2  # 화면의 5분의 1
    
    circles = []
    for i, (ticker, market_cap) in enumerate(market_caps):
        size = (market_cap / market_caps[0][1]) * max_size
        color = f'#{random.randint(0, 0xFFFFFF):06x}'
        circle = plt.Circle((0, 0), size/2, color=color, alpha=0.7)
        circles.append((circle, size))
    
    total_width = sum(size for _, size in circles) + (len(circles) - 1) * max_size * 0.05
    start_x = -total_width / 2
    
    for (circle, size), (ticker, _) in zip(circles, market_caps):
        circle.center = (start_x + size/2, 0)
        ax.add_artist(circle)
        ax.text(start_x + size/2, -max_size/2 - 10, ticker, ha='center', va='top')
        start_x += size + max_size * 0.05
    
    ax.set_xlim(-total_width/2 - max_size*0.1, total_width/2 + max_size*0.1)
    ax.set_ylim(-max_size/2 - 20, max_size/2)
    ax.axis('off')
    
    st.pyplot(fig)

st.title('주식 시가총액 비교 시각화')

tickers_input = st.text_input('ticker 심볼들을 쉼표로 구분하여 입력하세요 (예: AAPL,MSFT,GOOGL):')

if tickers_input:
    tickers = [ticker.strip() for ticker in tickers_input.split(',')]
    visualize_market_caps(tickers)
