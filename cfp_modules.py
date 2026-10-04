"""The 6 Thai CFP modules, shared by the home page and the sidebar menu."""

from dataclasses import dataclass


@dataclass
class Module:
    number: int
    name_en: str
    name_th: str
    description: str  # what the toolkit has (or ideas, until tools exist)
    home_page: str | None = None  # page the home card's "Open" button goes to


MODULES = [
    Module(1, "Fundamentals of financial planning", "พื้นฐานการวางแผนการเงิน",
           "Ideas: time value of money calculator, personal financial statements & ratios."),
    Module(2, "Investment planning", "การวางแผนการลงทุน",
           "Thai mutual fund data: latest NAV of every fund, full performance history, "
           "fund comparison, risk numbers. Portfolio simulator: Lump sum vs DCA vs VCA.",
           "module2_investment/dashboard.py"),
    Module(3, "Risk management & insurance planning", "การวางแผนการประกันภัย",
           "Ideas: life insurance needs calculator (income replacement / needs approach)."),
    Module(4, "Retirement planning & employee benefits", "การวางแผนเพื่อวัยเกษียณ",
           "Ideas: retirement savings gap, provident fund / RMF projections."),
    Module(5, "Tax & estate planning", "การวางแผนภาษีและมรดก",
           "Ideas: Thai personal income tax calculator with SSF/RMF/insurance deductions."),
    Module(6, "Financial plan development", "การจัดทำแผนการเงิน",
           "Ideas: bring modules 1-5 together into one client plan."),
]
