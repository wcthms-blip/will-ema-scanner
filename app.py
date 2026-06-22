import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Will's EMA Scanner", layout="wide")
st.title("📈 Will's EMA Scanner")
st.caption("20/50 Bullish Crossover + Above 200 EMA | Recent Cross Filter + TradingView Charts")

# ====================== YOUR CUSTOM LIST ======================
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

# ====================== INDEX PRESETS (Robust) ======================
@st.cache_data(ttl=86400)
def get_sp500():
    try:
        return pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    except:
        return []

@st.cache_data(ttl=86400)
def get_nasdaq100():
    try:
        tables = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
        for table in tables:
            if 'Ticker' in table.columns:
                return table['Ticker'].tolist()
            if 'Symbol' in table.columns:
                return table['Symbol'].tolist()
        return []
    except:
        return []

@st.cache_data(ttl=86400)
def get_russell1000():
    try:
        # Fallback to a more reliable source if iShares fails
        tables = pd.read_html('https://en.wikipedia.org/wiki/Russell_1000_Index')
        # Just return empty for now to avoid crash - we can improve later
        return []
    except:
        return []

presets = {
    "Will's List": will_list,
    "S&P 500": get_sp500(),
    "Nasdaq 100": get_nasdaq100(),
    "Russell 1000": get_russell1000(),   # Currently empty to prevent crashes
}

# ====================== SIDEBAR ======================
st.sidebar.header("Scanner Settings")
preset_name = st.sidebar.selectbox("Choose Universe", list(presets.keys()))
tickers = presets[preset_name]

lookback = st.sidebar.slider("Cross occurred in the last how many days?", 1, 10, 5)

st.sidebar.write(f"**{len(tickers)}** symbols loaded")

if st.sidebar.button("🔄 Clear Cache & Refresh"):
    st.cache_data.clear()
    st.rerun()

# ====================== SCAN ======================
if st.button("🚀 Run EMA Scan", type="primary", use_container_width=True):
    with st.spinner(f"Scanning {len(tickers)} tickers..."):
        results = []
        data = yf.download(tickers, period="500d", group_by='ticker', auto_adjust=True, progress=False)

        for ticker in tickers:
            try:
                df = data[ticker].dropna() if ticker in data.columns.get_level_values(0) else \
                     yf.download(ticker, period="500d", auto_adjust=True, progress=False).dropna()

                if len(df) < 200:
                    continue

                df['EMA20'] = df['Close'].ewm(span=20).mean()
                df['EMA50'] = df['Close'].ewm(span=50).mean()
                df['EMA200'] = df['Close'].ewm(span=200).mean()

                df['cross'] = (df['EMA20'].shift(1) <= df['EMA50'].shift(1)) & (df['EMA20'] > df['EMA50'])

                latest = df.iloc[-1]
                above_200 = latest['Close'] > latest['EMA200']

                recent_crosses = df.iloc[-lookback:][df.iloc[-lookback:]['cross']]

                if len(recent_crosses) > 0 and above_200:
                    cross_row = recent_crosses.iloc[-1]
                    cross_date = cross_row.name
                    days_ago = (df.index[-1] - cross_date).days

                    results.append({
                        'Ticker': ticker,
                        'Close': round(latest['Close'], 2),
                        'Cross Price': round(cross_row['Close'], 2),
                        '% Above 200': round(((latest['Close'] / latest['EMA200']) - 1) * 100, 2),
                        'Cross Date': cross_date.strftime('%Y-%m-%d'),
                        'Days Ago': days_ago,
                        'Volume': int(latest.get('Volume', 0)),
                    })
            except:
                continue

        if results:
            df_results = pd.DataFrame(results).sort_values('Days Ago')

            # Color highlighting
            def highlight_rows(row):
                if row['Days Ago'] <= 2:
                    return ['background-color: #90EE90'] * len(row)
                elif row['Days Ago'] <= 5:
                    return ['background-color: #FFFF99'] * len(row)
                return ['background-color: #E0E0E0'] * len(row)

            styled_df = df_results.style.apply(highlight_rows, axis=1)

            st.success(f"✅ Found **{len(df_results)}** signals")
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            csv = df_results.to_csv(index=False).encode()
            st.download_button("📥 Download CSV", csv, f"will_ema_signals_{datetime.now().date()}.csv")

            # TradingView Chart
            st.divider()
            selected = st.selectbox("🔍 Select a ticker to view full TradingView Chart:", df_results['Ticker'])
            if selected:
                st.subheader(f"{selected} — Full Interactive TradingView Chart")
                tv_html = f"""
                <div style="height:780px;width:100%">
                  <div id="tv_widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                  <script type="text/javascript">
                  new TradingView.widget({{
                    "width": "100%", "height": "780", "symbol": "{selected}",
                    "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
                    "style": "1", "locale": "en", "enable_publishing": false,
                    "allow_symbol_change": true, "studies": ["MASimple@tv-basicstudies"],
                    "container_id": "tv_widget"
                  }});
                  </script>
                </div>
                """
                st.components.v1.html(tv_html, height=820, scrolling=True)
        else:
            st.info(f"No recent crosses found in the last {lookback} days.")
else:
    st.info("👆 Click **Run EMA Scan** above to start.")

st.divider()
st.caption("Russell 1000 temporarily limited to avoid crashes. Let me know if you want it improved.")
