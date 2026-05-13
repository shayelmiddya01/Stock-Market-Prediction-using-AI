import streamlit as st

st.set_page_config(
     page_title = "Trading Guider",
     page_icon = ":chart_with_upwards_trend:", 
     layout = "wide"
)

st.title("Trading Guider :bar_chart:")
st.header("We Provide the Greatest platform for you to collect all information prior to investing in stock.")


try:
    st.image("app.png")
except:
    st.warning("app.png ")

st.markdown("## We provide the following services:")


st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stock.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted prices for the next 30 days based on historical stock data and advanced forecasting models.")

st.markdown("#### :three: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return based on risk.")

st.markdown("#### :four: CAPM Beta")
st.write("Calculate Beta and Expected Return for Individual Stock.")