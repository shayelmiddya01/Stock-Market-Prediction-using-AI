# import streamlit as st
# import pandas as pd
# import yfinance as yf
# import datetime
# import plotly.graph_objects as go
# import numpy as np
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense

# # ------------------- App Config -------------------
# st.set_page_config(page_title="Stock Prediction Dashboard", layout="wide")

# st.title("📈 AI Based Stock Prediction Dashboard")
# st.markdown("Stock Analysis & future prediction using AI based Model")

# # ------------------- Company Mapping -------------------
# company_dict = {
#     "TESLA": "TSLA",
#     "APPLE": "AAPL",
#     "GOOGLE": "GOOGL",
#     "AMAZON": "AMZN",
#     "MICROSOFT": "MSFT",
#     "RELIANCE": "RELIANCE.NS",
#     "TCS": "TCS.NS",
#     "INFOSYS": "INFY.NS"
# }

# # ------------------- Inputs -------------------
# col1, col2, col3 = st.columns(3)

# with col1:
#     user_input = st.text_input(" Company / Symbol", "AAPL").strip().upper()
#     ticker = company_dict.get(user_input, user_input)

# with col2:
#     start_date = st.date_input(
#         "📅 Start Date",
#         datetime.date.today() - datetime.timedelta(days=365)
#     )

# with col3:
#     end_date = st.date_input(
#         "📅 End Date",
#         datetime.date.today()
#     )

# future_days = st.slider("📊 Prediction Time Horizon (Days)", 1, 15, 5)

# # ------------------- Date Fix -------------------
# today = datetime.date.today()

# if end_date > today:
#     st.warning("End date adjusted to today.")
#     end_date = today

# if start_date >= end_date:
#     st.error("Start Date must be earlier than End Date")
#     st.stop()

# # ------------------- Load Data -------------------
# @st.cache_data(show_spinner=False)
# def load_data(symbol, start, end):
#     try:
#         df = yf.download(symbol, start=start, end=end, progress=False)
#         if df.empty:
#             return None
#         return df
#     except:
#         return None

# df = load_data(ticker, start_date, end_date)

# if df is None:
#     st.error(" No data found. Check stock or date.")
#     st.stop()

# # Fix columns
# if isinstance(df.columns, pd.MultiIndex):
#     df.columns = df.columns.get_level_values(0)

# df.reset_index(inplace=True)

# # ------------------- Live Price -------------------
# live_price = float(df["Close"].iloc[-1])

# if len(df) > 1:
#     prev = float(df["Close"].iloc[-2])
#     change = live_price - prev
#     percent = (change / prev) * 100
# else:
#     change, percent = 0, 0

# color = "green" if change >= 0 else "red"
# arrow = "▲" if change >= 0 else "▼"

# st.markdown(f"""
# <h2 style="color:{color}">₹{round(live_price,2)} {arrow}</h2>
# <p style="color:{color}">{round(change,2)} ({round(percent,2)}%)</p>
# """, unsafe_allow_html=True)

# # ------------------- Graph -------------------
# st.subheader(" Live Price Trend Graph")

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines"))

# st.plotly_chart(fig, use_container_width=True)

# # ------------------- MA -------------------
# df["MA"] = df["Close"].rolling(10).mean()
# valid_df = df.dropna()

# rmse = np.sqrt(mean_squared_error(valid_df["Close"], valid_df["MA"])) if len(valid_df) > 0 else 0

# # ------------------- LSTM -------------------
# time_step = 10

# if len(df) > time_step + 5:
#     try:
#         data = df[['Close']].values
#         scaler = MinMaxScaler()
#         scaled = scaler.fit_transform(data)

#         X, y = [], []
#         for i in range(time_step, len(scaled)):
#             X.append(scaled[i-time_step:i, 0])
#             y.append(scaled[i, 0])

#         X, y = np.array(X), np.array(y)
#         X = X.reshape(X.shape[0], X.shape[1], 1)

#         model = Sequential([
#             LSTM(50, input_shape=(X.shape[1], 1)),
#             Dense(1)
#         ])

#         model.compile(optimizer='adam', loss='mse')
#         model.fit(X, y, epochs=3, batch_size=16, verbose=0)

#         last_batch = scaled[-time_step:].reshape(1, time_step, 1)

#         future_pred = []
#         for _ in range(future_days):
#             pred = model.predict(last_batch, verbose=0)[0]
#             future_pred.append(pred)
#             last_batch = np.append(last_batch[:, 1:, :], [[pred]], axis=1)

#         future_pred = scaler.inverse_transform(future_pred).flatten()

#     except:
#         future_pred = np.array([live_price]*future_days)

# else:
#     future_pred = np.array([live_price]*future_days)

# # ------------------- Future Dates -------------------
# future_dates = pd.date_range(df["Date"].iloc[-1], periods=future_days+1)[1:]

# future_df = pd.DataFrame({
#     "Date": future_dates,
#     "Predicted Price": future_pred
# })

# # ------------------- Chart Type -------------------
# st.subheader("📈 Price Chart")

# chart_type = st.selectbox("📊 Select Chart Type", ["Line", "Candlestick", "Bar", "Area"])

# chart = go.Figure()

# if chart_type == "Line":
#     chart.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines"))

# elif chart_type == "Candlestick":
#     chart.add_trace(go.Candlestick(
#         x=df["Date"],
#         open=df["Open"],
#         high=df["High"],
#         low=df["Low"],
#         close=df["Close"]
#     ))

# elif chart_type == "Bar":
#     chart.add_trace(go.Bar(x=df["Date"], y=df["Close"]))

# elif chart_type == "Area":
#     chart.add_trace(go.Scatter(x=df["Date"], y=df["Close"], fill='tozeroy'))

# # MA
# chart.add_trace(go.Scatter(x=df["Date"], y=df["MA"], name="MA", line=dict(dash="dash")))

# # Prediction
# chart.add_trace(go.Scatter(x=future_df["Date"], y=future_df["Predicted Price"], name="Prediction"))

# st.plotly_chart(chart, use_container_width=True)

# # ------------------- Tables -------------------
# st.subheader("📊 Recent Data")
# st.dataframe(df.tail(5))

# st.subheader("📊 Future Prediction")
# st.dataframe(future_df)

# # ------------------- Chat -------------------
# st.subheader("💬 Chat")

# if "msg" not in st.session_state:
#     st.session_state.msg = []

# for m in st.session_state.msg:
#     st.write(m)

# user_msg = st.text_input("Ask something...")

# if user_msg:
#     st.session_state.msg.append(f"You: {user_msg}")
#     st.session_state.msg.append(f"Bot: Stock analysis feature coming soon!")



 

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ------------------- App Config -------------------
st.set_page_config(page_title="AI Stock Prediction", layout="wide")

st.title("🌍 Global AI Stock Prediction Dashboard")

st.markdown("Search ANY company stock symbol from all over the world")

# ------------------- User Input -------------------
col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input(
        "Enter Company Symbol",
        "AAPL"
    ).strip().upper()

with col2:
    start_date = st.date_input(
        "Start Date",
        datetime.date.today() - datetime.timedelta(days=365)
    )

with col3:
    end_date = st.date_input(
        "End Date",
        datetime.date.today()
    )

future_days = st.slider(
    "Prediction Days",
    1,
    30,
    7
)

# ------------------- Date Validation -------------------
today = datetime.date.today()

if end_date > today:
    end_date = today

if start_date >= end_date:
    st.error("Start date must be smaller than end date")
    st.stop()

# ------------------- Load Data -------------------
@st.cache_data(show_spinner=False)
def load_data(symbol, start, end):

    try:
        df = yf.download(
            symbol,
            start=start,
            end=end,
            progress=False
        )

        if df.empty:
            return None

        return df

    except:
        return None

df = load_data(ticker, start_date, end_date)

if df is None:
    st.error("No stock data found")
    st.info("""
Examples:

AAPL = Apple  
TSLA = Tesla  
MSFT = Microsoft  
GOOGL = Google  
AMZN = Amazon  
NVDA = Nvidia  

Indian Stocks:
RELIANCE.NS
TCS.NS
INFY.NS
SBIN.NS
""")
    st.stop()

# ------------------- Fix Columns -------------------
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.reset_index(inplace=True)

# ------------------- Live Price -------------------
live_price = float(df["Close"].iloc[-1])

if len(df) > 1:

    prev = float(df["Close"].iloc[-2])

    change = live_price - prev

    percent = (change / prev) * 100

else:

    change = 0
    percent = 0

color = "green" if change >= 0 else "red"

arrow = "▲" if change >= 0 else "▼"

st.markdown(
    f"""
    <h1 style='color:{color}'>
    ${round(live_price,2)} {arrow}
    </h1>

    <h4 style='color:{color}'>
    {round(change,2)} ({round(percent,2)}%)
    </h4>
    """,
    unsafe_allow_html=True
)

# ------------------- Main Graph -------------------
st.subheader("📈 Live Stock Graph")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Close"],
        mode="lines",
        name="Close Price"
    )
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# ------------------- Moving Average -------------------
df["MA10"] = df["Close"].rolling(10).mean()

valid_df = df.dropna()

if len(valid_df) > 0:

    rmse = np.sqrt(
        mean_squared_error(
            valid_df["Close"],
            valid_df["MA10"]
        )
    )

else:

    rmse = 0

# ------------------- LSTM AI Model -------------------
time_step = 10

if len(df) > time_step + 5:

    try:

        data = df[["Close"]].values

        scaler = MinMaxScaler()

        scaled_data = scaler.fit_transform(data)

        X = []
        y = []

        for i in range(time_step, len(scaled_data)):

            X.append(
                scaled_data[i-time_step:i, 0]
            )

            y.append(
                scaled_data[i, 0]
            )

        X = np.array(X)
        y = np.array(y)

        X = X.reshape(
            X.shape[0],
            X.shape[1],
            1
        )

        model = Sequential()

        model.add(
            LSTM(
                50,
                input_shape=(X.shape[1], 1)
            )
        )

        model.add(Dense(1))

        model.compile(
            optimizer="adam",
            loss="mse"
        )

        model.fit(
            X,
            y,
            epochs=5,
            batch_size=16,
            verbose=0
        )

        # Future Prediction
        last_batch = scaled_data[-time_step:]

        last_batch = last_batch.reshape(
            1,
            time_step,
            1
        )

        future_predictions = []

        for i in range(future_days):

            pred = model.predict(
                last_batch,
                verbose=0
            )[0]

            future_predictions.append(pred)

            last_batch = np.append(
                last_batch[:, 1:, :],
                [[pred]],
                axis=1
            )

        future_predictions = scaler.inverse_transform(
            future_predictions
        ).flatten()

    except:

        future_predictions = np.array(
            [live_price] * future_days
        )

else:

    future_predictions = np.array(
        [live_price] * future_days
    )

# ------------------- Future Dates -------------------
future_dates = pd.date_range(
    df["Date"].iloc[-1],
    periods=future_days + 1
)[1:]

future_df = pd.DataFrame({

    "Date": future_dates,

    "Predicted Price": future_predictions
})

# ------------------- Chart Type -------------------
st.subheader("📊 Advanced Chart")

chart_type = st.selectbox(

    "Select Chart Type",

    [
        "Line",
        "Candlestick",
        "Bar",
        "Area"
    ]
)

chart = go.Figure()

# Line
if chart_type == "Line":

    chart.add_trace(

        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close"
        )
    )

# Candlestick
elif chart_type == "Candlestick":

    chart.add_trace(

        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )
    )

# Bar
elif chart_type == "Bar":

    chart.add_trace(

        go.Bar(
            x=df["Date"],
            y=df["Close"]
        )
    )

# Area
elif chart_type == "Area":

    chart.add_trace(

        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            fill="tozeroy"
        )
    )

# Moving Average
chart.add_trace(

    go.Scatter(
        x=df["Date"],
        y=df["MA10"],
        name="MA10",
        line=dict(dash="dash")
    )
)

# Future Prediction
chart.add_trace(

    go.Scatter(
        x=future_df["Date"],
        y=future_df["Predicted Price"],
        mode="lines+markers",
        name="AI Prediction"
    )
)

chart.update_layout(height=600)

st.plotly_chart(chart, use_container_width=True)

# ------------------- Metrics -------------------
st.subheader("📌 Stock Metrics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Current Price",
    round(live_price, 2)
)

c2.metric(
    "Prediction RMSE",
    round(rmse, 2)
)

c3.metric(
    "Prediction Days",
    future_days
)

# ------------------- Tables -------------------
st.subheader("📋 Recent Stock Data")

st.dataframe(
    df.tail(10),
    use_container_width=True
)

st.subheader("🤖 Future Prediction")

st.dataframe(
    future_df,
    use_container_width=True
)

# ------------------- Download Prediction -------------------
csv = future_df.to_csv(index=False)

st.download_button(
    "⬇ Download Prediction CSV",
    csv,
    file_name=f"{ticker}_prediction.csv",
    mime="text/csv"
)

# ------------------- AI Chat -------------------
st.subheader("💬 AI Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.write(msg)

user_msg = st.text_input(
    "Ask about this stock..."
)

if user_msg:

    st.session_state.messages.append(
        f"You: {user_msg}"
    )

    bot_reply = f"""
AI Analysis for {ticker}:

Current Price = {round(live_price,2)}

Predicted after {future_days} days =
{round(future_predictions[-1],2)}

Trend Analysis:
{"Bullish 📈" if future_predictions[-1] > live_price else "Bearish 📉"}
"""

    st.session_state.messages.append(
        f"Bot: {bot_reply}"
    )

    st.write(bot_reply)