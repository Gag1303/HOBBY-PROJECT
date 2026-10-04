"""CFP Module 2 (Investment Planning) - Thai mutual fund dashboard.

This is one page of the CFP toolkit app. Start the whole app from the project folder with
    streamlit run app.py
(or double-click run_app.bat).
"""

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from module2_investment import client
from module2_investment.tables import (
    add_growth, amc_table, calendar_year_returns, dividends, drawdown, fund_stats, latest_nav,
    period_returns, to_dataframe,
)

# Colors (validated colorblind-safe order). Up/down use blue/red rather than color alone:
# numbers always carry a +/- sign too.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
UP_COLOR, DOWN_COLOR = "#2a78d6", "#e34948"
MAX_COMPARE = 5

# Months back for each period button. 0 = year to date, None = whole history.
PERIODS = {"1M": 1, "3M": 3, "6M": 6, "YTD": 0, "1Y": 12, "3Y": 36, "5Y": 60, "10Y": 120, "Max": None}


# ---------- data loading (cached so we don't call the API on every click) ----------

@st.cache_data(ttl=3600, show_spinner=False)
def load_last_date() -> date:
    return client.last_business_date()


@st.cache_data(ttl=3600 * 24, show_spinner=False)
def load_amcs() -> pd.DataFrame:
    return amc_table()


@st.cache_data(ttl=3600, show_spinner=False)
def load_market(day: date) -> pd.DataFrame:
    return latest_nav(day, amcs=load_amcs())


@st.cache_data(ttl=3600 * 6, show_spinner=False)
def load_full_history(symbol: str, to_date: date) -> pd.DataFrame:
    """Whole NAV history of a fund (one fast request), with the dividends-reinvested growth."""
    df = to_dataframe(client.nav_history(symbol, to_date=to_date), load_amcs())
    return add_growth(df.drop_duplicates(subset=["navDate"])) if not df.empty else df


def period_start(end: pd.Timestamp, months: int | None) -> pd.Timestamp | None:
    if months is None:
        return None
    if months == 0:
        return pd.Timestamp(end.year - 1, 12, 31)
    return end - pd.DateOffset(months=months)


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")  # BOM so Excel shows Thai text


def signed(x: float, digits: int = 2) -> str:
    return "–" if pd.isna(x) else f"{x:+.{digits}f}%"


# ---------- sidebar ----------

st.sidebar.subheader("Thai mutual funds")
try:
    last_date = load_last_date()
except Exception as e:  # network down, API changed, ...
    st.error(f"Could not reach the data source: {e}")
    st.stop()

day = st.sidebar.date_input("NAV date", value=last_date, max_value=last_date,
                            help="Weekends/holidays have no data.")
name_col = "nameTh" if st.sidebar.toggle("Show Thai fund names") else "nameEn"
if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()
st.sidebar.caption(
    "Data: thaimutualfund.com (AIMC) via api.settrade.com. "
    "For personal/educational use only, not for commercial use."
)

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
    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True,
        height=420,
        column_config={
            "symbol": "Symbol",
            name_col: "Fund name",
            "navDate": st.column_config.DateColumn("NAV date", format="DD MMM"),
            "amcCode": "Company",
            "navPerUnit": st.column_config.NumberColumn("NAV/unit", format="%.4f"),
            "change": st.column_config.NumberColumn("Change", format="%+.4f"),
            "changePct": st.column_config.NumberColumn("Change %", format="%+.2f%%"),
            "nav": st.column_config.NumberColumn("Fund size (M THB)", format="%,.1f"),
            "buyPrice": st.column_config.NumberColumn("Buy", format="%.4f"),
            "sellPrice": st.column_config.NumberColumn("Sell", format="%.4f"),
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
                          xaxis=dict(ticksuffix="%", zeroline=True), yaxis=dict(autorange="reversed"))
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

        # Price chart
        show = st.radio("Chart", ["Growth of 10,000 THB", "NAV per unit"], horizontal=True)
        has_dividends = hist["dividendValue"].fillna(0).gt(0).any()
        fig = go.Figure()
        if show == "NAV per unit":
            fig.add_trace(go.Scatter(
                x=hist["navDate"], y=hist["navPerUnit"], name="NAV per unit",
                line=dict(width=2, color=SERIES_COLORS[0]),
                hovertemplate="%{x|%d %b %Y}<br>NAV %{y:.4f}<extra></extra>",
            ))
        else:
            fig.add_trace(go.Scatter(
                x=hist["navDate"], y=hist["growth"] * 10_000, name="Dividends reinvested",
                line=dict(width=2, color=SERIES_COLORS[0]),
                hovertemplate="%{y:,.0f} THB<extra>Dividends reinvested</extra>",
            ))
            if has_dividends:
                price_only = hist["navPerUnit"] / hist["navPerUnit"].iloc[0] * 10_000
                fig.add_trace(go.Scatter(
                    x=hist["navDate"], y=price_only, name="Price only",
                    line=dict(width=2, color=SERIES_COLORS[1]),
                    hovertemplate="%{y:,.0f} THB<extra>Price only</extra>",
                ))
        fig.update_layout(
            height=420, margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified",
            showlegend=bool(has_dividends and show != "NAV per unit"),
            legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
            xaxis=dict(rangeselector=dict(buttons=[
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(count=10, label="10Y", step="year", stepmode="backward"),
                dict(label="All", step="all"),
            ])),
        )
        st.plotly_chart(fig, use_container_width=True)

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
        by_amc, hide_index=True, use_container_width=True,
        column_config={
            "amcCode": "Company",
            "funds": st.column_config.NumberColumn("Number of funds", format="%d"),
            "aum": st.column_config.NumberColumn("Total size (B THB)", format="%,.1f"),
            "median_change": st.column_config.NumberColumn("Median last change", format="%+.2f%%"),
        },
    )
    st.caption("Fund size is the sum of NAV across all share classes the company manages.")
