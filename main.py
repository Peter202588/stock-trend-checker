import streamlit as st
from trend_utils import resample_ma

st.title("📈 Stock MA Trend Checker")

st.markdown("输入你的股票数据 CSV（包含 date, close, vol）")

uploaded_file = st.file_uploader("上传CSV文件", type="csv")

if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    df.set_index("date", inplace=True)

    st.subheader("日线趋势")
    df_day = resample_ma(df, "D")
    st.line_chart(df_day[["close", "ma5", "ma10", "ma20"]])

    st.subheader("周线趋势")
    df_week = resample_ma(df, "W")
    st.line_chart(df_week[["close", "ma5", "ma10", "ma20"]])

    st.subheader("月线趋势")
    df_month = resample_ma(df, "M")
    st.line_chart(df_month[["close", "ma5", "ma10", "ma20"]])
