"""Official documents the entries are based on (copies of the PDFs are kept in the git-ignored data/sec/)."""

from regulation.model import Source

# ---------- SEC: personnel ----------

PERSONNEL_RULE = Source(
    "ทลธ. 8/2557",
    {"en": "Rules on capital market personnel (consolidated version)",
     "th": "หลักเกณฑ์เกี่ยวกับบุคลากรในธุรกิจตลาดทุน (ฉบับประมวล)"},
    "https://publish.sec.or.th/nrs/6727p_r.pdf")
QUALIFICATION_TABLES = Source(
    "ทลธ. 22/2568",
    {"en": "Qualification tables for capital market personnel (attachment)",
     "th": "ตารางคุณสมบัติของบุคลากรในธุรกิจตลาดทุน (แนบท้ายประกาศ)"},
    "https://publish.sec.or.th/nrs/10750p_r.pdf")
RENEWAL_TABLE = Source(
    "ทลธ. 22/2568",
    {"en": "Qualification table for renewal (attachment)",
     "th": "ตารางคุณสมบัติของผู้ขอความเห็นชอบในการต่ออายุ (แนบท้ายประกาศ)"},
    "https://publish.sec.or.th/nrs/10751p_r.pdf")
RENEWAL_GUIDELINE = Source(
    "นป. 5/2568",
    {"en": "Guideline on renewing IC, IP and analyst approval",
     "th": "แนวทางปฏิบัติในการต่ออายุการให้ความเห็นชอบ IC IP และนักวิเคราะห์การลงทุน"},
    "https://publish.sec.or.th/nrs/10782p_r.pdf")
SCOPE_TABLE = Source(
    "ทลธ. 70/2561",
    {"en": "What each type of approval may do (attachment)",
     "th": "ประเภทธุรกรรมที่ผู้ได้รับความเห็นชอบแต่ละประเภทสามารถทำได้ (แนบท้ายประกาศ)"},
    "https://publish.sec.or.th/nrs/7889p_r.pdf")
IC_SUMMARY = Source(
    "SEC website",
    {"en": "IC / IP rules summary page", "th": "หน้าสรุปหลักเกณฑ์ IC / IP"},
    "https://www.sec.or.th/TH/Pages/LawandRegulations/InvestmentConsultantSummary.aspx")
LAPSED_GUIDE = Source(
    "SEC guide",
    {"en": "How to re-apply when an IC/IP approval expired within 5 years",
     "th": "วิธีขอความเห็นชอบสำหรับ IC/IP ที่ใบอนุญาตขาดอายุไม่เกิน 5 ปี"},
    "https://www.sec.or.th/TH/Documents/InvestmentConsultant/5year.pdf")
CHECK_FIRST = Source(
    "SEC Check First",
    {"en": "Search licensed people and firms", "th": "ค้นหาบุคคลและผู้ประกอบธุรกิจที่ได้รับอนุญาต"},
    "https://market.sec.or.th/LicenseCheck/Search")

# ---------- SEC: conduct with clients ----------

DUTY_GUIDELINE = Source(
    "นป. 3/2562",
    {"en": "Guideline on how capital market personnel must perform their duties",
     "th": "แนวทางในการปฏิบัติหน้าที่ของบุคลากรในธุรกิจตลาดทุน"},
    "https://publish.sec.or.th/nrs/8027p_r.pdf")
DO_DONT = Source(
    "SEC checklist",
    {"en": "Do & Don't checklist for investment consultants (Nov 2013)",
     "th": "ข้อปฏิบัติที่พึงกระทำและไม่พึงกระทำของผู้แนะนำการลงทุน (พ.ย. 2556)"},
    "https://www.sec.or.th/TH/Documents/InvestmentConsultant/do_dont.pdf")
SALES_CIRCULAR = Source(
    "นจ.(ว) 17/2560",
    {"en": "Circular on the sales process and types of sellers",
     "th": "หนังสือเวียนเรื่องกระบวนการขายผลิตภัณฑ์ในตลาดทุนและประเภทคนขาย"},
    "https://publish.sec.or.th/nrs/7407s.pdf")

# ---------- SEC: penalties ----------

PENALTY_CIRCULAR = Source(
    "กธ.(ว) 3/2561",
    {"en": "Circular on penalty levels for capital market personnel",
     "th": "หนังสือเวียนเรื่องหลักเกณฑ์และแนวปฏิบัติในการพิจารณาลงโทษทางปกครองกับบุคลากรในธุรกิจตลาดทุน"},
    "https://publish.sec.or.th/nrs/7598s.pdf")
IC_PENALTY_2556 = Source(
    "บธ.(ว) 44/2556",
    {"en": "Circular raising penalties for investment consultants",
     "th": "หนังสือเวียนเรื่องปรับปรุงหลักเกณฑ์การพิจารณาลงโทษผู้แนะนำการลงทุน"},
    "https://www.sec.or.th/TH/Documents/InvestmentConsultant/Rulesor.pdf")
