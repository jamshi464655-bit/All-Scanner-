import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="EasyCharts Pro - Ultra Scanner", layout="wide", page_icon="🚀")

# ====================== BEAUTIFUL UI ======================
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #6b46c1, #7c3aed);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #ec4899, #f472b6);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        height: 130px;
    }
    .panel {
        background-color: #1e2937;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .panel-title {
        background: linear-gradient(135deg, #f59e0b, #fb923c);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🚀 EasyCharts Pro - Ultra Scanner</h1>
    <p>AI-Powered Multi-Indicator NSE Stock Scanner</p>
</div>
""", unsafe_allow_html=True)

# Scan Button
if st.button("🚀 START MARKET SCAN", type="primary", use_container_width=True):
    with st.spinner("Scanning Nifty 200 stocks..."):
        symbols = ["RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "TCS.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", 
                   "ITC.NS", "LT.NS", "HINDUNILVR.NS", "AXISBANK.NS", "KOTAKBANK.NS", "ADANIENT.NS", "SUNPHARMA.NS", 
                   "TITAN.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "DMART.NS", "TRENT.NS", "ZOMATO.NS"]

        def scan_stock(sym):
            try:
                ticker = yf.Ticker(sym)
                df = ticker.history(period="3mo")
                if df.empty or len(df) < 30: return None
                
                last = df.iloc[-1]
                change = ((last['Close'] - df.iloc[-2]['Close']) / df.iloc[-2]['Close']) * 100
                vol_ratio = last['Volume'] / df['Volume'].iloc[-20:].mean()
                dist = ((df['High'].iloc[-20:].max() - last['Close']) / df['High'].iloc[-20:].max()) * 100
                
                if dist < 3.0 and change > 0.8 and vol_ratio > 1.4:
                    return {"Type": "Live Breakout", "Symbol": sym.replace(".NS",""), "LTP": round(last['Close'],2), "%Chg": round(change,2), "Volx": round(vol_ratio,2)}
                elif dist < 5.0 and vol_ratio > 1.2:
                    return {"Type": "Pre-Breakout", "Symbol": sym.replace(".NS",""), "LTP": round(last['Close'],2), "%Chg": round(change,2), "Volx": round(vol_ratio,2)}
                elif change > 2.5 or vol_ratio > 2.0:
                    return {"Type": "Strong Momentum", "Symbol": sym.replace(".NS",""), "LTP": round(last['Close'],2), "%Chg": round(change,2), "Volx": round(vol_ratio,2)}
            except:
                return None

        results = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(scan_stock, s) for s in symbols]
            for future in as_completed(futures):
                if future.result():
                    results.append(future.result())

        df = pd.DataFrame(results)

        # ====================== UI ======================
        c1, c2, c3 = st.columns(3)
        
        with c1:
            pre = len(df[df["Type"] == "Pre-Breakout"])
            st.markdown(f"""
            <div class="metric-card">
                <h1 style="margin:0;">{pre}</h1>
                <p>Pre-Breakout Setups</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            live = len(df[df["Type"] == "Live Breakout"])
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #22c55e, #86efac);">
                <h1 style="margin:0;color:black;">{live}</h1>
                <p style="color:black;">Live Breakouts</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            mom = len(df[df["Type"] == "Strong Momentum"])
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #a855f7, #c084fc);">
                <h1 style="margin:0;">{mom}</h1>
                <p>Momentum Stocks</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="panel-title">🔵 Pre-Breakout (Early Stage)</div>', unsafe_allow_html=True)
            st.dataframe(df[df["Type"] == "Pre-Breakout"][["Symbol","LTP","%Chg"]], use_container_width=True, hide_index=True)

        with col2:
            st.markdown('<div class="panel-title">🟢 Live Breakout</div>', unsafe_allow_html=True)
            st.dataframe(df[df["Type"] == "Live Breakout"][["Symbol","LTP","%Chg"]], use_container_width=True, hide_index=True)

        with col3:
            st.markdown('<div class="panel-title">🔥 Strong Momentum</div>', unsafe_allow_html=True)
            st.dataframe(df[df["Type"] == "Strong Momentum"][["Symbol","LTP","%Chg"]], use_container_width=True, hide_index=True)

        st.success(f"✅ Scan completed at {datetime.now().strftime('%I:%M:%S %p')}")
else:
    st.info("👆 Click 'START MARKET SCAN' to begin analysis")

st.caption("Built with ❤️ | Beautiful UI + Fast Scanner")