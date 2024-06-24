import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random

def get_market_cap(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info['marketCap']
    except:
        st.warning(f"Could not fetch data for {ticker}")
        return None

def visualize_market_caps(tickers):
    market_caps = []
    valid_tickers = []
    for ticker in tickers:
        cap = get_market_cap(ticker)
        if cap is not None:
            market_caps.append(cap)
            valid_tickers.append(ticker)
    
    if not market_caps:
        st.error("No valid market cap data available.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    
    max_cap = max(market_caps)
    max_radius = 0.4  # 최대 원의 반지름
    
    x_position = 0
    for ticker, cap in zip(valid_tickers, market_caps):
        radius = (cap / max_cap) * max_radius
        color = f'#{random.randint(0, 0xFFFFFF):06x}'
        circle = Circle((x_position, 0), radius, fill=True, alpha=0.6, color=color)
        ax.add_patch(circle)
        ax.text(x_position, -max_radius - 0.05, f"{ticker}\n${cap/1e9:.1f}B", ha='center', va='top')
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
