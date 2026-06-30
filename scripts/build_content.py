import json
import re
import shutil
from datetime import date
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(r"C:\Users\jerry\Desktop\reparations")
REPORTS_DIR = ROOT / "public" / "reports"
DATA_DIR = ROOT / "src" / "data"
OUTPUT_PDF_DIR = ROOT / "output" / "pdf"
NATIONAL_REPORT_NAME = "negro-research-institute-united-states-reparations-breakdown.pdf"


PDFS = [
    ("Atlanta", "Georgia", "Atlanta", "The-Case-for-Reparations-African-Americans-in-Atlanta.pdf", 177_900_000_000),
    ("Austin", "Texas", "Austin, Texas", "The-Case-for-Reparations-African-Americans-in-Austin-Texas.pdf", 105_800_000_000),
    ("Baltimore", "Maryland", "Baltimore", "The-Case-for-Reparations-African-Americans-in-Baltimore.pdf", 151_700_000_000),
    ("Birmingham", "Alabama", "Birmingham, Alabama", "The-Case-for-Reparations-African-Americans-in-Birmingham-Alabama.pdf", 137_200_000_000),
    ("Boston", "Massachusetts", "Boston", "The-Case-for-Reparations-African-Americans-in-Boston.pdf", 125_100_000_000),
    ("Buffalo", "New York", "Buffalo, New York", "The-Case-for-Reparations-African-Americans-in-Buffalo-New-York.pdf", 81_600_000_000),
    ("Chicago", "Illinois", "Chicago", "The-Case-for-Reparations-African-Americans-in-Chicago.pdf", 253_800_000_000),
    ("Cincinnati", "Ohio", "Cincinnati", "The-Case-for-Reparations-African-Americans-in-Cincinnati.pdf", 82_900_000_000),
    ("Cleveland", "Ohio", "Cleveland, Ohio", "The-Case-for-Reparations-African-Americans-in-Cleveland-Ohio.pdf", 103_600_000_000),
    ("Denver", "Colorado", "Denver, Colorado", "The-Case-for-Reparations-African-Americans-in-Denver-Colorado.pdf", 89_100_000_000),
    ("East Palo Alto / San Mateo County", "California", "East Palo Alto and San Mateo County", "The-Case-for-Reparations-African-Americans-in-East-Palo-Alto-and-San-Mateo-County.pdf", 129_500_000_000),
    ("Flint / Genesee County", "Michigan", "Flint, Michigan and Genesee County", "The-Case-for-Reparations-African-Americans-in-Flint-Michigan-and-Genesee-County (1).pdf", 82_000_000_000),
    ("Jackson", "Mississippi", "Jackson, Mississippi", "The-Case-for-Reparations-African-Americans-in-Jackson-Mississippi.pdf", 78_400_000_000),
    ("Kansas City", "Missouri", "Kansas City, Missouri", "The-Case-for-Reparations-African-Americans-in-Kansas-City-Missouri.pdf", 86_700_000_000),
    ("Las Vegas", "Nevada", "Las Vegas, Nevada", "The-Case-for-Reparations-African-Americans-in-Las-Vegas-Nevada.pdf", 101_200_000_000),
    ("Louisville", "Kentucky", "Louisville", "The-Case-for-Reparations-African-Americans-in-Louisville.pdf", 93_900_000_000),
    ("Memphis", "Tennessee", "Memphis, Tennessee", "The-Case-for-Reparations-African-Americans-in-Memphis-Tennessee.pdf", 107_300_000_000),
    ("Milwaukee", "Wisconsin", "Milwaukee", "The-Case-for-Reparations-African-Americans-in-Milwaukee.pdf", 98_200_000_000),
    ("Nashville", "Tennessee", "Nashville, Tennessee", "The-Case-for-Reparations-African-Americans-in-Nashville-Tennessee.pdf", 91_500_000_000),
    ("New Orleans", "Louisiana", "New Orleans", "The-Case-for-Reparations-African-Americans-in-New-Orleans.pdf", 119_800_000_000),
    ("New York City", "New York", "New York City", "The-Case-for-Reparations-African-Americans-in-New-York-City.pdf", 608_800_000_000),
    ("Oklahoma City", "Oklahoma", "Oklahoma City", "The-Case-for-Reparations-African-Americans-in-Oklahoma-City.pdf", 74_600_000_000),
    ("Philadelphia", "Pennsylvania", "Philadelphia", "The-Case-for-Reparations-African-Americans-in-Philadelphia.pdf", 170_900_000_000),
    ("Phoenix", "Arizona", "Phoenix, Arizona", "The-Case-for-Reparations-African-Americans-in-Phoenix-Arizona.pdf", 92_400_000_000),
    ("Pittsburgh", "Pennsylvania", "Pittsburgh, Pennsylvania", "The-Case-for-Reparations-African-Americans-in-Pittsburgh-Pennsylvania.pdf", 87_700_000_000),
    ("Portland", "Oregon", "Portland", "The-Case-for-Reparations-African-Americans-in-Portland.pdf", 92_800_000_000),
    ("Providence", "Rhode Island", "Providence, Rhode Island", "The-Case-for-Reparations-African-Americans-in-Providence-Rhode-Island.pdf", 72_100_000_000),
    ("Richmond / Contra Costa County", "California", "Richmond and Contra Costa County", "The-Case-for-Reparations-African-Americans-in-Richmond-and-Contra-Costa-County.pdf", 153_200_000_000),
    ("Sacramento", "California", "Sacramento, California", "The-Case-for-Reparations-African-Americans-in-Sacramento-California (1).pdf", 114_700_000_000),
    ("San Francisco", "California", "San Francisco", "The-Case-for-Reparations-African-Americans-in-San-Francisco.pdf", 253_800_000_000),
    ("San Jose / Santa Clara County", "California", "San Jose and Santa Clara County", "The-Case-for-Reparations-African-Americans-in-San-Jose-and-Santa-Clara-County.pdf", 176_400_000_000),
    ("Seattle", "Washington", "Seattle", "The-Case-for-Reparations-African-Americans-in-Seattle.pdf", 109_600_000_000),
    ("St. Louis", "Missouri", "St. Louis", "The-Case-for-Reparations-African-Americans-in-St-Louis.pdf", 104_300_000_000),
    ("Virginia Beach / Norfolk / Newport News", "Virginia", "Virginia Beach, Norfolk, Newport News", "The-Case-for-Reparations-African-Americans-in-Virginia-Beach-Norfolk-Newport-News.pdf", 130_600_000_000),
    ("Washington, DC", "District of Columbia", "Washington DC", "The-Case-for-Reparations-African-Americans-in-Washington-DC.pdf", 268_500_000_000),
    ("Wichita", "Kansas", "Wichita, Kansas", "The-Case-for-Reparations-African-Americans-in-Wichita-Kansas.pdf", 60_900_000_000),
]


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def dollars(value):
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    return f"${value / 1_000_000_000:.1f}B"


def page_count(path):
    try:
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def parse_money(text):
    compact = re.search(r"\$\s*([0-9]+(?:\.[0-9]+)?)\s*([BT])\b", text, flags=re.I)
    if compact:
        number = float(compact.group(1))
        multiplier = 1_000_000_000_000 if compact.group(2).lower() == "t" else 1_000_000_000
        return int(number * multiplier)

    spelled = re.search(r"\$\s*([0-9]+(?:\.[0-9]+)?)\s*(billion|trillion)\b", text, flags=re.I)
    if spelled:
        number = float(spelled.group(1))
        multiplier = 1_000_000_000_000 if spelled.group(2).lower().startswith("t") else 1_000_000_000
        return int(number * multiplier)

    return None


def detect_total(path):
    try:
        reader = PdfReader(str(path))
        start = max(0, len(reader.pages) - 16)
        pages = [(i + 1, reader.pages[i].extract_text() or "") for i in range(start, len(reader.pages))]
    except Exception:
        return None

    priority_phrases = ("grand total", "what is owed", "total liability")
    for _page_number, text in pages:
        lowered = text.lower()
        if any(phrase in lowered for phrase in priority_phrases):
            amount = parse_money(text)
            if amount:
                return amount

    full_text = "\n".join(text for _page_number, text in pages)
    return parse_money(full_text)


def build_city_data():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)

    cities = []
    for name, state, jurisdiction, filename, fallback_total in PDFS:
        source = SOURCE_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing source PDF: {source}")
        slug = slugify(name)
        public_name = f"{slug}.pdf"
        target = REPORTS_DIR / public_name
        shutil.copy2(source, target)
        extracted_total = detect_total(source)
        if not extracted_total:
            raise ValueError(f"Could not detect headline total in {source}")
        total = extracted_total or fallback_total
        cities.append(
            {
                "name": name,
                "state": state,
                "jurisdiction": jurisdiction,
                "slug": slug,
                "fileName": public_name,
                "sourceFile": filename,
                "pdfPath": f"/reports/{public_name}",
                "total": total,
                "totalLabel": dollars(total),
                "pageCount": page_count(source),
                "sourcePageNote": "headline estimate extracted from closing liability pages",
            }
        )

    aggregate_total = sum(city["total"] for city in cities)
    data = {
        "agency": "NEGRO RESEARCH INSTITUTE",
        "reportDate": date.today().isoformat(),
        "sourceFolder": str(SOURCE_DIR),
        "cityCount": len(cities),
        "aggregateTotal": aggregate_total,
        "aggregateTotalLabel": dollars(aggregate_total),
        "nationalReportPath": f"/reports/{NATIONAL_REPORT_NAME}",
        "methodologyNote": (
            "The national figure is a sum of headline liability estimates across the 36 local "
            "and regional PDFs in the source folder. It is not presented as a complete national "
            "United States reparations estimate."
        ),
        "categories": [
            "Housing wealth destruction",
            "Business destruction",
            "Displacement and land loss",
            "Environmental harm",
            "Policing and incarceration",
            "Education exclusion",
            "Labor and wage extraction",
        ],
        "cities": cities,
    }
    (DATA_DIR / "reports.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6E6A60"))
    canvas.drawString(0.65 * inch, 0.45 * inch, "NEGRO RESEARCH INSTITUTE")
    canvas.drawRightString(7.85 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def make_national_pdf(data):
    output = OUTPUT_PDF_DIR / NATIONAL_REPORT_NAME
    public_output = REPORTS_DIR / NATIONAL_REPORT_NAME
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "Agency",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#B89145"),
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=32,
            textColor=colors.HexColor("#181713"),
            alignment=TA_CENTER,
            spaceAfter=16,
        )
    )
    styles.add(
        ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#292721"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "Metric",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#143B2F"),
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            "MetricLabel",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            textColor=colors.HexColor("#5E5A50"),
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#181713"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "TableHeader",
            parent=styles["Body"],
            fontName="Helvetica-Bold",
            textColor=colors.white,
        )
    )
    right = ParagraphStyle("Right", parent=styles["Body"], alignment=TA_RIGHT)

    doc = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    story = [
        Paragraph(data["agency"], styles["Agency"]),
        Paragraph("United States Reparations Breakdown", styles["ReportTitle"]),
        Paragraph(
            "A national-facing summary of 36 city and regional reparations briefs for Black people in the United States.",
            styles["Body"],
        ),
        Paragraph(
            "<b>Important framing:</b> this dossier summarizes the reports in the supplied archive. "
            "The headline figure is the sum of those local and regional estimates, not a complete "
            "national reparations total for every Black person or every jurisdiction in the United States.",
            styles["Body"],
        ),
        Spacer(1, 0.18 * inch),
    ]

    metrics = Table(
        [
            [
                Paragraph(data["aggregateTotalLabel"], styles["Metric"]),
                Paragraph(str(data["cityCount"]), styles["Metric"]),
                Paragraph("7", styles["Metric"]),
            ],
            [
                Paragraph("summed local liability estimates", styles["MetricLabel"]),
                Paragraph("city and regional PDFs", styles["MetricLabel"]),
                Paragraph("recurring harm categories", styles["MetricLabel"]),
            ],
        ],
        colWidths=[2.3 * inch, 2.3 * inch, 2.3 * inch],
    )
    metrics.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3EFE3")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBB883")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9CCAC")),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story += [
        metrics,
        Spacer(1, 0.2 * inch),
        Paragraph("Methodology And Limits", styles["Section"]),
        Paragraph(
            data["methodologyNote"]
            + " The source PDFs use internally stated calculations and citations; this generated summary does not independently validate population eligibility, jurisdictional overlap, or economic assumptions.",
            styles["Body"],
        ),
        Paragraph("Recurring Damage Categories", styles["Section"]),
        Paragraph(", ".join(data["categories"]) + ".", styles["Body"]),
        Paragraph("City And Regional Report Table", styles["Section"]),
    ]

    rows = [
        [
            Paragraph("Jurisdiction", styles["TableHeader"]),
            Paragraph("State", styles["TableHeader"]),
            Paragraph("Headline estimate", styles["TableHeader"]),
            Paragraph("Pages", styles["TableHeader"]),
        ]
    ]
    for city in sorted(data["cities"], key=lambda item: item["name"]):
        rows.append(
            [
                Paragraph(city["name"], styles["Body"]),
                Paragraph(city["state"], styles["Body"]),
                Paragraph(city["totalLabel"], right),
                Paragraph(str(city["pageCount"] or ""), right),
            ]
        )

    table = Table(rows, colWidths=[2.75 * inch, 1.45 * inch, 1.45 * inch, 0.75 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#181713")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D6D0C0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F6EF")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    story += [
        PageBreak(),
        Paragraph("Use On The Website", styles["Section"]),
        Paragraph(
            "Publish this PDF alongside the original local briefs. Pair each city card with its original source PDF so readers can inspect the full case, assumptions, and citations.",
            styles["Body"],
        ),
        Paragraph("Recommended Public Language", styles["Section"]),
        Paragraph(
            f"These 36 local and regional reports collectively claim approximately {data['aggregateTotalLabel']} in present-value reparations liability for the jurisdictions covered.",
            styles["Body"],
        ),
    ]
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    shutil.copy2(output, public_output)
    return output


if __name__ == "__main__":
    built = build_city_data()
    pdf_path = make_national_pdf(built)
    print(f"Wrote {DATA_DIR / 'reports.json'}")
    print(f"Wrote {pdf_path}")
    print(f"Copied reports into {REPORTS_DIR}")
