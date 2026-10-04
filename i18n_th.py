"""Thai translations: English text (exactly as written in t("...")) -> Thai.

Keep {placeholders} the same in both languages. Common finance abbreviations (NAV, DCA, VCA,
NPV, IRR, TVM, PV, FV, PMT, THB) stay in English, as in Thai CFP materials.
"""

TH = {
    # ---------- app, menu, home ----------
    "Home": "หน้าแรก",
    "TOOLS": "เครื่องมือ",
    "CFP MODULES": "ชุดวิชา CFP",
    "Financial calculator": "เครื่องคิดเลขการเงิน",
    "Thai mutual funds": "กองทุนรวมไทย",
    "Investment simulator": "จำลองการลงทุน",
    "Module {n}": "ชุดวิชาที่ {n}",
    "Coming later": "เร็ว ๆ นี้",
    "CFP Toolkit": "ชุดเครื่องมือ CFP",
    "Personal practice tools, organised by the 6 modules of the Thai CFP® program. "
    "Each module gets its own tools as I learn it.":
        "เครื่องมือฝึกส่วนตัว จัดตาม 6 หมวดวิชาของหลักสูตร CFP® ประเทศไทย "
        "แต่ละหมวดจะมีเครื่องมือเพิ่มขึ้นตามที่เรียนไป",
    "For personal learning only. Not financial advice, and the data sources used here "
    "do not allow commercial use.":
        "ใช้เพื่อการเรียนรู้ส่วนตัวเท่านั้น ไม่ใช่คำแนะนำทางการเงิน "
        "และแหล่งข้อมูลที่ใช้ไม่อนุญาตให้ใช้เชิงพาณิชย์",
    "**Tools** · for every module": "**เครื่องมือ** · ใช้ได้ทุกหมวด",
    "Financial calculator: TVM, NPV / IRR, interest rate conversion":
        "เครื่องคิดเลขการเงิน: TVM, NPV / IRR, แปลงอัตราดอกเบี้ย",
    "Open": "เปิด",
    # module descriptions (cfp_modules.py)
    "Ideas: time value of money calculator, personal financial statements & ratios.":
        "แนวคิด: เครื่องคิดมูลค่าเงินตามเวลา งบการเงินส่วนบุคคลและอัตราส่วนทางการเงิน",
    "Thai mutual fund data: latest NAV of every fund, full performance history, "
    "fund comparison, risk numbers. Portfolio simulator: Lump sum vs DCA vs VCA.":
        "ข้อมูลกองทุนรวมไทย: NAV ล่าสุดของทุกกองทุน ผลการดำเนินงานย้อนหลังทั้งหมด "
        "เปรียบเทียบกองทุน ตัวเลขความเสี่ยง และจำลองพอร์ต: ลงทุนก้อนเดียว vs DCA vs VCA",
    "Ideas: life insurance needs calculator (income replacement / needs approach).":
        "แนวคิด: คำนวณความต้องการทุนประกันชีวิต (วิธีทดแทนรายได้ / วิธีความจำเป็น)",
    "Ideas: retirement savings gap, provident fund / RMF projections.":
        "แนวคิด: ช่องว่างเงินออมเพื่อเกษียณ ประมาณการกองทุนสำรองเลี้ยงชีพ / RMF",
    "Ideas: Thai personal income tax calculator with SSF/RMF/insurance deductions.":
        "แนวคิด: คำนวณภาษีเงินได้บุคคลธรรมดา พร้อมค่าลดหย่อน SSF/RMF/ประกัน",
    "Ideas: bring modules 1-5 together into one client plan.":
        "แนวคิด: รวมหมวด 1-5 เป็นแผนการเงินฉบับเดียวสำหรับลูกค้า",

    # ---------- CFP career guide ----------
    "CAREER": "เส้นทางอาชีพ",
    "CFP career guide": "คู่มือเส้นทางอาชีพ CFP",
    "CFP career guide: path to CFP, ethics, renewal, working abroad, TFPA documents":
        "คู่มือเส้นทางอาชีพ CFP: ขั้นตอนสู่ CFP จรรยาบรรณ การต่ออายุ การทำงานต่างประเทศ เอกสารสมาคมฯ",
    "A personal study summary of the Thai Financial Planners Association (TFPA) documents. Rules and fees "
    "can change – always check the official documents in the Documents tab.":
        "สรุปเพื่อการศึกษาส่วนตัวจากเอกสารของสมาคมนักวางแผนการเงินไทย (TFPA) เกณฑ์และค่าธรรมเนียมอาจเปลี่ยนแปลงได้ "
        "ควรตรวจสอบเอกสารทางการในแท็บเอกสารเสมอ",
    "Path to CFP": "เส้นทางสู่ CFP",
    "Ethics and rules": "จรรยาบรรณและหลักปฏิบัติ",
    "Renewal and working abroad": "การต่ออายุและการทำงานต่างประเทศ",
    "Documents": "เอกสาร",
    "My progress": "ความคืบหน้าของฉัน",
    "To use the CFP® mark in Thailand you need all **4 E's**:":
        "การจะใช้เครื่องหมาย CFP® ในประเทศไทย ต้องมีครบ **4E**:",
    "The 6 steps of financial planning (practice standards)": "6 ขั้นตอนของการวางแผนการเงิน (หลักปฏิบัติ)",
    "The 8 principles of the Code of Ethics": "จรรยาบรรณ 8 ข้อ",
    "Key rules of conduct": "หลักปฏิบัติที่สำคัญ",
    "Grouped from the 37 rules of conduct. Breaking them can lead to disciplinary action and losing the "
    "right to use the CFP mark.":
        "จัดกลุ่มจากหลักปฏิบัติ 37 ข้อ การฝ่าฝืนอาจถูกลงโทษทางวินัยและเสียสิทธิ์ใช้เครื่องหมาย CFP",
    "Keeping your CFP: renewal and CPD": "การรักษาคุณวุฒิ CFP: การต่ออายุและ CPD",
    "Working in other countries (cross-border certification)":
        "การทำงานในต่างประเทศ (การขึ้นทะเบียนข้ามประเทศ)",
    "Official documents on the TFPA website. They open on tfpa.or.th.":
        "เอกสารทางการบนเว็บไซต์สมาคมฯ เปิดที่ tfpa.or.th",
    "Tick what you have done. It is saved on this computer only.":
        "ติ๊กสิ่งที่ทำแล้ว ข้อมูลบันทึกไว้ในเครื่องนี้เท่านั้น",
    "Training done (or exempted)": "อบรมแล้ว (หรือได้รับยกเว้น)",
    "Exams passed": "สอบผ่านแล้ว",
    "Experience": "ประสบการณ์",
    "Ethics": "จรรยาบรรณ",
    "Paper 1": "ฉบับที่ 1",
    "Paper 2": "ฉบับที่ 2",
    "Paper 3": "ฉบับที่ 3",
    "Paper 4 part 1": "ฉบับที่ 4 ส่วนที่ 1",
    "Paper 4 part 2": "ฉบับที่ 4 ส่วนที่ 2",
    "Years of qualifying work": "จำนวนปีที่ทำงานที่นับได้",
    "I have read the Code of Ethics": "อ่านประมวลจรรยาบรรณแล้ว",
    "Overall progress: {pct}": "ความคืบหน้ารวม: {pct}",
    "You meet all 4 E's – you can apply for CFP registration on tfpa.or.th.":
        "ครบ 4E แล้ว – ยื่นขอขึ้นทะเบียน CFP ได้ที่ tfpa.or.th",
    "Next: training for {m}": "ขั้นต่อไป: อบรม{m}",
    "Next: pass {p}": "ขั้นต่อไป: สอบ{p}ให้ผ่าน",
    "Next: build up 3 years of experience ({left} to go)": "ขั้นต่อไป: สะสมประสบการณ์ให้ครบ 3 ปี (เหลืออีก {left} ปี)",
    "Next: read the Code of Ethics (Ethics tab)": "ขั้นต่อไป: อ่านประมวลจรรยาบรรณ (แท็บจรรยาบรรณ)",
    "Modules 1–2 and papers 1–2 done: you may already qualify for AFPT (check that your module 2 is the "
    "2021 curriculum).":
        "ผ่านชุดวิชา 1–2 และข้อสอบฉบับ 1–2 แล้ว: อาจมีคุณสมบัติขอ AFPT ได้ "
        "(ตรวจสอบว่าชุดวิชาที่ 2 เป็นหลักสูตรปี 2564)",

    # ---------- shared ----------
    "Data: thaimutualfund.com (AIMC) via api.settrade.com. "
    "For personal/educational use only, not for commercial use.":
        "ข้อมูล: thaimutualfund.com (สมาคมบริษัทจัดการลงทุน) ผ่าน api.settrade.com "
        "ใช้เพื่อการส่วนตัว/การศึกษาเท่านั้น ห้ามใช้เชิงพาณิชย์",
    "Could not reach the data source: {error}": "เชื่อมต่อแหล่งข้อมูลไม่ได้: {error}",
    "Choose an option": "เลือก",
    "Fund (type to search)": "กองทุน (พิมพ์เพื่อค้นหา)",
    "Fund name": "ชื่อกองทุน",
    "Fund": "กองทุน",
    "Period": "ช่วงเวลา",
    "Periods": "จำนวนงวด",
    "Date": "วันที่",
    "Start": "เริ่ม",
    "End": "สิ้นสุด",
    "All": "ทั้งหมด",

    # ---------- Thai mutual funds page ----------
    "NAV date": "วันที่ NAV",
    "Weekends/holidays have no data.": "วันเสาร์-อาทิตย์และวันหยุดไม่มีข้อมูล",
    "Refresh data": "รีเฟรชข้อมูล",
    "Loading latest NAV of all funds as of {day} ...": "กำลังโหลด NAV ล่าสุดของทุกกองทุน ณ {day} ...",
    "No NAV data for {day} (weekend or holiday?). Pick another date.":
        "ไม่มีข้อมูล NAV วันที่ {day} (วันหยุด?) กรุณาเลือกวันอื่น",
    "Market overview": "ภาพรวมตลาด",
    "Fund detail": "รายละเอียดกองทุน",
    "Compare funds": "เปรียบเทียบกองทุน",
    "Fund companies": "บริษัทจัดการกองทุน",
    "All funds · latest NAV as of {day}": "กองทุนทั้งหมด · NAV ล่าสุด ณ {day}",
    "Many funds (especially foreign-investing ones) report NAV 1-3 days late, so each fund shows "
    "its most recent NAV. Check the NAV date column.":
        "หลายกองทุน (โดยเฉพาะกองทุนที่ลงทุนต่างประเทศ) ประกาศ NAV ช้า 1-3 วัน "
        "จึงแสดง NAV ล่าสุดของแต่ละกองทุน ดูวันที่ได้ที่คอลัมน์วันที่ NAV",
    "Funds": "จำนวนกองทุน",
    "Up (last change)": "ขึ้น (ครั้งล่าสุด)",
    "Down (last change)": "ลง (ครั้งล่าสุด)",
    "Median change": "การเปลี่ยนแปลงมัธยฐาน",
    "Search symbol or name": "ค้นหาชื่อย่อหรือชื่อกองทุน",
    "e.g. K-USA, SET50, ทองคำ": "เช่น K-USA, SET50, ทองคำ",
    "Fund company": "บลจ.",
    "Type": "ประเภท",
    "Symbol": "ชื่อย่อ",
    "Company": "บลจ.",
    "NAV/unit": "NAV/หน่วย",
    "Change": "เปลี่ยนแปลง",
    "Change %": "เปลี่ยนแปลง %",
    "Fund size (M THB)": "มูลค่ากองทุน (ล้านบาท)",
    "Redemption price": "ราคารับซื้อคืน",
    "Offer price": "ราคาขาย",
    "Download this table (CSV)": "ดาวน์โหลดตารางนี้ (CSV)",
    "Biggest movers": "เปลี่ยนแปลงมากที่สุด",
    "Top 10 gainers": "ขึ้นมากที่สุด 10 อันดับ",
    "Top 10 losers": "ลงมากที่สุด 10 อันดับ",
    "No data for this filter.": "ไม่มีข้อมูลตามตัวกรองนี้",
    "Loading full history of {sym} ...": "กำลังโหลดข้อมูลย้อนหลังทั้งหมดของ {sym} ...",
    "No history found for this fund.": "ไม่พบข้อมูลย้อนหลังของกองทุนนี้",
    "NAV/unit · {date}": "NAV/หน่วย · {date}",
    "Fund size": "มูลค่ากองทุน",
    "{n} M THB": "{n} ล้านบาท",
    "Data since": "มีข้อมูลตั้งแต่",
    "First NAV in the data. Usually the fund's launch date.":
        "NAV แรกในข้อมูล ส่วนใหญ่คือวันจัดตั้งกองทุน",
    "Performance · dividends reinvested": "ผลการดำเนินงาน · นำเงินปันผลกลับไปลงทุน",
    "Return": "ผลตอบแทน",
    "Per year (annualized)": "ต่อปี (annualized)",
    "Since launch": "ตั้งแต่จัดตั้ง",
    "Periods of 1 year or more are also shown per year, as on official factsheets. "
    "A dash means the fund is younger than the period.":
        "ช่วง 1 ปีขึ้นไปแสดงเป็นผลตอบแทนต่อปีด้วย เหมือนในหนังสือชี้ชวนส่วนสรุป (Fund Fact Sheet) "
        "ขีด (–) หมายถึงกองทุนยังจัดตั้งไม่ถึงช่วงเวลานั้น",
    "NAV per unit": "NAV ต่อหน่วย",
    "Simulate Lump sum / DCA / VCA in {sym}": "จำลองการลงทุนก้อนเดียว / DCA / VCA ใน {sym}",
    "Return by calendar year": "ผลตอบแทนรายปีปฏิทิน",
    "\\* partial year (from launch, or year to date)": "\\* ไม่เต็มปี (ตั้งแต่จัดตั้ง หรือตั้งแต่ต้นปีถึงปัจจุบัน)",
    "below previous high": "ต่ำกว่าจุดสูงสุดก่อนหน้า",
    "Drop from previous high · worst {pct}": "ลดลงจากจุดสูงสุดก่อนหน้า · แย่ที่สุด {pct}",
    "Shows how deep and how long the losses were. 0% = at a new high.":
        "แสดงว่าขาดทุนลึกและนานแค่ไหน 0% = ทำจุดสูงสุดใหม่",
    "Dividends · {n} payments, {total} THB/unit in total": "เงินปันผล · {n} ครั้ง รวม {total} บาท/หน่วย",
    "XD date": "วันที่ขึ้นเครื่องหมาย XD",
    "Pay date": "วันจ่าย",
    "THB per unit": "บาทต่อหน่วย",
    "% of NAV": "% ของ NAV",
    "Download full history (CSV)": "ดาวน์โหลดข้อมูลย้อนหลังทั้งหมด (CSV)",
    "Funds to compare (max {n})": "กองทุนที่ต้องการเปรียบเทียบ (สูงสุด {n})",
    "Max": "ทั้งหมด",
    "Pick one or more funds above.": "เลือกกองทุนอย่างน้อยหนึ่งกองด้านบน",
    "Loading history ...": "กำลังโหลดข้อมูลย้อนหลัง ...",
    "No history found for these funds in this period.": "ไม่พบข้อมูลของกองทุนเหล่านี้ในช่วงเวลานี้",
    "Growth of 100 THB · {period}": "การเติบโตของเงิน 100 บาท · {period}",
    "Value (start = 100)": "มูลค่า (เริ่มต้น = 100)",
    "Start NAV": "NAV เริ่มต้น",
    "Latest NAV": "NAV ล่าสุด",
    "Total return %": "ผลตอบแทนรวม %",
    "Annualized return %": "ผลตอบแทนต่อปี %",
    "Volatility % (yearly)": "ความผันผวน % (ต่อปี)",
    "Max drawdown %": "การลดลงสูงสุด % (Max drawdown)",
    "Days of data": "จำนวนวันที่มีข้อมูล",
    "Only shown for periods of about 1 year or more": "แสดงเฉพาะช่วงประมาณ 1 ปีขึ้นไป",
    "How much the price swings. Higher = riskier.": "ราคาแกว่งมากแค่ไหน ยิ่งสูง = ยิ่งเสี่ยง",
    "Worst fall from a peak during the period.": "การลดลงจากจุดสูงสุดที่แย่ที่สุดในช่วงเวลานี้",
    "Returns include dividends reinvested (total return). If a fund is younger than the period, "
    "its line starts at its launch date.":
        "ผลตอบแทนรวมการนำเงินปันผลกลับไปลงทุน (Total return) "
        "ถ้ากองทุนจัดตั้งไม่ถึงช่วงเวลานั้น เส้นจะเริ่มที่วันจัดตั้ง",
    "Download history (CSV)": "ดาวน์โหลดข้อมูลย้อนหลัง (CSV)",
    "Fund companies · as of {day}": "บริษัทจัดการกองทุน · ณ {day}",
    "Total fund size (billion THB)": "มูลค่ากองทุนรวม (พันล้านบาท)",
    "billion THB": "พันล้านบาท",
    "Top 15 companies by total fund size": "15 บลจ. ที่มีมูลค่ากองทุนรวมสูงสุด",
    "Number of funds": "จำนวนกองทุน",
    "Total size (B THB)": "มูลค่ารวม (พันล้านบาท)",
    "Median last change": "การเปลี่ยนแปลงล่าสุด (มัธยฐาน)",
    "Fund size is the sum of NAV across all share classes the company manages.":
        "มูลค่ากองทุนคือผลรวม NAV ของทุกชนิดหน่วยลงทุนที่ บลจ. บริหาร",

    # ---------- investment simulator ----------
    "What would have happened if you had invested in a portfolio of funds with Lump sum, DCA or "
    "VCA? Uses the funds' real NAV history, dividends reinvested.":
        "ถ้าลงทุนในพอร์ตกองทุนแบบก้อนเดียว, DCA หรือ VCA ผลจะเป็นอย่างไร? "
        "ใช้ NAV จริงย้อนหลังของกองทุน และนำเงินปันผลกลับไปลงทุน",
    "Loading fund list ...": "กำลังโหลดรายชื่อกองทุน ...",
    "Strategy": "กลยุทธ์",
    "Lump sum": "ลงทุนก้อนเดียว",
    "DCA": "DCA",
    "VCA": "VCA",
    "Every": "ทุก",
    "Monthly": "รายเดือน",
    "Weekly": "รายสัปดาห์",
    "Quarterly": "รายไตรมาส",
    "Sell when above target": "ขายเมื่อเกินเป้า",
    "Off: when the portfolio is above target you just skip that period. "
    "On: you sell the part above target.":
        "ปิด: ถ้าพอร์ตเกินเป้า งวดนั้นจะไม่ลงทุนเพิ่ม เปิด: ขายส่วนที่เกินเป้าออก",
    "Invest the whole amount once, on the start date.": "ลงทุนเงินทั้งหมดครั้งเดียวในวันเริ่มต้น",
    "Dollar cost averaging: invest the same amount every period, whatever the price.":
        "DCA (ถัวเฉลี่ยต้นทุน): ลงทุนเท่ากันทุกงวด ไม่ว่าราคาจะเป็นเท่าไร",
    "Value averaging: the portfolio should grow by a fixed amount every period. Each period you "
    "top up whatever is needed to reach the target, so you buy more when prices fall and less "
    "(or nothing) when they rise.":
        "VCA (ถัวเฉลี่ยมูลค่า): ให้มูลค่าพอร์ตเพิ่มขึ้นงวดละเท่า ๆ กัน แต่ละงวดเติมเงินเท่าที่ขาด "
        "จึงซื้อมากขึ้นเมื่อราคาลง และซื้อน้อยลง (หรือไม่ซื้อ) เมื่อราคาขึ้น",
    "Portfolio": "พอร์ตการลงทุน",
    "Total amount to invest (THB)": "เงินลงทุนทั้งหมด (บาท)",
    "Total amount each period (THB)": "เงินลงทุนรวมต่องวด (บาท)",
    "Total target growth each period (THB)": "เป้ามูลค่าเพิ่มขึ้นรวมต่องวด (บาท)",
    "Split equally": "แบ่งเท่ากัน",
    "Give every fund the same weight.": "ให้ทุกกองทุนมีสัดส่วนเท่ากัน",
    "Weight %": "สัดส่วน %",
    "Amount (THB)": "จำนวนเงิน (บาท)",
    "Units": "หน่วยลงทุน",
    "Units at the fund's latest NAV.": "จำนวนหน่วยคิดจาก NAV ล่าสุดของกองทุน",
    "Change **any one** of Weight %, Amount or Units and the other two follow. Funds you haven't "
    "set share the rest of the 100% equally. Units use each fund's latest NAV ({date}). Add a row "
    "with the + under the table, delete with the checkbox and 🗑. Up to {n} funds.":
        "แก้ **ช่องใดช่องหนึ่ง** ระหว่างสัดส่วน % จำนวนเงิน หรือหน่วยลงทุน อีกสองช่องจะปรับตาม "
        "กองทุนที่ไม่ได้กำหนดจะแบ่งส่วนที่เหลือของ 100% เท่า ๆ กัน หน่วยลงทุนคิดจาก NAV ล่าสุด ({date}) "
        "เพิ่มแถวด้วย + ใต้ตาราง ลบด้วยช่องติ๊กและ 🗑 ได้สูงสุด {n} กองทุน",
    "Add at least one fund.": "เพิ่มกองทุนอย่างน้อยหนึ่งกอง",
    "Only the first {n} funds are used.": "ใช้เฉพาะ {n} กองทุนแรก",
    "Weights add up to {pct}, so {left} THB of the {total} THB total is not invested. "
    "Simulating {amount} THB.":
        "สัดส่วนรวม {pct} จึงมีเงิน {left} บาท จากทั้งหมด {total} บาท ที่ไม่ได้ลงทุน "
        "จำลองด้วยเงิน {amount} บาท",
    "Weights add up to {pct}, so the funds need {amount} THB, {over} THB more than the total. "
    "Simulating {amount} THB.":
        "สัดส่วนรวม {pct} กองทุนจึงต้องใช้เงิน {amount} บาท มากกว่ายอดรวม {over} บาท "
        "จำลองด้วยเงิน {amount} บาท",
    "Total: 100% · {amount} THB": "รวม: 100% · {amount} บาท",
    "Set a total amount above 0.": "กรุณาใส่จำนวนเงินรวมมากกว่า 0",
    "Loading fund history ...": "กำลังโหลดข้อมูลย้อนหลังของกองทุน ...",
    "No history for: {funds}": "ไม่มีข้อมูลย้อนหลัง: {funds}",
    "These funds have no dates in common.": "กองทุนเหล่านี้ไม่มีวันที่ที่มีข้อมูลตรงกัน",
    "Rebalance": "ปรับสัดส่วน (Rebalance)",
    "None": "ไม่ปรับ",
    "Yearly": "รายปี",
    "Every period": "ทุกงวด",
    "Every amount invested is split by the target weights. Over time the funds that grew most take "
    "a bigger share. Rebalancing sells some of those and buys the others to get back to the target "
    "weights.":
        "เงินที่ลงทุนแต่ละครั้งแบ่งตามสัดส่วนเป้าหมาย เมื่อเวลาผ่านไปกองทุนที่โตมากจะมีสัดส่วนมากขึ้น "
        "การปรับสัดส่วนคือขายกองที่โตมากบางส่วนแล้วซื้อกองอื่น ให้กลับมาตามสัดส่วนเป้าหมาย",
    "Data starts {date} (the youngest fund, {fund}, launched then).":
        "มีข้อมูลตั้งแต่ {date} (วันจัดตั้งของกองทุนที่ใหม่ที่สุดคือ {fund})",
    "Data starts {date}.": "มีข้อมูลตั้งแต่ {date}",
    "Latest date {date}: today's NAV is left out because it may not be final yet.":
        "วันที่ล่าสุด {date}: ไม่รวม NAV ของวันนี้ เพราะอาจยังไม่เป็นตัวเลขสุดท้าย",
    "Start date must be before the end date.": "วันเริ่มต้องอยู่ก่อนวันสิ้นสุด",
    "Not enough NAV data in this period.": "ข้อมูล NAV ในช่วงนี้ไม่เพียงพอ",
    "Result": "ผลลัพธ์",
    "Money invested": "เงินที่ลงทุน",
    "Value at end": "มูลค่า ณ วันสิ้นสุด",
    "Profit": "กำไร",
    "Return per year": "ผลตอบแทนต่อปี",
    "Money-weighted return (IRR, like Excel XIRR). Fair for comparing strategies that put money "
    "in at different times.":
        "ผลตอบแทนแบบถ่วงน้ำหนักด้วยเงินลงทุน (IRR เหมือน XIRR ใน Excel) "
        "เหมาะสำหรับเปรียบเทียบกลยุทธ์ที่ลงเงินในเวลาต่างกัน",
    "Includes {amount} THB taken out by selling above target.": "รวมเงิน {amount} บาท ที่ขายออกเมื่อเกินเป้า",
    "Portfolio value": "มูลค่าพอร์ต",
    "By fund": "แยกตามกองทุน",
    "Target weight": "สัดส่วนเป้าหมาย",
    "Weight at end": "สัดส่วน ณ วันสิ้นสุด",
    "Fund return in period": "ผลตอบแทนกองทุนในช่วงนี้",
    "Value by fund": "มูลค่าแยกตามกองทุน",
    "Every buy / sell ({n})": "รายการซื้อ / ขายทั้งหมด ({n})",
    "Cash in (+) / out (−)": "เงินเข้า (+) / ออก (−)",
    "Portfolio value after": "มูลค่าพอร์ตหลังรายการ",
    "All strategies · same period ({frequency}, {amount} THB per period)":
        "ทุกกลยุทธ์ · ช่วงเวลาเดียวกัน ({frequency} งวดละ {amount} บาท)",
    "Money in": "เงินลงทุน",
    "Profit %": "กำไร %",
    "Return per year %": "ผลตอบแทนต่อปี %",
    "Largest single top-up": "เติมเงินมากที่สุดต่อครั้ง",
    "Lump sum invests the same total as DCA, all on the first day. VCA's target grows by the same "
    "amount per period, so the money it needs is different. Dividends are reinvested; fees and "
    "taxes are not included. Past performance does not guarantee future results.":
        "ลงทุนก้อนเดียวใช้เงินรวมเท่ากับ DCA แต่ลงทั้งหมดในวันแรก VCA ตั้งเป้าเพิ่มงวดละเท่ากัน "
        "จึงใช้เงินไม่เท่ากัน นำเงินปันผลกลับไปลงทุน ไม่รวมค่าธรรมเนียมและภาษี "
        "ผลการดำเนินงานในอดีตไม่ได้เป็นสิ่งยืนยันถึงผลการดำเนินงานในอนาคต",

    # ---------- financial calculator ----------
    "Works like the HP 10bII / Casio FC-200V used in the CFP exam. Sign rule: money you "
    "**pay out is negative**, money you **receive is positive**.":
        "ใช้งานเหมือนเครื่องคิดเลข HP 10bII / Casio FC-200V ที่ใช้สอบ CFP กฎเครื่องหมาย: "
        "เงินที่ **จ่ายออกเป็นลบ** เงินที่ **ได้รับเป็นบวก**",
    "TVM (N, I/Y, PV, PMT, FV)": "TVM (N, I/Y, PV, PMT, FV)",
    "Cash flows (NPV / IRR)": "กระแสเงินสด (NPV / IRR)",
    "Interest rate conversion": "แปลงอัตราดอกเบี้ย",
    "Load an example": "โหลดตัวอย่าง",
    "Pick a practice question (optional)": "เลือกโจทย์ฝึก (ไม่บังคับ)",
    "Save 5,000 a month for 10 years at 5%: how much at the end?":
        "ออมเดือนละ 5,000 บาท 10 ปี ผลตอบแทน 5%: ครบกำหนดได้เท่าไร?",
    "Home loan 3,000,000 THB, 6%, 30 years: monthly payment?":
        "กู้ซื้อบ้าน 3,000,000 บาท ดอกเบี้ย 6% 30 ปี: ผ่อนเดือนละเท่าไร?",
    "Want 10,000,000 THB in 25 years at 6%: how much to save each month?":
        "อยากมี 10,000,000 บาท ใน 25 ปี ผลตอบแทน 6%: ต้องออมเดือนละเท่าไร?",
    "Retirement: spend 30,000 a month for 25 years, money earns 4%: how much needed at retirement?":
        "เกษียณ: ใช้เดือนละ 30,000 บาท 25 ปี เงินได้ผลตอบแทน 4%: ต้องมีเงินเท่าไรตอนเกษียณ?",
    "1,000,000 THB grows to 2,000,000 in 10 years: what yearly return?":
        "เงิน 1,000,000 บาท โตเป็น 2,000,000 บาท ใน 10 ปี: ผลตอบแทนปีละเท่าไร?",
    "Save 10,000 a month at 5%: how long to reach 1,000,000?":
        "ออมเดือนละ 10,000 บาท ผลตอบแทน 5%: ใช้เวลานานเท่าไรถึง 1,000,000 บาท?",
    "Solve for": "หาค่า",
    "P/Y (payments per year)": "P/Y (จำนวนงวดชำระต่อปี)",
    "C/Y (compounding per year)": "C/Y (จำนวนครั้งทบต้นต่อปี)",
    "How often interest is added. Usually the same as P/Y.": "ดอกเบี้ยทบต้นบ่อยแค่ไหน ปกติเท่ากับ P/Y",
    "Payments at": "จ่ายเงินตอน",
    "END: at the end of each period (loans, most savings). BGN: at the start (rent, insurance "
    "premiums, retirement spending).":
        "END: ปลายงวด (เงินกู้ การออมส่วนใหญ่) BGN: ต้นงวด (ค่าเช่า เบี้ยประกัน ค่าใช้จ่ายหลังเกษียณ)",
    "Number of payment periods (e.g. 10 years of monthly payments = 120).":
        "จำนวนงวด (เช่น จ่ายรายเดือน 10 ปี = 120 งวด)",
    "Interest rate per year, in % (nominal).": "อัตราดอกเบี้ยต่อปี เป็น % (อัตราที่ประกาศ/nominal)",
    "Present value: money at the start. Paid out = negative, received = positive.":
        "มูลค่าปัจจุบัน: เงิน ณ ตอนเริ่ม จ่ายออก = ลบ ได้รับ = บวก",
    "Payment each period. Paid out = negative, received = positive.":
        "เงินแต่ละงวด จ่ายออก = ลบ ได้รับ = บวก",
    "Future value: money at the end.": "มูลค่าในอนาคต: เงิน ณ ตอนสิ้นสุด",
    "No solution for these values. Check the signs.": "ไม่มีคำตอบสำหรับค่าเหล่านี้ ลองตรวจเครื่องหมาย +/-",
    "No solution: with these values the money never reaches the target.":
        "ไม่มีคำตอบ: ด้วยค่าเหล่านี้เงินจะไม่มีวันถึงเป้าหมาย",
    "No solution: check the signs (money paid out must be negative).":
        "ไม่มีคำตอบ: ตรวจเครื่องหมาย (เงินที่จ่ายออกต้องเป็นลบ)",
    "N = {n} periods = {years} years": "N = {n} งวด = {years} ปี",
    "rate per period {pct}": "อัตราต่องวด {pct}",
    "effective rate per year {pct}": "อัตราที่แท้จริงต่อปี {pct}",
    "payments at {mode}": "จ่ายเงินตอน {mode}",
    "Schedule: balance period by period ({n} periods)": "ตารางยอดคงเหลือรายงวด ({n} งวด)",
    "Payment": "เงินงวด",
    "Interest": "ดอกเบี้ย",
    "Balance": "ยอดคงเหลือ",
    "Total payments {paid} · total interest {interest}. Signs follow the calculator's rule: when "
    "saving, the balance is negative (money you have put in, worth FV at the end); for a loan it is "
    "positive (money you still owe, 0 when paid off).":
        "เงินงวดรวม {paid} · ดอกเบี้ยรวม {interest} เครื่องหมายเป็นไปตามกฎของเครื่องคิดเลข: "
        "ถ้าเป็นการออม ยอดคงเหลือเป็นลบ (เงินที่ใส่เข้าไป มีมูลค่าเท่ากับ FV ตอนสิ้นสุด) "
        "ถ้าเป็นเงินกู้ ยอดคงเหลือเป็นบวก (หนี้ที่ยังค้าง เป็น 0 เมื่อผ่อนหมด)",
    "CF0 is today (usually the money you put in, negative). The following rows come at the end of "
    "each period. **Times** repeats a cash flow, like Nj on the calculator.":
        "CF0 คือวันนี้ (ปกติเป็นเงินที่ลงทุน จึงเป็นลบ) แถวถัดไปคือปลายงวดแต่ละงวด "
        "**จำนวนครั้ง** ใช้ซ้ำกระแสเงินสด เหมือนปุ่ม Nj บนเครื่องคิดเลข",
    "Cash flow (THB)": "กระแสเงินสด (บาท)",
    "Times": "จำนวนครั้ง",
    "Discount rate per period (%)": "อัตราคิดลดต่องวด (%)",
    "Enter CF0 and at least one later cash flow.": "ใส่ CF0 และกระแสเงินสดงวดถัดไปอย่างน้อยหนึ่งงวด",
    "Value today of all cash flows at the discount rate. Above 0 = worth doing.":
        "มูลค่าปัจจุบันของกระแสเงินสดทั้งหมดที่อัตราคิดลด มากกว่า 0 = คุ้มค่าที่จะลงทุน",
    "IRR per period": "IRR ต่องวด",
    "The rate at which NPV = 0.": "อัตราที่ทำให้ NPV = 0",
    "No IRR: cash flows need at least one negative and one positive amount.":
        "หา IRR ไม่ได้: กระแสเงินสดต้องมีทั้งค่าลบและค่าบวกอย่างน้อยอย่างละหนึ่ง",
    "Cash flows in order:": "กระแสเงินสดตามลำดับ:",
    "Nominal → effective (EAR)": "อัตราที่ประกาศ → อัตราที่แท้จริง (EAR)",
    "Effective → nominal": "อัตราที่แท้จริง → อัตราที่ประกาศ",
    "Nominal rate per year (%)": "อัตราที่ประกาศต่อปี (%)",
    "Effective rate per year (%)": "อัตราที่แท้จริงต่อปี (%)",
    "Effective rate per year": "อัตราที่แท้จริงต่อปี",
    "Nominal rate per year": "อัตราที่ประกาศต่อปี",
    "Compounded": "ทบต้น",
    "Yearly (1)": "รายปี (1)",
    "Half-yearly (2)": "ราย 6 เดือน (2)",
    "Quarterly (4)": "รายไตรมาส (4)",
    "Monthly (12)": "รายเดือน (12)",
    "Weekly (52)": "รายสัปดาห์ (52)",
    "Daily (365)": "รายวัน (365)",
    "Continuous": "ต่อเนื่อง",
    "A bank quoting 12% compounded monthly really pays 12.68% a year. Compare offers using the "
    "effective rate.":
        "ธนาคารที่ประกาศ 12% ทบต้นรายเดือน จ่ายจริง 12.68% ต่อปี "
        "ควรเปรียบเทียบข้อเสนอด้วยอัตราที่แท้จริง",
}
