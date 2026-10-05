"""Topic A – Licences & career path (SEC Thailand).

Summarised in my own words from SEC documents read on 2026-10-04/05 (copies kept in the git-ignored
data/sec/ folder). The linked official documents are what counts.
"""

from regulation.model import Entry, Source

CHECKED = "2026-10-05"

# ---------- sources ----------

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
SALES_CIRCULAR = Source(
    "นจ.(ว) 17/2560",
    {"en": "Circular on the sales process and types of sellers",
     "th": "หนังสือเวียนเรื่องกระบวนการขายผลิตภัณฑ์ในตลาดทุนและประเภทคนขาย"},
    "https://publish.sec.or.th/nrs/7407s.pdf")
CHECK_FIRST = Source(
    "SEC Check First",
    {"en": "Search licensed people and firms", "th": "ค้นหาบุคคลและผู้ประกอบธุรกิจที่ได้รับอนุญาต"},
    "https://market.sec.or.th/LicenseCheck/Search")

# ---------- tables shown on the page ----------

# What each licence may advise on (SCOPE_TABLE). Columns: non-complex products, high-risk/complex bonds
# and funds, derivatives, investment planning (asset allocation).
SCOPE_COLUMNS = [
    {"en": "Non-complex products", "th": "ผลิตภัณฑ์ที่ไม่ซับซ้อน"},
    {"en": "High-risk / complex bonds & funds", "th": "ตราสารหนี้และกองทุนที่มีความเสี่ยงสูง/ซับซ้อน"},
    {"en": "Derivatives", "th": "สัญญาซื้อขายล่วงหน้า"},
    {"en": "Investment planning (asset allocation)", "th": "วางแผนการลงทุน (asset allocation)"},
]
LICENCE_SCOPE = [
    ({"en": "Investment planner (IP)", "th": "ผู้วางแผนการลงทุน (IP)"}, (True, True, True, True)),
    ({"en": "IC complex type 1", "th": "IC ตราสารซับซ้อนประเภท 1"}, (True, True, True, False)),
    ({"en": "IC complex type 2", "th": "IC ตราสารซับซ้อนประเภท 2"}, (True, True, False, False)),
    ({"en": "IC complex type 3", "th": "IC ตราสารซับซ้อนประเภท 3"}, (True, False, True, False)),
    ({"en": "IC plain", "th": "IC ตราสารทั่วไป"}, (True, False, False, False)),
]

# Routes to becoming an IP (QUALIFICATION_TABLES pages 16-17): what you have -> what you still need.
IP_ROUTES = [
    ({"en": "AFPT (CFP modules 1–2, accepted curriculum)", "th": "AFPT (ชุดวิชาที่ 1–2 หลักสูตรที่สำนักงานยอมรับ)"},
     {"en": "Nothing more – no further SEC exams", "th": "ไม่ต้องสอบเพิ่ม"}),
    ({"en": "CFP, curriculum that includes derivatives", "th": "CFP หลักสูตรที่ปรับปรุงเพิ่มความรู้สัญญาซื้อขายล่วงหน้าแล้ว"},
     {"en": "Pass the rules & suitable advice paper", "th": "สอบผ่านกฎระเบียบที่เกี่ยวข้องและการให้คำแนะนำที่เหมาะสม"}),
    ({"en": "CFP, older curriculum without derivatives", "th": "CFP หลักสูตรเดิมที่ยังไม่มีความรู้สัญญาซื้อขายล่วงหน้า"},
     {"en": "Rules & suitable advice paper + derivatives training (no exam)",
      "th": "สอบกฎระเบียบฯ + อบรมความรู้สัญญาซื้อขายล่วงหน้า (ไม่ต้องสอบ)"}),
    ({"en": "Qualified as IC complex type 1 or capital market analyst",
      "th": "มีคุณสมบัติเป็น IC ตราสารซับซ้อนประเภท 1 หรือนักวิเคราะห์ด้านตลาดทุน"},
     {"en": "Pass CFP modules 1 and 2 (investment planning)", "th": "สอบผ่าน CFP ชุดวิชาที่ 1 และ 2 (การวางแผนการลงทุน)"}),
    ({"en": "CISA level 3 or CFA level 3", "th": "CISA ระดับสาม หรือ CFA ระดับสาม"},
     {"en": "Rules & suitable advice paper (not needed with CISA level 3)",
      "th": "สอบกฎระเบียบฯ (ยกเว้นผู้ผ่าน CISA ระดับสาม)"}),
    ({"en": "Approved as a planner by an accepted foreign regulator",
      "th": "ได้รับความเห็นชอบเป็นผู้วางแผนการลงทุนจากหน่วยงานกำกับต่างประเทศที่สำนักงานยอมรับ"},
     {"en": "Pass the rules & suitable advice paper", "th": "สอบผ่านกฎระเบียบฯ"}),
    ({"en": "None of the above", "th": "ไม่มีคุณสมบัติข้างต้น"},
     {"en": "Pass P1 + P2 + P3 and CFP modules 1 and 2", "th": "สอบผ่าน P1 + P2 + P3 และ CFP ชุดวิชาที่ 1 และ 2"}),
]

# ---------- entries ----------

ENTRIES = [
    Entry(
        "A01", "A",
        {"en": "IC, IP and analyst – what each one is", "th": "IC, IP และนักวิเคราะห์ – แต่ละแบบคืออะไร"},
        {"en": "The SEC approves three kinds of people who advise investors. Only the investment planner may "
               "use a client's full information to build a personal plan.",
         "th": "ก.ล.ต. ให้ความเห็นชอบบุคคลที่ให้คำแนะนำผู้ลงทุน 3 แบบ มีเพียงผู้วางแผนการลงทุนที่ใช้ข้อมูลลูกค้า"
               "เชิงลึกมาวางแผนเฉพาะรายได้"},
        (
            {"en": "Investment consultant (IC, ผู้แนะนำการลงทุน): contacts investors and recommends products, "
                   "without investment planning or analysis behind the advice.",
             "th": "ผู้แนะนำการลงทุน (IC): ติดต่อชักชวนและแนะนำการซื้อขายผลิตภัณฑ์ โดยไม่มีการวางแผนหรือการวิเคราะห์"
                   "การลงทุนประกอบคำแนะนำ"},
            {"en": "IC plain may only advise on non-complex products. IC complex adds high-risk/complex products: "
                   "type 1 all of them, type 2 only complex funds and bonds, type 3 only derivatives.",
             "th": "IC ตราสารทั่วไปแนะนำได้เฉพาะผลิตภัณฑ์ที่ไม่ซับซ้อน IC ตราสารซับซ้อนแนะนำผลิตภัณฑ์เสี่ยงสูง/ซับซ้อน"
                   "ได้เพิ่ม: ประเภท 1 ได้ทุกประเภท ประเภท 2 เฉพาะกองทุนและตราสารหนี้ ประเภท 3 เฉพาะสัญญาซื้อขายล่วงหน้า"},
            {"en": "Investment planner (IP, ผู้วางแผนการลงทุน): uses each client's information in depth to plan "
                   "and give specific advice that fits their risk tolerance and goals.",
             "th": "ผู้วางแผนการลงทุน (IP): ใช้ข้อมูลของลูกค้าแต่ละรายเชิงลึกมาวางแผนและให้คำแนะนำแบบเฉพาะเจาะจง "
                   "ให้สอดคล้องกับความเสี่ยงที่รับได้และวัตถุประสงค์การลงทุน"},
            {"en": "Investment analyst: analyses the value or suitability of products (fundamental or technical) "
                   "and advises on them.",
             "th": "นักวิเคราะห์การลงทุน: วิเคราะห์คุณค่าหรือความเหมาะสมของผลิตภัณฑ์ (ปัจจัยพื้นฐานหรือเทคนิค) "
                   "และให้คำแนะนำ"},
        ),
        (PERSONNEL_RULE,), "2019-01-01", CHECKED, ("ic", "ip", "analyst"), (1, 2),
        ("definition", "นิยาม", "plain", "complex"),
    ),
    Entry(
        "A02", "A",
        {"en": "What each licence may advise on", "th": "ใบอนุญาตแต่ละแบบแนะนำอะไรได้บ้าง"},
        {"en": "The licence decides which products you may recommend. Only the IP may do investment planning "
               "(asset allocation) – the closest licence to CFP work.",
         "th": "ประเภทใบอนุญาตกำหนดว่าแนะนำผลิตภัณฑ์ใดได้ มีเพียง IP ที่วางแผนการลงทุน (asset allocation) ได้ "
               "ซึ่งใกล้เคียงงานนักวางแผนการเงิน CFP ที่สุด"},
        (
            {"en": "See the table “What each licence may advise on” on this page.",
             "th": "ดูตาราง “ใบอนุญาตแต่ละแบบแนะนำอะไรได้บ้าง” ในหน้านี้"},
            {"en": "Advising outside your licence's scope is not allowed – a type 2 IC may not recommend "
                   "derivatives, for example.",
             "th": "ห้ามแนะนำเกินขอบเขตใบอนุญาต เช่น IC ตราสารซับซ้อนประเภท 2 แนะนำสัญญาซื้อขายล่วงหน้าไม่ได้"},
        ),
        (SCOPE_TABLE, PERSONNEL_RULE), "2019-01-01", CHECKED, ("ic", "ip"), (1, 2),
        ("scope", "ขอบเขต", "derivatives", "asset allocation"),
    ),
    Entry(
        "A03", "A",
        {"en": "You need SEC approval before you start – through a licensed firm",
         "th": "ต้องได้รับความเห็นชอบจาก ก.ล.ต. ก่อนเริ่มงาน – ผ่านผู้ประกอบธุรกิจที่ได้รับอนุญาต"},
        {"en": "Anyone who analyses, recommends or plans investments for clients must be qualified, free of "
               "disqualifications and approved by the SEC before working, and is appointed by a licensed firm.",
         "th": "ผู้ที่วิเคราะห์ แนะนำ หรือวางแผนการลงทุนให้ลูกค้า ต้องมีคุณสมบัติ ไม่มีลักษณะต้องห้าม และได้รับ"
               "ความเห็นชอบจาก ก.ล.ต. ก่อนปฏิบัติงาน โดยได้รับการแต่งตั้งจากผู้ประกอบธุรกิจ"},
        (
            {"en": "The firm (securities company, bank, asset manager…) appoints you and must report the "
                   "appointment and its end to the SEC within 7 business days.",
             "th": "ผู้ประกอบธุรกิจ (บริษัทหลักทรัพย์ ธนาคาร บลจ. ฯลฯ) เป็นผู้แต่งตั้ง และต้องรายงานการแต่งตั้งและ"
                   "การสิ้นสุดต่อ ก.ล.ต. ภายใน 7 วันทำการ"},
            {"en": "A CFP certificate on its own is not an SEC approval: to advise on capital market products "
                   "you still need IC or IP approval.",
             "th": "วุฒิบัตร CFP อย่างเดียวไม่ใช่ความเห็นชอบจาก ก.ล.ต. ถ้าจะแนะนำผลิตภัณฑ์ในตลาดทุนต้องได้รับความเห็นชอบ"
                   "เป็น IC หรือ IP ด้วย"},
        ),
        (PERSONNEL_RULE,), "2015-12-16", CHECKED, ("ic", "ip", "analyst", "firm"), (1, 2),
        ("appointment", "แต่งตั้ง", "approval", "ความเห็นชอบ"),
    ),
    Entry(
        "A04", "A",
        {"en": "Which exam papers each licence needs", "th": "ใบอนุญาตแต่ละแบบต้องสอบ paper ใดบ้าง"},
        {"en": "The SEC licence exams are split into papers P1, P2 and P3; each licence needs a different set.",
         "th": "ข้อสอบขอความเห็นชอบแบ่งเป็น P1, P2 และ P3 ใบอนุญาตแต่ละแบบใช้ชุดต่างกัน"},
        (
            {"en": "IC plain: P1. IC complex type 2: P1 + P2. IC complex type 3: P1 + P3. "
                   "IC complex type 1: P1 + P2 + P3.",
             "th": "IC ตราสารทั่วไป: P1 · IC ตราสารซับซ้อนประเภท 2: P1 + P2 · ประเภท 3: P1 + P3 · "
                   "ประเภท 1: P1 + P2 + P3"},
            {"en": "IP: P1 + P2 + P3 plus CFP modules 1 and 2 – unless a CFP/AFPT route applies (see “Routes to "
                   "becoming an IP”).",
             "th": "IP: P1 + P2 + P3 และ CFP ชุดวิชาที่ 1 และ 2 เว้นแต่ใช้เส้นทาง CFP/AFPT (ดู “เส้นทางสู่การเป็น IP”)"},
            {"en": "Exam results must be no more than 2 years old on the day you apply (the CFP module 1–2 "
                   "results used for IP planning knowledge are exempt from this limit).",
             "th": "ผลสอบต้องไม่เกิน 2 ปีในวันที่ยื่นคำขอ (ยกเว้นผลสอบ CFP ชุดวิชาที่ 1–2 ที่ใช้เป็นความรู้ด้านการวางแผน"
                   "สำหรับ IP)"},
        ),
        (LAPSED_GUIDE, QUALIFICATION_TABLES), "2025-07-01", CHECKED, ("ic", "ip"), (1, 2),
        ("exam", "สอบ", "P1", "P2", "P3"),
    ),
    Entry(
        "A05", "A",
        {"en": "Routes to becoming an IP with CFP or AFPT", "th": "เส้นทางสู่การเป็น IP ด้วย CFP หรือ AFPT"},
        {"en": "Your CFP studies count: with AFPT you need no further SEC exams, and with CFP you only pass "
               "the rules & suitable advice paper.",
         "th": "การเรียน CFP นำมาใช้ได้: ผ่าน AFPT ไม่ต้องสอบเพิ่ม ผ่าน CFP สอบเพิ่มเฉพาะกฎระเบียบที่เกี่ยวข้องและ"
               "การให้คำแนะนำที่เหมาะสม"},
        (
            {"en": "See the table “Routes to becoming an IP” on this page.",
             "th": "ดูตาราง “เส้นทางสู่การเป็น IP” ในหน้านี้"},
            {"en": "IP knowledge has 4 parts: foundation, rules & suitable advice, non-complex and complex products, "
                   "and investment planning (CFP modules 1 and 2).",
             "th": "ความรู้ของ IP มี 4 ส่วน: ความรู้พื้นฐาน กฎระเบียบและการให้คำแนะนำที่เหมาะสม ผลิตภัณฑ์ที่ไม่ซับซ้อนและ"
                   "ซับซ้อน และการวางแผนการลงทุน (CFP ชุดวิชาที่ 1 และ 2)"},
        ),
        (QUALIFICATION_TABLES,), "2025-07-01", CHECKED, ("ip",), (1, 2),
        ("CFP", "AFPT", "route", "เส้นทาง"),
    ),
    Entry(
        "A06", "A",
        {"en": "Using CFP, AFPT, CISA, CFA or FRM to become an IC", "th": "ใช้ CFP, AFPT, CISA, CFA หรือ FRM ขอเป็น IC"},
        {"en": "Passed results of CISA level 1+, CFA level 1+, FRM, CFP or AFPT can be used to apply as an IC "
               "(plain or complex, depending on the qualification).",
         "th": "ผลสอบผ่าน CISA ระดับ 1 ขึ้นไป CFA ระดับ 1 ขึ้นไป FRM, CFP หรือ AFPT ใช้ขอความเห็นชอบเป็น IC ได้ "
               "(ตราสารทั่วไปหรือซับซ้อน แล้วแต่คุณสมบัติ)"},
        (
            {"en": "With a foreign CFA, FRM or CFP you must also pass the Thai rules & suitable advice exam, "
                   "with a result no more than 2 years old.",
             "th": "ถ้าใช้ CFA, FRM หรือ CFP ของต่างประเทศ ต้องสอบผ่านกฎระเบียบที่เกี่ยวข้องและการให้คำแนะนำที่เหมาะสม"
                   "ของไทยด้วย (ผลสอบไม่เกิน 2 ปี)"},
            {"en": "Which IC type each qualification gives is in the qualification tables (pages 38–53).",
             "th": "IC ประเภทใดที่แต่ละคุณวุฒิขอได้ ดูตารางคุณสมบัติ (หน้า 38–53)"},
        ),
        (IC_SUMMARY, QUALIFICATION_TABLES), "2025-07-01", CHECKED, ("ic",), (1, 2),
        ("CISA", "CFA", "FRM", "foreign", "ต่างประเทศ"),
    ),
    Entry(
        "A07", "A",
        {"en": "How long approval lasts and when to renew", "th": "ความเห็นชอบมีอายุเท่าไร และต่ออายุเมื่อไร"},
        {"en": "IC, IP and analyst approval lasts 2 calendar years. Apply to renew between 1 September and the "
               "SEC's last working day of the year it expires – otherwise it ends.",
         "th": "ความเห็นชอบเป็น IC, IP และนักวิเคราะห์มีอายุ 2 ปีปฏิทิน ยื่นต่ออายุได้ตั้งแต่ 1 กันยายน ถึงวันทำการ"
               "สุดท้ายของสำนักงานในปีที่ครบอายุ ถ้าไม่ต่ออายุจะสิ้นสุดลง"},
        (
            {"en": "The first approval starts on the approval date, but the 2 years are counted from 1 January of "
                   "the following year.",
             "th": "ความเห็นชอบครั้งแรกมีผลตั้งแต่วันที่ได้รับ แต่นับระยะเวลา 2 ปีตั้งแต่ 1 มกราคมของปีถัดไป"},
            {"en": "If you get a broader approval later (e.g. IC then IP), the old one ends when the new one "
                   "starts; otherwise all your approvals end together with the latest one.",
             "th": "ถ้าได้รับความเห็นชอบที่มีขอบเขตกว้างกว่าในภายหลัง (เช่น จาก IC เป็น IP) ความเห็นชอบเดิมสิ้นสุดเมื่อ"
                   "แบบใหม่มีผล กรณีอื่นทุกประเภทสิ้นสุดพร้อมกับความเห็นชอบครั้งล่าสุด"},
        ),
        (PERSONNEL_RULE,), "2024-09-01", CHECKED, ("ic", "ip", "analyst"), (1,),
        ("renew", "ต่ออายุ", "expire", "หมดอายุ"),
    ),
    Entry(
        "A08", "A",
        {"en": "Renewal training: 15 hours every 2 years", "th": "อบรมเพื่อต่ออายุ: 15 ชั่วโมงทุก 2 ปี"},
        {"en": "To renew as IC or IP you need at least 15 hours of training or activities in the last 2 calendar "
               "years, including at least 3 hours on rules, ethics or law and at least 3 hours on ESG.",
         "th": "การต่ออายุ IC หรือ IP ต้องผ่านการอบรมหรือร่วมกิจกรรมไม่น้อยกว่า 15 ชั่วโมงในรอบ 2 ปีปฏิทินล่าสุด "
               "โดยเป็นกฎระเบียบ จรรยาบรรณ หรือกฎหมายอย่างน้อย 3 ชั่วโมง และ ESG อย่างน้อย 3 ชั่วโมง"},
        (
            {"en": "Which courses count is set by the SEC renewal guideline.",
             "th": "หลักสูตรที่นับได้เป็นไปตามแนวทางปฏิบัติในการต่ออายุของ ก.ล.ต."},
            {"en": "No training needed if you were approved as a firm's manager or are on the fund manager "
                   "register, while you still hold that status.",
             "th": "ไม่ต้องอบรมถ้าได้รับความเห็นชอบด้วยคุณสมบัติผู้จัดการของบริษัท หรือมีชื่อในทะเบียนผู้จัดการกองทุน "
                   "ขณะที่ยังดำรงสถานะนั้น"},
            {"en": "Approved through a foreign regulator: 3 hours of rules/ethics + 3 hours of ESG while still "
                   "licensed abroad, otherwise the full 15 hours.",
             "th": "ได้รับความเห็นชอบด้วยคุณสมบัติจากหน่วยงานกำกับต่างประเทศ: อบรมกฎระเบียบ/จรรยาบรรณ 3 ชั่วโมง + "
                   "ESG 3 ชั่วโมง ขณะยังมีสถานะในต่างประเทศ ไม่เช่นนั้นต้องครบ 15 ชั่วโมง"},
        ),
        (RENEWAL_TABLE, RENEWAL_GUIDELINE), "2025-07-01", CHECKED, ("ic", "ip"), (1,),
        ("CPD", "ESG", "training", "อบรม", "refresher"),
    ),
    Entry(
        "A09", "A",
        {"en": "Approval expired less than 5 years ago", "th": "ความเห็นชอบขาดอายุไม่เกิน 5 ปี"},
        {"en": "If your IC/IP approval expired within the last 5 years you can come back without new exams by "
               "taking a 15-hour refresher course or a 30-hour full course.",
         "th": "ถ้า IC/IP ขาดอายุไม่เกิน 5 ปี ขอความเห็นชอบใหม่ได้โดยไม่ต้องสอบ เพียงอบรม Refresher Course 15 ชั่วโมง "
               "หรือ Full Course 30 ชั่วโมง"},
        (
            {"en": "Steps: check eligibility in the SEC ORAP system (menu P2, answer within 5 business days), "
                   "apply in menu P1 and pay the 2,140 THB fee, then look for your name on SEC Check First after "
                   "5 business days.",
             "th": "ขั้นตอน: ตรวจสอบเบื้องต้นในระบบ ORAP (เมนู P2 แจ้งผลใน 5 วันทำการ) ยื่นคำขอในเมนู P1 และชำระ"
                   "ค่าธรรมเนียม 2,140 บาท แล้วตรวจรายชื่อใน SEC Check First หลังจาก 5 วันทำการ"},
            {"en": "The full course must be no more than 2 years old when you apply; course codes must not repeat.",
             "th": "Full Course ต้องอบรมมาไม่เกิน 2 ปีในวันที่ยื่นคำขอ และรหัสหลักสูตรที่อบรมต้องไม่ซ้ำกัน"},
            {"en": "Instead of training you may re-take the exams for your licence type (an IP may reuse "
                   "CFP 1 and CFP 2 results).",
             "th": "หรือเลือกสอบใหม่ตามประเภทใบอนุญาตแทนการอบรม (IP ใช้ผลสอบ CFP1 และ CFP2 เดิมได้)"},
        ),
        (LAPSED_GUIDE, QUALIFICATION_TABLES), "2025-07-01", CHECKED, ("ic", "ip"), (1,),
        ("ORAP", "reinstate", "full course", "refresher", "ขาดอายุ"),
    ),
    Entry(
        "A10", "A",
        {"en": "Coming back after suspension or revocation", "th": "การกลับมาหลังถูกสั่งพักหรือเพิกถอน"},
        {"en": "After a suspension ends, an IP only passes the rules exam again. After a revocation you start "
               "over like a new applicant – all exams again, including ethics.",
         "th": "เมื่อพ้นระยะเวลาสั่งพัก IP สอบเฉพาะกฎระเบียบที่เกี่ยวข้อง ถ้าถูกเพิกถอนต้องมีคุณสมบัติเหมือนผู้ยื่นครั้งแรก "
               "สอบใหม่ทุกส่วนรวมถึงจรรยาบรรณ"},
        (
            {"en": "This is from the IP table; other licence types have similar rows in their own tables.",
             "th": "ข้อมูลนี้มาจากตารางของ IP ใบอนุญาตประเภทอื่นมีหัวข้อทำนองเดียวกันในตารางของตน"},
        ),
        (QUALIFICATION_TABLES,), "2025-07-01", CHECKED, ("ip",), (1,),
        ("suspend", "revoke", "พัก", "เพิกถอน"),
    ),
    Entry(
        "A11", "A",
        {"en": "What disqualifies you", "th": "ลักษณะต้องห้าม"},
        {"en": "You cannot be (or stay) approved while a disqualification applies. The SEC groups them into "
               "3 groups; groups 1 and 2 are listed here, group 3 (improper behaviour) is under Penalties.",
         "th": "ผู้มีลักษณะต้องห้ามได้รับหรือคงความเห็นชอบไม่ได้ ก.ล.ต. แบ่งเป็น 3 กลุ่ม กลุ่มที่ 1 และ 2 อยู่ด้านล่าง "
               "กลุ่มที่ 3 (พฤติกรรมไม่เหมาะสม) อยู่ในหัวข้อบทลงโทษ"},
        (
            {"en": "Group 1: bankrupt or under receivership; legally incompetent; charged by the SEC or being "
                   "prosecuted after an SEC complaint; jailed for listed securities/derivatives/trust fraud offences "
                   "less than 3 years ago.",
             "th": "กลุ่มที่ 1: ถูกพิทักษ์ทรัพย์หรือล้มละลาย ไร้ความสามารถหรือเสมือนไร้ความสามารถ อยู่ระหว่างถูก ก.ล.ต. "
                   "กล่าวโทษหรือถูกดำเนินคดีจากการกล่าวโทษ หรือต้องคำพิพากษาให้จำคุกในความผิดตามที่กำหนดและพ้นโทษยังไม่ถึง 3 ปี"},
            {"en": "Group 2: jailed for fraud or dishonesty involving property less than 3 years ago; assets "
                   "seized under anti-corruption or anti-money-laundering law less than 3 years ago; barred by a "
                   "Thai or foreign financial regulator for fraud or law-breaking management.",
             "th": "กลุ่มที่ 2: ต้องคำพิพากษาให้จำคุกในความผิดเกี่ยวกับการหลอกลวง ฉ้อโกง หรือทุจริตเกี่ยวกับทรัพย์สิน"
                   "และพ้นโทษไม่ถึง 3 ปี ถูกศาลสั่งให้ทรัพย์สินตกเป็นของแผ่นดินตามกฎหมายป้องกันทุจริตหรือฟอกเงินไม่ถึง 3 ปี "
                   "หรือถูกห้ามดำรงตำแหน่งโดยหน่วยงานกำกับสถาบันการเงินไทยหรือต่างประเทศ"},
            {"en": "If a disqualification appears after approval, the approval can end and the firm must report "
                   "it to the SEC within 7 business days.",
             "th": "ถ้ามีลักษณะต้องห้ามภายหลังได้รับความเห็นชอบ ความเห็นชอบอาจสิ้นสุดลง และผู้ประกอบธุรกิจต้องรายงาน "
                   "ก.ล.ต. ภายใน 7 วันทำการ"},
        ),
        (PERSONNEL_RULE,), "2017-10-01", CHECKED, ("ic", "ip", "analyst", "fund_manager", "firm"), (1,),
        ("bankrupt", "ล้มละลาย", "fraud", "ฉ้อโกง", "money laundering", "ฟอกเงิน"),
    ),
    Entry(
        "A12", "A",
        {"en": "Your four core duties", "th": "หน้าที่หลัก 4 ข้อ"},
        {"en": "Every approved person must work honestly, with professional care and the investor's interest "
               "first, and within the law and the professional code.",
         "th": "บุคลากรที่ได้รับความเห็นชอบทุกคนต้องปฏิบัติหน้าที่ด้วยความซื่อสัตย์สุจริต รอบคอบเยี่ยงผู้ประกอบวิชาชีพ "
               "คำนึงถึงประโยชน์ของผู้ลงทุนเป็นสำคัญ และเป็นไปตามกฎหมายและจรรยาบรรณ"},
        (
            {"en": "1. Act honestly.", "th": "1. ปฏิบัติหน้าที่ด้วยความซื่อสัตย์สุจริต"},
            {"en": "2. Act with professional responsibility and care, treat every investor fairly and put the "
                   "investor's interest first.",
             "th": "2. รับผิดชอบและรอบคอบเยี่ยงผู้ประกอบวิชาชีพ ปฏิบัติต่อผู้ลงทุนทุกรายอย่างเป็นธรรม โดยคำนึงถึงประโยชน์"
                   "ของผู้ลงทุนเป็นสำคัญ"},
            {"en": "3. Follow the Securities and Exchange Act, the Derivatives Act and the rules made under them.",
             "th": "3. ปฏิบัติตาม พ.ร.บ. หลักทรัพย์ฯ พ.ร.บ. สัญญาซื้อขายล่วงหน้าฯ และประกาศที่เกี่ยวข้อง"},
            {"en": "4. Follow the ethics and professional standards set by the SEC or accepted associations.",
             "th": "4. ปฏิบัติตามจรรยาบรรณและมาตรฐานวิชาชีพที่ ก.ล.ต. หรือสมาคมที่สำนักงานยอมรับกำหนด"},
            {"en": "Breaking these is handled under the penalty rules (group 3 disqualification).",
             "th": "การฝ่าฝืนจะพิจารณาตามหลักเกณฑ์ลักษณะต้องห้ามกลุ่มที่ 3 (ดูหัวข้อบทลงโทษ)"},
        ),
        (PERSONNEL_RULE,), "2017-10-01", CHECKED, ("ic", "ip", "analyst", "fund_manager"), (1,),
        ("duty", "หน้าที่", "honest", "ซื่อสัตย์", "fiduciary"),
    ),
    Entry(
        "A13", "A",
        {"en": "Working across borders: foreign licences and ASEAN", "th": "ทำงานข้ามประเทศ: ใบอนุญาตต่างประเทศและอาเซียน"},
        {"en": "People approved by an accepted foreign regulator can apply in Thailand, and ASEAN professionals "
               "can give general advice under the ASEAN mobility scheme.",
         "th": "ผู้ได้รับความเห็นชอบจากหน่วยงานกำกับต่างประเทศที่สำนักงานยอมรับ ขอความเห็นชอบในไทยได้ และบุคลากร"
               "จากอาเซียนให้คำแนะนำทั่วไปได้ภายใต้โครงการ ASEAN mobility"},
        (
            {"en": "Foreign approval: show it is still valid and what it allows, and that you are fit and proper "
                   "under that country's rules; an IP also passes the Thai rules exam.",
             "th": "ใช้คุณสมบัติจากต่างประเทศ: แสดงว่ายังมีสถานะและขอบเขตงานเทียบได้ และมีสถานะ fit and proper "
                   "ตามเกณฑ์ประเทศนั้น สำหรับ IP ต้องสอบกฎระเบียบของไทยด้วย"},
            {"en": "ASEAN investment consultant: general advice only (not tailored to a person) and no "
                   "soliciting, on ASEAN-listed shares and non-complex ASEAN funds and bonds. It ends when the home "
                   "country registration ends.",
             "th": "ผู้แนะนำการลงทุนอาเซียน: ให้คำแนะนำทั่วไปเท่านั้น (ไม่พิจารณาเฉพาะบุคคล) และห้ามติดต่อชักชวน "
                   "ในหุ้นจดทะเบียนตลาดอาเซียน กองทุนและตราสารหนี้อาเซียนที่ไม่ซับซ้อน สิ้นสุดเมื่อการขึ้นทะเบียนในประเทศต้นทางสิ้นสุด"},
            {"en": "For your “work around the world” plan: each country has its own licence – check that "
                   "country's regulator before you move.",
             "th": "สำหรับแผนทำงานต่างประเทศ: แต่ละประเทศมีใบอนุญาตของตนเอง ควรตรวจสอบหน่วยงานกำกับของประเทศนั้นก่อน"},
        ),
        (PERSONNEL_RULE, SALES_CIRCULAR, QUALIFICATION_TABLES), "2019-01-01", CHECKED, ("ic", "ip", "analyst"), (1,),
        ("ASEAN", "อาเซียน", "foreign", "ต่างประเทศ", "abroad"),
    ),
    Entry(
        "A14", "A",
        {"en": "Fund manager – a different track", "th": "ผู้จัดการกองทุน – อีกเส้นทางหนึ่ง"},
        {"en": "Fund managers are approved on CISA/CFA qualifications, not CFP. They must be 20 or older with a "
               "bachelor's degree.",
         "th": "ผู้จัดการกองทุนใช้คุณสมบัติ CISA/CFA ไม่ใช่ CFP ต้องอายุครบ 20 ปีและจบปริญญาตรี"},
        (
            {"en": "CISA or CFA level 1 (or AISA) plus at least 2 years of investment experience within the last "
                   "5 years – or CISA/CFA level 3 (or the new CISA level 2) without the experience.",
             "th": "CISA หรือ CFA ระดับหนึ่ง (หรือ AISA) และประสบการณ์ด้านการลงทุนอย่างน้อย 2 ปีในช่วง 5 ปี "
                   "หรือ CISA/CFA ระดับสาม (หรือ CISA ใหม่ระดับสอง) โดยไม่ต้องมีประสบการณ์"},
            {"en": "Plus exams on securities law, related rules, and ethics & professional standards.",
             "th": "และสอบผ่านความรู้กฎหมายหลักทรัพย์ กฎระเบียบที่เกี่ยวข้อง และจรรยาบรรณและมาตรฐานวิชาชีพ"},
            {"en": "Approval lasts 2 calendar years; renewal needs a refresher on law, rules, ethics and ESG.",
             "th": "ความเห็นชอบมีอายุ 2 ปีปฏิทิน การต่ออายุต้องอบรมทบทวนกฎหมาย กฎระเบียบ จรรยาบรรณ และ ESG"},
        ),
        (QUALIFICATION_TABLES, PERSONNEL_RULE, RENEWAL_TABLE), "2025-07-01", CHECKED, ("fund_manager",), (2,),
        ("CISA", "CFA", "AISA", "fund manager"),
    ),
    Entry(
        "A15", "A",
        {"en": "Check anyone's licence: SEC Check First", "th": "ตรวจสอบใบอนุญาต: SEC Check First"},
        {"en": "SEC Check First lists approved people (IC, IP, analysts, fund managers) and licensed firms. "
               "After your own approval, your name appears there.",
         "th": "SEC Check First แสดงรายชื่อบุคคลที่ได้รับความเห็นชอบ (IC, IP, นักวิเคราะห์ ผู้จัดการกองทุน) และ"
               "ผู้ประกอบธุรกิจที่ได้รับอนุญาต เมื่อได้รับความเห็นชอบแล้วจะมีชื่อของเราในระบบ"},
        (
            {"en": "Use it to check a colleague, an adviser a client mentions, or a firm before working with it.",
             "th": "ใช้ตรวจสอบเพื่อนร่วมงาน ผู้แนะนำที่ลูกค้าพูดถึง หรือบริษัทก่อนร่วมงาน"},
        ),
        (CHECK_FIRST, LAPSED_GUIDE), "", CHECKED, ("ic", "ip", "analyst", "fund_manager", "firm"), (1,),
        ("check", "ตรวจสอบ", "license", "licence"),
    ),
]
