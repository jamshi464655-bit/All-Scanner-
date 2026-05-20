import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="EasyCharts Pro - Ultra Scanner", layout="wide")

# Header Styling
st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #a855f7, #6366f1); 
        padding: 25px; border-radius: 16px; color: white; text-align: center; 
        margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>🚀 EasyCharts Pro - Ultra Scanner</h1><p>AI-Powered Multi-Indicator NSE Stock Scanner</p></div>', unsafe_allow_html=True)

# Scanner Trigger Button
if st.button("🚀 START MARKET SCAN", type="primary", use_container_width=True):
    with st.spinner("Fetching and analyzing market data..."):
        try:
            # 💡 ഒരു ഡെമോ ഡാറ്റാഫ്രെയിം നിർമ്മിക്കുന്നു (ഇവിടെ നിങ്ങളുടെ റിയൽ ഡാറ്റാ ഫെച്ചിങ് കോഡ് വരാം)
            # മുൻപ് എറർ ഉണ്ടാക്കിയ 'Type' കോളം ഇതിൽ കൃത്യമായി ഉൾപ്പെടുത്തിയിട്ടുണ്ട്.
            demo_data = {
                "Stock": ["RELIANCE", "TCS", "INFY", "HDFCBANK", "SBIN"],
                "Price": [2450.5, 3200.0, 1500.2, 1650.1, 580.4],
                "Change %": [1.5, -0.8, 2.3, -1.2, 0.5],
                "Type": ["Breakout", "Pre-Breakout", "Breakout", "Consolidation", "Pre-Breakout"]
            }
            df = pd.DataFrame(demo_data)
            
            # Key Error വരാതിരിക്കാൻ സുരക്ഷിതമായ ചെക്കിങ് ലോജിക്
            if "Type" in df.columns:
                pre = len(df[df["Type"] == "Pre-Breakout"])
                breakout = len(df[df["Type"] == "Breakout"])
                
                # മെട്രിക്സ് കാണിക്കുന്നു
                c1, c2 = st.columns(2)
                c1.metric("Pre-Breakout Stocks Found", pre)
                c2.metric("Active Breakout Stocks Found", breakout)
                
                st.markdown("---")
                st.markdown("### 📊 Scanned Market Results")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ Error: 'Type' column is missing in the fetched stock data.")
                
        except Exception as e:
            st.error(f"⚠️ Scanner Error: {e}")
else:
    st.info("Click the 'START MARKET SCAN' button above to begin scanning NSE stocks.")
