"""Home page: overview of the 6 Thai CFP modules and which tools exist for each."""

import streamlit as st

from cfp_modules import MODULES

st.title("🧭 CFP Toolkit")
st.write("Personal practice tools, organised by the 6 modules of the Thai CFP® program. "
         "Each module gets its own tools as I learn it.")

with st.container(border=True):
    st.markdown("**Tools** · for every module")
    st.page_link("calculators/financial_calculator.py", label="Financial calculator: TVM, NPV / IRR, "
                 "interest rate conversion", icon="🧮")

for i, m in enumerate(MODULES):
    if i % 3 == 0:
        cols = st.columns(3)  # new row every 3 cards so rows line up
    with cols[i % 3].container(border=True):
        st.markdown(f"**Module {m.number}**  \n### {m.name_en}")
        st.caption(m.name_th)
        st.write(m.description)
        if m.home_page:
            st.page_link(m.home_page, label="Open", icon="➡️")
        else:
            st.markdown(":gray[Coming later]")

st.caption("For personal learning only. Not financial advice, and the data sources used here "
           "do not allow commercial use.")
