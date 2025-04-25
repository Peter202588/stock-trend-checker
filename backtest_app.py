import streamlit as st
import pandas as pd
import tushare as ts
from tqdm import tqdm

# 初始化 tushare pro
pro = ts.pro_api('你的tushare token')

def get_monthly_data(ts_code, start_date):
    try:
        df = pro.monthly(ts_code=ts_code, start_date=start_date)
        df = df.sort_values('trade_date', ascending=True)
        df['M5'] = df['close'].rolling(window=5).mean()
        df['M10'] = df['close'].rolling(window=10).mean()
        return df
    except:
        return None

def check_condition(df):
    if df is None or len(df) < 10:
        return False
    df_recent = df.iloc[-3:]
    for idx, row in df_recent.iterrows():
        if row['M5'] <= row['M10']:
            return False
    return True

def filter_stocks(start_date):
    stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
    results = []
    for _, row in tqdm(stock_basic.iterrows(), total=len(stock_basic)):
        ts_code = row['ts_code']
        df = get_monthly_data(ts_code, start_date)
        if check_condition(df):
            results.append({"ts_code": ts_code, "name": row['name']})
    return pd.DataFrame(results)

st.title("连续3月M5大于M10股票筛选")

start_date = st.text_input("输入开始日期 (例如20220101)", value="20220101")

if st.button("开始筛选"):
    with st.spinner('筛选中... 请稍等'):
        result_df = filter_stocks(start_date)
        st.success(f"筛选完成，共找到 {len(result_df)} 支股票！")
        st.dataframe(result_df)
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="下载结果 CSV", data=csv, file_name='筛选结果.csv', mime='text/csv')
