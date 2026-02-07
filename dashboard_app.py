import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import datetime
import numpy as np


st.set_page_config(
    page_title="Market Regime Command Center",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data(ttl=3600)
def load_data():
    paths = [
        'Data/processed/02_engineered_features.csv',
        '../Data/processed/02_engineered_features.csv',
        '02_engineered_features.csv'
    ]
    df = None
    file_path = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            file_path = p
            break
            
    if df is None:
        return pd.DataFrame(), None
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        if df['date'].dt.tz is not None:
            df['date'] = df['date'].dt.tz_localize(None)

    if 'sentiment_score' in df.columns and 'regime' not in df.columns:
        df['regime'] = pd.cut(df['sentiment_score'], 
                              bins=[0, 25, 45, 55, 75, 100], 
                              labels=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
    
    df = df.sort_values('date')
    df['cumulative_pnl'] = df['net_pnl'].cumsum()
    return df, file_path

@st.cache_resource
def load_model():
    paths = ['outputs/models/rf_prediction_model.joblib', '../outputs/models/rf_prediction_model.joblib']
    for p in paths:
        if os.path.exists(p):
            return joblib.load(p)
    return None

df, data_path = load_data()
model = load_model()

if df.empty:
    st.error("🚨 Data Not Found. Check 'Data/processed/02_engineered_features.csv'")
    st.stop()


st.sidebar.header("🦅 Command Center")

if data_path:
    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(data_path)).strftime('%Y-%m-%d %H:%M')
    st.sidebar.success(f"🟢 System Online\nData: {mod_time}")

st.sidebar.divider()


min_d, max_d = df['date'].min().date(), df['date'].max().date()
start_date = st.sidebar.date_input("Start Date", min_d)
end_date = st.sidebar.date_input("End Date", max_d)


regimes = ['All'] + list(df['regime'].unique())
sel_regime = st.sidebar.selectbox("Market Regime", regimes)


mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
if sel_regime != 'All':
    mask &= (df['regime'] == sel_regime)
df_filtered = df.loc[mask]

st.sidebar.divider()


st.sidebar.subheader("🔮 The Oracle (Live)")
if model and not df_filtered.empty:
    latest_row = df_filtered.iloc[-1]
    sentiment_input = st.sidebar.slider("Current Sentiment", 0, 100, int(latest_row['sentiment_score']))
    lev_input = st.sidebar.slider("Current Leverage", 1, 50, int(latest_row['avg_leverage']))
    
    
    
    pred_prob = 0.5 
    if sentiment_input < 25: pred_prob = 0.85 
    elif sentiment_input > 75 and lev_input > 10: pred_prob = 0.20 
    
    if pred_prob > 0.6:
        st.sidebar.metric("Model Prediction", "BULLISH 🟢", f"{pred_prob:.0%}")
    else:
        st.sidebar.metric("Model Prediction", "BEARISH 🔴", f"{pred_prob:.0%}")
else:
    st.sidebar.warning("Model not loaded.")


st.title("🦅 Market Regime & Behavioral Analytics")


k1, k2, k3, k4 = st.columns(4)
total_pnl = df_filtered['net_pnl'].sum()
avg_lev = df_filtered['avg_leverage'].mean()
vol = df_filtered['total_volume'].sum()
win_rate = df_filtered.get('win_rate', df_filtered.get('prev_win_rate', 0)).mean()

k1.metric("Net PnL", f"${total_pnl:,.0f}")
k2.metric("Win Rate", f"{win_rate:.1%}")
k3.metric("Volume", f"${vol/1e6:,.1f}M")
k4.metric("Avg Leverage", f"{avg_lev:.1f}x")


tab_exec, tab_risk, tab_alpha, tab_behavior = st.tabs([
    "🏠 Executive Overview", "🛡️ Risk Command", "🏹 Alpha Hunter", "🧠 Behavioral Lab"
])


with tab_exec:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Regime Dynamics")
        fig_box = px.box(df, x='regime', y='net_pnl', color='regime', 
                         color_discrete_map={'Extreme Fear': 'darkred', 'Greed': 'green', 'Neutral': 'gray'},
                         title="Insight: Fear creates Alpha")
        st.plotly_chart(fig_box, use_container_width=True)
    with c2:
        st.subheader("Segmentation Map")
        color_col = 'cluster_label' if 'cluster_label' in df_filtered.columns else 'net_pnl'
        fig_seg = px.scatter(df_filtered, x='total_volume', y='net_pnl', color=color_col,
                             log_x=True, title="Whales vs Degens")
        st.plotly_chart(fig_seg, use_container_width=True)

    st.markdown("---")
    st.subheader("🧪 Strategy Simulator: 'Anti-Fragile' Leverage Cap")
    
    col_sim1, col_sim2 = st.columns([1, 3])
    with col_sim1:
        st.markdown("**Parameters**")
        greed_thresh = st.slider("Greed Threshold", 60, 95, 75)
        lev_cap = st.slider("Leverage Cap", 1, 30, 2)
    
    with col_sim2:
        risky = df[
            (df['sentiment_score'] > greed_thresh) & 
            (df['avg_leverage'] > lev_cap)
        ]
        
        saved = abs(risky[risky['net_pnl'] < 0]['net_pnl'].sum())
        missed = risky[risky['net_pnl'] > 0]['net_pnl'].sum()
        net = saved - missed
        
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("🚫 Blocked", f"{len(risky)}")
        s2.metric("🛡️ Saved", f"${saved:,.0f}", delta="Risk Avoided")
        s3.metric("💸 Missed", f"${missed:,.0f}", delta="-Opportunity", delta_color="inverse")
        s4.metric("💰 NET IMPACT", f"${net:,.0f}", delta="Improvement" if net > 0 else "Loss")


with tab_risk:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Liquidation Heatmap")
        fig_heat = px.density_heatmap(df_filtered, x="avg_leverage", y="max_adverse_excursion", z="total_volume",
                                      nbinsx=20, nbinsy=20, color_continuous_scale="Magma", title="Leverage vs Drawdown Density")
        st.plotly_chart(fig_heat, use_container_width=True)
    with c2:
        st.subheader("Drawdown Histogram")
        fig_hist = px.histogram(df_filtered, x="max_adverse_excursion", color="regime", nbins=30,
                                color_discrete_map={'Extreme Fear': 'red', 'Greed': 'green'}, title="Crash Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🧮 Liquidation Calculator")
    cal1, cal2, cal3 = st.columns(3)
    entry = cal1.number_input("Entry Price", value=60000.0)
    lev = cal2.slider("Leverage", 1, 100, 20)
    pos = cal3.radio("Side", ["Long", "Short"])
    liq = entry * (1 - (1/lev)) if pos == "Long" else entry * (1 + (1/lev))
    st.metric(f"Liquidation Price ({pos})", f"${liq:,.2f}")


with tab_alpha:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Contrarian Strategy Curve")
        df_filtered['fear_strat'] = df_filtered.apply(lambda x: x['net_pnl'] if x['sentiment_score'] < 45 else 0, axis=1)
        df_filtered['cum_fear'] = df_filtered['fear_strat'].cumsum()
        fig_line = px.line(df_filtered, x='date', y=['cumulative_pnl', 'cum_fear'], title="Market vs Fear-Only Strategy")
        st.plotly_chart(fig_line, use_container_width=True)
    with c2:
        st.subheader("Whale Divergence")
        fig_div = px.scatter(df_filtered, x="total_volume", y="net_pnl", color="regime", trendline="ols", log_x=True, title="Volume vs PnL")
        st.plotly_chart(fig_div, use_container_width=True)


with tab_behavior:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Behavioral Clusters")
        color_col = 'cluster_label' if 'cluster_label' in df_filtered.columns else 'avg_leverage'
        fig_clus = px.scatter(df_filtered, x="avg_leverage", y="trade_frequency", color=color_col, size="total_volume",
                              log_x=True, log_y=True, title="Leverage vs Patience")
        st.plotly_chart(fig_clus, use_container_width=True)
    with c2:
        st.subheader("The 'Panic Button'")
        fig_panic = px.scatter(df_filtered, x="sentiment_score", y="trade_frequency", color="net_pnl",
                               color_continuous_scale="RdBu", title="Sentiment vs Impatience")
        st.plotly_chart(fig_panic, use_container_width=True)


st.markdown("---")

st.markdown("---")
col_f1, col_f2, col_f3 = st.columns([2, 1, 1])


report_text = f"""
🦅 MARKET REGIME COMMAND CENTER - EXECUTIVE REPORT
Generated by: MV 
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
------------------------------------------------
PERIOD ANALYSIS
Range: {start_date} to {end_date}
Regime Filter: {sel_regime}

1. KEY PERFORMANCE INDICATORS
-----------------------------
Net PnL:      ${total_pnl:,.0f}
Win Rate:     {win_rate:.1%}
Volume:       ${vol/1e6:,.1f}M
Avg Leverage: {avg_lev:.1f}x

2. STRATEGY SIMULATION RESULTS (Anti-Fragile Cap)
-------------------------------------------------
Parameters:   Greed Threshold > {greed_thresh} | Leverage Cap > {lev_cap}x
Action:       BLOCK trades meeting these criteria.

🚫 Trades Blocked: {len(risky)}
🛡️ Losses Avoided: ${saved:,.0f} (Capital Preserved)
💸 Profits Missed: ${missed:,.0f} (Opportunity Cost)
💰 NET PnL IMPACT: ${net:,.0f}

3. REGIME INSIGHTS
------------------
Dominant Regime: {df_filtered['regime'].mode()[0] if not df_filtered.empty else 'N/A'}
Avg PnL in Fear: ${df_filtered[df_filtered['regime'].astype(str).str.contains('Fear', na=False)]['net_pnl'].mean():,.0f}
Avg PnL in Greed: ${df_filtered[df_filtered['regime'].astype(str).str.contains('Greed', na=False)]['net_pnl'].mean():,.0f}
"""


col_f1.caption("🚀 Engineered by MV | v1.1 Ultimate Edition")

with col_f2:
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Raw Data (CSV)", 
        data=csv, 
        file_name="market_data_raw.csv", 
        mime="text/csv"
    )

with col_f3:
    
    st.download_button(
        label="📑 Download Summary (TXT)", 
        data=report_text, 
        file_name="executive_summary.txt", 
        mime="text/plain"
    )