"""CFP reading list: books to borrow from the Maruey Library (ห้องสมุดมารวย, SET), by CFP module.

Only catalog facts (title, author, publisher, pages, call number, link) taken from Maruey's public
catalog on 2026-10-07, plus a one-line note in my own words on why the book is worth reading. No book
content is copied: borrow the book at Maruey (free Trial Member, or eBook / full membership).
"""

from dataclasses import dataclass

MARUEY = "https://www.maruey.com"
CATALOG_CHECKED = "2026-10-07"
SET_LIBRARY = "ตลาดหลักทรัพย์แห่งประเทศไทย"
CFP_COURSE = "สถาบันกองทุนเพื่อพัฒนาตลาดทุน / ศูนย์ส่งเสริมการพัฒนาความรู้ตลาดทุน (SET)"

Text = dict  # {"en": ..., "th": ...}


@dataclass(frozen=True)
class Book:
    id: str            # stable key, used by my notes
    module: int        # CFP module it belongs to
    title: str         # as in the catalog (Thai or English)
    author: str
    publisher: str
    note: Text         # why read it, in my own words
    book: str = ""     # Maruey printed-book page ("" if none)
    ebook: str = ""    # Maruey eBook page ("" if none)
    pages: str = ""
    call_no: str = ""  # shelf number of the printed book
    core: bool = False  # the official Thai CFP course text for this module
    lang: str = "th"

    @property
    def links(self) -> list[tuple[str, str]]:
        return [(kind, url) for kind, url in (("book", self.book), ("ebook", self.ebook)) if url]


def _b(path: str) -> str:
    return f"{MARUEY}/{path}"


BOOKS = [
    # ---------- Module 1: foundation of financial planning, tax and ethics ----------
    Book("m1-course", 1, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 1 พื้นฐานการวางแผนการเงิน", CFP_COURSE, SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 1 – start here.",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 1 ควรเริ่มที่เล่มนี้"},
         book=_b("book/686587f59f7da"), ebook=_b("ebook/6866f8734afa8"), pages="336", call_no="PL00027", core=True),
    Book("m1-ethics", 1, "จรรยาบรรณและคู่มือการปฎิบัติงานสำหรับนักวางแผนการเงิน", "สมาคมนักวางแผนการเงินไทย (TFPA)",
         "เอส แอล พลับบลิเคชั่น",
         {"en": "TFPA's code of ethics and practice standards – examined in module 1 and needed for the CFP mark.",
          "th": "จรรยาบรรณและมาตรฐานการปฏิบัติงานของ TFPA ใช้สอบชุดวิชาที่ 1 และจำเป็นต่อการได้รับเครื่องหมาย CFP"},
         book=_b("book/68657c9374326"), ebook=_b("ebook/6866f2e912519"), pages="128", call_no="PL00007", core=True),
    Book("m1-competency", 1, "The financial planning competency handbook", "CFP Board (ed. Charles R. Chaffin)", "Wiley",
         {"en": "The US CFP Board's full handbook of what a planner must know – useful if you plan to work abroad.",
          "th": "คู่มือความรู้ที่นักวางแผนการเงินต้องมีของ CFP Board สหรัฐฯ เหมาะหากวางแผนทำงานต่างประเทศ"},
         book=_b("book/6864570ce109c"), ebook=_b("ebook/686775508f64a"), pages="735", call_no="PF00100", lang="en"),
    Book("m1-psychology", 1, "The psychology of financial planning", "Brad Klontz, Charles Chaffin, Ted Klontz",
         "John Wiley & Sons",
         {"en": "How money beliefs and behaviour affect clients – now part of the CFP Board's exam topics.",
          "th": "ความเชื่อและพฤติกรรมทางการเงินของลูกค้า ซึ่งเป็นหัวข้อสอบของ CFP Board แล้ว"},
         book=_b("book/686458832dc8f"), pages="264", call_no="PF00233", lang="en"),
    Book("m1-altfest", 1, "Personal financial planning", "Lewis J. Altfest", "McGraw-Hill Irwin",
         {"en": "A classic university textbook that covers the whole planning process end to end.",
          "th": "ตำรามหาวิทยาลัยคลาสสิกที่ครอบคลุมกระบวนการวางแผนการเงินทั้งหมด"},
         book=_b("book/6864518458a3e"), pages="624", call_no="PF00042", lang="en"),
    Book("m1-set-basics", 1, "เงินทองต้องใส่ใจ เล่ม 1 : วางแผนการเงินส่วนบุคคล", "กิตติพัฒน์ แสนทวีสุข", SET_LIBRARY,
         {"en": "A short, easy SET book on personal financial planning – good before the course text.",
          "th": "หนังสือ SET อ่านง่ายเรื่องวางแผนการเงินส่วนบุคคล เหมาะอ่านก่อนตำราหลักสูตร"},
         book=_b("book/68657c784f65d"), pages="232", call_no="SP00011"),

    # ---------- Module 2: investment planning ----------
    Book("m2-course", 2, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 2 การวางแผนการลงทุน", CFP_COURSE, SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 2.",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 2"},
         book=_b("book/686587f641525"), ebook=_b("ebook/6866f8abee8ce"), pages="532", call_no="PL00020", core=True),
    Book("m2-ic-fund", 2, "ผู้แนะนำการลงทุนด้านกองทุน = Fund investment consultant", "สมาคมบริษัทจัดการลงทุน (AIMC)", "AIMC",
         {"en": "Study book for the fund investment consultant licence (IC fund) – also covers the fund rules in Law & Regulation.",
          "th": "ตำราสอบผู้แนะนำการลงทุนด้านกองทุน (IC กองทุน) ครอบคลุมกฎเกณฑ์กองทุนในหน้ากฎหมายและกฎเกณฑ์ด้วย"},
         book=_b("book/68658180da46c"), pages="575", call_no="PL00033"),
    Book("m2-ip", 2, "ผู้วางแผนการลงทุน (Investment Planner) : ผู้ทำหน้าที่ขายหน่วยลงทุนกองทุนรวม", "สมาคมบริษัทจัดการลงทุน (AIMC)",
         "เอส แอล พลับบลิเคชั่น",
         {"en": "Study book for the investment planner (IP) licence – the licence closest to CFP work (see A05).",
          "th": "ตำราสอบผู้วางแผนการลงทุน (IP) ใบอนุญาตที่ใกล้เคียงงาน CFP ที่สุด (ดู A05)"},
         book=_b("book/6865817d0511f"), pages="402", call_no="PL00002"),
    Book("m2-ic-securities", 2, "ตลาดการเงินและการลงทุนในหลักทรัพย์ : หลักสูตรผู้แนะนำการลงทุนด้านหลักทรัพย์",
         "สถาบันพัฒนาความรู้ตลาดทุน", SET_LIBRARY,
         {"en": "Study book for the securities investment consultant licence (IC securities).",
          "th": "ตำราสอบผู้แนะนำการลงทุนด้านหลักทรัพย์ (IC หลักทรัพย์)"},
         book=_b("book/68657e1f44dde"), pages="654", call_no="PL00026"),
    Book("m2-complex", 2, "หลักสูตรผู้แนะนำการลงทุนตราสารซับซ้อน (P2) : ตราสารหนี้และกองทุนรวมที่ซับซ้อน",
         "ศูนย์ส่งเสริมการพัฒนาความรู้ตลาดทุน", SET_LIBRARY,
         {"en": "Study book for the complex products add-on (P2) – see B04 on complex products.",
          "th": "ตำราสอบตราสารซับซ้อน (P2) ดู B04 เรื่องผลิตภัณฑ์ซับซ้อน"},
         book=_b("book/686587eecbc93"), pages="160", call_no="PL00038"),
    Book("m2-funds", 2, "รู้วิเคราะห์...เจาะเรื่องกองทุนรวม", "ธนัยวงศ์ กีรติวานิชย์, ภัสรา ชวาลกร", SET_LIBRARY,
         {"en": "How to read and compare mutual funds – pairs with the Thai mutual funds page.",
          "th": "วิธีอ่านและเปรียบเทียบกองทุนรวม ใช้คู่กับหน้ากองทุนรวมไทยในแอป"},
         book=_b("book/68658471eb6e1"), pages="158", call_no="SP00007"),
    Book("m2-bonds", 2, "รู้วิเคราะห์...เจาะเรื่องตราสารหนี้", "ศุภชัย ศรีสุชาติ", SET_LIBRARY,
         {"en": "Bonds explained for Thai investors – duration, credit risk and pricing.",
          "th": "ตราสารหนี้สำหรับผู้ลงทุนไทย ทั้ง duration ความเสี่ยงด้านเครดิต และการคำนวณราคา"},
         book=_b("book/686584728bad0"), pages="244", call_no="SP00010"),
    Book("m2-ferri", 2, "All about asset allocation", "Richard A. Ferri", "McGraw-Hill",
         {"en": "A clear, practical guide to building a diversified portfolio.",
          "th": "คู่มือจัดสรรสินทรัพย์ให้กระจายความเสี่ยงที่อ่านง่ายและใช้ได้จริง"},
         book=_b("book/6864383e45126"), pages="302", call_no="IK00058", lang="en"),
    Book("m2-bernstein", 2, "The intelligent asset allocator", "William J. Bernstein", "McGraw-Hill",
         {"en": "Why the mix of assets matters more than picking winners – short and readable.",
          "th": "ทำไมสัดส่วนสินทรัพย์สำคัญกว่าการเลือกหุ้นเด่น อ่านสั้นและเข้าใจง่าย"},
         book=_b("book/6864579070110"), pages="207", call_no="IK00008", lang="en"),

    # ---------- Module 3: insurance planning ----------
    Book("m3-course", 3, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 3 การวางแผนการประกันภัย", CFP_COURSE, SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 3.",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 3"},
         book=_b("book/686587f6d1d09"), ebook=_b("ebook/6866f8f0de252"), pages="364", call_no="PL00020", core=True),
    Book("m3-insurance", 3, "การประกันภัย = Insurance", "บุษรา อึ๊งภากรณ์", "กระทรวงพาณิชย์",
         {"en": "Thai textbook on insurance principles and types of cover.",
          "th": "ตำราไทยว่าด้วยหลักการประกันภัยและประเภทความคุ้มครอง"},
         book=_b("book/6865795980795"), pages="304", call_no="PF00001"),
    Book("m3-law", 3, "คำอธิบายกฎหมายลักษณะประกันภัย ศึกษาแบบเรียงมาตรา", "สรพลจ์ สุขทรรศนีย์", "วิญญูชน",
         {"en": "The Civil and Commercial Code on insurance, section by section.",
          "th": "ประมวลกฎหมายแพ่งและพาณิชย์ลักษณะประกันภัย อธิบายเรียงมาตรา"},
         book=_b("book/68657b1fbe863"), pages="178", call_no="LR00089"),
    Book("m3-rejda", 3, "Principles of risk management and insurance", "George E. Rejda", "HarperCollins",
         {"en": "The standard international textbook on risk management and insurance.",
          "th": "ตำรามาตรฐานสากลด้านการบริหารความเสี่ยงและการประกันภัย"},
         book=_b("book/686451f055917"), call_no="IK00113", lang="en"),
    Book("m3-life-health", 3, "Life and health insurance", "Kenneth Black, Harold D. Skipper Jr.", "Prentice Hall",
         {"en": "In-depth reference on life and health insurance products and pricing.",
          "th": "ตำราอ้างอิงเชิงลึกเรื่องผลิตภัณฑ์และการกำหนดราคาประกันชีวิตและสุขภาพ"},
         book=_b("book/68644f03c12b0"), pages="1054", call_no="PF00002", lang="en"),
    Book("m3-life-easy", 3, "ล้วงลึก รู้ทันประกันชีวิต", "Mr. Financial", "GOODLIFE PUBLISHING",
         {"en": "An easy Thai read on choosing life insurance from the buyer's side.",
          "th": "อ่านง่าย มุมมองผู้ซื้อในการเลือกประกันชีวิต"},
         book=_b("book/68658505dbc55"), pages="144", call_no="PF00067"),

    # ---------- Module 4: retirement planning ----------
    Book("m4-course", 4, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 4 การวางแผนเพื่อวัยเกษียณ", CFP_COURSE, SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 4.",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 4"},
         book=_b("book/686587f7711a7"), ebook=_b("ebook/6866f90f19dcf"), pages="364", call_no="PL00020", core=True),
    Book("m4-tfpa", 4, "เกษียณแบบ Well Done สุขภาพแบบพอดี", "สมาคมนักวางแผนการเงินไทย (TFPA)", "TFPA",
         {"en": "TFPA's own short guide to retirement money and health.",
          "th": "คู่มือสั้นของ TFPA เรื่องเงินและสุขภาพยามเกษียณ"},
         book=_b("book/686579dcc6e87"), pages="154", call_no="SP00063"),
    Book("m4-pvd-qa", 4, "ถามมา-ตอบไปกับกองทุนสำรองเลี้ยงชีพ", "สำนักงาน ก.ล.ต.", "สำนักงาน ก.ล.ต.",
         {"en": "The SEC's Q&A on provident funds – what employees usually ask.",
          "th": "ถาม-ตอบเรื่องกองทุนสำรองเลี้ยงชีพของ ก.ล.ต. คำถามที่ลูกจ้างมักถาม"},
         book=_b("book/68657e991c7d1"), call_no="IK00001"),
    Book("m4-pvd-pro", 4, "องค์ความรู้บริหารกองทุนสำรองเลี้ยงชีพแบบมืออาชีพ", "สมาคมกองทุนสำรองเลี้ยงชีพ",
         "สมาคมกองทุนสำรองเลี้ยงชีพ",
         {"en": "How provident funds are run professionally – committees, investment policy, employee choice.",
          "th": "การบริหารกองทุนสำรองเลี้ยงชีพแบบมืออาชีพ ทั้งคณะกรรมการ นโยบายการลงทุน และการเลือกแผนของสมาชิก"},
         book=_b("book/68658848669c9"), pages="412", call_no="IK00024"),
    Book("m4-rmf", 4, "ยิ่งลงทุน ยิ่งรวย เกษียณสุขและมั่งคั่ง ด้วยกองทุนรวม RMF", "สรวิศ อิ่มบำรุง", "แฟมิลี่ โนฮาว",
         {"en": "Using RMFs for retirement – check the tax rules again, they have changed since (see D07).",
          "th": "ใช้ RMF วางแผนเกษียณ ควรตรวจเงื่อนไขภาษีปัจจุบันอีกครั้งเพราะมีการเปลี่ยนแปลง (ดู D07)"},
         book=_b("book/6865837713db3"), pages="260", call_no="IK00012"),
    Book("m4-10m", 4, "มี 10 ล้าน ก่อน 60 ต้องทำอย่างไร = Retirement planning absolute essentials", "ธีระ ภู่ตระกูล",
         "ซีเอ็ดยูเคชั่น",
         {"en": "Step-by-step Thai retirement planning with worked numbers.",
          "th": "วางแผนเกษียณแบบไทยทีละขั้น พร้อมตัวอย่างการคำนวณ"},
         book=_b("book/6865830e2a91d"), pages="221", call_no="PF00007"),
    Book("m4-leimberg", 4, "Tools & techniques of employee benefit & retirement planning", "Stephan R. Leimberg, John J. McFadden",
         "National Underwriter",
         {"en": "Professional reference on employee benefits and retirement plans (US-based).",
          "th": "ตำราอ้างอิงสำหรับมืออาชีพเรื่องสวัสดิการลูกจ้างและแผนเกษียณ (อิงสหรัฐฯ)"},
         book=_b("book/68657668e837e"), call_no="PF00001", lang="en"),
    Book("m4-quinn", 4, "How to make your money last", "Jane Bryant Quinn", "",
         {"en": "How to turn savings into income that lasts through retirement.",
          "th": "เปลี่ยนเงินออมเป็นรายได้ที่พอใช้ตลอดวัยเกษียณ"},
         book=_b("book/68644d28e10a1"), pages="366", call_no="PF00020", lang="en"),
    Book("m4-nrri", 4, "ดัชนีชี้วัดความพร้อมด้านการเกษียณอายุแห่งชาติ ปี 2566", "คณะพาณิชยศาสตร์และการบัญชี จุฬาฯ",
         "Capital Market Research Institute (CMRI)",
         {"en": "Thailand's retirement readiness index – data on how prepared Thais are.",
          "th": "ดัชนีความพร้อมการเกษียณของไทย ข้อมูลว่าคนไทยพร้อมแค่ไหน"},
         ebook=_b("ebook/6867683c10834"), pages="20"),

    # ---------- Module 5: tax & estate planning ----------
    Book("m5-course", 5, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 5 คำอธิบายประมวลรัษฎากร ภาษีเงินได้บุคคลธรรมดา",
         "ไพจิตร โรจนวานิช และคนอื่น ๆ", SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 5 (personal income tax).",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 5 (ภาษีเงินได้บุคคลธรรมดา)"},
         book=_b("book/686587f815a67"), call_no="PL00034", core=True),
    Book("m5-tax-guide", 5, "คู่มือภาษี ฉบับบุคคลธรรมดา", "สุนิติ ถนัดวณิชย์", SET_LIBRARY,
         {"en": "A short SET guide to personal income tax – check the year, deductions change often.",
          "th": "คู่มือภาษีบุคคลธรรมดาฉบับสั้นของ SET ควรดูปีที่พิมพ์ เพราะค่าลดหย่อนเปลี่ยนบ่อย"},
         book=_b("book/68657be9134f6"), pages="144", call_no="SP00030"),
    Book("m5-taxbugnoms", 5, "ตัดภาษี มีเงินออม : TaxBugnoms ช่วยได้", "TaxBugnoms", "ธิงค์ บียอนด์",
         {"en": "Easy Thai read linking tax deductions with saving and investing.",
          "th": "อ่านง่าย เชื่อมการลดหย่อนภาษีกับการออมและลงทุน"},
         book=_b("book/68657e39bc945"), pages="232", call_no="PF00012"),
    Book("m5-inheritance-tax", 5, "ภาษีการรับมรดก ฉบับสมบูรณ์", "กิติพงศ์ อุรพีพัฒนพงศ์", "อมรินทร์",
         {"en": "Thailand's inheritance tax explained in full.",
          "th": "อธิบายภาษีการรับมรดกของไทยอย่างครบถ้วน"},
         book=_b("book/686582b2a947f"), pages="184", call_no="LR00081"),
    Book("m5-estate-easy", 5, "มรดกชิลชิล... : จัดการได้ไม่ต้องรอรวย", "ปภาสร แก้วกอบสิน", "ซีเอ็ดยูเคชั่น",
         {"en": "Estate planning for ordinary people – wills, heirs and transfers.",
          "th": "วางแผนมรดกสำหรับคนทั่วไป ทั้งพินัยกรรม ทายาท และการโอน"},
         book=_b("book/686582cb33374"), pages="160", call_no="LR00065"),
    Book("m5-land-tax", 5, "วางแผนภาษีที่ดิน ภาษีมรดก", "พิชัย ยอดพฤติการ", "แสงมงคลออฟเซ็ทการพิมพ์",
         {"en": "Land and building tax together with inheritance tax planning.",
          "th": "การวางแผนภาษีที่ดินและสิ่งปลูกสร้างควบคู่กับภาษีมรดก"},
         book=_b("book/686585b685d3a"), pages="176", call_no="PF00024"),
    Book("m5-insurance-tax", 5, "ใช้ประกันฯ ลดภาษีทำได้ง่ายๆ", "กฤษฎา กฤษณะเศรณี", "ธิงค์ บียอนด์ บุ๊คส์",
         {"en": "How life and health insurance premiums reduce tax – links modules 3 and 5.",
          "th": "ใช้เบี้ยประกันชีวิตและสุขภาพลดหย่อนภาษี เชื่อมชุดวิชาที่ 3 กับ 5"},
         book=_b("book/68657d94c2fe4"), pages="200", call_no="PF00011"),
    Book("m5-maple", 5, "Estate planning", "Stephen Maple", "",
         {"en": "International view of estate planning – useful for clients with assets abroad.",
          "th": "มุมมองสากลของการวางแผนมรดก เหมาะกับลูกค้าที่มีทรัพย์สินต่างประเทศ"},
         book=_b("book/6864401593073"), pages="336", call_no="PF00001", lang="en"),

    # ---------- Module 6: financial plan construction ----------
    Book("m6-course", 6, "หลักสูตรวางแผนการเงิน : ชุดวิชาที่ 6 การวางแผนการเงินแบบองค์รวม", CFP_COURSE, SET_LIBRARY,
         {"en": "The official Thai CFP course text for module 6 – putting modules 1–5 together for one client.",
          "th": "ตำราหลักสูตร CFP ไทยของชุดวิชาที่ 6 รวมชุดวิชา 1–5 เป็นแผนเดียวสำหรับลูกค้า"},
         book=_b("book/686587f89c4b4"), ebook=_b("ebook/68670866c07c8"), pages="340", call_no="PL00020", core=True),
    Book("m6-hallman", 6, "Private wealth management : the complete reference for the personal financial planner",
         "G. Victor Hallman", "McGraw-Hill",
         {"en": "A complete reference for planners covering every area of a client's plan.",
          "th": "ตำราอ้างอิงครบทุกด้านของแผนการเงินลูกค้าสำหรับนักวางแผน"},
         book=_b("book/686451fc6907a"), pages="753", call_no="PF00052", lang="en"),
    Book("m6-evensky", 6, "The new wealth management", "Harold Evensky", "Wiley",
         {"en": "How advisors manage and invest client assets – a practitioner's classic.",
          "th": "แนวทางที่ที่ปรึกษาใช้บริหารและลงทุนให้ลูกค้า ตำราคลาสสิกของผู้ปฏิบัติงาน"},
         book=_b("book/6864353647e88"), pages="458", call_no="PF00160", lang="en"),
    Book("m6-goals", 6, "Goals-based wealth management", "Jean L. P. Brunel", "",
         {"en": "Planning around each client goal instead of one portfolio.",
          "th": "วางแผนตามเป้าหมายแต่ละข้อของลูกค้าแทนพอร์ตเดียว"},
         book=_b("book/68644bd76be7f"), pages="249", call_no="IK00082", lang="en"),
    Book("m6-client-psych", 6, "Client psychology", "CFP Board", "",
         {"en": "CFP Board's book on understanding and communicating with clients.",
          "th": "หนังสือของ CFP Board เรื่องเข้าใจและสื่อสารกับลูกค้า"},
         ebook=_b("ebook/6867301d76389"), pages="327", lang="en"),
    Book("m6-questions", 6, "Questions great financial advisors ask", "Alan Parisse", "Kaplan",
         {"en": "The questions that uncover what a client really wants – useful for data gathering.",
          "th": "คำถามที่ช่วยค้นหาสิ่งที่ลูกค้าต้องการจริง ใช้ในขั้นเก็บข้อมูลลูกค้า"},
         book=_b("book/686452367900b"), pages="162", call_no="IK00049", lang="en"),
    Book("m6-emotional", 6, "Working with the emotional investor", "Chris White, Richard Koonce", "Praeger",
         {"en": "Handling clients' fear and greed when markets move.",
          "th": "การดูแลความกลัวและความโลภของลูกค้าเมื่อตลาดผันผวน"},
         book=_b("book/686577f83f8ec"), pages="212", call_no="IK00136", lang="en"),
]

BY_ID = {b.id: b for b in BOOKS}


def problems() -> list[str]:
    """Things to fix in the list (empty = all good)."""
    found = [f"{b.id}: duplicate id" for i, b in enumerate(BOOKS) if b.id in {x.id for x in BOOKS[:i]}]
    for b in BOOKS:
        if b.module not in range(1, 7):
            found.append(f"{b.id}: module {b.module} is not 1-6")
        if not b.links or not all(u.startswith(MARUEY + "/") for _, u in b.links):
            found.append(f"{b.id}: needs a Maruey link")
        if not (b.note.get("en") and b.note.get("th")):
            found.append(f"{b.id}: note missing English or Thai")
    found += [f"module {m}: no core course text" for m in range(1, 7) if not any(b.core for b in BOOKS if b.module == m)]
    return found


if __name__ == "__main__":
    print(f"{len(BOOKS)} books, {len(problems())} problems", *problems(), sep="\n")
