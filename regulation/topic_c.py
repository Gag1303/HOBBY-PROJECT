"""Topic C – Penalties (SEC Thailand).

Summarised in my own words from the personnel rule ทลธ. 8/2557 (sections 28–39), the penalty-level
circular กธ.(ว) 3/2561 and the IC penalty circular บธ.(ว) 44/2556, read on 2026-10-05 (copies kept in
the git-ignored data/sec/). The linked official documents are what counts.
"""

from regulation.model import Entry, Table
from regulation.sources import IC_PENALTY_2556, PENALTY_CIRCULAR, PERSONNEL_RULE, QUALIFICATION_TABLES

CHECKED = "2026-10-05"
EVERYONE = ("ic", "ip", "analyst", "fund_manager", "firm")

TABLES = [
    Table(
        "C", "⚖️", {"en": "Starting penalty for each kind of misconduct", "th": "ระดับโทษเริ่มต้นตามกลุ่มพฤติกรรม"},
        ({"en": "Kind of misconduct", "th": "กลุ่มพฤติกรรม"}, {"en": "Examples", "th": "ตัวอย่าง"},
         {"en": "Starting penalty", "th": "โทษเริ่มต้น"}),
        (
            ({"en": "1. Dishonesty", "th": "1. ส่อไปในทางทุจริต"},
             {"en": "Fraud or embezzlement of client assets; opening an account in someone else's name; using a "
                    "client's account without consent; finding nominees; using company data for yourself",
              "th": "ทุจริต ยักยอก ฉ้อโกงทรัพย์สินผู้ลงทุน เปิดบัญชีในชื่อผู้อื่น ใช้บัญชีลูกค้าโดยไม่ยินยอม จัดหา nominee "
                    "นำข้อมูลบริษัทไปใช้ประโยชน์ส่วนตัว"},
             {"en": "Revoked for 4–5 years or more", "th": "เพิกถอน 4–5 ปีขึ้นไป"}),
            ({"en": "2. Taking advantage of investors", "th": "2. แสวงหาประโยชน์หรือเอาเปรียบผู้ลงทุน"},
             {"en": "Using a client's account with consent; churning; managing a portfolio for a share of profit; "
                    "selling IPO/off-market shares for your own benefit",
              "th": "ใช้บัญชีลูกค้าโดยลูกค้ายินยอม ชักชวนให้ซื้อขายบ่อย (churning) รับบริหารพอร์ตโดยเรียกผลตอบแทน "
                    "ขายหุ้น IPO/หุ้นนอกตลาดโดยได้ประโยชน์ตอบแทน"},
             {"en": "Suspended 1 year – revoked 2 years", "th": "พัก 1 ปี – เพิกถอน 2 ปี"}),
            ({"en": "3. Lack of professional care", "th": "3. ไม่ปฏิบัติด้วยความรับผิดชอบและรอบคอบเยี่ยงผู้ประกอบวิชาชีพ"},
             {"en": "False or misleading information; incomplete KYC/CDD or suitability test; untrue order records; "
                    "signing for work not done; inaccurate or non-independent advice; deciding for clients",
              "th": "ให้ข้อมูลเท็จหรือปกปิด ทำ KYC/CDD หรือ suitability test ไม่ครบ บันทึกคำสั่งไม่ตรงความจริง ลงนามโดยไม่ได้"
                    "ทำหน้าที่จริง ให้คำแนะนำไม่ถูกต้องหรือไม่เป็นอิสระ ตัดสินใจซื้อขายแทนลูกค้า"},
             {"en": "Suspended 3 months or 1 year – revoked 2 years", "th": "พัก 3 เดือน หรือ 1 ปี – เพิกถอน 2 ปี"}),
            ({"en": "4. Failure to supervise", "th": "4. ละเลยการตรวจสอบดูแลตามสมควร"},
             {"en": "Managers who don't put proper systems in place or don't act when they learn of problems",
              "th": "ผู้บริหารที่ไม่จัดให้มีระบบงานที่เพียงพอ หรือไม่แก้ไขเมื่อรู้ถึงปัญหา"},
             {"en": "Suspended 6 months – revoked 2 years", "th": "พัก 6 เดือน – เพิกถอน 2 ปี"}),
        ),
        PENALTY_CIRCULAR,
        {"en": "executives and fund managers start at double for groups 1–3",
         "th": "ผู้บริหารและผู้จัดการกองทุนเริ่มต้นที่ 2 เท่าสำหรับกลุ่มที่ 1–3"},
    ),
]

ENTRIES = [
    Entry(
        "C01", "C",
        {"en": "What counts as misconduct (group 3 disqualification)",
         "th": "พฤติกรรมที่ถือเป็นลักษณะต้องห้ามกลุ่มที่ 3"},
        {"en": "Besides the fixed disqualifications (Topic A), the SEC can act when there are reasonable grounds "
               "to believe someone behaved improperly – now or in the past.",
         "th": "นอกจากลักษณะต้องห้ามกลุ่มที่ 1–2 (หัวข้อ A) ก.ล.ต. ดำเนินการได้เมื่อมีเหตุอันควรเชื่อว่ามีหรือเคยมี"
               "พฤติกรรมไม่เหมาะสม"},
        (
            {"en": "Breaking the duty of honesty and fairness, lacking responsibility or care, taking advantage of "
                   "investors, or breaking ethics/professional standards – or helping someone else do it.",
             "th": "ประพฤติผิดต่อหน้าที่ซื่อสัตย์สุจริตและเป็นธรรม ขาดความรับผิดชอบและความรอบคอบ เอาเปรียบผู้ลงทุน หรือ"
                   "ขาดจรรยาบรรณและมาตรฐานวิชาชีพ หรือมีส่วนร่วม/สนับสนุนผู้อื่นกระทำ"},
            {"en": "Failing to supervise, so that the company or staff under you break securities law in a way "
                   "that harms confidence or clients.",
             "th": "ละเลยการตรวจสอบดูแลตามสมควร จนนิติบุคคลหรือผู้ใต้บังคับบัญชาฝ่าฝืนกฎหมายหลักทรัพย์ อันอาจทำให้"
                   "เสื่อมความเชื่อมั่นหรือเกิดความเสียหายต่อลูกค้า"},
            {"en": "Dishonest conduct that seriously damages your credibility – e.g. abusing your position for "
                   "benefit, or cheating in an exam.",
             "th": "พฤติกรรมส่อไปในทางไม่สุจริตที่กระทบความน่าเชื่อถืออย่างมีนัยสำคัญ เช่น อาศัยตำแหน่งแสวงหาประโยชน์ "
                   "หรือทุจริตการสอบ"},
        ),
        (PERSONNEL_RULE,), "2017-10-01", CHECKED, EVERYONE, (1,),
        ("misconduct", "ลักษณะต้องห้าม", "group 3", "กลุ่มที่ 3", "exam cheating"),
    ),
    Entry(
        "C02", "C",
        {"en": "What the SEC can do", "th": "ก.ล.ต. ดำเนินการอะไรได้บ้าง"},
        {"en": "Depending on the case the SEC refuses, suspends or revokes approval, and can bar a new "
               "application for up to 10 years.",
         "th": "แล้วแต่กรณี ก.ล.ต. ปฏิเสธ สั่งพัก หรือเพิกถอนความเห็นชอบ และกำหนดระยะเวลาห้ามยื่นคำขอใหม่ได้ไม่เกิน 10 ปี"},
        (
            {"en": "Group 1 disqualifications and group 2 criminal/asset-seizure cases: revocation. Other group 2 "
                   "cases: suspension or revocation. Group 3: suspension or revocation as the case deserves.",
             "th": "ลักษณะต้องห้ามกลุ่มที่ 1 และกลุ่มที่ 2 กรณีต้องคำพิพากษาหรือถูกริบทรัพย์: เพิกถอน กลุ่มที่ 2 กรณีอื่น: "
                   "พักหรือเพิกถอน กลุ่มที่ 3: พักหรือเพิกถอนตามสมควรแก่กรณี"},
            {"en": "A suspension cannot be longer than the approval's remaining term; afterwards you return to the "
                   "same role without re-applying.",
             "th": "ระยะเวลาสั่งพักต้องไม่เกินอายุความเห็นชอบที่เหลือ เมื่อพ้นแล้วกลับไปปฏิบัติหน้าที่เดิมได้โดยไม่ต้องยื่นใหม่"},
            {"en": "Minor cases, or behaviour more than 10 years old, may be dropped or only publicly disclosed.",
             "th": "กรณีไม่ร้ายแรงหรือเกิดขึ้นเกิน 10 ปี อาจไม่นำมาพิจารณา หรือลดระดับเป็นการเปิดเผยพฤติกรรมแทน"},
            {"en": "Staff who don't need SEC approval are barred from the role by their firm instead.",
             "th": "บุคลากรที่ไม่ต้องได้รับความเห็นชอบ ผู้ประกอบธุรกิจต้องห้ามบุคคลนั้นปฏิบัติหน้าที่แทน"},
        ),
        (PERSONNEL_RULE,), "2017-10-01", CHECKED, EVERYONE, (1,),
        ("suspend", "พัก", "revoke", "เพิกถอน", "ban", "10 years"),
    ),
    Entry(
        "C03", "C",
        {"en": "Starting penalties by kind of misconduct", "th": "ระดับโทษเริ่มต้นตามกลุ่มพฤติกรรม"},
        {"en": "Since March 2018 the SEC starts from a set penalty for each of 4 kinds of misconduct, then "
               "adjusts it for the facts of the case.",
         "th": "ตั้งแต่มีนาคม 2561 ก.ล.ต. กำหนดโทษเริ่มต้นตามกลุ่มพฤติกรรม 4 กลุ่ม แล้วปรับตามข้อเท็จจริงของแต่ละกรณี"},
        (
            {"en": "See the table “Starting penalty for each kind of misconduct” on this page.",
             "th": "ดูตาราง “ระดับโทษเริ่มต้นตามกลุ่มพฤติกรรม” ในหน้านี้"},
            {"en": "Executives and fund managers who commit groups 1–3 start at double the penalty.",
             "th": "ผู้บริหารและผู้จัดการกองทุนที่กระทำผิดกลุ่มที่ 1–3 มีโทษเริ่มต้นเป็น 2 เท่า"},
            {"en": "Since 2014 the SEC has been especially strict with ICs who use clients' accounts, trade "
                   "without orders, take discretion or don't record advice and orders fully.",
             "th": "ตั้งแต่ปี 2557 ก.ล.ต. ลงโทษ IC หนักขึ้นในกรณีใช้บัญชีลูกค้า ซื้อขายโดยลูกค้าไม่ได้สั่ง รับมอบหมายให้"
                   "ตัดสินใจแทน และไม่บันทึกการให้คำแนะนำและรับคำสั่งให้ครบถ้วน"},
        ),
        (PENALTY_CIRCULAR, IC_PENALTY_2556), "2018-03-01", CHECKED, EVERYONE, (1,),
        ("penalty", "โทษ", "churning", "nominee", "fraud", "ทุจริต"),
    ),
    Entry(
        "C04", "C",
        {"en": "How the SEC decides – and your right to explain", "th": "ก.ล.ต. พิจารณาอย่างไร และสิทธิชี้แจง"},
        {"en": "Before suspending or revoking for misconduct, the SEC lets you explain and asks an independent "
               "committee for its view.",
         "th": "ก่อนสั่งพักหรือเพิกถอนจากพฤติกรรมไม่เหมาะสม ก.ล.ต. ต้องให้โอกาสชี้แจงและขอความเห็นจากคณะกรรมการ"},
        (
            {"en": "Factors: your role and behaviour, penalties already received, harm caused, what you did to "
                   "fix or prevent it, cooperation with (or obstruction of) the SEC, and your past record.",
             "th": "ปัจจัยที่พิจารณา: บทบาทและพฤติกรรม โทษที่ได้รับไปแล้ว ผลกระทบหรือความเสียหาย การแก้ไขเยียวยา "
                   "การให้ความร่วมมือหรือขัดขวาง และประวัติในอดีต"},
            {"en": "The committee has up to 5 outside experts, including an investor representative, a trading "
                   "expert and 2 nominated by industry associations.",
             "th": "คณะกรรมการมีผู้ทรงคุณวุฒิภายนอกไม่เกิน 5 คน รวมผู้แทนผู้ลงทุน ผู้ทรงคุณวุฒิด้านการซื้อขาย และผู้ที่"
                   "สมาคมเสนออีก 2 คน"},
            {"en": "If the stock or derivatives exchange (or ThaiBMA) already punished you for the same thing – "
                   "other than with a fine – the SEC may decide not to punish again.",
             "th": "ถ้าตลาดหลักทรัพย์ ศูนย์ซื้อขายสัญญาซื้อขายล่วงหน้า หรือสมาคมตลาดตราสารหนี้ไทยลงโทษในเรื่องเดียวกันแล้ว "
                   "(ที่ไม่ใช่การปรับเงิน) ก.ล.ต. อาจไม่ลงโทษซ้ำ"},
        ),
        (PERSONNEL_RULE,), "2021-03-16", CHECKED, EVERYONE, (1,),
        ("committee", "คณะกรรมการ", "explain", "ชี้แจง", "appeal"),
    ),
    Entry(
        "C05", "C",
        {"en": "After a penalty: what it costs your career", "th": "หลังถูกลงโทษ: ผลต่ออาชีพ"},
        {"en": "A penalty is public and follows you: firms must report problems, the SEC publishes penalties, and "
               "coming back means extra exams.",
         "th": "การถูกลงโทษเป็นข้อมูลสาธารณะและติดตัว: ผู้ประกอบธุรกิจต้องรายงาน ก.ล.ต. เผยแพร่ข่าวการลงโทษ และการกลับมา"
               "ต้องสอบเพิ่ม"},
        (
            {"en": "After a suspension an IP passes the rules exam again; after a revocation, all exams including "
                   "ethics (see A10).",
             "th": "หลังถูกสั่งพัก IP ต้องสอบกฎระเบียบใหม่ ถ้าถูกเพิกถอนต้องสอบใหม่ทุกส่วนรวมถึงจรรยาบรรณ (ดู A10)"},
            {"en": "The SEC publishes news of penalties, and your firm is held responsible for supervising you.",
             "th": "ก.ล.ต. เผยแพร่ข่าวการลงโทษต่อสาธารณะ และบริษัทต้นสังกัดมีหน้าที่กำกับดูแลบุคลากรของตน"},
            {"en": "A ban on re-applying can last up to 10 years per case.",
             "th": "การห้ามยื่นคำขอใหม่อาจยาวถึง 10 ปีต่อกรณี"},
        ),
        (PERSONNEL_RULE, QUALIFICATION_TABLES, IC_PENALTY_2556), "2025-07-01", CHECKED, EVERYONE, (1,),
        ("career", "อาชีพ", "public", "เผยแพร่", "re-apply"),
    ),
]
