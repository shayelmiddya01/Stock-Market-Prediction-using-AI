# import streamlit as st

# st.set_page_config(
#     page_title="Stock Market Prediction AI",
#     page_icon="📈",
#     layout="wide"
# )

# st.title("📊 Stock Market Prediction (AI Based)")

# st.sidebar.title("📌 Navigation")
# page = st.sidebar.selectbox(
#     "Select Page",
#     ("Home", "Stock Analysis", "Stock Prediction")
# )

# if page == "Home":
#     st.write("Home Page Content")

# elif page == "Stock Analysis":
#     st.write("Stock Analysis Content")

# elif page == "Stock Prediction":
#     st.write("Stock Prediction Content")






# # import streamlit as st

# # st.set_page_config(
# #     page_title="Stock Market Prediction AI",
# #     page_icon="📈",
# #     layout="wide"
# # )

# # st.title("📊 Stock Market Prediction (AI Based)")

# # st.sidebar.title("📌 Navigation")
# # page = st.sidebar.selectbox(
# #     "Select Page",
# #     ("Home", "Trading App", "Stock Analysis", "Stock Prediction")
# # )

# # if page == "Home":
# #     st.write("Welcome to Stock AI App")

# # elif page == "Trading App":
# #     import Trading_App

# # elif page == "Stock Analysis":
# #     import Stock_Analysis   

# # elif page == "Stock Prediction":
# #     import Stock_prediction /







# import streamlit as st

# st.set_page_config(page_title="Stock AI", layout="wide")

# # 🔥 Custom CSS (dark theme + design)
# st.markdown("""
# <style>
# body {
#     background-color: #0b0f19;
#     color: white;
# }

# .navbar {
#     display:flex;
#     justify-content: space-between;
#     padding:20px 40px;
#     font-size:18px;
# }

# .logo {
#     font-weight:bold;
#     color:#00f5c4;
# }

# .menu a {
#     margin: 0 15px;
#     color:white;
#     text-decoration:none;
# }

# .hero {
#     display:flex;
#     align-items:center;
#     justify-content:space-between;
#     padding:60px;
# }

# .hero-text h1 {
#     font-size:48px;
# }

# .highlight {
#     color:#00f5c4;
# }

# .btn {
#     background:#00f5c4;
#     padding:10px 20px;
#     border:none;
#     border-radius:5px;
#     margin-top:20px;
#     cursor:pointer;
# }

# .card-container {
#     display:flex;
#     justify-content:space-around;
#     margin-top:40px;
# }

# .card {
#     background:#111827;
#     padding:20px;
#     border-radius:10px;
#     width:20%;
#     text-align:center;
# }
# </style>
# """, unsafe_allow_html=True)

# # 🔝 Navbar
# st.markdown("""
# <div class="navbar">
#   <div class="logo">Stock Market</div>
#   <div class="menu">
#     <a href="#">Home</a>
#     <a href="#">Market</a>
#     <a href="#">News</a>
#     <a href="#">About</a>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # 🏆 Hero Section
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("""
#     <div class="hero-text">
#         <h1>
#         Stock <span class="highlight">Market</span><br>
#         is the Best Way to <br>
#         <span class="highlight">Invest</span> your Money
#         </h1>
#         <p>Learn smart investing using AI tools.</p>
#         <button class="btn">Learn More</button>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.image("01_app.png")

# # 📊 Cards Section
# st.markdown("""
# <div class="card-container">
#   <div class="card">S&P 500 📈 +1.5%</div>
#   <div class="card">Nasdaq 📈 +2.2%</div>
#   <div class="card">Bitcoin 📉 -0.8%</div>
#   <div class="card">EUR/USD 📉 -0.5%</div>
# </div>
# """, unsafe_allow_html=True)




import streamlit as st

st.set_page_config(page_title="Stock Market Prediction Using AI Based", layout="wide")

# 🔥 Session State
if "show_info" not in st.session_state:
    st.session_state.show_info = False

if "card_info" not in st.session_state:
    st.session_state.card_info = ""

# 🎨 Custom CSS (UPDATED)
st.markdown("""
<style>
body {
    background-color: #0b0f19;
    color: white;
}

/* 🔥 Big Gradient Heading */
.main-heading {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f5c4, #00c3ff, #7a5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 20px;
    text-shadow: 0px 0px 20px rgba(0,255,200,0.3);
}

.navbar {
    display:flex;
    justify-content: space-between;
    padding:20px 40px;
    font-size:18px;
}

.logo {
    font-weight:bold;
    color:#00f5c4;
}

.menu a {
    margin: 0 15px;
    color:white;
    text-decoration:none;
}

.hero-text h1 {
    font-size:48px;
}

.highlight {
    color:#00f5c4;
}

.card {
    background:#111827;
    padding:15px;
    border-radius:10px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# 🔝 🔥 Stylish Heading
st.markdown("""
<div class="main-heading">
Stock Market Prediction Using AI Based
</div>
""", unsafe_allow_html=True)

# 🏆 Hero Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="hero-text">
        <h1>
        Stock <span class="highlight">Market</span><br>
        is the Best Way to <br>
        <span class="highlight">Invest</span> your Money
        </h1>
        <p>Build wealth smartly using AI-powered tools and real-time insights.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Learn More About Investing"):
        st.session_state.show_info = not st.session_state.show_info

    if st.session_state.show_info:
        st.success("""
### 📊 Welcome to Smart Investing!

Stock market investing is one of the most powerful ways to grow your money over time.  

✔️ **Grow Wealth**  
✔️ **Passive Income**  
✔️ **AI Insights**  
✔️ **Long-Term Stability**  

💡 Always research before investing.
""")

with col2:
    st.image("01_app.png")

# 📊 Cards Section
# 📊 Cards Section
# 📊 Cards Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("S&P 500 📈 +1.5%"):
        st.session_state.card_info = """
### 🇺🇸 S&P 500

👉 Tracks 500 big companies in the USA  
👉 Shows overall market performance  

📊 +1.5% → Market is going up today  
💡 Good for long-term investment
"""

with col2:
    if st.button("Nasdaq 📈 +2.2%"):
        st.session_state.card_info = """
### 💻 Nasdaq

👉 Focuses on technology companies  
👉 Includes companies like Apple, Google  

📊 +2.2% → Tech stocks are rising  
💡 Good for growth investing
"""

with col3:
    if st.button("Bitcoin 📉 -0.8%"):
        st.session_state.card_info = """
### 🪙 Bitcoin

👉 Digital money (crypto)  
👉 Price changes very fast  

📉 -0.8% → Price is going down today  
⚠️ High risk but high return
"""

with col4:
    if st.button("EUR/USD 📉 -0.5%"):
        st.session_state.card_info = """
### 💱 EUR/USD

👉 Euro vs US Dollar  
👉 Used in forex trading  

📉 -0.5% → Dollar is getting stronger  
💡 Used for short-term trading
"""
# 🔥 Show Details
if st.session_state.card_info:
    st.info(st.session_state.card_info)