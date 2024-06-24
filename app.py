import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
import random

# 주식 티커 입력
tickers = st.text_input('Enter stock tickers (comma separated):', 'AAPL, MSFT, GOOGL, AMZN')

# 시가 총액 데이터 가져오기
tickers_list = tickers.split(',')
data = yf.Tickers(tickers_list)
market_caps = {ticker: data.tickers[ticker].info['marketCap'] for ticker in tickers_list}
sorted_market_caps = dict(sorted(market_caps.items(), key=lambda item: item[1], reverse=True))

# 원 크기 계산
max_diameter = st.sidebar.slider("Maximum diameter (as fraction of screen width):", 0.1, 0.5, 0.2)
screen_width = st.sidebar.number_input("Screen width in pixels:", 800)
max_radius = (max_diameter * screen_width) / 2

max_market_cap = max(sorted_market_caps.values())
diameters = {ticker: (market_cap / max_market_cap) * max_diameter * screen_width for ticker, market_cap in sorted_market_caps.items()}
radii = {ticker: diameter / 2 for ticker, diameter in diameters.items()}

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
current_x = 0

for ticker in sorted_market_caps.keys():
    radius = radii[ticker]
    color = (random.random(), random.random(), random.random())
    circle = plt.Circle((current_x + radius, radius), radius, color=color, alpha=0.6)
    ax.add_artist(circle)
    ax.text(current_x + radius, radius, ticker, horizontalalignment='center', verticalalignment='center')
    current_x += radius * 2 + 10  # Adding a small gap between circles

ax.set_xlim(0, current_x)
ax.set_ylim(0, max_radius * 2)
ax.set_aspect('equal', 'box')
ax.axis('off')

st.pyplot(fig)
