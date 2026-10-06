"""Topic E – Fund rules (SEC Thailand).

Summarised in my own words from the fee circular นจ.(ว) 2/2569, the NAV-error appendix of สน. 9/2564,
the fund classification appendix of ทน. 87/2558 and the Thai ESG circulars นจ.(ว) 3/2569 and
นจ.(ว) 4/2568, read on 2026-10-06 (copies kept in the git-ignored data/sec/). The linked official
documents are what counts. Tax deductions for Thai ESG funds are set by the Revenue Department.
"""

from regulation.model import Entry, Table
from regulation.sources import FEE_CIRCULAR, FUND_TYPES, NAV_ERRORS, THAI_ESG_CIRCULAR, THAI_ESGX_CIRCULAR

CHECKED = "2026-10-06"
FEES_SINCE = "2026-02-01"  # fee package (ทน. 51–52/2568, สน. 52–55/2568, สธ. 55/2568)
FUND_PEOPLE = ("ic", "ip", "fund_manager", "firm")

TABLES = [
    Table(
        "E", "🧮", {"en": "When a fund's price was wrong", "th": "เมื่อราคาหน่วยลงทุนไม่ถูกต้อง"},
        ({"en": "How big the error is", "th": "ขนาดความผิดพลาด"}, {"en": "What the AMC must do", "th": "บลจ. ต้องทำอะไร"},
         {"en": "Deadline", "th": "ระยะเวลา"}),
        (
            ({"en": "Small: under 1 satang or under 0.5% of the right price",
              "th": "เล็ก: น้อยกว่า 1 สตางค์ หรือน้อยกว่า 0.5% ของราคาที่ถูกต้อง"},
             {"en": "Report the error, its cause and how to prevent it to the trustee; correct the price from "
                    "the day it was found",
              "th": "รายงานผู้ดูแลผลประโยชน์ถึงราคาที่ผิด ราคาที่ถูก สาเหตุ และมาตรการป้องกัน และแก้ราคาตั้งแต่วันที่พบ"},
             {"en": "Report within 7 business days", "th": "รายงานภายใน 7 วันทำการ"}),
            ({"en": "Big: 1 satang or more AND 0.5% or more", "th": "ใหญ่: ตั้งแต่ 1 สตางค์ และตั้งแต่ 0.5%"},
             {"en": "Recalculate back to the first wrong day and send the trustee a correction report to certify",
              "th": "คำนวณราคาย้อนหลังถึงวันแรกที่ผิด และส่งรายงานการแก้ไขให้ผู้ดูแลผลประโยชน์รับรอง"},
             {"en": "Next business day", "th": "วันทำการถัดไป"}),
            ({"en": "Big – telling investors", "th": "ใหญ่ – แจ้งผู้ลงทุน"},
             {"en": "Publish which fund was corrected and for which dates",
              "th": "เผยแพร่ชื่อกองทุนและวันที่มีการแก้ไขราคา"},
             {"en": "Within 3 business days of certification", "th": "ภายใน 3 วันทำการนับแต่ผู้ดูแลผลประโยชน์รับรอง"}),
            ({"en": "Big – open funds: paying back", "th": "ใหญ่ – กองทุนเปิด: ชดเชยราคา"},
             {"en": "Compensate buyers and sellers who traded at the wrong price (in units or money; amounts under "
                    "100 baht may wait for the next payout)",
              "th": "ชดเชยผู้ซื้อหรือขายคืนที่ทำรายการในราคาที่ผิด (เป็นหน่วยหรือเงิน ถ้าไม่ถึง 100 บาทอาจรวมจ่ายในโอกาสแรก)"},
             {"en": "Within 5 business days of certification", "th": "ภายใน 5 วันทำการนับแต่ผู้ดูแลผลประโยชน์รับรอง"}),
            ({"en": "Big – open funds: reporting to the SEC", "th": "ใหญ่ – กองทุนเปิด: รายงาน ก.ล.ต."},
             {"en": "Send the prevention plan and the correction report", "th": "ส่งมาตรการป้องกันพร้อมสำเนารายงานการแก้ไข"},
             {"en": "Within 7 business days of certification", "th": "ภายใน 7 วันทำการนับแต่ผู้ดูแลผลประโยชน์รับรอง"}),
        ),
        NAV_ERRORS,
    ),
]

ENTRIES = [
    Entry(
        "E01", "E",
        {"en": "Three principles for every fund fee", "th": "หลัก 3 ข้อของค่าธรรมเนียมกองทุนรวม"},
        {"en": "Since February 2026 every fee, charge or expense of a fund must be appropriate, transparent and "
               "fair, and stated in the project and the prospectus.",
         "th": "ตั้งแต่กุมภาพันธ์ 2569 ค่าธรรมเนียม เงินตอบแทน และค่าใช้จ่ายทุกรายการต้องเหมาะสม โปร่งใส และเป็นธรรม "
               "และระบุไว้ในโครงการและหนังสือชี้ชวน"},
        (
            {"en": "Appropriate: matches the fund's objective and the service investors get, and is reasonable "
                   "compared with the market.",
             "th": "เหมาะสม: สอดคล้องกับวัตถุประสงค์และบริการที่ผู้ลงทุนได้รับ และสมเหตุสมผลเมื่อเทียบกับมาตรฐานตลาด"},
            {"en": "Transparent: disclosed clearly enough to help an investor decide.",
             "th": "โปร่งใส: เปิดเผยชัดเจนและเพียงพอให้ผู้ลงทุนใช้ตัดสินใจ"},
            {"en": "Fair: clearly grouped, never charged twice, not discriminatory and not an undue burden.",
             "th": "เป็นธรรม: จัดหมวดหมู่ชัดเจน ไม่ซ้ำซ้อน ไม่เลือกปฏิบัติ และไม่สร้างภาระเกินควร"},
            {"en": "AMCs also follow the AIMC's fee guideline approved by the SEC.",
             "th": "บลจ. ต้องปฏิบัติตามแนวปฏิบัติของ AIMC ที่ ก.ล.ต. เห็นชอบด้วย"},
        ),
        (FEE_CIRCULAR,), FEES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("fee", "ค่าธรรมเนียม", "expense", "ค่าใช้จ่าย", "AIMC", "fee for reasons"),
    ),
    Entry(
        "E02", "E",
        {"en": "Management fee: base, maximum and actual", "th": "ค่าธรรมเนียมการจัดการ: ขั้นต้น ขั้นสูง และที่เก็บจริง"},
        {"en": "A fund now shows three management fee rates. Raising the actual fee needs a review by the trustee "
               "and at least 15 business days' notice; going above the maximum needs a unitholder vote.",
         "th": "กองทุนต้องแสดงค่าธรรมเนียมการจัดการ 3 อัตรา การปรับขึ้นอัตราที่เก็บจริงต้องให้ผู้ดูแลผลประโยชน์สอบทาน"
               "และแจ้งล่วงหน้าไม่น้อยกว่า 15 วันทำการ ถ้าเกินอัตราขั้นสูงต้องขอมติผู้ถือหน่วย"},
        (
            {"en": "Base fee: what the AMC means to charge in the long run (shown in the project). Maximum fee: "
                   "the most it may ever charge. Actual fee: what it charges now.",
             "th": "ขั้นต้น (base): อัตราที่ บลจ. ตั้งใจเก็บจริงในระยะยาว (ระบุในโครงการ) ขั้นสูง (maximum): อัตราสูงสุดที่"
                   "อาจเก็บได้ ที่เก็บจริง (actual): อัตราที่เก็บอยู่ในปัจจุบัน"},
            {"en": "Raising the actual fee above the base: the AMC explains why, the trustee reviews it, and the AMC "
                   "shows what past returns would have been with the higher fee.",
             "th": "ปรับขึ้นเกินขั้นต้น: บลจ. ต้องมีเหตุผล ให้ผู้ดูแลผลประโยชน์สอบทาน และแสดงผลตอบแทนย้อนหลังเสมือน"
                   "เก็บอัตราใหม่"},
            {"en": "Changing the base or maximum fee needs a unitholder vote; lowering them counts as approved by "
                   "the SEC.",
             "th": "เปลี่ยนอัตราขั้นต้นหรือขั้นสูงต้องขอมติผู้ถือหน่วย ถ้าเป็นการลดให้ถือว่า ก.ล.ต. เห็นชอบ"},
            {"en": "A cut below the base fee for a promotion may last at most 1 year and must not be a trick to "
                   "avoid setting a true base fee.",
             "th": "ลดต่ำกว่าขั้นต้นเพื่อส่งเสริมการขายได้ไม่เกิน 1 ปี และต้องไม่ใช่การหลีกเลี่ยงการกำหนดอัตราขั้นต้นที่แท้จริง"},
        ),
        (FEE_CIRCULAR,), FEES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("management fee", "ค่าธรรมเนียมการจัดการ", "base fee", "maximum fee", "actual fee", "ขั้นต้น", "ขั้นสูง"),
    ),
    Entry(
        "E03", "E",
        {"en": "Performance fees", "th": "ค่าธรรมเนียมตามผลการดำเนินงาน (performance fee)"},
        {"en": "Only actively managed funds may charge a fee based on results – never money market or capital "
               "protected funds – and only after past losses are made up.",
         "th": "เฉพาะกองทุนที่บริหารแบบ active เท่านั้นที่เก็บ performance fee ได้ (ห้ามกองทุนตลาดเงินและมุ่งรักษาเงินต้น) "
               "และต้องชดเชยผลขาดทุนก่อน"},
        (
            {"en": "Allowed methods: fulcrum fee (the fee moves up or down with results against a benchmark, "
                   "between 0% and 200% of the management fee), high-water mark, or another method the SEC "
                   "approves.",
             "th": "วิธีที่ใช้ได้: fulcrum fee (ปรับขึ้นลงตามผลเทียบ benchmark ระหว่าง 0–200% ของค่าธรรมเนียมการจัดการ) "
                   "high water mark หรือวิธีอื่นที่ ก.ล.ต. เห็นชอบ"},
            {"en": "Charged at most once a year, after all costs, on the same day for all classes, and not on NAV "
                   "growth from new money.",
             "th": "เก็บได้ไม่เกินปีละครั้ง คำนวณหลังหักค่าใช้จ่ายทั้งหมด วันเดียวกันทุก class และไม่นับ NAV ที่เพิ่มจากเงินลงทุนใหม่"},
            {"en": "Losses or underperformance in the period must be recovered before the next performance fee.",
             "th": "ผลขาดทุนหรือผลต่ำกว่าตัวชี้วัดสะสมต้องชดเชยก่อนเก็บ performance fee ครั้งถัดไป"},
            {"en": "Before a new measuring period starts, unitholders get at least 30 days to leave without a "
                   "redemption fee.",
             "th": "ก่อนเริ่มรอบวัดผลใหม่ ต้องให้สิทธิผู้ถือหน่วยขายคืนโดยไม่เสียค่าธรรมเนียมล่วงหน้าไม่น้อยกว่า 30 วัน"},
            {"en": "If the fund may charge it even when its return is negative (but beat the benchmark), the "
                   "project and prospectus must say so with a warning.",
             "th": "ถ้าอาจเก็บได้แม้ผลตอบแทนติดลบ (แต่ชนะตัวชี้วัด) ต้องระบุพร้อมคำเตือนในโครงการและหนังสือชี้ชวน"},
        ),
        (FEE_CIRCULAR,), FEES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("performance fee", "fulcrum", "high water mark", "HWM", "hurdle rate", "benchmark"),
    ),
    Entry(
        "E04", "E",
        {"en": "Trailer fees: what selling agents must tell clients", "th": "trailer fee: สิ่งที่ตัวแทนขายต้องบอกลูกค้า"},
        {"en": "Fund companies pay selling agents an ongoing trailer fee. From 2026 that payment must match real "
               "advice, be disclosed, and be returned to the client if the service stops.",
         "th": "บลจ. จ่ายค่าตอบแทนต่อเนื่อง (trailer fee) แก่ตัวแทนขาย ตั้งแต่ปี 2569 ค่าตอบแทนต้องสอดคล้องกับคำแนะนำ"
               "ที่ให้จริง ต้องเปิดเผย และต้องคืนลูกค้าหากหยุดให้บริการ"},
        (
            {"en": "The payment must fit the advice or service the client gets and must not push the agent away "
                   "from the client's best interest.",
             "th": "ค่าตอบแทนต้องเหมาะสมกับคำแนะนำหรือบริการที่ลูกค้าได้รับ และต้องไม่จูงใจให้ขัดกับประโยชน์สูงสุดของลูกค้า"},
            {"en": "The prospectus says whether a trailer fee is paid, why, what service comes with it and the "
                   "conflicts it may cause.",
             "th": "หนังสือชี้ชวนต้องเปิดเผยว่ามีการจ่าย trailer fee หรือไม่ วัตถุประสงค์ บริการที่ได้รับ และความขัดแย้ง"
                   "ทางผลประโยชน์ที่อาจเกิดขึ้น"},
            {"en": "The selling agent gives clients a sales document: what it receives from the AMC, the service it "
                   "gives in return, and any conflict of interest (plus its house view, if the fund was picked "
                   "that way).",
             "th": "ตัวแทนขายต้องมีเอกสารประกอบการขายแจกลูกค้า: ค่าตอบแทนที่ได้รับจาก บลจ. บริการที่ให้ และความขัดแย้ง"
                   "ทางผลประโยชน์ (รวมถึง house view หากคัดเลือกกองทุนตามนั้น)"},
            {"en": "An agent that receives trailer fees must have SEC-approved staff advising clients on an ongoing "
                   "basis; if it cannot, it must return the trailer fee to the client.",
             "th": "ตัวแทนที่ได้รับ trailer fee ต้องมีบุคลากรที่ได้รับความเห็นชอบจาก ก.ล.ต. ให้คำแนะนำลูกค้าอย่างต่อเนื่อง "
                   "หากทำไม่ได้ต้องคืน trailer fee ให้ลูกค้าโดยไม่ชักช้า"},
            {"en": "AMCs must review their trailer fee payments within 3 years of February 2026.",
             "th": "บลจ. ต้องทบทวนการจ่าย trailer fee ภายใน 3 ปีนับแต่กุมภาพันธ์ 2569"},
        ),
        (FEE_CIRCULAR,), FEES_SINCE, CHECKED, ("ic", "ip", "firm"), (1, 2),
        ("trailer fee", "selling agent", "ตัวแทนขาย", "commission", "ค่าตอบแทน", "house view", "conflict"),
    ),
    Entry(
        "E05", "E",
        {"en": "Yearly fee review", "th": "การทบทวนค่าธรรมเนียมประจำปี"},
        {"en": "Every year the AMC reviews each fund's fees and its payments to selling agents, and reports to "
               "its board and the trustee.",
         "th": "ทุกปี บลจ. ต้องทบทวนค่าธรรมเนียมของแต่ละกองทุนและค่าตอบแทนตัวแทนขาย และรายงานคณะกรรมการบริษัท"
               "และผู้ดูแลผลประโยชน์"},
        (
            {"en": "The report goes to the board within 3 months of the AMC's year end, then to the trustee to "
                   "review and comment.",
             "th": "เสนอรายงานต่อคณะกรรมการบริษัทภายใน 3 เดือนนับแต่สิ้นรอบปีบัญชีของ บลจ. และรายงานผู้ดูแลผลประโยชน์"
                   "เพื่อสอบทานและให้ความเห็น"},
            {"en": "The trustee gives its view in the fund's 6-month and annual reports.",
             "th": "ผู้ดูแลผลประโยชน์ให้ความเห็นไว้ในรายงานรอบ 6 เดือนและรายงานประจำปีของกองทุน"},
            {"en": "Existing funds had to review their management fees within 1 year of February 2026.",
             "th": "กองทุนเดิมต้องทบทวนค่าธรรมเนียมการจัดการภายใน 1 ปีนับแต่กุมภาพันธ์ 2569"},
        ),
        (FEE_CIRCULAR,), FEES_SINCE, CHECKED, ("fund_manager", "firm"), (2,),
        ("fee review", "ทบทวนค่าธรรมเนียม", "board", "คณะกรรมการ", "trustee"),
    ),
    Entry(
        "E06", "E",
        {"en": "When a NAV or unit price is wrong", "th": "เมื่อมูลค่าหรือราคาหน่วยลงทุนไม่ถูกต้อง"},
        {"en": "A big pricing error (1 satang or more and 0.5% or more) must be recalculated, certified by the "
               "trustee and paid back to the investors affected.",
         "th": "ราคาผิดพลาดมาก (ตั้งแต่ 1 สตางค์ และตั้งแต่ 0.5%) ต้องคำนวณย้อนหลัง ให้ผู้ดูแลผลประโยชน์รับรอง และ"
               "ชดเชยผู้ลงทุนที่ได้รับผลกระทบ"},
        (
            {"en": "See the table “When a fund's price was wrong” on this page for each step and deadline.",
             "th": "ดูขั้นตอนและระยะเวลาในตาราง “เมื่อราคาหน่วยลงทุนไม่ถูกต้อง” ในหน้านี้"},
            {"en": "Price too low: buyers got too many units (cut back or the AMC pays), sellers got too little "
                   "(topped up). Price too high: the opposite.",
             "th": "ราคาต่ำกว่าที่ถูก: ผู้ซื้อได้หน่วยเกิน (ลดหน่วยหรือ บลจ. จ่ายแทน) ผู้ขายคืนได้เงินน้อยไป (ชดเชยเพิ่ม) "
                   "ราคาสูงกว่าที่ถูก: กลับกัน"},
            {"en": "If the error came from outside the AMC's control (e.g. a wrong exchange price) and the trustee "
                   "confirms it, the AMC doesn't have to pay from its own money where the client has no (or too few) units left.",
             "th": "หากเกิดจากปัจจัยภายนอกที่ควบคุมไม่ได้ (เช่น ราคาจากตลาดผิด) และผู้ดูแลผลประโยชน์รับรอง บลจ. ไม่ต้อง"
                   "จ่ายเงินของตนในกรณีที่ลูกค้าไม่มีหน่วยเหลือหรือเหลือไม่พอ"},
        ),
        (NAV_ERRORS,), FEES_SINCE, CHECKED, FUND_PEOPLE, (2,),
        ("NAV", "wrong price", "ราคาไม่ถูกต้อง", "compensation", "ชดเชย", "0.5%", "satang", "สตางค์"),
    ),
    Entry(
        "E07", "E",
        {"en": "Thai ESG fund: what it may invest in", "th": "กองทุน Thai ESG ลงทุนอะไรได้บ้าง"},
        {"en": "A Thai ESG fund keeps at least 80% of NAV (on average over its year) in Thai sustainability "
               "assets issued by the Thai state or Thai companies.",
         "th": "กองทุน Thai ESG ต้องลงทุนในทรัพย์สินด้านความยั่งยืนที่ออกโดยภาครัฐไทยหรือกิจการไทย โดยเฉลี่ยรอบปีบัญชี"
               "ไม่น้อยกว่า 80% ของ NAV"},
        (
            {"en": "SET/mai shares rated strong on environment or ESG by the SET or a recognised rater, or that "
                   "disclose greenhouse gas data with verified carbon footprints.",
             "th": "หุ้นใน SET/mai ที่ได้รับการคัดเลือกว่าโดดเด่นด้าน E หรือ ESG หรือที่เปิดเผยข้อมูลก๊าซเรือนกระจก"
                   "พร้อมทวนสอบคาร์บอนฟุตพริ้นท์"},
            {"en": "Shares with a corporate governance score (CGR) of 90 or more plus a published value-up plan – "
                   "or, since 1 March 2026, JUMP+ companies with CGR 90 or more.",
             "th": "หุ้นที่มีคะแนน CGR ตั้งแต่ 90 พร้อมเปิดเผยแผนเพิ่มมูลค่ากิจการ หรือตั้งแต่ 1 มี.ค. 2569 หุ้นในโครงการ "
                   "JUMP+ ที่มีคะแนน CGR ตั้งแต่ 90"},
            {"en": "Green, sustainability and sustainability-linked bonds (including government ones), "
                   "sustainability investment tokens, and ESG-rated infrastructure funds and REITs.",
             "th": "green bond, sustainability bond และ sustainability-linked bond (รวมพันธบัตรรัฐ) โทเคนดิจิทัล"
                   "กลุ่มความยั่งยืน และกองทุน infra หรือ REIT ที่ได้รับการคัดเลือกด้าน ESG"},
            {"en": "The tax deduction and holding period are Revenue Department rules – check them before advising.",
             "th": "วงเงินลดหย่อนและระยะเวลาถือครองเป็นเกณฑ์ของกรมสรรพากร ควรตรวจสอบก่อนให้คำแนะนำ"},
        ),
        (FUND_TYPES, THAI_ESG_CIRCULAR), "2026-03-01", CHECKED, FUND_PEOPLE, (2, 5),
        ("Thai ESG", "ThaiESG", "ESG", "ความยั่งยืน", "JUMP+", "CGR", "green bond", "tax", "ภาษี", "ลดหย่อน"),
    ),
    Entry(
        "E08", "E",
        {"en": "Thai ESG Extra (Thai ESGX) and the end of LTF", "th": "Thai ESGX และการสิ้นสุดของ LTF"},
        {"en": "Thai ESGX is a separate tax-benefit fund created in 2025: at least 65% in qualifying shares and "
               "80% in Thai ESG assets. Old LTF holders could switch into it in mid-2025.",
         "th": "Thai ESGX เป็นกองทุนสิทธิประโยชน์ทางภาษีที่ตั้งขึ้นในปี 2568 ต้องลงทุนในหุ้นที่เข้าเกณฑ์ไม่น้อยกว่า 65% และ"
               "ทรัพย์สิน Thai ESG ไม่น้อยกว่า 80% ผู้ถือ LTF สับเปลี่ยนเข้ามาได้ในกลางปี 2568"},
        (
            {"en": "Must be a new open-ended retail fund with no end date, named “…ไทยเพื่อความยั่งยืนแบบพิเศษ”; "
                   "it cannot be an RMF or SSF, and units cannot be transferred or pledged.",
             "th": "ต้องเป็นกองทุนเปิดใหม่ เสนอขายรายย่อย ไม่กำหนดอายุ ระบุ “ไทยเพื่อความยั่งยืนแบบพิเศษ” ท้ายชื่อ "
                   "ไม่เป็น RMF หรือ SSF และห้ามโอนหรือจำนำหน่วยลงทุน"},
            {"en": "2025 tax deductions per the SEC circular: LTF money switched 1 May–30 June 2025 up to "
                   "500,000 baht; new money in 2025 up to 300,000 baht (max 30% of income).",
             "th": "สิทธิลดหย่อนปี 2568 ตามหนังสือเวียน: เงินลงทุนเดิมที่สับเปลี่ยนจาก LTF ระหว่าง 1 พ.ค.–30 มิ.ย. 2568 สูงสุด "
                   "500,000 บาท เงินลงทุนใหม่ในปี 2568 สูงสุด 300,000 บาท (ไม่เกิน 30% ของเงินได้)"},
            {"en": "Performance is measured against a total return index (the SET's free-float TRI where there is one).",
             "th": "วัดผลเทียบกับดัชนีผลตอบแทนรวม (ใช้ free float TRI ของตลาดหลักทรัพย์ ถ้ามี)"},
            {"en": "LTFs lost their tax status and had to become ordinary funds (no “หุ้นระยะยาว” in the name) "
                   "by 31 December 2025.",
             "th": "LTF สิ้นสุดสิทธิประโยชน์ทางภาษี และต้องแก้ไขเป็นกองทุนรวมทั่วไป (ไม่มีคำว่า “หุ้นระยะยาว” ในชื่อ) "
                   "ภายใน 31 ธ.ค. 2568"},
        ),
        (THAI_ESGX_CIRCULAR, FUND_TYPES), "2025-04-16", CHECKED, FUND_PEOPLE, (2, 5),
        ("Thai ESGX", "ESGX", "LTF", "หุ้นระยะยาว", "switch", "สับเปลี่ยน", "tax", "ภาษี", "ลดหย่อน"),
    ),
]
