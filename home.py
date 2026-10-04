"""Home page: overview of the 6 Thai CFP modules and which tools exist for each."""

import streamlit as st

# (number, English name, Thai name, what this toolkit has / could have, page link or None)
MODULES = [
    (1, "Fundamentals of financial planning", "พื้นฐานการวางแผนการเงิน",
     "Ideas: time value of money calculator, personal financial statements & ratios.", None),
    (2, "Investment planning", "การวางแผนการลงทุน",
     "Thai mutual fund data: latest NAV of every fund, full performance history, "
     "fund comparison, risk numbers. Investment simulator: Lump sum vs DCA vs VCA.",
     "module2_investment/dashboard.py"),
    (3, "Risk management & insurance planning", "การวางแผนการประกันภัย",
     "Ideas: life insurance needs calculator (income replacement / needs approach).", None),
    (4, "Retirement planning & employee benefits", "การวางแผนเพื่อวัยเกษียณ",
     "Ideas: retirement savings gap, provident fund / RMF projections.", None),
    (5, "Tax & estate planning", "การวางแผนภาษีและมรดก",
     "Ideas: Thai personal income tax calculator with SSF/RMF/insurance deductions.", None),
    (6, "Financial plan development", "การจัดทำแผนการเงิน",
     "Ideas: bring modules 1-5 together into one client plan.", None),
]

st.title("🧭 CFP Toolkit")
st.write("Personal practice tools, organised by the 6 modules of the Thai CFP® program. "
         "Each module gets its own tools as I learn it.")

for i, (num, name_en, name_th, text, page) in enumerate(MODULES):
    if i % 3 == 0:
        cols = st.columns(3)  # new row every 3 cards so rows line up
    with cols[i % 3].container(border=True):
        st.markdown(f"**Module {num}**  \n### {name_en}")
        st.caption(name_th)
        st.write(text)
        if page:
            st.page_link(page, label="Open", icon="➡️")
        else:
            st.markdown(":gray[Coming later]")

st.caption("For personal learning only. Not financial advice, and the data sources used here "
           "do not allow commercial use.")
