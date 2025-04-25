import pandas as pd

def resample_kline(df, freq='W'):
    """
    将日线行情重采样为周线或月线
    :param df: 包含 ['trade_date', 'open', 'high', 'low', 'close', 'vol'] 等字段
    :param freq: 'W' 表示周线，'M' 表示月线
    :return: 重采样后的 DataFrame
    """
    df = df.copy()
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    df = df.sort_index()

    df_resampled = pd.DataFrame()
    df_resampled['open'] = df['open'].resample(freq).first()
    df_resampled['high'] = df['high'].resample(freq).max()
    df_resampled['low'] = df['low'].resample(freq).min()
    df_resampled['close'] = df['close'].resample(freq).last()
    df_resampled['vol'] = df['vol'].resample(freq).sum()
    df_resampled.dropna(inplace=True)
    df_resampled.reset_index(inplace=True)
    df_resampled['trade_date'] = df_resampled['trade_date'].dt.strftime('%Y%m%d')
    return df_resampled

def check_multi_ma_trend(df, ma_list=[5, 10, 20, 40]):
    """
    判断指定周期的均线（如 M5/M10/M20/M40）是否为多头排列，且同步向上
    多头排列：ma5 > ma10 > ma20 > ma40
    同步向上：当前周期所有均线 > 前一周期对应均线
    """
    df = df.copy()
    for ma in ma_list:
        df[f'ma{ma}'] = df['close'].rolling(ma).mean()

    if len(df) < max(ma_list) + 2:
        return False

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    latest_mas = [latest[f'ma{ma}'] for ma in ma_list]
    previous_mas = [previous[f'ma{ma}'] for ma in ma_list]

    is_multi_head = all(x > y for x, y in zip(latest_mas[:-1], latest_mas[1:]))
    is_all_up = all(x > y for x, y in zip(latest_mas, previous_mas))

    return is_multi_head and is_all_up

def check_multi_timeframe_trend(df, freqs=['W', 'M'], ma_list=[5, 10, 20, 40]):
    """
    多周期均线趋势判断器：
    判断每个周期（如周线/月线）的指定均线是否为多头排列且同步向上。
    """
    for freq in freqs:
        df_resampled = resample_kline(df, freq)
        if not check_multi_ma_trend(df_resampled, ma_list):
            return False
    return True
  
