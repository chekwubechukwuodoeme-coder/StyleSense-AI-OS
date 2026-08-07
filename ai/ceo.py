from ai.designer import designer_agent
from ai.business import business_agent
from ai.marketing import marketing_agent
from ai.finance import finance_agent
from ai.production import production_agent
from ai.research import research_agent
from ai.trend import trend_agent
from ai.stylist import stylist_agent


def ceo_agent(task):

    task_lower = task.lower()

    report = []

    report.append("# 👔 StyleSense AI Executive Report")

    # ----------------------------------------------------
    # BUSINESS REQUESTS
    # ----------------------------------------------------

    if any(word in task_lower for word in [
        "brand",
        "business",
        "startup",
        "company",
        "launch",
        "fashion label"
    ]):

        report.append("## 💼 Business Strategy")
        report.append(business_agent(task))

        report.append("## 💰 Financial Analysis")
        report.append(finance_agent(task))

        report.append("## 📢 Marketing Strategy")
        report.append(marketing_agent(task))

        report.append("## 🔍 Market Research")
        report.append(research_agent(task))

    # ----------------------------------------------------
    # DESIGN REQUESTS
    # ----------------------------------------------------

    if any(word in task_lower for word in [
        "design",
        "dress",
        "outfit",
        "collection",
        "fashion",
        "gown",
        "senator",
        "agbada"
    ]):

        report.append("## 👗 Fashion Design")
        report.append(designer_agent(task))

        report.append("## 👔 Styling")
        report.append(stylist_agent(task))

        report.append("## 🏭 Production")
        report.append(production_agent(task))

        report.append("## 📈 Fashion Trends")
        report.append(trend_agent(task))

    # ----------------------------------------------------
    # DEFAULT
    # ----------------------------------------------------

    if len(report) == 1:

        report.append(designer_agent(task))

    return "\n\n---\n\n".join(report)