import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Will's EMA Scanner", layout="wide", initial_sidebar_state="collapsed")

# ====================== PREMIUM FINTECH CSS ======================
st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #e0e0e0; }
    .main .block-container { padding-top: 1.5rem; max-width: 1400px; }
    .metric-card {
        background-color: #1a1d27;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid #2a2f3a;
    }
    .result-card {
        background-color: #1a1d27;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border: 1px solid #2a2f3a;
        transition: all 0.15s ease;
    }
    .result-card:hover { border-color: #4a90e2; }
    .ticker-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .ticker-logo { width: 36px; height: 36px; border-radius: 8px; }
    .positive { color: #00d26a; font-weight: 700; }
    .days-green { color: #00d26a; font-weight: 700; }
    .days-yellow { color: #ffaa00; font-weight: 700; }
    .days-red { color: #ff4757; font-weight: 700; }
    .stButton > button { background-color: #4a90e2; border-radius: 10px; height: 48px; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Will's EMA Scanner")
st.caption("20/50 Bullish Crossover • Above 200 EMA • Modern & Actionable")

# ====================== DATA & PRESETS (unchanged) ======================
raw_list = "NASDAQ:AXTI,NYSE:AVEX,NASDAQ:ASTS,AMEX:BITX,NYSE:LMT,NYSE:HII,NYSE:RTX,NASDAQ:SPCX,NYSE:GD,NYSE:VICI,NASDAQ:KTOS,NASDAQ:MSTR,NASDAQ:AAOI,NASDAQ:VIAV,NYSE:SCHW,NYSE:FICO,NYSE:MSCI,NYSE:DOCN,NYSE:JPM,NYSE:DELL,NASDAQ:LITE,NYSE:OXY,NYSE:CVX,NYSE:ABBV,NYSE:CRM,NYSE:XOM,NYSE:CLS,NASDAQ:APP,NYSE:WFC,NYSE:FN,NYSE:SPGI,NYSE:XPEV,NASDAQ:PLTR,NYSE:HPE,NYSE:STT,NASDAQ:VRTX,NASDAQ:DDOG,NASDAQ:COST,NYSE:NU,NASDAQ:SNPS,NYSE:BA,NYSE:NET,NYSE:MCO,NASDAQ:JD,NYSE:LLY,OTC:BYDDF,NYSE:VZ,NYSE:TWLO,NASDAQ:COIN,NYSE:BX,NYSE:V,NASDAQ:WMT,NASDAQ:QLYS,NASDAQ:INTU,NYSE:NVO,NYSE:AXP,NYSE:WCN,NASDAQ:RKLB,NYSE:KO,NYSE:BN,NYSE:MA,NASDAQ:DPZ,NYSE:EFX,NYSE:BAC,NYSE:WM,NASDAQ:CDNS,NASDAQ:ADBE,AMEX:KWEB,OTC:EVVTY,NYSE:NOW,NYSE:CRCL,NYSE:PINS,AMEX:GLD,NASDAQ:PDD,NYSE:BRK.B,NASDAQ:MNST,NYSE:BABA,NYSE:UPS,NYSE:ALL,NYSE:TJX,NYSE:LYV,NYSE:HLT,NASDAQ:VRSN,TSX:ATD,NASDAQ:LULU,NASDAQ:CZR,NYSE:GME,NYSE:MP,NYSE:FDX,NASDAQ:BKNG,NASDAQ:AXON,NYSE:BRO,NYSE:ENS,NASDAQ:BIDU,NYSE:DE,NASDAQ:MSFT,NASDAQ:FFIV,NASDAQ:HON,NASDAQ:TMUS,NASDAQ:MELI,NYSE:PGR,NYSE:MO,NASDAQ:DKNG,NASDAQ:CRWD,NASDAQ:PEP,NASDAQ:EBAY,NYSE:UNH,NASDAQ:ZS,NASDAQ:STX,NASDAQ:DLO,NASDAQ:ADSK,NYSE:PATH,NASDAQ:MAR,NASDAQ:FTNT,NYSE:ORCL,NASDAQ:OPEN,NYSE:OSCR,NYSE:CP,NASDAQ:NFLX,NYSE:CBRE,NASDAQ:EXPE,NASDAQ:EOSE,NASDAQ:PAYX,OTC:LVMUY,NASDAQ:AAPL,NASDAQ:SHOP,NYSE:CCJ,TSX:CSU,NASDAQ:SBUX,NASDAQ:LYFT,NASDAQ:IBKR,NASDAQ:PYPL,NYSE:TOST,NYSE:UBER,NASDAQ:TSLA,NASDAQ:ISRG,NASDAQ:FSLR,NASDAQ:ULTA,NYSE:NEE,NYSE:FIG,NYSE:CAVA,NASDAQ:ABNB,NASDAQ:CELH,NYSE:RBRK,NASDAQ:OSS,NASDAQ:GOOG,NYSE:S,NASDAQ:AVAV,NYSE:ETSY,NYSE:MDT,NYSE:UHAL,NASDAQ:RIVN,NASDAQ:ONDS,NASDAQ:TSCO,NASDAQ:META,NASDAQ:DUOL,NASDAQ:TTD,NYSE:CMG,NASDAQ:PANW,NASDAQ:NBIS,NYSE:HD,NASDAQ:BOTZ,NASDAQ:UAL,NYSE:ZETA,AMEX:ARKK,NASDAQ:CAKE,NYSE:RACE,NASDAQ:APLD,NYSE:LOW,NYSE:NKE,NASDAQ:SOUN,NYSE:DAL,NASDAQ:CRWV,NASDAQ:TXRH,NYSE:CHWY,NASDAQ:CEG,NYSE:LMND,NYSE:SPOT,NASDAQ:CORZ,NASDAQ:HOOD,NYSE:LUV,NASDAQ:SOFI,NASDAQ:FSLY,NYSE:COHR,NYSE:EL,NYSE:ANET,NASDAQ:AMZN,NASDAQ:NVDA,NYSE:ANF,NYSE:DIS,NYSE:ONON,NYSE:ELF,NYSE:VST,NYSE:CAT,NASDAQ:WYNN,NASDAQ:IREN,NYSE:DECK,NASDAQ:ASML,NYSE:IONQ,NYSE:TE,NASDAQ:GRAB,NYSE:DHI,NASDAQ:AAL,NYSE:LEN,NASDAQ:SYM,NASDAQ:PGY,NASDAQ:LRCX,NYSE:OKLO,NYSE:TOL,NASDAQ:CART,NASDAQ:AMAT,NASDAQ:TEM,NASDAQ:SWKS,NASDAQ:AFRM,NASDAQ:USAR,NASDAQ:AMKR,NASDAQ:AVGO,NASDAQ:DASH,NASDAQ:AMD,NYSE:VRT,NASDAQ:ARM,NASDAQ:DLTR,NASDAQ:TTWO,NASDAQ:NXPI,CBOE:ARKG,NYSE:RDDT,NYSE:KLAR,NYSE:BLDR,NASDAQ:FLNC,NASDAQ:QCOM,NASDAQ:TQQQ,NYSE:TSM,NASDAQ:TXN,NASDAQ:ROOT,NASDAQ:MRVL,NYSE:RBLX,NASDAQ:NVTS,NYSE:BROS,NASDAQ:TMDX,NASDAQ:ON,NYSE:AMPX,NASDAQ:MPWR,AMEX:UUUU,NASDAQ:MU,NASDAQ:CRDO,NYSE:RKT,NYSE:RH,OTC:KRKNF,NASDAQ:ENPH,NASDAQ:CBRS,NASDAQ:SMCI,NASDAQ:INTC,NASDAQ:CIFR,NYSE:GLW,NYSE:HIMS,NASDAQ:ALAB,NASDAQ:NNE,NASDAQ:SNDK,NASDAQ:PENG,NYSE:SMR,NYSE:BE,AMEX:SOXL"

def clean_ticker(t):
    t = t.strip().upper()
    prefixes = ['NASDAQ:', 'NYSE:', 'AMEX:', 'OTC:', 'TSX:', 'CBOE:']
    for p in prefixes:
        if t.startswith(p):
            t = t[len(p):]
            break
    return 'BRK-B' if t == 'BRK.B' else t

will_list = [clean_ticker(t) for t in raw_list.split(',') if t.strip()]

@st.cache_data(ttl=86400)
def get_sp500(): 
    try: return pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    except: return []

@st.cache_data(ttl=86400)
def get_nasdaq100():
    try:
        tables = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
        for t in tables:
            if 'Ticker' in t.columns: return t['Ticker'].tolist()
        return []
    except: return []

@st.cache_data(ttl=86400)
def get_russell1000():
    try:
        tables = pd.read_html('https://www.ishares.com/us/products/239707/ishares-russell-1000-etf')
        for t in tables:
            if 'Ticker' in t.columns: return t['Ticker'].dropna().tolist()
        return []
    except: return []

presets = {"Will's List": will_list, "S&P 500": get_sp500(), "Nasdaq 100": get_nasdaq100(), "Russell 1000": get_russell1000()}

with st.sidebar:
    st.header("Scanner Settings")
    preset_name = st.selectbox("Universe", list(presets.keys()))
    tickers = presets[preset_name]
    lookback = st.slider("Cross in last X days", 1, 10, 5)
    if st.button("🔄 Refresh Cache"):
        st.cache_data.clear()
        st.rerun()

# ====================== SESSION STATE + SCAN ======================
if "results" not in st.session_state:
    st.session_state.results = None

if st.button("🚀 Run EMA Scan", type="primary", use_container_width=True):
    with st.spinner("Scanning..."):
        results = []
        data = yf.download(tickers, period="500d", group_by='ticker', auto_adjust=True, progress=False)

        for ticker in tickers:
            try:
                df = data[ticker].dropna() if ticker in data.columns.get_level_values(0) else yf.download(ticker, period="500d", auto_adjust=True, progress=False).dropna()
                if len(df) < 200: continue

                df['EMA20'] = df['Close'].ewm(span=20).mean()
                df['EMA50'] = df['Close'].ewm(span=50).mean()
                df['EMA200'] = df['Close'].ewm(span=200).mean()
                df['cross'] = (df['EMA20'].shift(1) <= df['EMA50'].shift(1)) & (df['EMA20'] > df['EMA50'])

                latest = df.iloc[-1]
                above_200 = latest['Close'] > latest['EMA200']
                recent = df.iloc[-lookback:][df.iloc[-lookback:]['cross']]

                if len(recent) > 0 and above_200:
                    cross_row = recent.iloc[-1]
                    days_ago = (df.index[-1] - cross_row.name).days
                    results.append({
                        'Ticker': ticker,
                        'Close': round(latest['Close'], 2),
                        'Cross Price': round(cross_row['Close'], 2),
                        '% Above 200': round(((latest['Close'] / latest['EMA200']) - 1) * 100, 2),
                        'Cross Date': cross_row.name.strftime('%Y-%m-%d'),
                        'Days Ago': days_ago,
                    })
            except: continue

        st.session_state.results = results if results else None

# ====================== DISPLAY RESULTS (PERSISTENT) ======================
if st.session_state.results:
    results = st.session_state.results
    df_results = pd.DataFrame(results).sort_values('Days Ago')

    st.success(f"✅ Found **{len(df_results)}** signals")

    # Compact Card Grid (smaller cards)
    st.markdown("### 📋 Signals")
    cols = st.columns(4)  # 4 columns = smaller cards
    for i, row in df_results.iterrows():
        with cols[i % 4]:
            logo = f"https://logo.clearbit.com/{row['Ticker'].lower()}.com"
            
            # Color logic for Days Ago
            if row['Days Ago'] <= 3:
                days_class = "days-green"
            elif row['Days Ago'] <= 7:
                days_class = "days-yellow"
            else:
                days_class = "days-red"

            st.markdown(f"""
            <div class="result-card">
                <div class="ticker-header">
                    <img src="{logo}" class="ticker-logo" onerror="this.src='https://via.placeholder.com/36/1a1d27/ffffff?text={row['Ticker'][:2]}'">
                    <div>
                        <h4 style="margin:0; font-size:1.15rem;">{row['Ticker']}</h4>
                        <small style="color:#888;">{row['Days Ago']} day{'s' if row['Days Ago']>1 else ''} ago</small>
                    </div>
                </div>
                <div style="font-size:1.55rem; font-weight:700; margin:6px 0;">${row['Close']}</div>
                <div style="display:flex; justify-content:space-between; font-size:0.95rem;">
                    <div><span class="positive">+{row['% Above 200']}%</span> above 200</div>
                    <div style="text-align:right;"><span class="{days_class}">{row['Days Ago']}d</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Detailed View + Chart (now persistent)
    st.divider()
    st.subheader("📊 Detailed Chart")
    selected = st.selectbox("Select ticker to view chart", df_results['Ticker'])

    if selected:
        row = df_results[df_results['Ticker'] == selected].iloc[0]
        st.markdown(f"""
        <div class="metric-card">
            <div style="display:flex; align-items:center; gap:16px;">
                <img src="https://logo.clearbit.com/{selected.lower()}.com" style="width:60px;height:60px;border-radius:10px;" onerror="this.src='https://via.placeholder.com/60/1a1d27/ffffff?text={selected[:2]}'">
                <div>
                    <h3 style="margin:0;">{selected}</h3>
                    <p style="margin:2px 0; color:#00d26a;">Bullish crossover {row['Days Ago']} days ago</p>
                </div>
                <div style="margin-left:auto; text-align:right;">
                    <div style="font-size:2rem; font-weight:700;">${row['Close']}</div>
                    <div class="positive">+{row['% Above 200']}% above 200 EMA</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # TradingView with EMAs
        tv_html = f"""
        <div style="border-radius:14px; overflow:hidden; box-shadow:0 4px 18px rgba(0,0,0,0.35);">
          <div id="tv_widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script>
          new TradingView.widget({{
            "width": "100%", "height": "720", "symbol": "{selected}",
            "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
            "style": "1", "locale": "en",
            "studies": ["MASimple@tv-basicstudies","MASimple@tv-basicstudies","MASimple@tv-basicstudies"],
            "container_id": "tv_widget"
          }});
          </script>
        </div>
        """
        st.components.v1.html(tv_html, height=760)

    if st.button("🗑️ Clear Results"):
        st.session_state.results = None
        st.rerun()

else:
    st.info("Click **Run EMA Scan** to generate results.")
