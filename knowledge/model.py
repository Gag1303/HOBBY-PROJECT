"""Building blocks of the Knowledge library (study notes for the CFP modules).

Every concept is one Concept: a short explanation in English and Thai, its formulas, a worked example,
practice questions, and the official learning objectives (LOS) it covers. Concepts are my own study
summary of standard finance theory, organised by the TFPA course chapters – not the course text itself.
"""

from dataclasses import dataclass, field

Text = dict  # {"en": ..., "th": ...}


@dataclass(frozen=True)
class Chapter:
    module: int
    number: int
    part: str        # key of PARTS
    title: Text
    los_count: int   # learning objectives the TFPA lists for this chapter


@dataclass(frozen=True)
class Formula:
    name: Text
    latex: str
    where: Text      # what the symbols mean


@dataclass(frozen=True)
class Question:
    question: Text
    answer: Text     # the answer with the working


@dataclass(frozen=True)
class Concept:
    id: str          # e.g. "K2-02-01": module 2, chapter 2, concept 1 (stable, notes can point at it)
    module: int
    chapter: int
    title: Text
    summary: Text
    points: tuple[Text, ...]
    formulas: tuple[Formula, ...] = ()
    example: Text | None = None             # a worked example
    questions: tuple[Question, ...] = ()    # practice questions with answers
    los: tuple[str, ...] = ()               # learning objectives covered, e.g. ("2.1", "2.2")
    books: tuple[str, ...] = ()             # reading list book ids (reading/books.py)
    rules: tuple[str, ...] = ()             # Law & Regulation entry ids
    tools: tuple[str, ...] = ()             # app tools to practise with, keys of TOOLS
    keywords: tuple[str, ...] = field(default=())


TOOLS = {
    "calculator": {"en": "Financial calculator (TVM, NPV / IRR, rate conversion)",
                   "th": "เครื่องคิดเลขการเงิน (TVM, NPV / IRR, แปลงอัตราดอกเบี้ย)"},
    "funds": {"en": "Thai mutual funds page (real returns, volatility, drawdown)",
              "th": "หน้ากองทุนรวมไทย (ผลตอบแทนจริง ความผันผวน drawdown)"},
    "simulator": {"en": "Investment simulator (portfolios, DCA, rebalancing)",
                  "th": "จำลองการลงทุน (พอร์ต DCA การปรับสัดส่วน)"},
}
