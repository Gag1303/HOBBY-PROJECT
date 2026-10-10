"""Module 2, chapter 2 – Return and risk (LOS 2.1–2.23).

My own study summary of standard finance theory, organised by TFPA's learning objectives for the chapter.
Every number in the examples and practice questions was computed, not estimated. Check details against the
course text (reading list: m2-course).
"""

from knowledge.model import Concept, Formula, Question

M, CH = 2, 2
COURSE = ("m2-course",)

CONCEPTS = [
    Concept(
        "K2-02-01", M, CH,
        {"en": "Holding period return", "th": "อัตราผลตอบแทนจากการถือครอง (HPR)"},
        {"en": "The return over one period has two parts: cash received (dividends, interest) and the change in price.",
         "th": "ผลตอบแทนต่องวดมี 2 ส่วน คือ กระแสเงินสดรับ (เงินปันผล ดอกเบี้ย) และการเปลี่ยนแปลงของราคา"},
        (
            {"en": "Current yield = cash received ÷ beginning price; capital gain yield = price change ÷ beginning price.",
             "th": "อัตราผลตอบแทนจากกระแสเงินสด = เงินสดรับ ÷ ราคาต้นงวด ส่วนกำไรจากส่วนต่างราคา = ราคาที่เปลี่ยน ÷ ราคาต้นงวด"},
            {"en": "For a mutual fund the price is the NAV per unit; a dividend fund's NAV drops by the dividend paid.",
             "th": "กองทุนรวมใช้ NAV ต่อหน่วยเป็นราคา กองทุนที่จ่ายปันผล NAV จะลดลงเท่ากับเงินปันผลที่จ่าย"},
        ),
        (Formula({"en": "Holding period return", "th": "อัตราผลตอบแทนจากการถือครอง"},
                 r"HPR = \frac{P_1 - P_0 + D}{P_0}",
                 {"en": "P₀ = price at the start, P₁ = price at the end, D = cash received during the period",
                  "th": "P₀ = ราคาต้นงวด, P₁ = ราคาปลายงวด, D = เงินสดที่ได้รับระหว่างงวด"}),),
        {"en": "Bought a share at 50 baht, received a 2-baht dividend, sold at 54: HPR = (54 − 50 + 2) ÷ 50 = 12% "
               "(4% from the dividend + 8% from the price).",
         "th": "ซื้อหุ้นที่ 50 บาท ได้ปันผล 2 บาท ขายที่ 54 บาท: HPR = (54 − 50 + 2) ÷ 50 = 12% (ปันผล 4% + ส่วนต่างราคา 8%)"},
        (Question({"en": "You bought fund units at NAV 12.00 and sold at 12.60. No dividend. What is the HPR?",
                   "th": "ซื้อหน่วยลงทุนที่ NAV 12.00 ขายที่ 12.60 ไม่มีปันผล HPR เท่ากับเท่าไร"},
                  {"en": "(12.60 − 12.00) ÷ 12.00 = 5%", "th": "(12.60 − 12.00) ÷ 12.00 = 5%"}),),
        ("2.1",), COURSE, tools=("funds",), keywords=("HPR", "dividend yield", "capital gain", "ปันผล", "ส่วนต่างราคา"),
    ),
    Concept(
        "K2-02-02", M, CH,
        {"en": "Average return: arithmetic vs geometric mean", "th": "ผลตอบแทนเฉลี่ย: ค่าเฉลี่ยเลขคณิต vs เรขาคณิต"},
        {"en": "The arithmetic mean (AM) is the simple average of yearly returns; the geometric mean (GM) is the "
               "compound growth rate you actually earned. GM ≤ AM, and the gap grows with volatility.",
         "th": "ค่าเฉลี่ยเลขคณิต (AM) คือค่าเฉลี่ยธรรมดาของผลตอบแทนแต่ละปี ค่าเฉลี่ยเรขาคณิต (GM) คืออัตราการเติบโตแบบทบต้นที่ได้จริง "
               "GM ≤ AM เสมอ และห่างกันมากขึ้นเมื่อผันผวนมาก"},
        (
            {"en": "Use GM to describe past performance over many periods; AM is the better estimate of next year's "
                   "expected return.",
             "th": "ใช้ GM อธิบายผลการดำเนินงานในอดีตหลายงวด ส่วน AM เหมาะกับการประมาณผลตอบแทนที่คาดหวังของงวดถัดไป"},
            {"en": "Fund factsheets show annualised (geometric) returns.",
             "th": "factsheet กองทุนแสดงผลตอบแทนต่อปีแบบทบต้น (เรขาคณิต)"},
        ),
        (Formula({"en": "Arithmetic mean", "th": "ค่าเฉลี่ยเลขคณิต"}, r"AM = \frac{R_1 + R_2 + \dots + R_n}{n}",
                 {"en": "Rₜ = return in period t, n = number of periods", "th": "Rₜ = ผลตอบแทนงวดที่ t, n = จำนวนงวด"}),
         Formula({"en": "Geometric mean", "th": "ค่าเฉลี่ยเรขาคณิต"},
                 r"GM = \left[(1+R_1)(1+R_2)\cdots(1+R_n)\right]^{1/n} - 1",
                 {"en": "the constant yearly rate that gives the same ending value", "th": "อัตราคงที่ต่อปีที่ให้มูลค่าปลายทางเท่ากัน"})),
        {"en": "+50% then −50%: AM = 0%, but 100 baht → 150 → 75. GM = √(1.5 × 0.5) − 1 = −13.4% a year – the real loss.",
         "th": "+50% แล้ว −50%: AM = 0% แต่ 100 บาท → 150 → 75 บาท GM = √(1.5 × 0.5) − 1 = −13.4% ต่อปี คือขาดทุนจริง"},
        (Question({"en": "Returns were +10%, +20% and −15%. Find the AM and the GM.",
                   "th": "ผลตอบแทน 3 ปีคือ +10%, +20% และ −15% หา AM และ GM"},
                  {"en": "AM = (10 + 20 − 15) ÷ 3 = 5%. GM = (1.10 × 1.20 × 0.85)^(1/3) − 1 = 1.122^(1/3) − 1 ≈ 3.91%.",
                   "th": "AM = (10 + 20 − 15) ÷ 3 = 5% GM = (1.10 × 1.20 × 0.85)^(1/3) − 1 = 1.122^(1/3) − 1 ≈ 3.91%"}),),
        ("2.2",), COURSE, keywords=("arithmetic mean", "geometric mean", "AM", "GM", "annualised", "ทบต้น"),
    ),
    Concept(
        "K2-02-03", M, CH,
        {"en": "Expected return", "th": "อัตราผลตอบแทนที่คาดหวัง"},
        {"en": "The expected return is the probability-weighted average of the possible returns.",
         "th": "อัตราผลตอบแทนที่คาดหวังคือค่าเฉลี่ยถ่วงน้ำหนักด้วยความน่าจะเป็นของผลตอบแทนที่อาจเกิดขึ้น"},
        ({"en": "The probabilities of all scenarios must add up to 100%.",
          "th": "ความน่าจะเป็นของทุกสถานการณ์ต้องรวมกันได้ 100%"},),
        (Formula({"en": "Expected return", "th": "อัตราผลตอบแทนที่คาดหวัง"}, r"E(R) = \sum_{i} p_i R_i",
                 {"en": "pᵢ = probability of scenario i, Rᵢ = return in scenario i",
                  "th": "pᵢ = ความน่าจะเป็นของสถานการณ์ i, Rᵢ = ผลตอบแทนในสถานการณ์ i"}),),
        {"en": "Boom 30% → +20%, normal 50% → +10%, recession 20% → −10%: E(R) = 0.3×20 + 0.5×10 + 0.2×(−10) = 9%.",
         "th": "เศรษฐกิจดี 30% → +20%, ปกติ 50% → +10%, ถดถอย 20% → −10%: E(R) = 0.3×20 + 0.5×10 + 0.2×(−10) = 9%"},
        (Question({"en": "A 40% chance of +15% and a 60% chance of +5%. What is the expected return?",
                   "th": "โอกาส 40% ได้ +15% และโอกาส 60% ได้ +5% ผลตอบแทนที่คาดหวังเท่าไร"},
                  {"en": "0.4 × 15% + 0.6 × 5% = 9%", "th": "0.4 × 15% + 0.6 × 5% = 9%"}),),
        ("2.3",), COURSE, keywords=("expected return", "probability", "scenario", "ความน่าจะเป็น"),
    ),
    Concept(
        "K2-02-04", M, CH,
        {"en": "What a nominal return is made of", "th": "องค์ประกอบของอัตราผลตอบแทนที่เป็นตัวเงิน"},
        {"en": "A nominal return pays for three things: the real risk-free rate, expected inflation and a risk premium.",
         "th": "อัตราผลตอบแทนที่เป็นตัวเงินชดเชย 3 ส่วน คืออัตราปราศจากความเสี่ยงที่แท้จริง ภาวะเงินเฟ้อที่คาดไว้ และส่วนชดเชยความเสี่ยง"},
        (
            {"en": "Real risk-free rate: reward for waiting, with no risk and no inflation.",
             "th": "อัตราปราศจากความเสี่ยงที่แท้จริง: ผลตอบแทนจากการรอ โดยไม่มีความเสี่ยงและเงินเฟ้อ"},
            {"en": "Nominal risk-free rate (e.g. a Thai T-bill) ≈ real risk-free rate + expected inflation.",
             "th": "อัตราปราศจากความเสี่ยงที่เป็นตัวเงิน (เช่น ตั๋วเงินคลัง) ≈ อัตราที่แท้จริง + เงินเฟ้อที่คาดไว้"},
            {"en": "Risk premium: extra return for business, financial, liquidity, exchange-rate and country risk.",
             "th": "ส่วนชดเชยความเสี่ยง: ผลตอบแทนส่วนเพิ่มสำหรับความเสี่ยงทางธุรกิจ การเงิน สภาพคล่อง อัตราแลกเปลี่ยน และประเทศ"},
        ),
        (Formula({"en": "Exact (Fisher) relation", "th": "ความสัมพันธ์แบบเต็ม (Fisher)"},
                 r"(1 + R_{nominal}) = (1 + r_{real})(1 + \pi)(1 + RP)",
                 {"en": "π = expected inflation, RP = risk premium; approximately R ≈ r + π + RP",
                  "th": "π = เงินเฟ้อที่คาดไว้, RP = ส่วนชดเชยความเสี่ยง โดยประมาณ R ≈ r + π + RP"}),),
        {"en": "Real risk-free 1%, inflation 2%, risk premium 4%: approximately 7%; exactly 1.01 × 1.02 × 1.04 − 1 = 7.14%.",
         "th": "อัตราแท้จริง 1% เงินเฟ้อ 2% ส่วนชดเชยความเสี่ยง 4%: โดยประมาณ 7% แบบเต็ม 1.01 × 1.02 × 1.04 − 1 = 7.14%"},
        (Question({"en": "A bond fund returns 6% a year with 2% inflation. What is the real return?",
                   "th": "กองทุนตราสารหนี้ได้ 6% ต่อปี เงินเฟ้อ 2% ผลตอบแทนที่แท้จริงเท่าไร"},
                  {"en": "About 4%; exactly 1.06 ÷ 1.02 − 1 = 3.92%.", "th": "ประมาณ 4% แบบเต็ม 1.06 ÷ 1.02 − 1 = 3.92%"}),),
        ("2.4", "2.5"), COURSE, keywords=("real return", "inflation", "risk premium", "risk-free", "Fisher", "เงินเฟ้อ"),
    ),
    Concept(
        "K2-02-05", M, CH,
        {"en": "After-tax and taxable-equivalent yield", "th": "ผลตอบแทนหลังภาษีและผลตอบแทนเทียบเท่าก่อนภาษี"},
        {"en": "Compare taxed and tax-free investments on the same basis: either take tax off the taxed one, or gross "
               "up the tax-free one.",
         "th": "เปรียบเทียบการลงทุนที่เสียภาษีกับไม่เสียภาษีบนฐานเดียวกัน โดยหักภาษีจากรายการที่เสียภาษี หรือแปลงรายการปลอดภาษีเป็นอัตราก่อนภาษี"},
        ({"en": "In Thailand interest on bonds and deposits is usually taxed at a 15% withholding tax (check current "
                "Revenue Department rules and exemptions).",
          "th": "ในไทย ดอกเบี้ยพันธบัตรและเงินฝากโดยทั่วไปถูกหักภาษี ณ ที่จ่าย 15% (ตรวจสอบเกณฑ์และข้อยกเว้นของกรมสรรพากรปัจจุบัน)"},),
        (Formula({"en": "After-tax yield", "th": "ผลตอบแทนหลังภาษี"}, r"R_{after\,tax} = R \times (1 - t)",
                 {"en": "t = tax rate", "th": "t = อัตราภาษี"}),
         Formula({"en": "Taxable-equivalent yield", "th": "ผลตอบแทนเทียบเท่าก่อนภาษี"},
                 r"R_{taxable\,equivalent} = \frac{R_{tax\,free}}{1 - t}",
                 {"en": "the taxed yield needed to match a tax-free one", "th": "ผลตอบแทนก่อนภาษีที่ต้องได้เพื่อให้เท่ากับผลตอบแทนปลอดภาษี"})),
        {"en": "A tax-free 3% equals a taxed 3 ÷ 0.85 = 3.53% at 15% tax; a taxed 4% leaves 4 × 0.85 = 3.4% after tax.",
         "th": "ผลตอบแทนปลอดภาษี 3% เทียบเท่าผลตอบแทนที่เสียภาษี 15% ที่ 3 ÷ 0.85 = 3.53% ผลตอบแทน 4% ที่เสียภาษี เหลือ 4 × 0.85 = 3.4%"},
        (Question({"en": "Bond A pays 3.5% taxed at 15%; bond B pays 3.0% tax-free. Which pays more after tax?",
                   "th": "หุ้นกู้ A ให้ 3.5% เสียภาษี 15% หุ้นกู้ B ให้ 3.0% ปลอดภาษี แบบไหนได้มากกว่าหลังภาษี"},
                  {"en": "A: 3.5 × 0.85 = 2.975% < 3.0%, so B pays slightly more.",
                   "th": "A: 3.5 × 0.85 = 2.975% < 3.0% ดังนั้น B ได้มากกว่าเล็กน้อย"}),),
        ("2.6",), COURSE, keywords=("after-tax", "tax-free", "taxable equivalent", "withholding", "ภาษี", "ภาษีหัก ณ ที่จ่าย"),
    ),
    Concept(
        "K2-02-06", M, CH,
        {"en": "Time value of money: present and future value", "th": "มูลค่าเงินตามเวลา: มูลค่าปัจจุบันและมูลค่าอนาคต"},
        {"en": "Money today is worth more than the same money later, because it can earn a return. Compounding moves "
               "money forward in time; discounting moves it back.",
         "th": "เงินวันนี้มีค่ามากกว่าเงินจำนวนเดียวกันในอนาคต เพราะนำไปลงทุนได้ การทบต้นพาเงินไปอนาคต การคิดลดพาเงินกลับมาปัจจุบัน"},
        ({"en": "An annuity is the same payment every period – e.g. a monthly DCA or a pension.",
          "th": "เงินงวด (annuity) คือการจ่ายเท่ากันทุกงวด เช่น DCA รายเดือนหรือเงินบำนาญ"},),
        (Formula({"en": "Future and present value of one sum", "th": "มูลค่าอนาคตและปัจจุบันของเงินก้อนเดียว"},
                 r"FV = PV (1 + r)^n \qquad PV = \frac{FV}{(1 + r)^n}",
                 {"en": "r = rate per period, n = number of periods", "th": "r = อัตราต่องวด, n = จำนวนงวด"}),
         Formula({"en": "Present value of an annuity", "th": "มูลค่าปัจจุบันของเงินงวด"},
                 r"PV = PMT \times \frac{1 - (1 + r)^{-n}}{r}",
                 {"en": "PMT = payment each period (end of period)", "th": "PMT = เงินงวด (ปลายงวด)"})),
        {"en": "100,000 at 5% for 10 years grows to 100,000 × 1.05¹⁰ = 162,889. Receiving 10,000 a year for 5 years at 4% "
               "is worth 10,000 × 4.4518 = 44,518 today.",
         "th": "100,000 บาท ที่ 5% 10 ปี เป็น 100,000 × 1.05¹⁰ = 162,889 บาท การได้รับ 10,000 บาทต่อปี 5 ปี ที่ 4% "
               "มีมูลค่าปัจจุบัน 10,000 × 4.4518 = 44,518 บาท"},
        (Question({"en": "A client needs 1,000,000 baht in 20 years and can earn 6% a year. How much should they invest today?",
                   "th": "ลูกค้าต้องการ 1,000,000 บาทในอีก 20 ปี ได้ผลตอบแทน 6% ต่อปี ต้องลงทุนวันนี้เท่าไร"},
                  {"en": "PV = 1,000,000 ÷ 1.06²⁰ = 1,000,000 ÷ 3.2071 ≈ 311,805 baht.",
                   "th": "PV = 1,000,000 ÷ 1.06²⁰ = 1,000,000 ÷ 3.2071 ≈ 311,805 บาท"}),),
        ("2.7", "2.8"), COURSE, tools=("calculator",), keywords=("TVM", "present value", "future value", "annuity", "PV", "FV"),
    ),
    Concept(
        "K2-02-07", M, CH,
        {"en": "Compounding and the effective annual rate", "th": "การทบต้นและอัตราผลตอบแทนที่แท้จริงต่อปี (EAR)"},
        {"en": "The more often interest is compounded within a year, the higher the effective annual rate (EAR) for the "
               "same quoted rate.",
         "th": "ยิ่งทบต้นบ่อยในหนึ่งปี อัตราผลตอบแทนที่แท้จริงต่อปี (EAR) ยิ่งสูงขึ้น แม้อัตราที่ประกาศเท่ากัน"},
        ({"en": "Use the EAR to compare products that compound at different frequencies.",
          "th": "ใช้ EAR เปรียบเทียบผลิตภัณฑ์ที่ทบต้นด้วยความถี่ต่างกัน"},),
        (Formula({"en": "Effective annual rate", "th": "อัตราผลตอบแทนที่แท้จริงต่อปี"},
                 r"EAR = \left(1 + \frac{APR}{m}\right)^m - 1",
                 {"en": "APR = quoted yearly rate, m = compounding periods per year",
                  "th": "APR = อัตราต่อปีที่ประกาศ, m = จำนวนครั้งที่ทบต้นต่อปี"}),),
        {"en": "6% compounded monthly: (1 + 0.06/12)¹² − 1 = 6.17%.", "th": "6% ทบต้นรายเดือน: (1 + 0.06/12)¹² − 1 = 6.17%"},
        (Question({"en": "What is the EAR of 5% compounded quarterly?", "th": "5% ทบต้นรายไตรมาส มี EAR เท่าไร"},
                  {"en": "(1 + 0.05/4)⁴ − 1 = 1.0125⁴ − 1 ≈ 5.09%", "th": "(1 + 0.05/4)⁴ − 1 = 1.0125⁴ − 1 ≈ 5.09%"}),),
        ("2.9",), COURSE, tools=("calculator",), keywords=("EAR", "APR", "compounding", "effective rate", "ทบต้น"),
    ),
    Concept(
        "K2-02-08", M, CH,
        {"en": "Types of investment risk", "th": "ประเภทความเสี่ยงจากการลงทุน"},
        {"en": "Risk is the chance that the actual return differs from the expected return. Some risks hit the whole "
               "market, others only one company or asset.",
         "th": "ความเสี่ยงคือโอกาสที่ผลตอบแทนจริงต่างจากที่คาดไว้ บางความเสี่ยงกระทบทั้งตลาด บางความเสี่ยงกระทบเฉพาะกิจการหรือสินทรัพย์"},
        (
            {"en": "Market-wide (systematic): market risk, interest rate risk, inflation (purchasing power) risk, "
                   "exchange-rate risk, country/political risk.",
             "th": "ทั้งระบบ: ความเสี่ยงตลาด อัตราดอกเบี้ย เงินเฟ้อ (อำนาจซื้อ) อัตราแลกเปลี่ยน และประเทศ/การเมือง"},
            {"en": "Company-specific (unsystematic): business risk, financial (debt) risk, management risk, credit "
                   "(default) risk of one issuer, liquidity risk of one security.",
             "th": "เฉพาะตัว: ความเสี่ยงทางธุรกิจ ทางการเงิน (ภาระหนี้) ผู้บริหาร ความเสี่ยงผิดนัดชำระของผู้ออกรายหนึ่ง และสภาพคล่องของหลักทรัพย์ตัวหนึ่ง"},
        ),
        (),
        None,
        (Question({"en": "A rise in Thai interest rates and fraud at one listed company: which is systematic risk?",
                   "th": "อัตราดอกเบี้ยไทยสูงขึ้น กับการทุจริตในบริษัทจดทะเบียนแห่งหนึ่ง ข้อใดเป็นความเสี่ยงที่เป็นระบบ"},
                  {"en": "The interest rate rise (it affects the whole market); the fraud is unsystematic and can be "
                         "diversified away.",
                   "th": "อัตราดอกเบี้ยที่สูงขึ้น (กระทบทั้งตลาด) ส่วนการทุจริตเป็นความเสี่ยงเฉพาะตัวที่กระจายความเสี่ยงได้"}),),
        ("2.10",), COURSE, keywords=("risk types", "interest rate risk", "inflation risk", "liquidity risk", "ความเสี่ยง"),
    ),
    Concept(
        "K2-02-09", M, CH,
        {"en": "Measuring risk: variance, standard deviation and coefficient of variation",
         "th": "การวัดความเสี่ยง: ความแปรปรวน ส่วนเบี่ยงเบนมาตรฐาน และสัมประสิทธิ์ความแปรผัน"},
        {"en": "Standard deviation (SD) measures how widely returns spread around the expected return. To compare "
               "assets with different returns, use risk per unit of return (CV).",
         "th": "ส่วนเบี่ยงเบนมาตรฐาน (SD) วัดการกระจายของผลตอบแทนรอบค่าที่คาดหวัง หากผลตอบแทนต่างกันให้เทียบความเสี่ยงต่อหน่วยผลตอบแทน (CV)"},
        (
            {"en": "Higher expected return usually comes with higher risk – the risk–return trade-off.",
             "th": "ผลตอบแทนที่คาดหวังสูงมักมาพร้อมความเสี่ยงสูง (risk–return trade-off)"},
            {"en": "Ranking: with equal return pick the lower SD; with equal SD pick the higher return; otherwise compare CV.",
             "th": "การจัดลำดับ: ผลตอบแทนเท่ากันเลือก SD ต่ำ SD เท่ากันเลือกผลตอบแทนสูง กรณีอื่นเทียบ CV"},
        ),
        (Formula({"en": "Variance and standard deviation", "th": "ความแปรปรวนและส่วนเบี่ยงเบนมาตรฐาน"},
                 r"\sigma^2 = \sum_i p_i \left(R_i - E(R)\right)^2 \qquad \sigma = \sqrt{\sigma^2}",
                 {"en": "with history instead of scenarios, average the squared deviations (÷ n − 1 for a sample)",
                  "th": "หากใช้ข้อมูลในอดีตแทนสถานการณ์ ให้เฉลี่ยกำลังสองของส่วนเบี่ยงเบน (หารด้วย n − 1 สำหรับข้อมูลตัวอย่าง)"}),
         Formula({"en": "Coefficient of variation", "th": "สัมประสิทธิ์ความแปรผัน"}, r"CV = \frac{\sigma}{E(R)}",
                 {"en": "risk per 1% of expected return – lower is better", "th": "ความเสี่ยงต่อผลตอบแทนที่คาดหวัง 1% ยิ่งต่ำยิ่งดี"})),
        {"en": "Using the scenarios of K2-02-03 (E = 9%): σ² = 0.3×11² + 0.5×1² + 0.2×(−19)² = 109, σ = 10.44%, CV = 1.16.",
         "th": "ใช้สถานการณ์ใน K2-02-03 (E = 9%): σ² = 0.3×11² + 0.5×1² + 0.2×(−19)² = 109, σ = 10.44%, CV = 1.16"},
        (Question({"en": "Fund A: E = 8%, SD = 12%. Fund B: E = 10%, SD = 20%. Which has less risk per unit of return?",
                   "th": "กองทุน A: E = 8%, SD = 12% กองทุน B: E = 10%, SD = 20% กองไหนเสี่ยงต่อหน่วยผลตอบแทนน้อยกว่า"},
                  {"en": "CV A = 12 ÷ 8 = 1.5; CV B = 20 ÷ 10 = 2.0 → fund A.",
                   "th": "CV A = 12 ÷ 8 = 1.5, CV B = 20 ÷ 10 = 2.0 → กองทุน A"}),),
        ("2.11", "2.12", "2.13"), COURSE, tools=("funds",),
        keywords=("standard deviation", "variance", "volatility", "CV", "ความผันผวน", "ส่วนเบี่ยงเบนมาตรฐาน"),
    ),
    Concept(
        "K2-02-10", M, CH,
        {"en": "Portfolio expected return, covariance and correlation",
         "th": "ผลตอบแทนคาดหวังของพอร์ต ความแปรปรวนร่วม และสหสัมพันธ์"},
        {"en": "A portfolio's expected return is the weighted average of its assets' returns. How the assets move "
               "together is measured by covariance and, on a −1 to +1 scale, by the correlation coefficient.",
         "th": "ผลตอบแทนคาดหวังของพอร์ตคือค่าเฉลี่ยถ่วงน้ำหนักของผลตอบแทนแต่ละสินทรัพย์ การเคลื่อนไหวร่วมกันวัดด้วยความแปรปรวนร่วม "
               "และสัมประสิทธิ์สหสัมพันธ์ (−1 ถึง +1)"},
        (
            {"en": "ρ = +1: move exactly together; 0: unrelated; −1: move exactly opposite.",
             "th": "ρ = +1 เคลื่อนไหวไปทางเดียวกันทั้งหมด, 0 ไม่สัมพันธ์กัน, −1 สวนทางกันทั้งหมด"},),
        (Formula({"en": "Portfolio expected return", "th": "ผลตอบแทนคาดหวังของพอร์ต"}, r"E(R_p) = \sum_i w_i \, E(R_i)",
                 {"en": "wᵢ = weight of asset i (weights add up to 1)", "th": "wᵢ = สัดส่วนสินทรัพย์ i (รวมกันได้ 1)"}),
         Formula({"en": "Covariance and correlation", "th": "ความแปรปรวนร่วมและสหสัมพันธ์"},
                 r"\rho_{AB} = \frac{Cov(R_A, R_B)}{\sigma_A \sigma_B}",
                 {"en": "Cov = ρ × σ_A × σ_B", "th": "Cov = ρ × σ_A × σ_B"})),
        {"en": "60% in an equity fund (E = 10%) and 40% in a bond fund (E = 5%): E(Rp) = 0.6×10 + 0.4×5 = 8%.",
         "th": "กองทุนหุ้น 60% (E = 10%) และกองทุนตราสารหนี้ 40% (E = 5%): E(Rp) = 0.6×10 + 0.4×5 = 8%"},
        (Question({"en": "σ_A = 20%, σ_B = 10%, ρ = 0.5. What is the covariance?",
                   "th": "σ_A = 20%, σ_B = 10%, ρ = 0.5 ความแปรปรวนร่วมเท่าไร"},
                  {"en": "Cov = 0.5 × 0.20 × 0.10 = 0.01", "th": "Cov = 0.5 × 0.20 × 0.10 = 0.01"}),),
        ("2.14", "2.15", "2.16"), COURSE, tools=("simulator",),
        keywords=("portfolio return", "covariance", "correlation", "สหสัมพันธ์", "ความแปรปรวนร่วม"),
    ),
    Concept(
        "K2-02-11", M, CH,
        {"en": "Portfolio risk and diversification", "th": "ความเสี่ยงของพอร์ตและการกระจายความเสี่ยง"},
        {"en": "Unless correlation is +1, a portfolio's SD is lower than the weighted average of its assets' SDs. The "
               "lower the correlation, the bigger the diversification benefit.",
         "th": "หากสหสัมพันธ์ไม่เท่ากับ +1 SD ของพอร์ตจะต่ำกว่าค่าเฉลี่ยถ่วงน้ำหนักของ SD แต่ละสินทรัพย์ ยิ่งสหสัมพันธ์ต่ำ ประโยชน์จากการกระจายความเสี่ยงยิ่งมาก"},
        ({"en": "To build a portfolio, look for assets with low or negative correlation, not just high returns.",
          "th": "ในการสร้างพอร์ต ให้มองหาสินทรัพย์ที่สหสัมพันธ์ต่ำหรือติดลบ ไม่ใช่เพียงผลตอบแทนสูง"},),
        (Formula({"en": "Two-asset portfolio variance", "th": "ความแปรปรวนของพอร์ต 2 สินทรัพย์"},
                 r"\sigma_p^2 = w_A^2\sigma_A^2 + w_B^2\sigma_B^2 + 2 w_A w_B \rho_{AB} \sigma_A \sigma_B",
                 {"en": "σ_p = √σ_p²", "th": "σ_p = √σ_p²"}),),
        {"en": "60% A (σ 20%) + 40% B (σ 10%), ρ = 0.2: σp² = 0.0144 + 0.0016 + 0.00192 = 0.01792 → σp = 13.39%, "
               "below the 16% weighted average.",
         "th": "A 60% (σ 20%) + B 40% (σ 10%), ρ = 0.2: σp² = 0.0144 + 0.0016 + 0.00192 = 0.01792 → σp = 13.39% "
               "ต่ำกว่าค่าเฉลี่ยถ่วงน้ำหนัก 16%"},
        (Question({"en": "Two funds each with σ = 15%, 50/50, correlation 0. What is the portfolio SD?",
                   "th": "2 กองทุน σ = 15% เท่ากัน ลงทุน 50/50 สหสัมพันธ์ 0 SD ของพอร์ตเท่าไร"},
                  {"en": "σp² = 0.25×0.0225 + 0.25×0.0225 = 0.01125 → σp ≈ 10.61% (vs 15% for either fund).",
                   "th": "σp² = 0.25×0.0225 + 0.25×0.0225 = 0.01125 → σp ≈ 10.61% (เทียบกับ 15% ของแต่ละกอง)"}),),
        ("2.17", "2.18"), COURSE, tools=("simulator",), rules=("B02",),
        keywords=("diversification", "portfolio risk", "กระจายความเสี่ยง"),
    ),
    Concept(
        "K2-02-12", M, CH,
        {"en": "Systematic vs unsystematic risk, and beta", "th": "ความเสี่ยงที่เป็นระบบ ไม่เป็นระบบ และเบต้า"},
        {"en": "Diversification removes unsystematic risk but not systematic risk. Beta measures an asset's systematic "
               "risk: how much it tends to move when the market moves.",
         "th": "การกระจายการลงทุนขจัดความเสี่ยงที่ไม่เป็นระบบได้ แต่ขจัดความเสี่ยงที่เป็นระบบไม่ได้ เบต้าวัดความเสี่ยงที่เป็นระบบ "
               "ว่าสินทรัพย์มักเปลี่ยนแปลงเท่าไรเมื่อตลาดเปลี่ยน"},
        (
            {"en": "Total risk = systematic + unsystematic. The market only rewards systematic risk.",
             "th": "ความเสี่ยงรวม = ความเสี่ยงที่เป็นระบบ + ไม่เป็นระบบ ตลาดให้ผลตอบแทนชดเชยเฉพาะความเสี่ยงที่เป็นระบบ"},
            {"en": "β = 1 moves with the market, β > 1 is aggressive, β < 1 defensive; the market's β is 1.",
             "th": "β = 1 เคลื่อนไหวเท่าตลาด, β > 1 เชิงรุก, β < 1 เชิงรับ ตลาดมี β = 1"},
        ),
        (Formula({"en": "Beta", "th": "เบต้า"}, r"\beta_i = \frac{Cov(R_i, R_m)}{\sigma_m^2}",
                 {"en": "Rₘ = market return, σₘ² = market variance", "th": "Rₘ = ผลตอบแทนตลาด, σₘ² = ความแปรปรวนของตลาด"}),),
        {"en": "A stock with β = 1.2 is expected to rise about 6% when the market rises 5% (1.2 × 5%).",
         "th": "หุ้นที่ β = 1.2 คาดว่าจะขึ้นประมาณ 6% เมื่อตลาดขึ้น 5% (1.2 × 5%)"},
        (Question({"en": "A fund has β = 0.8. The market falls 10%. What is the expected move of the fund?",
                   "th": "กองทุนมี β = 0.8 ตลาดลดลง 10% กองทุนคาดว่าจะเปลี่ยนแปลงเท่าไร"},
                  {"en": "0.8 × (−10%) = −8%", "th": "0.8 × (−10%) = −8%"}),),
        ("2.19", "2.20"), COURSE, keywords=("beta", "systematic", "unsystematic", "เบต้า", "ความเสี่ยงที่เป็นระบบ"),
    ),
    Concept(
        "K2-02-13", M, CH,
        {"en": "CAPM and the security market line", "th": "แบบจำลอง CAPM และเส้น SML"},
        {"en": "CAPM gives the return investors should require for an asset's systematic risk. Plotted against beta it "
               "is the security market line (SML).",
         "th": "CAPM บอกอัตราผลตอบแทนที่ผู้ลงทุนควรต้องการตามความเสี่ยงที่เป็นระบบของสินทรัพย์ เมื่อพล็อตกับเบต้าจะได้เส้น SML"},
        (
            {"en": "Expected return above the SML → undervalued (buy); below → overvalued (sell).",
             "th": "ผลตอบแทนที่คาดไว้อยู่เหนือ SML → ราคาต่ำกว่ามูลค่า (ซื้อ) ต่ำกว่า SML → ราคาสูงกว่ามูลค่า (ขาย)"},
            {"en": "The SML shifts up or down when the risk-free rate (e.g. inflation expectations) changes, and gets "
                   "steeper when investors become more risk-averse (higher market risk premium).",
             "th": "SML เลื่อนขึ้นลงเมื่ออัตราปราศจากความเสี่ยงเปลี่ยน (เช่น การคาดการณ์เงินเฟ้อ) และชันขึ้นเมื่อผู้ลงทุนกลัวความเสี่ยงมากขึ้น "
                   "(ส่วนชดเชยความเสี่ยงตลาดสูงขึ้น)"},
        ),
        (Formula({"en": "CAPM", "th": "CAPM"}, r"E(R_i) = R_f + \beta_i \left[E(R_m) - R_f\right]",
                 {"en": "R_f = risk-free rate, E(Rₘ) − R_f = market risk premium",
                  "th": "R_f = อัตราปราศจากความเสี่ยง, E(Rₘ) − R_f = ส่วนชดเชยความเสี่ยงตลาด"}),),
        {"en": "R_f = 2%, market 8%, β = 1.2: required return = 2 + 1.2 × (8 − 2) = 9.2%. If you expect 11%, the stock "
               "plots above the SML – undervalued.",
         "th": "R_f = 2% ตลาด 8% β = 1.2: ผลตอบแทนที่ต้องการ = 2 + 1.2 × (8 − 2) = 9.2% หากคาดว่าจะได้ 11% หุ้นอยู่เหนือ SML "
               "– ราคาต่ำกว่ามูลค่า"},
        (Question({"en": "R_f = 2.5%, market risk premium 5%, β = 1.4. What return should investors require?",
                   "th": "R_f = 2.5% ส่วนชดเชยความเสี่ยงตลาด 5% β = 1.4 ผู้ลงทุนควรต้องการผลตอบแทนเท่าไร"},
                  {"en": "2.5% + 1.4 × 5% = 9.5%", "th": "2.5% + 1.4 × 5% = 9.5%"}),),
        ("2.21", "2.22"), COURSE, keywords=("CAPM", "SML", "required return", "market risk premium", "undervalued"),
    ),
    Concept(
        "K2-02-14", M, CH,
        {"en": "Risk-adjusted performance: Sharpe, Treynor and Jensen", "th": "ผลตอบแทนปรับความเสี่ยง: Sharpe, Treynor และ Jensen"},
        {"en": "Raw returns can't be compared fairly when risk differs. These three measures adjust for risk.",
         "th": "ผลตอบแทนดิบเปรียบเทียบกันไม่ได้เมื่อความเสี่ยงต่างกัน มาตรวัดทั้งสามปรับด้วยความเสี่ยง"},
        (
            {"en": "Sharpe uses total risk (σ) – right for a client's whole portfolio. Treynor and Jensen use β – right "
                   "for a fund that is one part of a diversified portfolio.",
             "th": "Sharpe ใช้ความเสี่ยงรวม (σ) เหมาะกับพอร์ตทั้งหมดของลูกค้า Treynor และ Jensen ใช้ β "
                   "เหมาะกับกองทุนที่เป็นส่วนหนึ่งของพอร์ตที่กระจายความเสี่ยงแล้ว"},
            {"en": "Limits: they rely on past data, a choice of risk-free rate and benchmark, and (for β) CAPM holding.",
             "th": "ข้อจำกัด: อิงข้อมูลในอดีต ขึ้นกับอัตราปราศจากความเสี่ยงและดัชนีอ้างอิงที่เลือก และ (สำหรับ β) สมมติว่า CAPM ถูกต้อง"},
        ),
        (Formula({"en": "Sharpe ratio", "th": "Sharpe ratio"}, r"S = \frac{R_p - R_f}{\sigma_p}",
                 {"en": "excess return per unit of total risk", "th": "ผลตอบแทนส่วนเกินต่อความเสี่ยงรวม 1 หน่วย"}),
         Formula({"en": "Treynor ratio", "th": "Treynor ratio"}, r"T = \frac{R_p - R_f}{\beta_p}",
                 {"en": "excess return per unit of systematic risk", "th": "ผลตอบแทนส่วนเกินต่อความเสี่ยงที่เป็นระบบ 1 หน่วย"}),
         Formula({"en": "Jensen's alpha", "th": "Jensen's alpha"}, r"\alpha_p = R_p - \left[R_f + \beta_p (R_m - R_f)\right]",
                 {"en": "return above what CAPM requires – positive means the manager added value",
                  "th": "ผลตอบแทนที่เกินกว่าที่ CAPM ต้องการ ค่าบวกแปลว่าผู้จัดการกองทุนสร้างมูลค่าเพิ่ม"})),
        {"en": "Fund return 10%, R_f 2%, σ 16%, β 1.1, market 8%: Sharpe = 8 ÷ 16 = 0.50; Treynor = 8 ÷ 1.1 = 7.27%; "
               "alpha = 10 − (2 + 1.1 × 6) = +1.4%.",
         "th": "กองทุนได้ 10% R_f 2% σ 16% β 1.1 ตลาด 8%: Sharpe = 8 ÷ 16 = 0.50, Treynor = 8 ÷ 1.1 = 7.27%, "
               "alpha = 10 − (2 + 1.1 × 6) = +1.4%"},
        (Question({"en": "Fund A: 12% return, σ 20%. Fund B: 9% return, σ 10%. R_f = 2%. Which is better risk-adjusted?",
                   "th": "กองทุน A ได้ 12% σ 20% กองทุน B ได้ 9% σ 10% R_f = 2% กองไหนดีกว่าเมื่อปรับความเสี่ยง"},
                  {"en": "Sharpe A = (12 − 2) ÷ 20 = 0.5; Sharpe B = (9 − 2) ÷ 10 = 0.7 → fund B.",
                   "th": "Sharpe A = (12 − 2) ÷ 20 = 0.5, Sharpe B = (9 − 2) ÷ 10 = 0.7 → กองทุน B"}),),
        ("2.23",), COURSE, tools=("funds",), keywords=("Sharpe", "Treynor", "Jensen", "alpha", "risk-adjusted"),
    ),
]
