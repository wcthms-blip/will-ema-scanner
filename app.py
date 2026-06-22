# ====================== SIDEBAR ======================
st.sidebar.header("Scanner Settings")
preset_name = st.sidebar.selectbox("Choose Universe", list(presets.keys()))
tickers = presets[preset_name]

st.sidebar.write(f"**{len(tickers)}** symbols loaded")

if st.sidebar.button("🔄 Clear Cache"):
    st.cache_data.clear()
    st.rerun()

# ====================== MAIN SCAN ======================
if st.button("🚀 Run EMA Scan", type="primary", use_container_width=True):
    with st.spinner(f"Scanning {len(tickers)} tickers... (30–90 seconds)"):
        results = []
        data = yf.download(tickers, period="400d", group_by='ticker', auto_adjust=True, progress=False)

        for ticker in tickers:
            try:
                df = data[ticker].dropna() if ticker in data.columns.get_level_values(0) else \
                     yf.download(ticker, period="400d", auto_adjust=True, progress=False).dropna()
                
                if len(df) < 200:
                    continue

                df['EMA20'] = df['Close'].ewm(span=20).mean()
                df['EMA50'] = df['Close'].ewm(span=50).mean()
                df['EMA200'] = df['Close'].ewm(span=200).mean()

                latest = df.iloc[-1]
                prev = df.iloc[-2]

                bull_cross = (prev['EMA20'] <= prev['EMA50']) and (latest['EMA20'] > latest['EMA50'])
                above_200 = latest['Close'] > latest['EMA200']

                if bull_cross and above_200:
                    results.append({
                        'Ticker': ticker,
                        'Close': round(latest['Close'], 2),
                        '% Above 200': round(((latest['Close'] / latest['EMA200']) - 1) * 100, 2),
                        'Volume': int(latest.get('Volume', 0)),
                        'Date': latest.name.strftime('%Y-%m-%d')
                    })
            except:
                continue

        if results:
            df_results = pd.DataFrame(results).sort_values('% Above 200', ascending=False)
            
            st.success(f"✅ **{len(df_results)}** strong signals found on {datetime.now().date()}")
            st.dataframe(df_results, use_container_width=True, hide_index=True)

            # Download
            csv = df_results.to_csv(index=False).encode()
            st.download_button("📥 Download Results as CSV", csv, f"will_ema_signals_{datetime.now().date()}.csv", type="secondary")

            # === Embedded TradingView Chart ===
            st.divider()
            selected = st.selectbox("🔍 Select a ticker to view full TradingView Chart:", df_results['Ticker'])
            
            if selected:
                st.subheader(f"{selected} — Interactive TradingView Chart")
                
                tv_symbol = selected  # TradingView usually handles it well
                
                tv_html = f"""
                <div class="tradingview-widget-container" style="height:750px; width:100%">
                  <div id="tradingview_widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                  <script type="text/javascript">
                  new TradingView.widget({{
                    "width": "100%",
                    "height": "750",
                    "symbol": "{tv_symbol}",
                    "interval": "D",
                    "timezone": "Etc/UTC",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "toolbar_bg": "#f1f3f6",
                    "enable_publishing": false,
                    "allow_symbol_change": true,
                    "studies": ["MASimple@tv-basicstudies","MASimple@tv-basicstudies","MASimple@tv-basicstudies"],
                    "container_id": "tradingview_widget"
                  }});
                  </script>
                </div>
                """
                st.components.v1.html(tv_html, height=780, scrolling=True)
                
                st.caption("✅ You can zoom, draw, add indicators, and change timeframes directly in the chart above.")
        else:
            st.info("No new 20/50 bullish crossovers above the 200 EMA today.")
else:
    st.info("👆 Click **Run EMA Scan** to analyze your selected universe.")

st.divider()
st.caption("Built with Streamlit + yfinance • TradingView charts embedded • Free to host")
