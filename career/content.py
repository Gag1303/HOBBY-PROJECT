"""CFP career guide content (English / Thai).

A personal study summary, in my own words, of documents published by the Thai Financial Planners
Association (TFPA, www.tfpa.or.th). It is not the official text: always check the linked TFPA
documents, which can change. Sources: registration handbook (version 1_2026), code of ethics and
rules of conduct (version 1_2023), CFP course outline and LOS, approved calculator list.
"""

# Each text is {"en": ..., "th": ...}; the page shows the one for the current language.

FOUR_E = [
    {
        "key": "education",
        "icon": "📚",
        "title": {"en": "Education", "th": "การศึกษา (Education)"},
        "points": [
            {"en": "Train in all 6 modules at a TFPA-approved institute. Each module is 40 hours "
                   "(24 in class + 16 self-study); the 2021 (B.E. 2564) Investment module has 48 class hours.",
             "th": "อบรมครบ 6 ชุดวิชากับสถาบันอบรมที่สมาคมฯ อนุญาต ชุดละ 40 ชั่วโมง (ห้องเรียน 24 + "
                   "ศึกษาเอง 16) ชุดวิชาที่ 2 หลักสูตรปรับปรุงปี 2564 เรียนในห้อง 48 ชั่วโมง"},
            {"en": "Module 6 (Financial plan construction) can only be taken after modules 1–5.",
             "th": "ชุดวิชาที่ 6 (การจัดทำแผนการเงิน) ต้องผ่านการอบรมชุดวิชาที่ 1–5 ก่อน"},
            {"en": "Transcript review (1,605 THB per module): skip a module if your degree covered it "
                   "(e.g. personal finance, tax and TVM → module 1; investment and securities analysis → "
                   "module 2; insurance → module 3) or you hold a related licence (IC Plain/Complex, "
                   "analyst, life insurance agent/broker → module 3).",
             "th": "เทียบเคียงพื้นฐานความรู้ (1,605 บาท/ชุดวิชา): ยกเว้นการอบรมได้ถ้าเคยเรียนวิชาที่เกี่ยวข้อง "
                   "(เช่น การเงินส่วนบุคคล ภาษี มูลค่าเงินตามเวลา → ชุด 1; การลงทุน วิเคราะห์หลักทรัพย์ → ชุด 2; "
                   "ประกันภัย → ชุด 3) หรือมีใบอนุญาตที่เกี่ยวข้อง (IC Plain/Complex นักวิเคราะห์ "
                   "ตัวแทน/นายหน้าประกันชีวิต → ชุด 3)"},
            {"en": "Challenge status (5,350 THB): go straight to the exams with a PhD in finance, economics, "
                   "business or accounting, or CPA, CISA level 3 or CFA level 3.",
             "th": "ขอสิทธิ์สอบโดยไม่อบรม (5,350 บาท): จบปริญญาเอกด้านการเงิน เศรษฐศาสตร์ บริหารธุรกิจ "
                   "หรือบัญชี หรือมี CPA, CISA ระดับ 3, CFA ระดับ 3"},
        ],
    },
    {
        "key": "exam",
        "icon": "📝",
        "title": {"en": "Examination", "th": "การสอบ (Examination)"},
        "points": [
            {"en": "Pass 4 exam papers (fees: general public / TFPA member, THB, incl. VAT):",
             "th": "สอบผ่านข้อสอบ 4 ฉบับ (ค่าสอบ บุคคลทั่วไป / สมาชิก รวม VAT แล้ว):"},
            {"en": "Paper 1 – Foundation, tax and ethics (module 1): 2,000 / 1,700",
             "th": "ฉบับที่ 1 – พื้นฐานการวางแผนการเงิน ภาษี และจรรยาบรรณ (ชุด 1): 2,000 / 1,700"},
            {"en": "Paper 2 – Investment planning (module 2): 3,000 / 2,550",
             "th": "ฉบับที่ 2 – การวางแผนการลงทุน (ชุด 2): 3,000 / 2,550"},
            {"en": "Paper 3 – Insurance and retirement planning (modules 3–4): 3,000 / 2,550",
             "th": "ฉบับที่ 3 – การวางแผนการประกันภัยและเพื่อวัยเกษียณ (ชุด 3–4): 3,000 / 2,550"},
            {"en": "Paper 4 – part 1 Tax and estate planning (module 5): 2,000 / 1,700; part 2 Financial plan "
                   "case (module 6): 4,500 / 3,825",
             "th": "ฉบับที่ 4 – ส่วนที่ 1 ภาษีและมรดก (ชุด 5): 2,000 / 1,700; ส่วนที่ 2 ข้อสอบแผนการเงิน "
                   "(ชุด 6): 4,500 / 3,825"},
            {"en": "Approved calculators include HP 10B/10BII, HP 12c, TI BA II Plus, Casio FC-100V/FC-200V "
                   "and basic calculators – this app's financial calculator works like these.",
             "th": "เครื่องคิดเลขที่อนุญาต เช่น HP 10B/10BII, HP 12c, TI BA II Plus, Casio FC-100V/FC-200V "
                   "และเครื่องคิดเลขทั่วไป – เครื่องคิดเลขการเงินในแอปนี้ใช้งานแบบเดียวกัน"},
        ],
    },
    {
        "key": "experience",
        "icon": "💼",
        "title": {"en": "Experience", "th": "ประสบการณ์การทำงาน (Experience)"},
        "points": [
            {"en": "3 years of work directly related to financial planning for clients, covering at least one "
                   "of the 6 practice-standard steps.",
             "th": "ทำงานที่เกี่ยวข้องกับการให้บริการวางแผนการเงินแก่ลูกค้าโดยตรง 3 ปี "
                   "ครอบคลุมหลักปฏิบัติการวางแผนการเงินอย่างน้อย 1 ด้าน"},
            {"en": "The 3 years must fall within 5 years before passing the exam, or within 8 years after it "
                   "(or a mix of both).",
             "th": "3 ปีนั้นต้องอยู่ภายใน 5 ปีก่อนสอบผ่าน หรือภายใน 8 ปีหลังสอบผ่าน (หรือรวมกันทั้งสองช่วง)"},
            {"en": "Typical employers: banks, securities firms, asset management companies, life and non-life "
                   "insurers, GPF, Social Security Office, regulators, accounting and law firms. Roles include "
                   "financial planner, investment consultant, analyst, fund manager, insurance agent, trainer.",
             "th": "หน่วยงานที่นับได้ เช่น ธนาคาร บริษัทหลักทรัพย์ บลจ. บริษัทประกันชีวิต/วินาศภัย กบข. "
                   "สำนักงานประกันสังคม หน่วยงานกำกับดูแล สำนักงานบัญชี/กฎหมาย ตำแหน่ง เช่น นักวางแผนการเงิน "
                   "ผู้แนะนำการลงทุน นักวิเคราะห์ ผู้จัดการกองทุน ตัวแทนประกัน วิทยากร"},
            {"en": "University teaching of finance counts for at most 2 of the 3 years.",
             "th": "ประสบการณ์สอนวิชาการเงินในมหาวิทยาลัยนับได้สูงสุด 2 ปี"},
        ],
    },
    {
        "key": "ethics",
        "icon": "⚖️",
        "title": {"en": "Ethics", "th": "จรรยาบรรณ (Ethics)"},
        "points": [
            {"en": "Agree to follow the Code of Ethics and the Financial Planning Practice Standards.",
             "th": "ตกลงปฏิบัติตามประมวลจรรยาบรรณและหลักปฏิบัติการวางแผนการเงิน"},
            {"en": "Never had a professional licence revoked or suspended, and not blacklisted by the SEC, SET, "
                   "Bank of Thailand or OIC.",
             "th": "ไม่เคยถูกเพิกถอน/ระงับใบอนุญาต และไม่อยู่ในบัญชีดำของ ก.ล.ต. ตลท. ธปท. หรือ คปภ."},
            {"en": "Disclose any involvement in civil or criminal investigations.",
             "th": "เปิดเผยการมีส่วนเกี่ยวข้องในการไต่สวนหรือสอบสวนคดีแพ่งหรืออาญา"},
        ],
    },
]

AFPT = {
    "en": "AFPT™ (Associate Financial Planner Thailand) is a smaller qualification on the way: modules 1 and 2 "
          "(2021 curriculum) plus exam papers 1 and 2, with no experience requirement. AFPT advisers give "
          "advice on investment, and/or insurance and retirement planning.",
    "th": "AFPT™ (ที่ปรึกษาการเงิน) เป็นคุณวุฒิระหว่างทาง: อบรมชุดวิชาที่ 1 และ 2 (หลักสูตรปี 2564) และสอบ "
          "ฉบับที่ 1 และ 2 ไม่ต้องมีประสบการณ์ทำงาน ให้คำแนะนำด้านการลงทุน และ/หรือการประกันชีวิตและวัยเกษียณ",
}

RENEWAL = [
    {"en": "Renew every 2 calendar years and pay the TFPA fee; deadline 31 December of the renewal year "
           "(grace period to the end of February).",
     "th": "ต่ออายุทุก 2 ปีปฏิทินและชำระค่าบำรุงสมาคมฯ ภายใน 31 ธันวาคมของปีที่ครบกำหนด "
           "(ผ่อนผันได้ถึงสิ้นเดือนกุมภาพันธ์)"},
    {"en": "At least 30 CPD hours per 2 years, including ≥3 hours on ethics / practice standards run by TFPA "
           "and ≥9 hours of training or seminars (live or e-learning). Extra hours do not carry over.",
     "th": "สะสม CPD อย่างน้อย 30 ชั่วโมงต่อ 2 ปี โดยต้องมีหัวข้อจรรยาบรรณ/หลักปฏิบัติที่สมาคมฯ จัด ≥3 ชั่วโมง "
           "และการอบรม/สัมมนา (สดหรือ e-Learning) ≥9 ชั่วโมง ชั่วโมงที่เกินยกไปรอบหน้าไม่ได้"},
    {"en": "CPD also counts for passing CFA (15 h per level) or CISA, licence exams (3 h), teaching (2× hours), "
           "writing articles (1 h per 1,000 characters) and more – keep evidence for 3 years.",
     "th": "นับ CPD ได้จากการสอบผ่าน CFA (ระดับละ 15 ชม.) CISA ใบอนุญาต (3 ชม.) การเป็นวิทยากร (2 เท่า) "
           "เขียนบทความ (1 ชม./1,000 ตัวอักษร) ฯลฯ ต้องเก็บหลักฐานไว้ 3 ปี"},
    {"en": "Lapsed less than 4 years: catch up the CPD and fees. More than 4 years: re-take the exam and meet "
           "the experience requirement again.",
     "th": "ขาดต่ออายุไม่เกิน 4 ปี: สะสม CPD และชำระค่าบำรุงให้ครบ เกิน 4 ปี: ต้องสอบใหม่และมีประสบการณ์ตามเกณฑ์"},
]

CROSS_BORDER = [
    {"en": "The CFP mark is managed worldwide by FPSB; TFPA is Thailand's licensing body (since 2009).",
     "th": "เครื่องหมาย CFP บริหารโดย FPSB ทั่วโลก สมาคมนักวางแผนการเงินไทยเป็นผู้ได้รับอนุญาตในประเทศไทย (ตั้งแต่ปี 2552)"},
    {"en": "A CFP certified in another FPSB country who wants to work in Thailand takes TFPA's cross-border "
           "exam: 100 multiple-choice questions in English on Thai laws and rules; education and experience "
           "from the home country are accepted.",
     "th": "ผู้ที่ได้ CFP จากประเทศสมาชิก FPSB อื่นและต้องการทำงานในไทย ต้องสอบ cross-border ของสมาคมฯ: "
           "ข้อสอบภาษาอังกฤษ 100 ข้อ เรื่องกฎหมายและกฎระเบียบไทย โดยยอมรับการศึกษาและประสบการณ์จากประเทศต้นทาง"},
    {"en": "Going the other way (a Thai CFP working abroad) works the same in principle – check the "
           "cross-border rules of that country's FPSB member before you plan the move.",
     "th": "ในทางกลับกัน (CFP ไทยไปทำงานต่างประเทศ) มีหลักการแบบเดียวกัน ควรตรวจสอบเกณฑ์ cross-border "
           "ของสมาชิก FPSB ในประเทศนั้นก่อนวางแผน"},
]

ETHICS_PRINCIPLES = [
    ("Client First", "คำนึงถึงประโยชน์ของลูกค้าเป็นสำคัญ",
     "Put the client's interests first; never put your own gain above the client's.",
     "ให้ความสำคัญกับผลประโยชน์ของลูกค้าเป็นอันดับแรก ไม่ถือประโยชน์ส่วนตัวมากกว่าลูกค้า"),
    ("Integrity", "การยึดมั่นในสิ่งที่ถูกต้องและชอบธรรม",
     "Be honest and candid, in both the letter and the spirit of the rules.",
     "ซื่อสัตย์ ตรงไปตรงมา ทั้งตามลายลักษณ์อักษรและเจตนา"),
    ("Objectivity", "ความเป็นกลาง",
     "Be impartial and manage conflicts of interest with professional judgment.",
     "เที่ยงธรรม ไม่ลำเอียง และจัดการความขัดแย้งทางผลประโยชน์อย่างมืออาชีพ"),
    ("Fairness", "ความเป็นธรรม",
     "Be fair and reasonable to clients, employers and others; disclose and manage conflicts of interest.",
     "ปฏิบัติอย่างเป็นธรรมและมีเหตุผล เปิดเผยและจัดการความขัดแย้งทางผลประโยชน์"),
    ("Professionalism", "ความเป็นมืออาชีพ",
     "Act with dignity and courtesy, follow the rules, and protect the profession's reputation.",
     "ประพฤติตนอย่างมีเกียรติ ปฏิบัติตามกฎระเบียบ และร่วมรักษาภาพลักษณ์ของวิชาชีพ"),
    ("Competence", "ความรู้ความสามารถ",
     "Know your limits, refer clients when needed, and keep learning.",
     "รู้ขีดจำกัดของตนเอง แนะนำลูกค้าให้ผู้อื่นเมื่อจำเป็น และหมั่นเพิ่มพูนความรู้"),
    ("Confidentiality", "การรักษาความลับ",
     "Protect client information; share it only with the client's consent (or when the law requires).",
     "ปกป้องข้อมูลลูกค้า เปิดเผยได้เฉพาะเมื่อลูกค้ายินยอม (หรือกฎหมายกำหนด)"),
    ("Diligence", "ความใส่ใจระมัดระวัง",
     "Serve clients promptly and thoroughly, and plan and supervise your work properly.",
     "ให้บริการอย่างรวดเร็วและรอบคอบ วางแผนและควบคุมดูแลงานอย่างเหมาะสม"),
]

# Key rules of conduct, grouped. The numbers refer to the 37 rules in TFPA's document.
RULES = [
    {
        "title": {"en": "🚫 Never", "th": "🚫 ห้ามเด็ดขาด"},
        "items": [
            {"en": "Mislead anyone about your competence, your services or the benefits of the plan (rules 1–2).",
             "th": "ทำให้เข้าใจผิดเกี่ยวกับความสามารถ บริการ หรือประโยชน์ที่จะได้รับ (ข้อ 1–2)"},
            {"en": "Act dishonestly, fraudulently or deceitfully, or misrepresent facts (rule 4).",
             "th": "ทุจริต ฉ้อโกง หลอกลวง หรือบิดเบือนข้อเท็จจริง (ข้อ 4)"},
            {"en": "Borrow money from a client – unless the client is family, or a lending business and the loan "
                   "has nothing to do with your planning work (rule 16).",
             "th": "กู้ยืมเงินจากลูกค้า ยกเว้นลูกค้าเป็นคนในครอบครัว หรือเป็นธุรกิจให้กู้และไม่เกี่ยวกับงานวางแผน (ข้อ 16)"},
            {"en": "Lend money to a client – unless the client is family, or you work for a lending business "
                   "and it is the business's money, not yours (rule 17).",
             "th": "ให้ลูกค้ากู้ยืมเงิน ยกเว้นเป็นคนในครอบครัว หรือเป็นเงินของบริษัทผู้ให้กู้ที่ตนเป็นลูกจ้าง (ข้อ 17)"},
            {"en": "Mix client assets with your own, your employer's or other clients' (rule 7).",
             "th": "นำทรัพย์สินของลูกค้าไปปะปนกับของตนเอง นายจ้าง หรือลูกค้ารายอื่น (ข้อ 7)"},
            {"en": "Let personal bias or self-interest affect your advice (rule 10).",
             "th": "ให้อคติหรือผลประโยชน์ส่วนตัวมีผลต่อบริการ (ข้อ 10)"},
            {"en": "Give advice outside your competence – consult or refer to a qualified professional (rule 12).",
             "th": "ให้คำแนะนำในด้านที่ตนไม่ชำนาญ ต้องปรึกษาหรือแนะนำผู้เชี่ยวชาญ (ข้อ 12)"},
        ],
    },
    {
        "title": {"en": "📄 Always disclose in writing", "th": "📄 ต้องเปิดเผยเป็นลายลักษณ์อักษร"},
        "items": [
            {"en": "How you and your employer are paid: fees, commissions and other sources, and how they are "
                   "calculated (rule 15a).",
             "th": "ค่าตอบแทนของตนและบริษัท: ค่าธรรมเนียม คอมมิชชั่น แหล่งที่มาอื่น และวิธีคิด (ข้อ 15 ก)"},
            {"en": "Any conflict of interest – family, contractual or business relationships (rule 15b).",
             "th": "ความขัดแย้งทางผลประโยชน์ เช่น ความสัมพันธ์ทางครอบครัว สัญญา หรือธุรกิจ (ข้อ 15 ข)"},
            {"en": "Anything material to the client's decision, the scope of your competence, and your contact "
                   "details – and update the client at once if they change (rule 15c–e).",
             "th": "ข้อมูลที่มีผลต่อการตัดสินใจ ขอบเขตความสามารถ และข้อมูลติดต่อ หากเปลี่ยนต้องแจ้งทันที (ข้อ 15 ค–จ)"},
            {"en": "A written engagement agreement: each party's role, date and term, how to end it, and the "
                   "scope of service (rule 34).",
             "th": "ข้อตกลงการให้บริการเป็นลายลักษณ์อักษร: บทบาทแต่ละฝ่าย วันที่และอายุ วิธียกเลิก และขอบเขตบริการ (ข้อ 34)"},
        ],
    },
    {
        "title": {"en": "✅ Always do", "th": "✅ ต้องปฏิบัติเสมอ"},
        "items": [
            {"en": "Give suitable advice, use prudent judgment, and follow the law (rules 11, 20, 21).",
             "th": "ให้คำแนะนำที่เหมาะสม ใช้วิจารณญาณอย่างรอบคอบ และปฏิบัติตามกฎหมาย (ข้อ 11, 20, 21)"},
            {"en": "Keep client information confidential and protect client data and assets, paper and "
                   "electronic (rules 18–19).",
             "th": "รักษาความลับและปกป้องข้อมูลและทรัพย์สินของลูกค้า ทั้งเอกสารและอิเล็กทรอนิกส์ (ข้อ 18–19)"},
            {"en": "Keep records of client assets you hold or control, and return them on request (rules 5–6, 31).",
             "th": "บันทึกทรัพย์สินของลูกค้าที่ตนดูแล และส่งคืนเมื่อลูกค้าร้องขอ (ข้อ 5–6, 31)"},
            {"en": "Study products carefully before recommending them, and supervise staff you delegate to "
                   "(rules 29–30).",
             "th": "ศึกษาผลิตภัณฑ์อย่างรอบคอบก่อนแนะนำ และควบคุมดูแลผู้ใต้บังคับบัญชา (ข้อ 29–30)"},
            {"en": "Explain recommendations so the client can decide, and serve them carefully and on time "
                   "(rules 28, 35).",
             "th": "อธิบายคำแนะนำให้ลูกค้าเข้าใจพอจะตัดสินใจได้ และให้บริการอย่างรอบคอบทันเวลา (ข้อ 28, 35)"},
            {"en": "Keep up your CPD and use the CFP marks correctly (rules 13–14, 23–24).",
             "th": "พัฒนาความรู้ (CPD) อย่างต่อเนื่อง และใช้เครื่องหมาย CFP อย่างถูกต้อง (ข้อ 13–14, 23–24)"},
            {"en": "Tell TFPA in writing within 10 working days about any criminal matter or licence "
                   "suspension/revocation (rule 25).",
             "th": "แจ้งสมาคมฯ เป็นลายลักษณ์อักษรภายใน 10 วันทำการ หากเกี่ยวข้องกับความผิดอาญาหรือถูกพัก/เพิกถอนคุณวุฒิ (ข้อ 25)"},
        ],
    },
]

PRACTICE_STEPS = [
    ("Establish the client relationship", "การสร้างความสัมพันธ์กับลูกค้า"),
    ("Gather client information", "การเก็บรวบรวมข้อมูลลูกค้า"),
    ("Analyse and assess the client's financial status", "การวิเคราะห์และประเมินฐานะการเงินของลูกค้า"),
    ("Develop and present the financial plan", "การจัดทำและนำเสนอแผนการเงิน"),
    ("Implement the plan", "การดำเนินการตามแผน"),
    ("Monitor the plan", "การติดตามแผนการเงิน"),
]

# Official TFPA downloads (www.tfpa.or.th → เอกสารดาวน์โหลด). Links go to TFPA's own site.
DOCUMENTS = [
    ("For CFP / AFPT holders", "นักวางแผนการเงิน CFP และที่ปรึกษาการเงิน AFPT", [
        ("CFP and AFPT registration handbook", "คู่มือการขึ้นทะเบียนคุณวุฒิวิชาชีพ CFP และ AFPT",
         "https://www.tfpa.or.th/upload/92f06327-b978-41c2-9e44-3e136ad2e601.pdf"),
        ("CFP and AFPT handbook", "คู่มือนักวางแผนการเงิน CFP และที่ปรึกษาการเงิน AFPT",
         "https://www.tfpa.or.th/upload/2317d684-575e-474a-bf25-4458a5eff053.pdf"),
        ("Code of ethics and rules of conduct", "ประมวลจรรยาบรรณฯ และหลักปฏิบัติของผู้ประกอบวิชาชีพ",
         "https://www.tfpa.or.th/upload/98de1c40-8a39-4080-af44-59bf9f6e41d0.pdf"),
        ("Financial planning practice standards", "หลักปฏิบัติการวางแผนการเงิน",
         "https://tfpa.or.th/Upload/หลักปฏิบัติการวางแผนการเงิน.pdf"),
        ("Financial planner competency profile", "กรอบความสามารถของนักวางแผนการเงิน",
         "https://tfpa.or.th/Upload/กรอบความสามารถในการทำงานของนักวางแผนการเงิน.pdf"),
        ("PDPA manual for CFP/AFPT", "คู่มือ PDPA สำหรับ CFP/AFPT",
         "https://www.tfpa.or.th/upload/ff91ac80-0e99-4bee-8736-bbb3882e6f68.pdf"),
        ("CPD rules", "เกณฑ์การพัฒนาคุณวุฒิวิชาชีพอย่างต่อเนื่อง (CPD)",
         "https://www.tfpa.or.th/upload/7f54d7bf-4e1a-4690-b944-3644071325e9.pdf"),
        ("Guidance note: using AI in financial planning", "แนวปฏิบัติการใช้ปัญญาประดิษฐ์ (AI) กับการวางแผนการเงิน",
         "https://www.tfpa.or.th/upload/8a3f8bd7-377d-4bdb-bfb2-4b7acd4c562c.pdf"),
    ]),
    ("For trainees and exam candidates", "ผู้อบรมและผู้สมัครสอบ", [
        ("Training timetable", "ตารางอบรมประจำปี",
         "https://www.tfpa.or.th/upload/d0fdccb0-97d3-44c5-8181-b442dad66469.pdf"),
        ("Exam timetable", "ตารางสอบประจำปี",
         "https://www.tfpa.or.th/upload/c46dedcd-9d83-49e7-9f04-e5fc9e16ca6e.pdf"),
        ("CFP exam handbook", "คู่มือการสอบหลักสูตรการวางแผนการเงิน CFP",
         "https://www.tfpa.or.th/upload/4806dd1b-c4d2-4445-a29f-b3316d590475.pdf"),
        ("Infographic: preparing for the exam", "Infographic การเตรียมตัวเพื่อเข้าสอบ",
         "https://www.tfpa.or.th/upload/57318bbd-124d-4b25-a3d4-5b44f48d7d6c.jpg"),
        ("Approved calculators", "เครื่องคิดเลขรุ่นที่กำหนดในการสอบ",
         "https://www.tfpa.or.th/upload/08c91869-1386-4a3c-aa1d-f70048da7086.pdf"),
        ("Infographic: exam steps", "Infographic ขั้นตอนการสอบ",
         "https://www.tfpa.or.th/upload/b3588e8a-3041-4141-af97-f7c323658f6c.jpg"),
        ("Course outline and learning objectives (LOS)", "รายละเอียดรายวิชาและวัตถุประสงค์การเรียนรู้",
         "https://www.tfpa.or.th/upload/97202118453.pdf"),
        ("Module 2 (2021) training/exam format", "รูปแบบการอบรม/สอบ ชุดวิชาที่ 2 (ปี 2564)",
         "https://www.tfpa.or.th/upload/cca3e894-625f-4243-8d9f-a0f491f48473.pdf"),
        ("Module 2 (2021) learning objectives (LOS)", "LOS ชุดวิชาที่ 2 การวางแผนการลงทุน (ปี 2564)",
         "https://www.tfpa.or.th/Upload/03_LOS_New%20M2.pdf"),
        ("FAQ: module 6 and the new financial plan exam (from 2026)", "FAQ ชุดวิชาที่ 6 และข้อสอบแผนการเงินรูปแบบใหม่ (ปี 2569)",
         "https://www.tfpa.or.th/upload/5ec3af0e-2be8-41f6-841b-808330419ef5.pdf"),
        ("Module 6 learning objectives (from 2026)", "LOS ชุดวิชาที่ 6 การจัดทำแผนการเงิน (ปี 2569)",
         "https://www.tfpa.or.th/upload/9c0f089f-5179-46f6-bcec-e5156ef11960.pdf"),
        ("Sample case and plan: Warabi & Matcha (exam 1/69)", "กรณีศึกษาคุณวาราบิและมัทฉะ (ตัวอย่างข้อสอบ 1/69)",
         "https://www.tfpa.or.th/upload/b8fc81e4-435e-4cc3-882f-a61faf43f036.pdf"),
        ("Sample case and plan: Jit-aree family (exam 2/69)", "กรณีศึกษาครอบครัวจิตย์อารีย์ (ตัวอย่างข้อสอบ 2/69)",
         "https://www.tfpa.or.th/upload/9ca416bb-2853-4b75-b0da-d4e7130fc294.pdf"),
        ("Reading list", "รายการหนังสือประกอบการอ่านสอบ",
         "https://www.tfpa.or.th/upload/14fd37e3-1737-40ae-a00d-804324207e7d.pdf"),
        ("Textbook update notice", "แจ้งการปรับปรุงเนื้อหาตำรา",
         "https://www.tfpa.or.th/upload/8f79138d-25a6-48a3-bb69-09add5772bc9.pdf"),
    ]),
]
