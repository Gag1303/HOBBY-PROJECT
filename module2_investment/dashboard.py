"""CFP Module 2 (Investment Planning) - Thai mutual fund dashboard.

This is one page of the CFP toolkit app. Start the whole app from the project folder with
    streamlit run app.py
(or double-click run_app.bat).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from module2_investment.common import (
    DATA_NOTE, DOWN_COLOR, SERIES_COLORS, UP_COLOR, csv_bytes, fund_label, last_date_or_stop,
    load_full_history, load_market, signed,
)
from module2_investment.tables import (
    calendar_year_returns, dividends, drawdown, fund_stats, period_returns,
)

MAX_COMPARE = 5

# Months back for each period button. 0 = year to date, None = whole history.
PERIODS = {"1M": 1, "3M": 3, "6M": 6, "YTD": 0, "1Y": 12, "3Y": 36, "5Y": 60, "10Y": 120, "Max": None}


def period_start(end: pd.Timestamp, months: int | None) -> pd.Timestamp | None:
    if months is None:
        return None
    if months == 0:
        return pd.Timestamp(end.year - 1, 12, 31)
    return end - pd.DateOffset(months=months)


# ---------- sidebar ----------

st.sidebar.subheader("Thai mutual funds")
last_date = last_date_or_stop()

day = st.sidebar.date_input("NAV date", value=last_date, max_value=last_date,
                            help="Weekends/holidays have no data.")
name_col = "nameTh" if st.sidebar.toggle("Show Thai fund names") else "nameEn"
if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()
st.sidebar.caption(DATA_NOTE)

with st.spinner(f"Loading latest NAV of all funds as of {day} ..."):
    market = load_market(day)

if market.empty:
    st.warning(f"No NAV data for {day:%d %b %Y} (weekend or holiday?). Pick another date.")
    st.stop()

tab_market, tab_detail, tab_history, tab_amc = st.tabs(
    ["🏦 Market overview", "🔎 Fund detail", "📊 Compare funds", "🏢 Fund companies"]
)


# ---------- tab 1: market overview ----------

with tab_market:
    st.subheader(f"All funds · latest NAV as of {day:%d %b %Y}")
    st.caption("Many funds (especially foreign-investing ones) report NAV 1-3 days late, so each "
               "fund shows its most recent NAV. Check the NAV date column.")

    changed = market["changePct"].dropna()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Funds", f"{len(market):,}")
    k2.metric("Up (last change)", f"{(changed > 0).sum():,}")
    k3.metric("Down (last change)", f"{(changed < 0).sum():,}")
    k4.metric("Median change", signed(changed.median()))

    f1, f2, f3 = st.columns([2, 2, 1])
    search = f1.text_input("Search symbol or name", placeholder="e.g. K-USA, SET50, ทองคำ")
    amc_pick = f2.multiselect("Fund company", sorted(market["amcCode"].dropna().unique()))
    type_pick = f3.multiselect("Type", sorted(market["projectType"].dropna().unique()))

    view = market
    if search:
        s = search.lower()
        view = view[view["symbol"].str.lower().str.contains(s, regex=False)
                    | view["nameEn"].fillna("").str.lower().str.contains(s, regex=False)
                    | view["nameTh"].fillna("").str.contains(search, regex=False)]
    if amc_pick:
        view = view[view["amcCode"].isin(amc_pick)]
    if type_pick:
        view = view[view["projectType"].isin(type_pick)]

    table = view[["symbol", name_col, "navDate", "amcCode", "navPerUnit", "change", "changePct",
                  "nav", "buyPrice", "sellPrice", "projectType"]].copy()
    table["nav"] = table["nav"] / 1e6
    # ETFs have no buy/sell price (they trade on the exchange). Streamlit shows empty cells as
    # "None", so turn these two columns into text with a dash instead.
    for col in ["buyPrice", "sellPrice"]:
        table[col] = table[col].map(lambda v: "–" if pd.isna(v) else f"{v:.4f}")
    st.dataframe(
        table.style.format({
            "navDate": "{:%d %b}", "navPerUnit": "{:.4f}", "change": "{:+.4f}", "changePct": signed,
            "nav": "{:,.1f}",
        }),
        hide_index=True,
        use_container_width=True,
        height=420,
        column_config={
            "symbol": "Symbol",
            name_col: "Fund name",
            "navDate": "NAV date",
            "amcCode": "Company",
            "navPerUnit": "NAV/unit",
            "change": "Change",
            "changePct": "Change %",
            "nav": "Fund size (M THB)",
            "buyPrice": "Buy",
            "sellPrice": "Sell",
            "projectType": "Type",
        },
    )
    st.download_button("⬇️ Download this table (CSV)", csv_bytes(view),
                       file_name=f"nav_{day}.csv", mime="text/csv")

    st.markdown("#### Biggest movers")
    movers = view.dropna(subset=["changePct"]).sort_values("changePct")
    g1, g2 = st.columns(2)
    for col, title, rows, color in [
        (g1, "Top 10 gainers", movers.tail(10), UP_COLOR),
        (g2, "Top 10 losers", movers.head(10).iloc[::-1], DOWN_COLOR),
    ]:
        if rows.empty:
            col.info("No data for this filter.")
            continue
        fig = go.Figure(go.Bar(
            x=rows["changePct"], y=rows["symbol"], orientation="h", marker_color=color,
            text=[signed(v) for v in rows["changePct"]], textposition="outside", cliponaxis=False,
            customdata=rows[[name_col, "navPerUnit", "navDate"]],
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>NAV %{customdata[1]:.4f} (%{customdata[2]|%d %b})"
                          "<br>Change %{x:+.2f}%<extra></extra>",
        ))
        fig.update_layout(title=title, height=380, margin=dict(l=0, r=40, t=40, b=0),
                          xaxis=dict(ticksuffix="%", zeroline=True,
                                     # extra room so the value labels don't run into the fund names
                                     range=[min(0, rows["changePct"].min()) * 1.35,
                                            max(0, rows["changePct"].max()) * 1.35]),
                          yaxis=dict(autorange="reversed"))
        col.plotly_chart(fig, use_container_width=True)


# ---------- tab 2: one fund in detail ----------

with tab_detail:
    funds = market.sort_values("symbol")
    labels = dict(zip(funds["symbol"], funds["symbol"] + "  ·  " + funds[name_col].fillna("")))
    choices = list(labels)
    sym = st.selectbox("Fund (type to search)", choices, format_func=labels.get,
                       index=choices.index("ES-GQG") if "ES-GQG" in labels else 0)

    with st.spinner(f"Loading full history of {sym} ..."):
        hist = load_full_history(sym, day)

    if hist.empty:
        st.warning("No history found for this fund.")
    else:
        last = hist.iloc[-1]
        st.subheader(sym)
        st.caption(f"{last['nameEn']}  ·  {last['nameTh']}  ·  {last['amcNameEn']}")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(f"NAV/unit · {last['navDate']:%d %b %Y}", f"{last['navPerUnit']:.4f}",
                  signed(last["changePct"]))
        m2.metric("Fund size", f"{last['nav'] / 1e6:,.0f} M THB" if pd.notna(last["nav"]) else "–")
        m3.metric("Data since", f"{hist['navDate'].iloc[0]:%d %b %Y}",
                  help="First NAV in the data. Usually the fund's launch date.")
        m4.metric("Type", last["projectType"] or "–")

        # Factsheet-style performance table
        st.markdown("#### Performance · dividends reinvested")
        perf = period_returns(hist).set_index("Period").T
        perf.index = ["Return", "Per year (annualized)"]
        st.dataframe(perf.map(signed), use_container_width=True)
        st.caption("Periods of 1 year or more are also shown per year, as on official factsheets. "
                   "A dash means the fund is younger than the period.")

        fig = go.Figure(go.Scatter(
            x=hist["navDate"], y=hist["navPerUnit"], name="NAV per unit",
            line=dict(width=2, color=SERIES_COLORS[0]),
            hovertemplate="%{x|%d %b %Y}<br>NAV %{y:.4f}<extra></extra>",
        ))
        fig.update_layout(
            height=420, margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified",
            xaxis=dict(rangeselector=dict(buttons=[
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(count=10, label="10Y", step="year", stepmode="backward"),
                dict(label="All", step="all"),
            ])),
        )
        st.plotly_chart(fig, use_container_width=True)
        if st.button(f"📈 Simulate Lump sum / DCA / VCA in {sym}"):
            # Start the simulator with a portfolio of just this fund.
            st.session_state["sim_portfolio"] = pd.DataFrame(
                [{"Fund": fund_label(sym, last["nameEn"]), "Weight %": 100}])
            st.session_state.pop("sim_editor", None)  # forget edits to the previous portfolio
            st.switch_page("module2_investment/simulator.py")

        c1, c2 = st.columns(2)

        # Calendar-year returns
        years = calendar_year_returns(hist)
        year_labels = [f"{y}*" if note else str(y) for y, note in zip(years["Year"], years["Note"])]
        fig = go.Figure(go.Bar(
            x=year_labels, y=years["Return %"],
            marker_color=[UP_COLOR if v >= 0 else DOWN_COLOR for v in years["Return %"]],
            text=[signed(v, 1) for v in years["Return %"]], textposition="outside", cliponaxis=False,
            customdata=years["Note"],
            hovertemplate="<b>%{x}</b> %{y:+.2f}%<br>%{customdata}<extra></extra>",
        ))
        fig.update_layout(title="Return by calendar year", height=360, margin=dict(l=0, r=0, t=40, b=0),
                          yaxis=dict(ticksuffix="%"), xaxis=dict(type="category"))
        c1.plotly_chart(fig, use_container_width=True)
        c1.caption("\\* partial year (from launch, or year to date)")

        # Drawdown
        dd = drawdown(hist) * 100
        fig = go.Figure(go.Scatter(
            x=dd.index, y=dd.values, fill="tozeroy", line=dict(width=1.5, color=DOWN_COLOR),
            hovertemplate="%{x|%d %b %Y}<br>%{y:.1f}% below previous high<extra></extra>",
        ))
        fig.update_layout(title=f"Drop from previous high · worst {dd.min():.1f}%", height=360,
                          margin=dict(l=0, r=0, t=40, b=0), yaxis=dict(ticksuffix="%"))
        c2.plotly_chart(fig, use_container_width=True)
        c2.caption("Shows how deep and how long the losses were. 0% = at a new high.")

        # Dividends
        divs = dividends(hist)
        if not divs.empty:
            st.markdown(f"#### Dividends · {len(divs)} payments, "
                        f"{divs['dividendValue'].sum():.2f} THB/unit in total")
            st.dataframe(divs, hide_index=True, use_container_width=True, column_config={
                "navDate": st.column_config.DateColumn("XD date", format="DD MMM YYYY"),
                "dividendDate": st.column_config.DateColumn("Pay date", format="DD MMM YYYY"),
                "dividendValue": st.column_config.NumberColumn("THB per unit", format="%.4f"),
                "yieldPct": st.column_config.NumberColumn("% of NAV", format="%.2f%%"),
            })

        st.download_button("⬇️ Download full history (CSV)", csv_bytes(hist),
                           file_name=f"{sym}_full_history_{day}.csv", mime="text/csv")


# ---------- tab 3: compare funds ----------

with tab_history:
    st.subheader("Compare funds")
    symbols = sorted(market["symbol"].unique())
    default = [s for s in ["K-USA-A(A)", "SCBSET"] if s in symbols]

    c1, c2 = st.columns([3, 2])
    picked = c1.multiselect(f"Funds to compare (max {MAX_COMPARE})", symbols, default=default,
                            max_selections=MAX_COMPARE)
    period = c2.radio("Period", list(PERIODS), index=list(PERIODS).index("1Y"), horizontal=True)

    if not picked:
        st.info("Pick one or more funds above.")
    else:
        histories = {}
        with st.spinner("Loading history ..."):
            for sym in picked:
                h = load_full_history(sym, day)
                if h.empty:
                    continue
                start = period_start(h["navDate"].iloc[-1], PERIODS[period])
                if start is not None:
                    # Measure from the last NAV on/before the start date (factsheet convention).
                    before = h.loc[h["navDate"] <= start, "navDate"]
                    h = h[h["navDate"] >= before.iloc[-1]] if len(before) else h
                histories[sym] = h
        histories = {s: h for s, h in histories.items() if len(h) > 1}
        if not histories:
            st.warning("No history found for these funds in this period.")
        else:
            # Rebase every fund to 100 at its first date so different NAV levels share one axis.
            fig = go.Figure()
            for i, (sym, h) in enumerate(histories.items()):
                indexed = h["growth"] / h["growth"].iloc[0] * 100
                fig.add_trace(go.Scatter(
                    x=h["navDate"], y=indexed, name=sym, mode="lines",
                    line=dict(width=2, color=SERIES_COLORS[i % len(SERIES_COLORS)]),
                    customdata=h["navPerUnit"],
                    hovertemplate=f"<b>{sym}</b> %{{y:.1f}} (NAV %{{customdata:.4f}})<extra></extra>",
                ))
            fig.add_hline(y=100, line_width=1, line_dash="dot", line_color="gray")
            fig.update_layout(
                title=f"Growth of 100 THB · {period}", height=450, hovermode="x unified",
                margin=dict(l=0, r=0, t=50, b=0), yaxis_title="Value (start = 100)",
                legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
            )
            st.plotly_chart(fig, use_container_width=True)

            stats = pd.DataFrame({s: fund_stats(h) for s, h in histories.items()}).T
            stats.insert(0, "Fund name", [histories[s][name_col].iloc[-1] for s in stats.index])
            st.dataframe(
                stats, use_container_width=True,
                column_config={
                    "Start NAV": st.column_config.NumberColumn(format="%.4f"),
                    "Latest NAV": st.column_config.NumberColumn(format="%.4f"),
                    "Total return %": st.column_config.NumberColumn(format="%+.2f%%"),
                    "Annualized return %": st.column_config.NumberColumn(
                        format="%+.2f%%", help="Only shown for periods of about 1 year or more"),
                    "Volatility % (yearly)": st.column_config.NumberColumn(
                        format="%.2f%%", help="How much the price swings. Higher = riskier."),
                    "Max drawdown %": st.column_config.NumberColumn(
                        format="%.2f%%", help="Worst fall from a peak during the period."),
                    "Days of data": st.column_config.NumberColumn(format="%d"),
                },
            )
            st.caption("Returns include dividends reinvested (total return). If a fund is younger "
                       "than the period, its line starts at its launch date.")

            all_hist = pd.concat(histories.values(), ignore_index=True)
            st.download_button("⬇️ Download history (CSV)", csv_bytes(all_hist),
                               file_name=f"history_{period}_{day}.csv", mime="text/csv")


# ---------- tab 4: fund companies ----------

with tab_amc:
    st.subheader(f"Fund companies · as of {day:%d %b %Y}")
    by_amc = (market.groupby("amcCode", dropna=False)
              .agg(funds=("symbol", "count"), aum=("nav", "sum"), median_change=("changePct", "median"))
              .reset_index().sort_values("aum", ascending=False))
    by_amc["aum"] = by_amc["aum"] / 1e9

    top = by_amc.head(15).iloc[::-1]
    fig = px.bar(top, x="aum", y="amcCode", orientation="h", text="aum",
                 labels={"aum": "Total fund size (billion THB)", "amcCode": ""},
                 color_discrete_sequence=[SERIES_COLORS[0]])
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False,
                      hovertemplate="<b>%{y}</b><br>%{x:,.1f} billion THB<extra></extra>")
    fig.update_layout(title="Top 15 companies by total fund size", height=480,
                      margin=dict(l=0, r=40, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        by_amc.style.format({"aum": "{:,.1f}", "median_change": signed}), hide_index=True,
        use_container_width=True,
        column_config={
            "amcCode": "Company",
            "funds": "Number of funds",
            "aum": "Total size (B THB)",
            "median_change": "Median last change",
        },
    )
    st.caption("Fund size is the sum of NAV across all share classes the company manages.")
