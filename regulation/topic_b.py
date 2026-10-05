"""Topic B – Conduct with clients (SEC Thailand).

Summarised in my own words from the SEC duty guideline นป. 3/2562, the IC Do & Don't checklist and the
sales-process circular นจ.(ว) 17/2560, read on 2026-10-05 (copies kept in the git-ignored data/sec/).
The linked official documents are what counts.
"""

from regulation.model import Entry
from regulation.sources import DO_DONT, DUTY_GUIDELINE, PERSONNEL_RULE, SALES_CIRCULAR

CHECKED = "2026-10-05"
GUIDE_SINCE = "2019-04-01"  # นป. 3/2562 was issued on 1 April 2019
SALES_SINCE = "2017-02-16"  # the sales-process notifications took effect on 16 Feb 2017

ADVISERS = ("ic", "ip")

ENTRIES = [
    Entry(
        "B01", "B",
        {"en": "Know your client before anything else (KYC/CDD)", "th": "รู้จักลูกค้าก่อนทุกอย่าง (KYC/CDD)"},
        {"en": "Identify the client and the real owner of the money completely, and do the suitability test "
               "before giving advice.",
         "th": "ทำความรู้จักและระบุตัวตนลูกค้ารวมถึงผู้รับประโยชน์ที่แท้จริงให้ครบถ้วน และทำแบบประเมินความเหมาะสม"
               "ก่อนให้คำแนะนำ"},
        (
            {"en": "Do KYC/CDD fully; if anything looks unusual or suspicious, do enhanced KYC/CDD without delay.",
             "th": "ทำ KYC/CDD ให้ครบถ้วน ถ้าพบรายการผิดปกติหรือมีเหตุสงสัย ต้องทำ enhanced KYC/CDD โดยไม่ชักช้า"},
            {"en": "Account opening: introduce yourself (licence number or staff card), get complete, current "
                   "documents, have the client sign in front of you, and explain that you advise – you do not "
                   "manage their portfolio.",
             "th": "การเปิดบัญชี: แนะนำตัว (เลขทะเบียนหรือบัตรพนักงาน) ใช้เอกสารที่ครบถ้วนและเป็นปัจจุบัน ให้ลูกค้าลงนาม"
                   "ต่อหน้า และอธิบายว่าผู้แนะนำการลงทุนไม่มีหน้าที่บริหารพอร์ตให้ลูกค้า"},
            {"en": "Never: accept missing or expired documents, dress up a client's financial information, sign "
                   "for a client, let a client use your address, or ask for a higher credit limit the client did "
                   "not want.",
             "th": "ห้าม: รับเอกสารไม่ครบหรือหมดอายุ ตกแต่งข้อมูลทางการเงินของลูกค้า ลงนามแทนลูกค้า ให้ลูกค้าใช้ที่อยู่"
                   "ของตน หรือขอเพิ่มวงเงินโดยลูกค้าไม่ได้ต้องการ"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1, 2),
        ("KYC", "CDD", "account", "เปิดบัญชี", "beneficial owner"),
    ),
    Entry(
        "B02", "B",
        {"en": "Advice must follow the suitability test", "th": "คำแนะนำต้องสอดคล้องกับผลประเมินความเหมาะสม"},
        {"en": "Recommendations must match the client's suitability test result or a basic asset allocation – "
               "the SEC publishes a standard one firms may use.",
         "th": "คำแนะนำต้องสอดคล้องกับผล suitability test หรือ basic asset allocation ของลูกค้า ซึ่ง ก.ล.ต. "
               "มีแบบมาตรฐานให้ผู้ประกอบธุรกิจใช้ได้"},
        (
            {"en": "A low risk score does not ban every riskier product – riskier products should just be a "
                   "small share of the whole portfolio.",
             "th": "ผลประเมินความเสี่ยงต่ำไม่ได้แปลว่าห้ามลงทุนในผลิตภัณฑ์ที่เสี่ยงกว่าเลย แต่ควรมีสัดส่วนน้อยเมื่อเทียบ"
                   "กับพอร์ตทั้งหมด"},
            {"en": "SEC example – a moderately-high risk client: deposits and short-term debt under 10%, "
                   "government bonds over 1 year plus corporate bonds under 60%, equities under 30%, "
                   "alternatives under 10%; suitable funds are risk levels 1–5.",
             "th": "ตัวอย่างของ ก.ล.ต. – ลูกค้าเสี่ยงปานกลางค่อนข้างสูง: เงินฝากและตราสารหนี้ระยะสั้นไม่เกิน 10% "
                   "ตราสารหนี้ภาครัฐอายุเกิน 1 ปีรวมตราสารหนี้เอกชนไม่เกิน 60% ตราสารทุนไม่เกิน 30% การลงทุนทางเลือก"
                   "ไม่เกิน 10% กองทุนที่เหมาะสมคือระดับความเสี่ยง 1–5"},
            {"en": "Wealth management (advising on the whole portfolio) means monitoring the client's whole "
                   "position continuously, not just at the sale.",
             "th": "ถ้าให้บริการแบบ wealth management ต้องติดตามสถานะการลงทุนทั้งหมดของลูกค้าอย่างต่อเนื่อง ไม่ใช่"
                   "เฉพาะตอนขาย"},
        ),
        (SALES_CIRCULAR, DUTY_GUIDELINE), SALES_SINCE, CHECKED, ADVISERS, (1, 2),
        ("suitability", "asset allocation", "risk level", "ระดับความเสี่ยง", "ประเมินความเหมาะสม"),
    ),
    Entry(
        "B03", "B",
        {"en": "When the client wants something riskier (mismatch)", "th": "เมื่อลูกค้าต้องการลงทุนเสี่ยงกว่าที่รับได้ (mismatch)"},
        {"en": "A client may still invest beyond their risk profile, but you must make sure they understand the "
               "extra risk and keep a record.",
         "th": "ลูกค้ายังลงทุนเกินระดับความเสี่ยงที่รับได้ได้ แต่ต้องทำให้ลูกค้ารับทราบและตระหนักถึงความเสี่ยง และเก็บ"
               "หลักฐานไว้"},
        (
            {"en": "Example: a client fit for risk levels 1–5 who wants a level-6 equity fund (or more than 30% "
                   "in equities) must be warned so they can reconsider.",
             "th": "ตัวอย่าง: ลูกค้าที่เหมาะกับระดับความเสี่ยง 1–5 แต่ต้องการกองทุนหุ้นระดับ 6 (หรือหุ้นเกิน 30%) "
                   "ต้องได้รับคำเตือนเพื่อทบทวนการตัดสินใจ"},
            {"en": "How is up to the firm – e.g. the client signs an acknowledgement or the adviser explains the "
                   "risk – but keep evidence for supervision and complaints.",
             "th": "วิธีการขึ้นกับระบบของบริษัท เช่น ให้ลูกค้าลงนามรับทราบ หรือคนขายอธิบายความเสี่ยง แต่ต้องเก็บหลักฐาน"
                   "ไว้ใช้กำกับดูแลและกรณีร้องเรียน"},
        ),
        (SALES_CIRCULAR,), SALES_SINCE, CHECKED, ADVISERS, (1, 2),
        ("mismatch", "warning", "คำเตือน", "risk", "ความเสี่ยง"),
    ),
    Entry(
        "B04", "B",
        {"en": "Complex and high-risk products need extra steps", "th": "ผลิตภัณฑ์ซับซ้อนและเสี่ยงสูงต้องมีขั้นตอนเพิ่ม"},
        {"en": "Before selling a complex or high-risk product, assess the client's knowledge and make sure they "
               "receive and acknowledge its key risks before deciding.",
         "th": "ก่อนขายผลิตภัณฑ์ซับซ้อนหรือเสี่ยงสูง ต้องประเมินความรู้ความสามารถของลูกค้า และให้ลูกค้ารับทราบความเสี่ยง"
               "สำคัญก่อนตัดสินใจลงทุน"},
        (
            {"en": "Counted as complex/high-risk funds: funds using complex derivatives strategies or exotic "
                   "derivatives, and funds with more than 60% of NAV in non-investment-grade or unrated bonds.",
             "th": "กองทุนที่ถือว่าซับซ้อน/เสี่ยงสูง เช่น กองทุนที่ใช้กลยุทธ์อนุพันธ์ซับซ้อนหรือ exotic derivatives และ"
                   "กองทุนที่ลงทุนในตราสารหนี้ต่ำกว่าระดับลงทุนได้หรือไม่มีเรตติ้งเกิน 60% ของ NAV"},
            {"en": "Knowledge assessment: a client with relevant experience or education can get a technical "
                   "explanation; a client with none needs much more careful explanation.",
             "th": "การประเมินความรู้: ลูกค้าที่มีประสบการณ์หรือการศึกษาที่เกี่ยวข้องอธิบายด้วยศัพท์เทคนิคได้ ลูกค้าที่ไม่มี"
                   "ต้องอธิบายลักษณะและความเสี่ยงอย่างละเอียดมากขึ้น"},
            {"en": "Risk disclosure must be specific to that product, not a generic all-purpose document.",
             "th": "การเปิดเผยความเสี่ยงต้องเฉพาะเจาะจงกับผลิตภัณฑ์นั้น ไม่ใช่เอกสารมาตรฐานที่ใช้กับทุกผลิตภัณฑ์"},
        ),
        (SALES_CIRCULAR,), "2017-07-01", CHECKED, ADVISERS, (2,),
        ("complex", "ซับซ้อน", "knowledge assessment", "derivatives", "high yield"),
    ),
    Entry(
        "B05", "B",
        {"en": "How to give advice", "th": "วิธีให้คำแนะนำ"},
        {"en": "Say who you are, give neutral and well-supported advice, separate facts from opinions, and give "
               "complete, current information about the product and its risks.",
         "th": "แจ้งชื่อและบริษัทที่สังกัด ให้คำแนะนำอย่างเป็นกลางและมีเอกสารอ้างอิง แยกข้อเท็จจริงกับความเห็น และให้"
               "ข้อมูลผลิตภัณฑ์และความเสี่ยงที่ครบถ้วนเป็นปัจจุบัน"},
        (
            {"en": "Follow your firm's house view so the firm's advice is consistent.",
             "th": "ควรเป็นไปตามแนวทางของบริษัท (house opinion) เพื่อให้คำแนะนำไปในทางเดียวกัน"},
            {"en": "Point out special features and risks – e.g. warrants about to expire, a fund being merged, "
                   "term-fund conditions, dividends, tax, auto-redeem.",
             "th": "แจ้งลักษณะและความเสี่ยงเฉพาะ เช่น ใบสำคัญแสดงสิทธิใกล้หมดอายุ กองทุนที่อยู่ระหว่างควบรวม เงื่อนไขกองทุน"
                   "ที่มีกำหนดระยะเวลา เงินปันผล ภาษี และ auto redeem"},
            {"en": "Selling fund units: give the prospectus, advise on the client's updated profile, and keep "
                   "informing them after the sale (e.g. material events).",
             "th": "การขายหน่วยลงทุน: แจกหนังสือชี้ชวน ให้คำแนะนำตามข้อมูลลูกค้าที่เป็นปัจจุบัน และแจ้งข้อมูลสำคัญต่อเนื่อง"
                   "หลังการขาย (เช่น material event)"},
            {"en": "Cite the source of any news you use; never pass on rumours; never rush a client's decision.",
             "th": "แจ้งที่มาของข่าวที่ใช้ ห้ามเผยแพร่ข่าวลือ และห้ามเร่งรัดให้ลูกค้าตัดสินใจ"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1, 2),
        ("advice", "คำแนะนำ", "prospectus", "หนังสือชี้ชวน", "rumour", "ข่าวลือ"),
    ),
    Entry(
        "B06", "B",
        {"en": "Taking client orders", "th": "การรับคำสั่งซื้อขายจากลูกค้า"},
        {"en": "Take orders only from the account owner (or someone with written authority), through recorded "
               "channels, and never trade without the client's instruction.",
         "th": "รับคำสั่งจากเจ้าของบัญชีหรือผู้รับมอบอำนาจเป็นลายลักษณ์อักษรเท่านั้น ผ่านช่องทางที่มีการบันทึก และห้าม"
               "ซื้อขายโดยลูกค้าไม่ได้สั่ง"},
        (
            {"en": "Get clear details (product, price, amount), read the order back, and process orders in the "
                   "order they arrive.",
             "th": "รับคำสั่งที่มีรายละเอียดชัดเจน (ชื่อหลักทรัพย์ ราคา จำนวน) ทวนคำสั่ง และส่งคำสั่งตามลำดับก่อนหลัง"},
            {"en": "Never take orders on your own mobile phone, public e-mail or social media to avoid the "
                   "recorded line.",
             "th": "ห้ามรับคำสั่งทางโทรศัพท์มือถือส่วนตัว อีเมลสาธารณะ หรือ social media เพื่อหลีกเลี่ยงการบันทึกเทป"},
            {"en": "Never accept discretion to decide for the client, never trade first and tell them later – even "
                   "to make them a profit – and never change the price they asked for.",
             "th": "ห้ามรับมอบหมายให้ตัดสินใจแทนลูกค้า ห้ามซื้อขายก่อนแล้วแจ้งทีหลังแม้หวังทำกำไรให้ลูกค้า และห้ามเปลี่ยน"
                   "ราคาที่ลูกค้าสั่งเอง"},
            {"en": "Records must be true; never send manipulative orders, and stop or report anyone you suspect "
                   "is breaking securities law.",
             "th": "บันทึกการรับคำสั่งต้องตรงความจริง ห้ามส่งคำสั่งที่ไม่เหมาะสม และต้องยับยั้งหรือแจ้งเมื่อสงสัยว่ามีการ"
                   "ฝ่าฝืนกฎหมาย"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (2,),
        ("order", "คำสั่ง", "discretion", "recorded line", "บันทึกเทป"),
    ),
    Entry(
        "B07", "B",
        {"en": "Hands off the client's money and accounts", "th": "ห้ามยุ่งกับเงินและบัญชีของลูกค้า"},
        {"en": "Do not handle clients' payments, assets or log-ins, and never use a client's account for "
               "yourself or anyone else.",
         "th": "ห้ามยุ่งเกี่ยวกับการรับจ่ายเงิน ทรัพย์สิน หรือรหัสผ่านของลูกค้า และห้ามใช้บัญชีลูกค้าเพื่อตนเองหรือผู้อื่น"},
        (
            {"en": "No holding ATM cards or bank books, paying or settling for a client, moving securities or "
                   "collateral for them, or having them pre-sign withdrawal forms.",
             "th": "ห้ามถือบัตร ATM หรือสมุดบัญชีของลูกค้า ห้ามชำระเงินแทน ห้ามโอนย้ายหลักทรัพย์หรือวางหลักประกันแทน "
                   "และห้ามให้ลูกค้าลงนามแบบฟอร์มเบิกถอนไว้ล่วงหน้า"},
            {"en": "No using a client's username/password, and no using their account – with or without their "
                   "consent.",
             "th": "ห้ามใช้ username/password ของลูกค้า และห้ามใช้บัญชีลูกค้าซื้อขาย ไม่ว่าลูกค้าจะยินยอมหรือไม่"},
            {"en": "No helping a client trade beyond their means, and no part in informal (loan-shark) borrowing "
                   "for trading.",
             "th": "ห้ามช่วยให้ลูกค้าซื้อขายเกินฐานะการเงิน และห้ามเกี่ยวข้องกับเงินกู้นอกระบบเพื่อการซื้อขาย"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1, 2),
        ("money", "เงิน", "ATM", "password", "loan", "เงินกู้"),
    ),
    Entry(
        "B08", "B",
        {"en": "No guarantees, no profit-sharing, no side payments", "th": "ห้ามรับประกันผล ห้ามแบ่งกำไร ห้ามรับผลประโยชน์แอบแฝง"},
        {"en": "Never promise a return or protection from losses, never charge clients anything beyond the firm's "
               "fees, and never accept bribes or extra benefits.",
         "th": "ห้ามรับประกันผลตอบแทนหรือผลขาดทุน ห้ามเก็บค่าตอบแทนจากลูกค้านอกเหนือจากที่ชำระให้บริษัท และห้ามรับสินบน"
               "หรือผลประโยชน์เกินปกติ"},
        (
            {"en": "Examples: managing a client's portfolio for a share of the profit, marking up IPO shares, "
                   "or sourcing IPO/off-market shares for a fee.",
             "th": "เช่น รับบริหารพอร์ตโดยเรียกส่วนแบ่งกำไร ขายหุ้น IPO โดยได้ผลตอบแทนเกินกว่าที่ลูกค้าจ่ายจริง หรือหาหุ้น "
                   "IPO/หุ้นนอกตลาดมาขายโดยคิดค่าดำเนินการ"},
            {"en": "Never invest together with a client or have a personal stake in their trades.",
             "th": "ห้ามลงทุนร่วมกับลูกค้าหรือมีส่วนได้เสียกับการซื้อขายของลูกค้า"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1,),
        ("guarantee", "รับประกัน", "profit share", "bribe", "สินบน", "IPO"),
    ),
    Entry(
        "B09", "B",
        {"en": "Conflicts of interest: avoid or disclose", "th": "ความขัดแย้งทางผลประโยชน์: หลีกเลี่ยงหรือเปิดเผย"},
        {"en": "Avoid advice where you or your firm has a conflict of interest – or tell the client about it.",
         "th": "หลีกเลี่ยงการแนะนำที่อาจมีความขัดแย้งทางผลประโยชน์ เว้นแต่ได้เปิดเผยให้ลูกค้าทราบ"},
        (
            {"en": "Typical conflicts: you or the firm hold over 5% of the issuer's voting shares (counting "
                   "spouse and minor children); the firm or a related company issued the product; you are a "
                   "director of the issuer; the firm is the issuer's financial adviser.",
             "th": "ตัวอย่าง: ตนเองหรือบริษัทถือหุ้นผู้ออกหลักทรัพย์เกิน 5% ของหุ้นที่มีสิทธิออกเสียง (นับรวมคู่สมรสและบุตร"
                   "ที่ยังไม่บรรลุนิติภาวะ) บริษัทหรือบริษัทที่เกี่ยวข้องเป็นผู้ออก ตนเป็นกรรมการของผู้ออก หรือบริษัทเป็นที่ปรึกษา"
                   "ทางการเงินของผู้ออก"},
            {"en": "Also a conflict: you earn different rewards for different products – e.g. more sales points "
                   "or fees for one fund than another.",
             "th": "เป็นความขัดแย้งด้วย ถ้าได้รับผลตอบแทนต่างกันตามผลิตภัณฑ์ เช่น ได้คะแนนผลงานหรือค่าธรรมเนียมจากการขาย"
                   "กองทุนหนึ่งมากกว่าอีกกองทุนหนึ่ง"},
            {"en": "Tell the client when the firm is the other side of their trade (except as market maker or "
                   "dealer).",
             "th": "แจ้งลูกค้าเมื่อบริษัทเป็นคู่สัญญากับลูกค้าเอง (ยกเว้นกรณี market maker หรือ dealer)"},
        ),
        (DUTY_GUIDELINE,), GUIDE_SINCE, CHECKED, ("ic", "ip", "analyst"), (1, 2),
        ("conflict", "ขัดแย้ง", "disclose", "เปิดเผย", "commission", "ค่าธรรมเนียม"),
    ),
    Entry(
        "B10", "B",
        {"en": "No churning, no pushing", "th": "ห้ามกระตุ้นให้ซื้อขายบ่อย ห้ามเร่งรัด"},
        {"en": "Never encourage clients to trade often or in large volume to earn commission.",
         "th": "ห้ามกระตุ้นหรือสนับสนุนให้ลูกค้าซื้อขายบ่อยครั้งหรือปริมาณมากเพื่อหวังค่าคอมมิชชั่น"},
        (
            {"en": "This includes pushing day trading or same-day net settlement for commission.",
             "th": "รวมถึงการสนับสนุนให้เล่นรอบหรือซื้อขายแบบหักกลบภายในวันเดียวกันเพื่อหวังค่าคอมมิชชั่น"},
            {"en": "Give clients enough time to study and decide.",
             "th": "ให้เวลาลูกค้าศึกษาข้อมูลและตัดสินใจอย่างเพียงพอ"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1, 2),
        ("churning", "commission", "ค่าคอมมิชชั่น", "day trade"),
    ),
    Entry(
        "B11", "B",
        {"en": "Confidentiality and honest paperwork", "th": "รักษาความลับและเอกสารต้องตรงความจริง"},
        {"en": "Keep client information confidential and never sign or create documents that do not reflect "
               "what really happened.",
         "th": "รักษาความลับข้อมูลลูกค้า และห้ามลงนามหรือจัดทำเอกสารที่ไม่ตรงกับความเป็นจริง"},
        (
            {"en": "Don't disclose clients' personal, investment or financial data (except as your duty requires) "
                   "or use it for yourself or others – e.g. passing it to another broker.",
             "th": "ห้ามเปิดเผยข้อมูลส่วนบุคคล ข้อมูลการลงทุน หรือฐานะการเงินของลูกค้า (เว้นแต่ตามหน้าที่) หรือนำไปหา"
                   "ประโยชน์ เช่น มอบให้บริษัทหลักทรัพย์อื่น"},
            {"en": "Don't sign forms (e.g. fund orders, suitability tests) for work you didn't do; never give "
                   "false or incomplete information to the firm, the SEC or clients.",
             "th": "ห้ามลงนามในเอกสาร (เช่น ใบคำสั่งซื้อหน่วยลงทุน แบบ suitability test) โดยไม่ได้ทำหน้าที่นั้นจริง และห้าม"
                   "ให้ข้อมูลเท็จหรือไม่ครบถ้วนต่อบริษัท ก.ล.ต. หรือลูกค้า"},
        ),
        (DUTY_GUIDELINE, DO_DONT), GUIDE_SINCE, CHECKED, ADVISERS, (1,),
        ("confidential", "ความลับ", "privacy", "PDPA", "signature", "ลงนาม"),
    ),
    Entry(
        "B12", "B",
        {"en": "Stay within your licence and your firm's rules", "th": "ทำงานภายในขอบเขตใบอนุญาตและระเบียบบริษัท"},
        {"en": "Work only within the type of approval you hold and the duties your firm gives you, and follow its "
               "rules on staff trading.",
         "th": "ปฏิบัติงานตามประเภทที่ได้รับความเห็นชอบและขอบเขตที่บริษัทมอบหมาย และปฏิบัติตามระเบียบการซื้อขาย"
               "หลักทรัพย์ของพนักงาน"},
        (
            {"en": "No advice on social media, blogs or websites, and no teaching securities-analysis courses, "
                   "without your firm's permission.",
             "th": "ห้ามให้คำแนะนำผ่าน social media เว็บไซต์ หรือ blog หรือเป็นวิทยากรสอนวิเคราะห์หลักทรัพย์ โดยไม่ได้รับ"
                   "อนุญาตจากบริษัท"},
            {"en": "Cooperate with the SEC, report unusual volumes or prices to your supervisor, and correct a "
                   "client's improper order behaviour as soon as the exchange warns.",
             "th": "ให้ความร่วมมือกับ ก.ล.ต. รายงานผู้บังคับบัญชาทันทีเมื่อพบปริมาณหรือราคาซื้อขายผิดปกติ และแนะนำลูกค้า"
                   "ให้แก้ไขพฤติกรรมการส่งคำสั่งที่ไม่เหมาะสมทันทีที่ตลาดหลักทรัพย์แจ้งเตือน"},
            {"en": "Don't handle back-office documents that belong to operations.",
             "th": "ห้ามจัดการเอกสารที่อยู่ในความรับผิดชอบของสายงานปฏิบัติการ (back office)"},
        ),
        (DUTY_GUIDELINE, DO_DONT, PERSONNEL_RULE), GUIDE_SINCE, CHECKED, ADVISERS, (1,),
        ("social media", "scope", "ขอบเขต", "staff trading", "พนักงาน"),
    ),
]
