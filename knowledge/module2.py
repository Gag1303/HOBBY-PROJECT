"""Module 2 (Investment planning): the course structure of the 2021 updated course.

Chapters, parts and the number of learning objectives (LOS) per chapter come from TFPA's learning outcome
statements for Module 2 and its course structure summary (exam: 120 questions, 4 h 30 min, pass 70% overall
and 70% in the product and sales-practice parts). Read on 2026-10-10.
"""

from knowledge.model import Chapter

LOS_URL = "https://www.tfpa.or.th/Upload/03_LOS_New%20M2.pdf"

PARTS = {
    "foundation": {"en": "Part 1 · Foundations (10 exam questions)", "th": "ส่วนที่ 1 · ความรู้พื้นฐาน (ข้อสอบ 10 ข้อ)"},
    "products": {"en": "Part 2 · Investment products (55 exam questions)",
                 "th": "ส่วนที่ 2 · ผลิตภัณฑ์การลงทุน (ข้อสอบ 55 ข้อ)"},
    "planning": {"en": "Part 3 · Investment planning (40 exam questions)",
                 "th": "ส่วนที่ 3 · การวางแผนการลงทุน (ข้อสอบ 40 ข้อ)"},
}

CHAPTERS = [
    Chapter(2, 1, "foundation", {"en": "Financial markets", "th": "ตลาดการเงิน"}, 13),
    Chapter(2, 2, "foundation", {"en": "Return and risk", "th": "ผลตอบแทนและความเสี่ยงจากการลงทุน"}, 23),
    Chapter(2, 3, "foundation", {"en": "Fundamental and technical analysis",
                                 "th": "การวิเคราะห์หลักทรัพย์โดยใช้ปัจจัยพื้นฐานและปัจจัยทางเทคนิค"}, 31),
    Chapter(2, 4, "products", {"en": "Plain capital market products and valuation",
                               "th": "ผลิตภัณฑ์ในตลาดทุนที่ไม่มีความซับซ้อนและการประเมินมูลค่า"}, 123),
    Chapter(2, 5, "products", {"en": "High-risk and complex products",
                               "th": "ผลิตภัณฑ์ในตลาดทุนที่มีความเสี่ยงสูงหรือความซับซ้อน"}, 24),
    Chapter(2, 6, "products", {"en": "Alternative and foreign investments",
                               "th": "การลงทุนทางเลือกและการลงทุนในหลักทรัพย์ต่างประเทศ"}, 52),
    Chapter(2, 7, "products", {"en": "Derivatives", "th": "สัญญาซื้อขายล่วงหน้า"}, 66),
    Chapter(2, 8, "planning", {"en": "Asset allocation", "th": "การจัดสรรสินทรัพย์ลงทุน"}, 16),
    Chapter(2, 9, "planning", {"en": "Portfolio management strategies", "th": "กลยุทธ์การบริหารกลุ่มหลักทรัพย์"}, 11),
    Chapter(2, 10, "planning", {"en": "Portfolio monitoring and rebalancing", "th": "การติดตามและปรับปรุงกลุ่มหลักทรัพย์"}, 6),
    Chapter(2, 11, "planning", {"en": "Wealth management and behavioural finance",
                                "th": "การบริหารความมั่งคั่งและการเงินเชิงพฤติกรรม"}, 11),
]
