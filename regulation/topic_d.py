"""Topic D – Fund structure (SEC Thailand).

Summarised in my own words from the SEC's plain summary of the Securities and Exchange Act part 7
(sections 117–132) and the fund classification appendix of ทน. 87/2558 (as amended by ทน. 1/2569),
read on 2026-10-06 (copies kept in the git-ignored data/sec/). The linked official documents are what counts.
"""

from regulation.model import Entry, Table
from regulation.sources import FUND_TYPES, SEC_ACT_FUNDS

CHECKED = "2026-10-06"
CLASSES_SINCE = "2026-03-01"  # current version of the classification appendix (ทน. 1/2569)
FUND_PEOPLE = ("ic", "ip", "fund_manager", "firm")

TABLES = [
    Table(
        "D", "🗂️", {"en": "Fund types at a glance", "th": "ประเภทกองทุนรวมโดยสรุป"},
        ({"en": "Fund type", "th": "ประเภทกองทุน"}, {"en": "What it must hold", "th": "ต้องลงทุนอะไร"},
         {"en": "Worth telling a client", "th": "ควรบอกลูกค้า"}),
        (
            ({"en": "Equity fund", "th": "กองทุนรวมตราสารทุน"},
             {"en": "At least 80% of NAV in shares (average over the fund's year)",
              "th": "ตราสารทุนโดยเฉลี่ยรอบปีบัญชีไม่น้อยกว่า 80% ของ NAV"},
             {"en": "Highest ups and downs of the main types", "th": "ผันผวนสูงที่สุดในกลุ่มหลัก"}),
            ({"en": "Fixed income fund", "th": "กองทุนรวมตราสารหนี้"},
             {"en": "At least 80% in deposits, bonds, sukuk and similar; at most 20% in hybrid or Basel III bonds",
              "th": "เงินฝาก ตราสารหนี้ ศุกูก และทรัพย์สินทำนองเดียวกันไม่น้อยกว่า 80% ตราสารกึ่งหนี้กึ่งทุนหรือ Basel III ไม่เกิน 20%"},
             {"en": "Can still lose money (rates, credit)", "th": "ยังขาดทุนได้ (ดอกเบี้ย เครดิต)"}),
            ({"en": "Alternative investment fund", "th": "กองทุนรวมทรัพย์สินทางเลือก"},
             {"en": "At least 80% in property or infrastructure funds, commodities, gold or private equity",
              "th": "หน่วย property / infra สินค้าโภคภัณฑ์ ทองคำ หรือ private equity ไม่น้อยกว่า 80%"},
             {"en": "Often harder to sell quickly", "th": "มักมีสภาพคล่องต่ำกว่า"}),
            ({"en": "Mixed fund", "th": "กองทุนรวมผสม"},
             {"en": "Any mix set in the fund's project, or no fixed mix",
              "th": "สัดส่วนตามที่กำหนดในโครงการ หรือไม่กำหนดสัดส่วนแน่นอน"},
             {"en": "Read the actual mix in the factsheet", "th": "ดูสัดส่วนจริงใน factsheet"}),
            ({"en": "Money market fund", "th": "กองทุนรวมตลาดเงิน"},
             {"en": "Only deposits and debt maturing within 397 days; portfolio duration under 92 days",
              "th": "เฉพาะเงินฝากและตราสารหนี้อายุไม่เกิน 397 วัน portfolio duration ไม่เกิน 92 วัน"},
             {"en": "Low risk, but not a bank deposit", "th": "ความเสี่ยงต่ำ แต่ไม่ใช่เงินฝาก"}),
            ({"en": "Capital protected fund", "th": "กองทุนรวมมุ่งรักษาเงินต้น"},
             {"en": "A plan of Thai government bonds, highly rated deposits etc. that aims to keep the principal",
              "th": "แผนการลงทุนในตราสารภาครัฐไทย เงินฝากที่มี rating สูง ฯลฯ เพื่อมุ่งรักษาเงินต้น"},
             {"en": "“Aims to” – no one guarantees it", "th": "“มุ่ง” รักษา ไม่มีผู้ประกัน"}),
            ({"en": "Guarantee fund", "th": "กองทุนรวมมีประกัน"},
             {"en": "Someone else (not the trustee) guarantees the amount if held to the end",
              "th": "มีบุคคลอื่น (ที่ไม่ใช่ผู้ดูแลผลประโยชน์) ประกันเงินตามที่กำหนดหากถือครบระยะเวลา"},
             {"en": "Only if held to the end; check the guarantor", "th": "ต้องถือครบกำหนด และดูว่าใครเป็นผู้ประกัน"}),
            ({"en": "Feeder / fund of funds", "th": "ฟีดเดอร์ / กองทุนรวมหน่วยลงทุน"},
             {"en": "At least 80% in one other fund (feeder) or in other funds (fund of funds)",
              "th": "ลงทุนในกองทุนอื่นเพียงกองเดียว (feeder) หรือหลายกอง (FoF) ไม่น้อยกว่า 80%"},
             {"en": "Two layers of fees", "th": "มีค่าธรรมเนียม 2 ชั้น"}),
            ({"en": "Index fund / ETF", "th": "กองทุนรวมดัชนี / ETF"},
             {"en": "Follows an index; an ETF also trades on the exchange",
              "th": "สร้างผลตอบแทนตามดัชนี ETF ซื้อขายในตลาดได้ด้วย"},
             {"en": "Usually lower fees", "th": "ค่าธรรมเนียมมักต่ำกว่า"}),
            ({"en": "RMF / SSF / Thai ESG", "th": "RMF / SSF / Thai ESG"},
             {"en": "Funds tied to tax benefits (holding rules set by the Revenue Department)",
              "th": "กองทุนที่ผูกกับสิทธิประโยชน์ทางภาษี (เงื่อนไขการถือครองตามกรมสรรพากร)"},
             {"en": "Breaking the holding rules means paying the tax back",
              "th": "ผิดเงื่อนไขต้องคืนภาษี"}),
        ),
        FUND_TYPES,
        {"en": "summary; see D06–D08 for the details", "th": "สรุปย่อ รายละเอียดดู D06–D08"},
    ),
]

ENTRIES = [
    Entry(
        "D01", "D",
        {"en": "Who's who in a mutual fund", "th": "ใครเป็นใครในกองทุนรวม"},
        {"en": "A mutual fund has two key players: the fund company (AMC) that manages it and the trustee that "
               "holds the assets and watches the AMC. Once registered, the fund is a legal entity of its own.",
         "th": "กองทุนรวมมีผู้เล่นหลัก 2 ฝ่าย คือ บลจ. ที่บริหารจัดการ และผู้ดูแลผลประโยชน์ที่เก็บรักษาทรัพย์สินและ"
               "ดูแล บลจ. เมื่อจดทะเบียนแล้วกองทุนรวมเป็นนิติบุคคลแยกต่างหาก"},
        (
            {"en": "AMC (บลจ.): sets up the fund with SEC approval, invests the money, keeps the accounts and the "
                   "register of unitholders.",
             "th": "บลจ.: จัดตั้งกองทุนเมื่อได้รับอนุมัติจาก ก.ล.ต. ลงทุน จัดทำบัญชีและทะเบียนผู้ถือหน่วย"},
            {"en": "Trustee (ผู้ดูแลผลประโยชน์): must be a commercial bank or a financial institution the SEC "
                   "approves; the AMC must appoint one before selling units.",
             "th": "ผู้ดูแลผลประโยชน์: ต้องเป็นธนาคารพาณิชย์หรือสถาบันการเงินที่มีคุณสมบัติตามที่ ก.ล.ต. กำหนด "
                   "และ บลจ. ต้องแต่งตั้งก่อนเสนอขายหน่วยลงทุน"},
            {"en": "Selling agents (banks, brokers) and their ICs sell the units; the SEC regulates all of them.",
             "th": "ตัวแทนขาย (ธนาคาร บล.) และ IC เป็นผู้ขายหน่วยลงทุน โดยทั้งหมดอยู่ภายใต้การกำกับของ ก.ล.ต."},
            {"en": "Because the fund is its own legal entity and the trustee holds the assets separately, the "
                   "fund's money is not the AMC's money.",
             "th": "เพราะกองทุนเป็นนิติบุคคลและทรัพย์สินฝากแยกไว้กับผู้ดูแลผลประโยชน์ เงินของกองทุนจึงไม่ใช่เงินของ บลจ."},
        ),
        (SEC_ACT_FUNDS,), "", CHECKED, FUND_PEOPLE, (2,),
        ("AMC", "บลจ.", "trustee", "ผู้ดูแลผลประโยชน์", "custodian", "juristic person", "นิติบุคคล"),
    ),
    Entry(
        "D02", "D",
        {"en": "How a fund is set up and launched", "th": "การจัดตั้งและเสนอขายกองทุนรวม"},
        {"en": "The AMC applies to the SEC with the fund's project, the unitholder commitment and the trustee "
               "contract. After approval it has 2 years to sell units, and needs at least 35 unitholders.",
         "th": "บลจ. ยื่นขออนุมัติต่อ ก.ล.ต. พร้อมโครงการ ร่างข้อผูกพัน และร่างสัญญาแต่งตั้งผู้ดูแลผลประโยชน์ "
               "เมื่อได้รับอนุมัติต้องเสนอขายภายใน 2 ปี และต้องมีผู้ถือหน่วยไม่น้อยกว่า 35 ราย"},
        (
            {"en": "A normal application is answered within 90 days of complete documents; simple funds (fully "
                   "hedged, no feeder, no derivatives except hedging, one class) may use a fast general approval.",
             "th": "คำขอแบบปกติ ก.ล.ต. แจ้งผลภายใน 90 วันนับแต่เอกสารครบ กองทุนที่เรียบง่าย (hedge เต็มจำนวน ไม่ใช่ "
                   "feeder ไม่ลงทุน derivatives ยกเว้นเพื่อลดความเสี่ยง ไม่แบ่ง class) ยื่นแบบอนุมัติเป็นการทั่วไปได้"},
            {"en": "Units may be sold only with a prospectus. The AMC may sell up to 15% more than approved "
                   "(greenshoe) if the project says so.",
             "th": "เสนอขายได้เมื่อแจกจ่ายหนังสือชี้ชวน และอาจขายเกินจำนวนที่อนุมัติได้ไม่เกิน 15% (greenshoe) "
                   "หากระบุไว้ในโครงการ"},
            {"en": "Fewer than 35 unitholders after the IPO: the approval ends and subscriptions are refunded "
                   "within 1 month.",
             "th": "หลัง IPO มีผู้ถือหน่วยไม่ถึง 35 ราย การอนุมัติสิ้นสุด และต้องคืนเงินค่าจองซื้อภายใน 1 เดือน"},
            {"en": "A fund's name must not mislead about its type, risk or return. Funds not for retail "
                   "investors (AI funds) end their name with “ห้ามขายผู้ลงทุนรายย่อย” and cannot be RMFs or ETFs.",
             "th": "ชื่อกองทุนต้องไม่ทำให้เข้าใจผิดเรื่องประเภท ความเสี่ยง หรือผลตอบแทน กองทุน AI ต้องมีคำว่า "
                   "“ห้ามขายผู้ลงทุนรายย่อย” ท้ายชื่อ และเป็น RMF หรือ ETF ไม่ได้"},
            {"en": "A fund may have several unit classes, but all units of one class have equal rights.",
             "th": "แบ่งหน่วยลงทุนได้หลายชนิด (multi-class) แต่หน่วยชนิดเดียวกันต้องมีสิทธิเท่าเทียมกัน"},
        ),
        (SEC_ACT_FUNDS,), "", CHECKED, FUND_PEOPLE, (2,),
        ("IPO", "approval", "อนุมัติ", "35", "greenshoe", "AI fund", "multi-class", "prospectus", "หนังสือชี้ชวน"),
    ),
    Entry(
        "D03", "D",
        {"en": "What the fund company must and must not do", "th": "หน้าที่และข้อห้ามของ บลจ."},
        {"en": "The AMC must manage the fund exactly as its approved project says and must avoid conflicts of "
               "interest with unitholders.",
         "th": "บลจ. ต้องจัดการกองทุนตามโครงการที่ได้รับอนุมัติ และต้องไม่กระทำการที่อาจขัดแย้งทางผลประโยชน์กับผู้ถือหน่วย"},
        (
            {"en": "Must: follow the project, keep the fund's assets with the trustee, keep investment accounts, "
                   "report investments to the trustee, keep the unitholder register, and collect the income.",
             "th": "ต้อง: จัดการตามโครงการ ฝากทรัพย์สินไว้กับผู้ดูแลผลประโยชน์ จัดทำบัญชีการลงทุน รายงานการลงทุน"
                   "ต่อผู้ดูแลผลประโยชน์ จัดทำทะเบียนผู้ถือหน่วย และรับผลประโยชน์จากการลงทุนฝากไว้กับผู้ดูแลผลประโยชน์"},
            {"en": "Must not: act with a conflict of interest, or buy shares of the AMC itself for the fund.",
             "th": "ห้าม: กระทำการที่อาจเกิดความขัดแย้งทางผลประโยชน์ หรือลงทุนในหุ้นของ บลจ. เอง"},
            {"en": "May invest in other funds of the same AMC only under the rules and if the project and "
                   "prospectus say so clearly.",
             "th": "ลงทุนในกองทุนอื่นของ บลจ. เดียวกันได้เมื่อทำตามหลักเกณฑ์และเปิดเผยไว้ชัดเจนในโครงการและหนังสือชี้ชวน"},
        ),
        (SEC_ACT_FUNDS,), "", CHECKED, ("fund_manager", "firm"), (2,),
        ("AMC duties", "หน้าที่", "conflict of interest", "ขัดแย้งทางผลประโยชน์", "section 125", "มาตรา 125"),
    ),
    Entry(
        "D04", "D",
        {"en": "The trustee: the unitholders' watchdog", "th": "ผู้ดูแลผลประโยชน์: ผู้เฝ้าดูแทนผู้ถือหน่วย"},
        {"en": "The trustee keeps the fund's assets apart from everything else and checks that the AMC does its "
               "job – and can report it to the SEC or sue it.",
         "th": "ผู้ดูแลผลประโยชน์เก็บรักษาทรัพย์สินของกองทุนแยกจากทรัพย์สินอื่น และดูแลให้ บลจ. ปฏิบัติหน้าที่ "
               "รวมถึงรายงาน ก.ล.ต. หรือฟ้องร้อง บลจ. ได้"},
        (
            {"en": "Holds the fund's assets separately and keeps accounts of what comes in and goes out.",
             "th": "รับฝากทรัพย์สินของกองทุนแยกไว้ต่างหาก และจัดทำบัญชีการรับจ่ายทรัพย์สิน"},
            {"en": "Reports to the SEC when the AMC causes the fund a loss or fails its duties.",
             "th": "รายงาน ก.ล.ต. เมื่อ บลจ. กระทำหรืองดเว้นจนเกิดความเสียหายแก่กองทุน หรือไม่ปฏิบัติหน้าที่"},
            {"en": "Can take the AMC to court to make it do its duties or to claim damages.",
             "th": "ฟ้องร้องบังคับให้ บลจ. ปฏิบัติหน้าที่ หรือเรียกค่าเสียหายจาก บลจ."},
            {"en": "Also certifies NAV corrections and reviews fee increases (see E02 and E06).",
             "th": "รับรองการแก้ไขราคาหน่วยย้อนหลังและสอบทานการปรับขึ้นค่าธรรมเนียมด้วย (ดู E02 และ E06)"},
        ),
        (SEC_ACT_FUNDS,), "", CHECKED, FUND_PEOPLE, (2,),
        ("trustee", "ผู้ดูแลผลประโยชน์", "custodian", "ผู้รับฝาก", "bank", "ธนาคาร", "section 127", "มาตรา 127"),
    ),
    Entry(
        "D05", "D",
        {"en": "Changing or closing a fund", "th": "การแก้ไขโครงการและการเลิกกองทุน"},
        {"en": "To change a fund's project or how it is managed the AMC needs a unitholder vote (or SEC approval "
               "in its place), and must tell everyone within 15 days.",
         "th": "การแก้ไขโครงการหรือวิธีจัดการต้องได้มติผู้ถือหน่วย (หรือ ก.ล.ต. เห็นชอบแทน) และต้องแจ้งทุกคน"
               "ภายใน 15 วัน"},
        (
            {"en": "The vote can be a unitholder meeting or a written request for votes.",
             "th": "ขอมติได้ทั้งการประชุมผู้ถือหน่วยหรือการส่งหนังสือขอมติ"},
            {"en": "The change must be reported to the SEC, sent to every unitholder and published within 15 "
                   "days of the vote.",
             "th": "ต้องแจ้ง ก.ล.ต. แจ้งผู้ถือหน่วยทุกคน และเผยแพร่ภายใน 15 วันนับแต่วันที่มีมติ"},
            {"en": "When a fund closes, a liquidator collects and pays out the assets, then deregisters the fund "
                   "with the SEC.",
             "th": "เมื่อเลิกกองทุน ผู้ชำระบัญชีรวบรวมและแจกจ่ายทรัพย์สินแก่ผู้ถือหน่วย แล้วจดทะเบียนเลิกกองทุนกับ ก.ล.ต."},
        ),
        (SEC_ACT_FUNDS,), "", CHECKED, FUND_PEOPLE, (2,),
        ("vote", "มติ", "unitholder meeting", "ประชุมผู้ถือหน่วย", "liquidation", "ชำระบัญชี", "เลิกกองทุน"),
    ),
    Entry(
        "D06", "D",
        {"en": "Fund types by what they invest in", "th": "ประเภทกองทุนตามทรัพย์สินที่ลงทุน"},
        {"en": "Every fund is labelled by its main asset, measured as at least 80% of NAV on average over the "
               "fund's accounting year.",
         "th": "ทุกกองทุนต้องจัดประเภทตามทรัพย์สินหลัก โดยวัดจากสัดส่วนเฉลี่ยรอบปีบัญชีไม่น้อยกว่า 80% ของ NAV"},
        (
            {"en": "Equity: at least 80% in shares.", "th": "ตราสารทุน: หุ้นไม่น้อยกว่า 80%"},
            {"en": "Fixed income: at least 80% in deposits, bonds, sukuk, reverse repos and funds that hold only "
                   "these; at most 20% in hybrid or Basel III bonds. Shares received from a conversion must be "
                   "sold within 30 days.",
             "th": "ตราสารหนี้: เงินฝาก ตราสารหนี้ ศุกูก reverse repo และกองทุนที่ลงทุนเฉพาะสิ่งเหล่านี้ ไม่น้อยกว่า 80% "
                   "ตราสารกึ่งหนี้กึ่งทุนหรือ Basel III ไม่เกิน 20% หุ้นที่ได้จากการแปลงสภาพต้องขายภายใน 30 วัน"},
            {"en": "Alternative: at least 80% in property or infrastructure fund units, commodities (e.g. oil, "
                   "gold), gold bars or private equity.",
             "th": "ทรัพย์สินทางเลือก: หน่วย property หน่วย infra สินค้าโภคภัณฑ์ (เช่น น้ำมัน ทองคำ) ทองคำแท่ง "
                   "หรือ private equity ไม่น้อยกว่า 80%"},
            {"en": "Mixed: anything else – a fixed mix stated in the project, or no fixed mix.",
             "th": "ผสม: กรณีอื่น ๆ โดยกำหนดสัดส่วนแน่นอนในโครงการ หรือไม่กำหนดก็ได้"},
            {"en": "A feeder fund takes the type of the foreign fund it buys.",
             "th": "กองทุนฟีดเดอร์จัดประเภทตามกองทุนต่างประเทศที่ไปลงทุน"},
        ),
        (FUND_TYPES,), CLASSES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("equity fund", "ตราสารทุน", "fixed income", "ตราสารหนี้", "alternative", "ทรัพย์สินทางเลือก",
         "mixed fund", "กองทุนผสม", "80%", "fund type", "ประเภทกองทุน"),
    ),
    Entry(
        "D07", "D",
        {"en": "Special fund types", "th": "กองทุนรวมที่มีลักษณะพิเศษ"},
        {"en": "On top of its asset type a fund may carry a special label that tells the client something "
               "important – its liquidity, its protection, its structure or its tax status.",
         "th": "นอกจากประเภทตามทรัพย์สินแล้ว กองทุนอาจมีลักษณะพิเศษที่บอกเรื่องสำคัญแก่ลูกค้า เช่น สภาพคล่อง "
               "การรักษาเงินต้น โครงสร้าง หรือสิทธิประโยชน์ทางภาษี"},
        (
            {"en": "Money market: redeemable every business day; only deposits, debt maturing within 397 days, "
                   "other money market funds and similar; portfolio duration under 92 days; at least 10% in very "
                   "liquid assets; foreign part under 50% and fully hedged.",
             "th": "ตลาดเงิน: รับซื้อคืนทุกวันทำการ ลงทุนเฉพาะเงินฝาก ตราสารหนี้อายุไม่เกิน 397 วัน กองทุนตลาดเงินอื่น "
                   "และทรัพย์สินทำนองเดียวกัน portfolio duration ไม่เกิน 92 วัน มีทรัพย์สินสภาพคล่องสูงไม่น้อยกว่า 10% "
                   "ส่วนต่างประเทศไม่เกิน 50% และต้อง hedge เต็มจำนวน"},
            {"en": "Capital protected vs guarantee: a capital protected fund only aims to keep the principal "
                   "through its investment plan; a guarantee fund has another party (not the trustee) that "
                   "guarantees the amount if you hold to the end.",
             "th": "มุ่งรักษาเงินต้น vs มีประกัน: กองทุนมุ่งรักษาเงินต้นเพียงวางแผนการลงทุนเพื่อรักษาเงินต้น ส่วนกองทุน"
                   "มีประกันมีบุคคลอื่น (ที่ไม่ใช่ผู้ดูแลผลประโยชน์) ประกันเงินตามที่กำหนดหากถือครบระยะเวลา"},
            {"en": "Sector, fund of funds, feeder and gold funds: at least 80% in one industry, in other funds, "
                   "in one single fund, or in gold bars.",
             "th": "หมวดอุตสาหกรรม กองทุนรวมหน่วยลงทุน ฟีดเดอร์ และทองคำ: ลงทุนในอุตสาหกรรมเดียว ในกองทุนอื่น "
                   "ในกองทุนเดียว หรือในทองคำแท่ง ไม่น้อยกว่า 80%"},
            {"en": "Index and ETF: follow an index; ETFs also trade on the exchange and deal directly only with "
                   "large investors (from 10 million baht). Leveraged (2×) and inverse ETFs are sold after the "
                   "IPO only to large investors.",
             "th": "ดัชนีและ ETF: สร้างผลตอบแทนตามดัชนี ETF ซื้อขายในตลาดได้ และซื้อขายกับ บลจ. โดยตรงเฉพาะผู้ลงทุน"
                   "รายใหญ่ (ตั้งแต่ 10 ล้านบาท) ETF แบบ leveraged (2 เท่า) หรือ inverse ขายหลัง IPO ได้เฉพาะผู้ลงทุนรายใหญ่"},
            {"en": "Tax-linked funds: RMF (retirement saving, open-ended only), SSF (Super Savings Fund) and Thai "
                   "ESG (see E07–E08). Their tax rules come from the Revenue Department, not the SEC.",
             "th": "กองทุนที่มีสิทธิประโยชน์ทางภาษี: RMF (ออมเพื่อเลี้ยงชีพ ต้องเป็นกองทุนเปิด) SSF และ Thai ESG "
                   "(ดู E07–E08) เงื่อนไขภาษีเป็นของกรมสรรพากร ไม่ใช่ ก.ล.ต."},
            {"en": "Islamic funds invest only in assets that follow Islamic rules.",
             "th": "กองทุนรวมอิสลามลงทุนเฉพาะทรัพย์สินที่เป็นไปตามหลักศาสนาอิสลาม"},
        ),
        (FUND_TYPES, SEC_ACT_FUNDS), CLASSES_SINCE, CHECKED, FUND_PEOPLE, (2, 4, 5),
        ("money market", "ตลาดเงิน", "MMF", "capital protected", "มุ่งรักษาเงินต้น", "guarantee", "มีประกัน",
         "feeder", "ฟีดเดอร์", "ETF", "index", "ดัชนี", "RMF", "SSF", "gold", "ทองคำ", "sector", "Islamic"),
    ),
    Entry(
        "D08", "D",
        {"en": "Foreign investment risk label", "th": "การจัดประเภทตามความเสี่ยงต่างประเทศ"},
        {"en": "Each fund also says how much foreign risk it takes, so clients know about currency and "
               "overseas risks.",
         "th": "ทุกกองทุนต้องจัดประเภทตามความเสี่ยงต่างประเทศด้วย เพื่อให้ลูกค้าตระหนักถึงความเสี่ยงค่าเงินและต่างประเทศ"},
        (
            {"en": "Mainly foreign: at least 80% of NAV exposed to foreign risk on average.",
             "th": "เน้นลงทุนแบบมีความเสี่ยงต่างประเทศ: เฉลี่ยไม่น้อยกว่า 80% ของ NAV"},
            {"en": "No foreign risk: no foreign exposure at all.",
             "th": "ลงทุนแบบไม่มีความเสี่ยงต่างประเทศ: ไม่มี exposure ต่างประเทศเลย"},
            {"en": "Both: anything in between, fixed or not.",
             "th": "ลงทุนแบบมีความเสี่ยงทั้งในและต่างประเทศ: กรณีอื่น ๆ จะกำหนดสัดส่วนหรือไม่ก็ได้"},
            {"en": "Foreign risk means a foreign issuer or counterparty (not a licensed Thai branch of a foreign "
                   "bank) or exchange-rate risk.",
             "th": "ความเสี่ยงต่างประเทศคือผู้ออกหรือคู่สัญญาต่างประเทศ (ยกเว้นสาขาธนาคารต่างประเทศที่ได้รับอนุญาตในไทย) "
                   "หรือความเสี่ยงอัตราแลกเปลี่ยน"},
        ),
        (FUND_TYPES,), CLASSES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("foreign", "ต่างประเทศ", "currency", "ค่าเงิน", "FX", "hedge"),
    ),
]
