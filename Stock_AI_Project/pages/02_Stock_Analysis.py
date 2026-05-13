# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import streamlit as st
# import pandas as pd
# import yfinance as yf 
# import plotly.graph_objects as go
# import datetime
# import ta
# from utils.plotly_figure import plotly_table 

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Stock Analysis Pro",
#     page_icon="📈",
#     layout="wide",
# )

# st.title("📊 Stock Analysis Dashboard")

# # --- User Inputs ---
# col1, col2, col3 = st.columns(3)
# today = datetime.date.today()

# with col1:
#     ticker = st.text_input("Stock Ticker", "TSLA").upper()
# with col2:
#     start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
# with col3:
#     end_date = st.date_input("Choose End Date", today)

# # --- Fetch Data ---
# stock = yf.Ticker(ticker)
# data = yf.download(ticker, start=start_date, end=end_date)

# # FIX: Multi-index columns handling for YFinance
# if not data.empty:
#     if isinstance(data.columns, pd.MultiIndex):
#         data.columns = data.columns.get_level_values(0)
# else:
#     st.error("No data found for this ticker. Please check the symbol.")
#     st.stop()

# # --- Company Information ---
# st.subheader(f"About {ticker}")
# with st.expander("Company Summary"):
#     st.write(stock.info.get('longBusinessSummary', 'No summary available.'))
#     col_inf1, col_inf2 = st.columns(2)
#     col_inf1.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
#     col_inf1.write(f"**Employees:** {stock.info.get('fullTimeEmployees', 'N/A')}")
#     col_inf2.write(f"**Website:** [Visit Website]({stock.info.get('website', '#')})")

# # --- Financial Metrics ---
# st.markdown("---")
# col_m1, col_m2 = st.columns(2)

# with col_m1:
#     m_df1 = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
#     m_df1['Value'] = [
#         stock.info.get("marketCap", "N/A"),
#         stock.info.get("beta", "N/A"),
#         stock.info.get("trailingEps", "N/A"),
#         stock.info.get("trailingPE", "N/A")
#     ]
#     st.plotly_chart(plotly_table(m_df1), use_container_width=True)

# with col_m2:
#     m_df2 = pd.DataFrame(index=['Quick Ratio', 'Revenue/Share', 'Profit Margins', 'Debt to Equity', 'ROE'])
#     m_df2['Value'] = [
#         stock.info.get("quickRatio", "N/A"),
#         stock.info.get("revenuePerShare", "N/A"),
#         stock.info.get("profitMargins", "N/A"),
#         stock.info.get("debtToEquity", "N/A"),
#         stock.info.get("returnOnEquity", "N/A")
#     ]
#     st.plotly_chart(plotly_table(m_df2), use_container_width=True)

# # --- Daily Performance & History ---
# st.markdown("---")
# latest_price = float(data['Close'].iloc[-1])
# prev_price = float(data['Close'].iloc[-2])
# daily_change = latest_price - prev_price

# st.metric(label=f"{ticker} Latest Price", value=f"${latest_price:,.2f}", delta=f"{daily_change:,.2f}")

# with st.expander("View Last 10 Days History"):
#     last_10_df = data.tail(10).sort_index(ascending=False).round(3)
#     st.plotly_chart(plotly_table(last_10_df), use_container_width=True)

# # --- Interactive Graph Controls ---
# st.markdown("---")
# st.subheader("📈 Analysis Chart")
# c_col1, c_col2, _ = st.columns([1, 1, 2])

# with c_col1:
#     chart_type = st.selectbox('Select Chart Style', ('Candle', 'Line'))

# with c_col2:
#     # Option list theke 'None' ke pore dewa hoyeche jate MA/RSI default hoy
#     if chart_type == 'Candle':
#         indicators = st.selectbox('Select Indicator', ('RSI', 'MACD', 'None'))
#     else:
#         indicators = st.selectbox('Select Indicator', ('Moving Average', 'RSI', 'MACD', 'None'))

# # --- Main Professional Chart Section ---
# fig = go.Figure()

# if chart_type == 'Candle':
#     fig.add_trace(go.Candlestick(
#         x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
#         name='Market Price', increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
#     ))
# else:
#     fig.add_trace(go.Scatter(
#         x=data.index, y=data['Close'], mode='lines', name='Close Price',
#         line=dict(color='#2962ff', width=2.5)
#     ))

# # Indicators logic
# if indicators == 'Moving Average':
#     ma20 = data['Close'].rolling(window=20).mean()
#     fig.add_trace(go.Scatter(x=data.index, y=ma20, name='20 Day MA', line=dict(color='#ff9800', width=1.5, dash='dot')))

# # Styling
# fig.update_layout(
#     height=600, template="plotly_dark", hovermode="x unified",
#     xaxis=dict(showgrid=False, rangeslider=dict(visible=False)),
#     yaxis=dict(side="right", gridcolor="#2a2a2a", title="Price (USD)"),
#     margin=dict(l=10, r=10, t=30, b=10),
#     legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0)")
# )
# st.plotly_chart(fig, use_container_width=True)

# # RSI & MACD Sub-charts
# if indicators == 'RSI':
#     rsi_val = ta.momentum.rsi(data['Close'].squeeze(), window=14)
#     st.write("**Relative Strength Index (RSI)**")
#     rsi_fig = go.Figure(go.Scatter(x=data.index, y=rsi_val, name='RSI', line=dict(color='#b28dff', width=2)))
#     rsi_fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1)
#     rsi_fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1)
#     rsi_fig.update_layout(height=250, template="plotly_dark", yaxis=dict(side="right", range=[0, 100]))
#     st.plotly_chart(rsi_fig, use_container_width=True)

# elif indicators == 'MACD':
#     macd_obj = ta.trend.MACD(data['Close'].squeeze())
#     st.write("**MACD (Trend Momentum)**")
#     macd_fig = go.Figure()
#     macd_fig.add_trace(go.Bar(x=data.index, y=macd_obj.macd_diff(), name='Histogram', marker_color='gray', opacity=0.5))
#     macd_fig.add_trace(go.Scatter(x=data.index, y=macd_obj.macd(), name='MACD', line=dict(color='#2196f3')))
#     macd_fig.add_trace(go.Scatter(x=data.index, y=macd_obj.macd_signal(), name='Signal', line=dict(color='#ff5252')))
#     macd_fig.update_layout(height=280, template="plotly_dark", yaxis=dict(side="right"))
#     st.plotly_chart(macd_fig, use_container_width=True)







import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import yfinance as yf 
import plotly.graph_objects as go
import datetime
import ta

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Analysis Pro",
    page_icon="📈",
    layout="wide",
)

st.title("📊 Stock Analysis Dashboard")

# --- User Inputs ---
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA").upper()
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", today)

# --- Fetch Data ---
stock = yf.Ticker(ticker)
data = yf.download(ticker, start=start_date, end=end_date)

# Fix multi-index issue
if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
else:
    st.error("No data found for this ticker.")
    st.stop()

# --- Company Info ---
st.subheader(f"About {ticker}")
with st.expander("Company Summary"):
    st.write(stock.info.get('longBusinessSummary', 'No summary available.'))
    col_inf1, col_inf2 = st.columns(2)
    col_inf1.write(f"**Sector:** {stock.info.get('sector', 'N/A')}")
    col_inf1.write(f"**Employees:** {stock.info.get('fullTimeEmployees', 'N/A')}")
    col_inf2.write(f"**Website:** {stock.info.get('website', 'N/A')}")

# --- Financial Metrics (UPDATED) ---
st.markdown("---")
st.subheader("📊 Financial Metrics")

col_m1, col_m2 = st.columns(2)

with col_m1:
    m_df1 = pd.DataFrame({
        "Metric": ['Market Cap', 'Beta', 'EPS', 'PE Ratio'],
        "Value": [
            stock.info.get("marketCap", "N/A"),
            stock.info.get("beta", "N/A"),
            stock.info.get("trailingEps", "N/A"),
            stock.info.get("trailingPE", "N/A")
        ]
    })
    st.dataframe(m_df1, use_container_width=True)

with col_m2:
    m_df2 = pd.DataFrame({
        "Metric": ['Quick Ratio', 'Revenue/Share', 'Profit Margins', 'Debt to Equity', 'ROE'],
        "Value": [
            stock.info.get("quickRatio", "N/A"),
            stock.info.get("revenuePerShare", "N/A"),
            stock.info.get("profitMargins", "N/A"),
            stock.info.get("debtToEquity", "N/A"),
            stock.info.get("returnOnEquity", "N/A")
        ]
    })
    st.dataframe(m_df2, use_container_width=True)

# --- Price Info ---
st.markdown("---")
latest_price = float(data['Close'].iloc[-1])
prev_price = float(data['Close'].iloc[-2])
daily_change = latest_price - prev_price

st.metric(label=f"{ticker} Latest Price", value=f"${latest_price:,.2f}", delta=f"{daily_change:,.2f}")

# --- History Table ---
with st.expander("View Last 10 Days History"):
    last_10_df = data.tail(10).sort_index(ascending=False).round(3)
    st.dataframe(last_10_df, use_container_width=True)

# --- Chart Controls ---
st.markdown("---")
st.subheader("📈 Analysis Chart")

c1, c2 = st.columns(2)

with c1:
    chart_type = st.selectbox('Chart Type', ('Candle', 'Line'))

with c2:
    if chart_type == 'Candle':
        indicator = st.selectbox('Indicator', ('RSI', 'MACD', 'None'))
    else:
        indicator = st.selectbox('Indicator', ('Moving Average', 'RSI', 'MACD', 'None'))

# --- Chart ---
fig = go.Figure()

if chart_type == 'Candle':
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))
else:
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price'
    ))

# Moving Average
if indicator == 'Moving Average':
    ma = data['Close'].rolling(20).mean()
    fig.add_trace(go.Scatter(x=data.index, y=ma, name='20 MA'))

fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# --- RSI ---
if indicator == 'RSI':
    rsi = ta.momentum.rsi(data['Close'], window=14)
    st.write("RSI")
    st.line_chart(rsi)

# --- MACD ---
elif indicator == 'MACD':
    macd = ta.trend.MACD(data['Close'])
    st.write("MACD")
    st.line_chart(macd.macd())
