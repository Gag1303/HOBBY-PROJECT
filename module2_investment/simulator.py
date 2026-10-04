"""CFP Module 2 (Investment Planning) - investment simulator page.

Back-test Lump sum, DCA and VCA on a portfolio of Thai mutual funds using their real NAV
history. The calculations live in simulate.py; this file is only the page.
"""

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from i18n import lang, t
from module2_investment.common import (
    DATA_NOTE, SERIES_COLORS, fund_label, last_date_or_stop, load_full_history, load_market,
    signed, symbol_of,
)
from module2_investment.simulate import (
    FREQUENCIES, REBALANCING, STRATEGIES, align_prices, simulate, trade_dates,
)

MAX_FUNDS = len(SERIES_COLORS)  # one distinct color per fund

STRATEGY_HELP = {
    "Lump sum": "Invest the whole amount once, on the start date.",
    "DCA": "Dollar cost averaging: invest the same amount every period, whatever the price.",
    "VCA": "Value averaging: the portfolio should grow by a fixed amount every period. Each period you "
           "top up whatever is needed to reach the target, so you buy more when prices fall and "
           "less (or nothing) when they rise.",
}
REBALANCE_HELP = ("Every amount invested is split by the target weights. Over time the funds that "
                  "grew most take a bigger share. Rebalancing sells some of those and buys the "
                  "others to get back to the target weights.")

st.title("📈 " + t("Investment simulator"))
st.caption(t("What would have happened if you had invested in a portfolio of funds with Lump sum, "
             "DCA or VCA? Uses the funds' real NAV history, dividends reinvested."))
st.sidebar.caption(t(DATA_NOTE))

last_date = last_date_or_stop()
with st.spinner(t("Loading fund list ...")):
    market = load_market(last_date)
funds = market.sort_values("symbol")
name_col = "nameTh" if lang() == "th" else "nameEn"
options = [fund_label(s, n) for s, n in zip(funds["symbol"], funds[name_col])]
by_symbol = {symbol_of(o): o for o in options}

# ---------- strategy ----------

st.markdown("#### " + t("Strategy"))
c1, c2, c3 = st.columns([2, 1, 1])
strategy = c1.radio(t("Strategy"), STRATEGIES, index=1, horizontal=True, format_func=t,
                    label_visibility="collapsed")
if strategy == "Lump sum":
    frequency, allow_sell = "Monthly", False
else:
    frequency = c2.selectbox(t("Every"), list(FREQUENCIES), format_func=t)
    allow_sell = strategy == "VCA" and c3.toggle(
        t("Sell when above target"), help=t("Off: when the portfolio is above target you just skip "
                                            "that period. On: you sell the part above target."))
st.caption(t(STRATEGY_HELP[strategy]))

# ---------- portfolio: total money box and fund table ----------

st.markdown("#### " + t("Portfolio"))
label, default_total = {
    "Lump sum": ("Total amount to invest (THB)", 100_000),
    "DCA": ("Total amount each period (THB)", 5_000),
    "VCA": ("Total target growth each period (THB)", 5_000),
}[strategy]
total_box = st.number_input(t(label), min_value=0, value=default_total, step=500, format="%d",
                            key=f"sim_total_{strategy}")

latest_nav = dict(zip(funds["symbol"], funds["navPerUnit"]))
latest_nav_date = dict(zip(funds["symbol"], funds["navDate"]))
COLS = ["Fund", "Weight %", "Amount (THB)", "Units"]


def changed(new, old) -> bool:
    if pd.isna(new) and pd.isna(old):
        return False
    return pd.isna(new) != pd.isna(old) or abs(float(new) - float(old)) > 1e-6


def resolve(edited: pd.DataFrame, before: pd.DataFrame, total: float) -> pd.DataFrame:
    """Keep Weight %, Amount (THB) and Units in step after an edit.

    Whichever of the three the user changed in a row wins and the other two are recalculated
    (THB = weight x total; units = THB / the fund's latest NAV). Rows the user hasn't set
    ("auto") share whatever weight is left equally, so 5 untouched funds get 20% each.
    """
    df = edited.copy()
    for c in ["Weight %", "Amount (THB)", "Units"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["auto"] = df["auto"].astype("boolean").fillna(True).astype(bool) if "auto" in df else True
    for i in df.index:
        old = before.loc[i] if i in before.index else None
        nav = latest_nav.get(symbol_of(df.at[i, "Fund"]) if isinstance(df.at[i, "Fund"], str) else "")
        w, a, u = df.at[i, "Weight %"], df.at[i, "Amount (THB)"], df.at[i, "Units"]
        if old is None:  # new row: whatever the user typed decides, empty = auto
            edited_col = ("Units" if pd.notna(u) and u > 0 else "Amount (THB)" if pd.notna(a) and a > 0
                          else "Weight %" if pd.notna(w) and w > 0 else None)
        else:
            edited_col = next((c for c in ["Units", "Amount (THB)", "Weight %"]
                               if changed(df.at[i, c], old[c])), None)
        if edited_col and pd.isna(df.at[i, edited_col]):
            df.at[i, "auto"] = True  # the user cleared the cell: hand the row back to auto
        elif edited_col == "Units" and nav and total:
            df.at[i, "Weight %"], df.at[i, "auto"] = u * nav / total * 100, False
        elif edited_col == "Amount (THB)" and total:
            df.at[i, "Weight %"], df.at[i, "auto"] = a / total * 100, False
        elif edited_col == "Weight %":
            df.at[i, "auto"] = False
    has_fund = df["Fund"].notna()
    manual = has_fund & ~df["auto"]
    auto = has_fund & df["auto"]
    left = max(0.0, 100 - df.loc[manual, "Weight %"].fillna(0).sum())
    df.loc[auto, "Weight %"] = left / auto.sum() if auto.any() else 0
    df["Weight %"] = df["Weight %"].fillna(0).round(4)
    df["Amount (THB)"] = (df["Weight %"] / 100 * total).round(2)
    navs = df["Fund"].map(lambda f: latest_nav.get(symbol_of(f)) if isinstance(f, str) else None)
    df["Units"] = (df["Amount (THB)"] / pd.to_numeric(navs, errors="coerce")).round(4)
    return df[COLS + ["auto"]]


if "sim_portfolio" not in st.session_state:
    st.session_state["sim_portfolio"] = pd.DataFrame(
        [{"Fund": by_symbol.get(s), "auto": True} for s in ["ES-GQG", "SCBSET"] if s in by_symbol],
        columns=COLS + ["auto"])
# Missing columns (e.g. a portfolio started from Fund detail) are filled in by resolve().
base = st.session_state["sim_portfolio"].reindex(columns=COLS + ["auto"])
if base["auto"].isna().all():
    base["auto"] = True
# Show fund names in the current language (the table may have been saved in the other one).
base["Fund"] = base["Fund"].map(lambda f: by_symbol.get(symbol_of(f), f) if isinstance(f, str) else f)
base = resolve(base, base, total_box)  # e.g. the total changed: refresh THB and units

if st.button("⚖️ " + t("Split equally"), help=t("Give every fund the same weight.")):
    base = resolve(base.assign(auto=True), base.assign(auto=True), total_box)
    st.session_state["sim_portfolio"] = base
    st.session_state.pop("sim_editor", None)
    st.rerun()

edited = st.data_editor(
    base, key="sim_editor", num_rows="dynamic", hide_index=True, use_container_width=True,
    column_order=COLS,  # "auto" stays hidden
    column_config={
        "Fund": st.column_config.SelectboxColumn(t("Fund (type to search)"), options=options,
                                                 required=True, width="large"),
        "Weight %": st.column_config.NumberColumn(t("Weight %"), min_value=0, max_value=100,
                                                  step=0.5, format="%.1f%%"),
        "Amount (THB)": st.column_config.NumberColumn(t("Amount (THB)"), min_value=0, step=500,
                                                      format="%.0f"),
        "Units": st.column_config.NumberColumn(t("Units"), min_value=0, format="%.4f",
                                               help=t("Units at the fund's latest NAV.")),
    },
)
resolved = resolve(edited, base, total_box)
if not resolved[COLS].equals(base[COLS]) or not resolved.index.equals(base.index):
    st.session_state["sim_portfolio"] = resolved.reset_index(drop=True)
    st.session_state.pop("sim_editor", None)  # show the recalculated table
    st.rerun()
st.session_state["sim_portfolio"] = base

nav_dates = {latest_nav_date[symbol_of(f)] for f in base["Fund"].dropna() if symbol_of(f) in latest_nav_date}
st.caption(
    t("Change **any one** of Weight %, Amount or Units and the other two follow. Funds you haven't "
      "set share the rest of the 100% equally. Units use each fund's latest NAV ({date}). Add a row "
      "with the + under the table, delete with the checkbox and 🗑. Up to {n} funds.",
      date=f"{max(nav_dates):%d %b %Y}" if nav_dates else "–", n=MAX_FUNDS)
)

rows = base[base["Fund"].notna() & (base["Weight %"] > 0)]
weights = rows.groupby(rows["Fund"].map(symbol_of), sort=False)["Weight %"].sum()  # merge duplicates
if weights.empty:
    st.info(t("Add at least one fund."))
    st.stop()
if len(weights) > MAX_FUNDS:
    st.warning(t("Only the first {n} funds are used.", n=MAX_FUNDS))
    weights = weights.iloc[:MAX_FUNDS]
weight_sum = weights.sum()
amount = weight_sum / 100 * total_box
if weight_sum < 99.95:
    st.info(t("Weights add up to {pct}, so {left} THB of the {total} THB total is not invested. "
              "Simulating {amount} THB.", pct=f"{weight_sum:.1f}%", left=f"{total_box - amount:,.0f}",
              total=f"{total_box:,.0f}", amount=f"{amount:,.0f}"))
elif weight_sum > 100.05:
    st.warning(t("Weights add up to {pct}, so the funds need {amount} THB, {over} THB more than the "
                 "total. Simulating {amount} THB.", pct=f"{weight_sum:.1f}%", amount=f"{amount:,.0f}",
                 over=f"{amount - total_box:,.0f}"))
else:
    st.caption("**" + t("Total: 100% · {amount} THB", amount=f"{amount:,.0f}") + "**")
if amount <= 0:
    st.info(t("Set a total amount above 0."))
    st.stop()
weights = weights / weight_sum * 100

with st.spinner(t("Loading fund history ...")):
    histories = {s: load_full_history(s, last_date) for s in weights.index}
missing = [s for s, h in histories.items() if len(h) < 2]
if missing:
    st.warning(t("No history for: {funds}", funds=", ".join(missing)))
    st.stop()
prices = align_prices({s: h.set_index("navDate")["growth"] for s, h in histories.items()})
# Leave out today's NAV: funds can still revise it, and many funds haven't published it yet.
prices = prices[prices.index < pd.Timestamp(date.today())]
if len(prices) < 2:
    st.warning(t("These funds have no dates in common."))
    st.stop()

first_day, last_day = prices.index[0].date(), prices.index[-1].date()
default_start = max(first_day, (prices.index[-1] - pd.DateOffset(years=5)).date())
youngest = max(histories, key=lambda s: histories[s]["navDate"].iloc[0])

# ---------- period and rebalancing ----------

st.markdown("#### " + t("Period"))
c1, c2, c3 = st.columns([1, 1, 1])
start = c1.date_input(t("Start"), value=default_start, min_value=first_day, max_value=last_day)
end = c2.date_input(t("End"), value=last_day, min_value=first_day, max_value=last_day)
rebalance = "None"
if len(weights) > 1:
    choices = REBALANCING if strategy != "Lump sum" else ["None", "Yearly"]
    rebalance = c3.selectbox(t("Rebalance"), choices, format_func=t, help=t(REBALANCE_HELP))
if len(weights) > 1:
    note = t("Data starts {date} (the youngest fund, {fund}, launched then).",
             date=f"{first_day:%d %b %Y}", fund=youngest)
else:
    note = t("Data starts {date}.", date=f"{first_day:%d %b %Y}")
note += " " + t("Latest date {date}: today's NAV is left out because it may not be final yet.",
                date=f"{last_day:%d %b %Y}")
st.caption(note)

if start >= end:
    st.warning(t("Start date must be before the end date."))
    st.stop()
run = dict(frequency=frequency, weights=weights.to_dict(), rebalance=rebalance)
timeline, trades, s, by_fund = simulate(prices, start, end, strategy, amount,
                                        allow_sell=allow_sell, **run)
if not s:
    st.warning(t("Not enough NAV data in this period."))
    st.stop()

# ---------- results ----------

st.markdown("#### " + t("Result"))
m1, m2, m3, m4 = st.columns(4)
m1.metric(t("Money invested"), f"{s['Money in']:,.0f} THB")
m2.metric(t("Value at end"), f"{s['Value now']:,.0f} THB")
m3.metric(t("Profit"), f"{s['Profit']:,.0f} THB", signed(s["Profit %"]))
m4.metric(t("Return per year"), signed(s["Return per year %"]),
          help=t("Money-weighted return (IRR, like Excel XIRR). Fair for comparing strategies "
                 "that put money in at different times."))
if s["Money out (sold)"] > 0:
    st.caption(t("Includes {amount} THB taken out by selling above target.",
                 amount=f"{s['Money out (sold)']:,.0f}"))

fig = go.Figure([
    go.Scatter(x=timeline.index, y=timeline["value"], name=t("Portfolio value"),
               line=dict(width=2, color=SERIES_COLORS[0]),
               hovertemplate="%{y:,.0f} THB<extra>" + t("Portfolio value") + "</extra>"),
    go.Scatter(x=timeline.index, y=timeline["invested"], name=t("Money invested"),
               line=dict(width=2, color=SERIES_COLORS[1], shape="hv"),
               hovertemplate="%{y:,.0f} THB<extra>" + t("Money invested") + "</extra>"),
])
fig.update_layout(height=420, margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified",
                  yaxis=dict(title="THB", tickformat=","),
                  legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"))
st.plotly_chart(fig, use_container_width=True)

if len(weights) > 1:
    # Per-fund breakdown: where the money ended up, and how far the weights drifted.
    window = prices.loc[timeline.index]
    end_values = by_fund.iloc[-1]
    breakdown = pd.DataFrame({
        "Fund": [by_symbol.get(f, f) for f in weights.index],
        "Target weight": weights.values,
        "Value at end": end_values[weights.index].values,
        "Weight at end": (end_values / end_values.sum() * 100)[weights.index].values,
        "Fund return in period": ((window.iloc[-1] / window.iloc[0] - 1) * 100)[weights.index].values,
    })
    st.markdown("#### " + t("By fund"))
    st.dataframe(
        breakdown.style.format({"Target weight": "{:.1f}%", "Value at end": "{:,.0f}",
                                "Weight at end": "{:.1f}%", "Fund return in period": signed}),
        hide_index=True, use_container_width=True,
        column_config={c: t(c) for c in breakdown.columns},
    )

    fig = go.Figure([
        go.Scatter(x=by_fund.index, y=by_fund[f], name=f, stackgroup="funds", mode="lines",
                   line=dict(width=1, color=SERIES_COLORS[i]),
                   hovertemplate=f"%{{y:,.0f}} THB<extra>{f}</extra>")
        for i, f in enumerate(weights.index)
    ])
    fig.update_layout(title=t("Value by fund"), height=380, margin=dict(l=0, r=0, t=40, b=0),
                      hovermode="x unified", yaxis=dict(title="THB", tickformat=","),
                      legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom",
                                  traceorder="normal"))  # same order as the table
    st.plotly_chart(fig, use_container_width=True)

with st.expander(t("Every buy / sell ({n})", n=s["Trades"])):
    rows = trades[trades["cash"] != 0].style.format(
        {"date": "{:%d %b %Y}", "cash": "{:+,.0f}", "valueAfter": "{:,.0f}"})
    st.dataframe(rows, hide_index=True, use_container_width=True, column_config={
        "date": t("Date"), "cash": t("Cash in (+) / out (−)"), "valueAfter": t("Portfolio value after"),
    })

# Same period and portfolio, all three strategies, with comparable amounts.
per_period = amount
if strategy == "Lump sum":
    per_period = amount / max(len(trade_dates(prices, start, end, frequency)), 1)
dca = simulate(prices, start, end, "DCA", per_period, **run)[2]
results = {
    "Lump sum": simulate(prices, start, end, "Lump sum", dca["Money in"],
                         **{**run, "rebalance": "None" if rebalance == "Every period" else rebalance})[2],
    "DCA": dca,
    "VCA": simulate(prices, start, end, "VCA", per_period, allow_sell=allow_sell, **run)[2],
}
table = pd.DataFrame(results).T[["Money in", "Value now", "Profit", "Profit %",
                                 "Return per year %", "Largest single top-up"]]
table.index = [t(i) for i in table.index]
st.markdown("#### " + t("All strategies · same period ({frequency}, {amount} THB per period)",
                        frequency=t(frequency).lower(), amount=f"{per_period:,.0f}"))
money_cols = ["Money in", "Value now", "Profit", "Largest single top-up"]
styled = (table.style.format("{:,.0f}", subset=money_cols)
          .format(signed, subset=["Profit %", "Return per year %"]))
st.dataframe(styled, use_container_width=True,
             column_config={c: t("Value at end" if c == "Value now" else c) for c in table.columns})
st.caption(t("Lump sum invests the same total as DCA, all on the first day. VCA's target grows by "
             "the same amount per period, so the money it needs is different. Dividends are "
             "reinvested; fees and taxes are not included. Past performance does not guarantee "
             "future results."))
