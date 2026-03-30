"""
Generates 30 sample PDFs for the evaluation harness.
Run once: python scripts/generate_sample_pdfs.py
"""
import json
from pathlib import Path
from fpdf import FPDF, XPos, YPos

OUT = Path(__file__).parent.parent / "sample_pdfs"
OUT.mkdir(exist_ok=True)

GT_PATH = Path(__file__).parent.parent / "eval" / "ground_truth.json"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

INVOICES = [
    {"sender": "Acme GmbH",         "recipient": "Beta Corp",          "date": "15.03.2024", "invoice_number": "INV-2024-001", "total": "1.250,00 EUR", "items": [("Software Development", "1", "1.050,00 EUR"), ("System Integration", "1", "200,00 EUR")]},
    {"sender": "TechSolutions AG",   "recipient": "Global Retail GmbH", "date": "02.04.2024", "invoice_number": "INV-2024-002", "total": "3.800,00 EUR", "items": [("Consulting Services", "4", "800,00 EUR"), ("Travel Expenses", "1", "200,00 EUR")]},
    {"sender": "DataWorks UG",       "recipient": "FinanceHub Ltd",     "date": "18.04.2024", "invoice_number": "INV-2024-003", "total": "650,00 EUR",   "items": [("Data Analysis Report", "1", "650,00 EUR")]},
    {"sender": "CloudPeak GmbH",     "recipient": "Stadtwerke Bonn",    "date": "05.05.2024", "invoice_number": "INV-2024-004", "total": "2.100,00 EUR", "items": [("Cloud Migration", "1", "1.800,00 EUR"), ("Support Hours", "3", "100,00 EUR")]},
    {"sender": "DesignLab Studio",   "recipient": "Markus Bauer",       "date": "22.05.2024", "invoice_number": "INV-2024-005", "total": "480,00 EUR",   "items": [("Logo Design", "1", "300,00 EUR"), ("Brand Manual", "1", "180,00 EUR")]},
    {"sender": "NetSecure GmbH",     "recipient": "MedTech AG",         "date": "10.06.2024", "invoice_number": "INV-2024-006", "total": "5.500,00 EUR", "items": [("Penetration Testing", "1", "4.000,00 EUR"), ("Security Report", "1", "1.500,00 EUR")]},
    {"sender": "PrintMaster KG",     "recipient": "Verlag Hoffmann",    "date": "28.06.2024", "invoice_number": "INV-2024-007", "total": "920,00 EUR",   "items": [("Brochure Printing 500x", "1", "750,00 EUR"), ("Delivery", "1", "170,00 EUR")]},
    {"sender": "LegalTech UG",       "recipient": "Kanzlei Schneider",  "date": "14.07.2024", "invoice_number": "INV-2024-008", "total": "1.800,00 EUR", "items": [("Software License", "1", "1.200,00 EUR"), ("Training Session", "2", "300,00 EUR")]},
    {"sender": "GreenEnergy GmbH",   "recipient": "Bauamt Hamburg",     "date": "31.07.2024", "invoice_number": "INV-2024-009", "total": "7.200,00 EUR", "items": [("Solar Panel Installation", "1", "6.500,00 EUR"), ("Inspection Fee", "1", "700,00 EUR")]},
    {"sender": "AutoServ AG",        "recipient": "Logistik Weber",     "date": "19.08.2024", "invoice_number": "INV-2024-010", "total": "340,00 EUR",   "items": [("Vehicle Inspection", "2", "120,00 EUR"), ("Oil Change", "2", "50,00 EUR")]},
]

ID_FORMS = [
    {"full_name": "Maria Mustermann",  "date_of_birth": "12.05.1990", "id_number": "DE123456789", "nationality": "German",     "address": "Hauptstrasse 7, 20095 Hamburg"},
    {"full_name": "Thomas Richter",    "date_of_birth": "03.11.1985", "id_number": "DE987654321", "nationality": "German",     "address": "Gartenweg 14, 50667 Cologne"},
    {"full_name": "Priya Sharma",      "date_of_birth": "27.08.1993", "id_number": "IN456789012", "nationality": "Indian",     "address": "Schillerstrasse 3, 80336 Munich"},
    {"full_name": "Jean-Luc Moreau",   "date_of_birth": "15.02.1978", "id_number": "FR234567890", "nationality": "French",     "address": "Rheinufer 22, 40213 Dusseldorf"},
    {"full_name": "Sofia Rossi",       "date_of_birth": "09.07.1995", "id_number": "IT345678901", "nationality": "Italian",    "address": "Bahnhofstrasse 11, 10115 Berlin"},
    {"full_name": "Ahmed Al-Farsi",    "date_of_birth": "21.12.1982", "id_number": "AE567890123", "nationality": "Emirati",    "address": "Lessingstrasse 5, 60329 Frankfurt"},
    {"full_name": "Emma Johnson",      "date_of_birth": "04.03.1999", "id_number": "GB678901234", "nationality": "British",    "address": "Mozartstrasse 8, 70182 Stuttgart"},
    {"full_name": "Carlos Fernandez",  "date_of_birth": "30.09.1976", "id_number": "ES789012345", "nationality": "Spanish",    "address": "Beethovenstrasse 19, 04109 Leipzig"},
    {"full_name": "Yuki Tanaka",       "date_of_birth": "17.06.1988", "id_number": "JP890123456", "nationality": "Japanese",   "address": "Friedrichstrasse 44, 01067 Dresden"},
    {"full_name": "Anna Kowalski",     "date_of_birth": "25.01.1991", "id_number": "PL901234567", "nationality": "Polish",     "address": "Marktplatz 2, 28195 Bremen"},
]

CONTRACTS = [
    {"party_a": "Acme GmbH",        "party_b": "Beta Corp",          "date": "01.01.2024", "subject": "Software Development Services",   "scope": "Party A will design, implement and test a document extraction pipeline. All deliverables due by 30.06.2024.", "payment": "12.000,00 EUR upon delivery."},
    {"party_a": "TechSolutions AG", "party_b": "RetailGroup GmbH",   "date": "15.01.2024", "subject": "IT Infrastructure Maintenance",    "scope": "Party A will maintain and monitor all IT infrastructure of Party B for a period of 12 months.", "payment": "2.000,00 EUR per month."},
    {"party_a": "DataWorks UG",     "party_b": "FinanceHub Ltd",     "date": "01.02.2024", "subject": "Data Analytics Consulting",        "scope": "Party A provides monthly data analysis reports and strategic recommendations based on Party B financial data.", "payment": "800,00 EUR per report."},
    {"party_a": "CloudPeak GmbH",   "party_b": "Stadtwerke Bonn",   "date": "20.02.2024", "subject": "Cloud Migration Project",          "scope": "Party A will migrate all on-premise systems of Party B to a cloud-based infrastructure within 6 months.", "payment": "25.000,00 EUR fixed fee."},
    {"party_a": "NetSecure GmbH",   "party_b": "MedTech AG",        "date": "05.03.2024", "subject": "Cybersecurity Assessment",         "scope": "Party A will perform a full penetration test and deliver a detailed security assessment report within 30 days.", "payment": "5.500,00 EUR upon report delivery."},
    {"party_a": "LegalTech UG",     "party_b": "Kanzlei Schneider", "date": "18.03.2024", "subject": "Legal Software Licensing",         "scope": "Party A grants Party B a non-exclusive license to use the CaseMgr v3 software for 2 years.", "payment": "1.200,00 EUR per year."},
    {"party_a": "GreenEnergy GmbH", "party_b": "Bauamt Hamburg",    "date": "02.04.2024", "subject": "Solar Installation Contract",      "scope": "Party A will supply and install a 50kW solar panel system at the premises of Party B. Warranty: 10 years.", "payment": "7.200,00 EUR upon commissioning."},
    {"party_a": "DesignLab Studio", "party_b": "Startup Nexus UG",  "date": "22.04.2024", "subject": "Brand Identity Design",           "scope": "Party A will deliver a full brand identity package including logo, color scheme, typography and brand manual.", "payment": "3.500,00 EUR, 50% upfront."},
    {"party_a": "AutoServ AG",      "party_b": "Logistik Weber",    "date": "10.05.2024", "subject": "Fleet Maintenance Agreement",      "scope": "Party A will perform quarterly vehicle inspections and all routine maintenance for the fleet of 8 vehicles of Party B.", "payment": "340,00 EUR per vehicle per quarter."},
    {"party_a": "PrintMaster KG",   "party_b": "Verlag Hoffmann",   "date": "28.05.2024", "subject": "Print Services Framework Contract","scope": "Party A will provide on-demand printing services for Party B for a period of 24 months at agreed unit prices.", "payment": "As per order confirmation."},
]


# ---------------------------------------------------------------------------
# PDF builders
# ---------------------------------------------------------------------------

def cell(pdf, w, h, txt, bold=False, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT):
    style = "B" if bold else ""
    pdf.set_font("Helvetica", style, 11)
    pdf.cell(w, h, txt, border=border, new_x=new_x, new_y=new_y)


def make_invoice(data: dict, idx: int) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"From:  {data['sender']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    pdf.cell(0, 7, f"To:    {data['recipient']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    cell(pdf, 60, 7, "Invoice Number:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["invoice_number"])
    cell(pdf, 60, 7, "Date:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["date"])
    pdf.ln(6)

    cell(pdf, 100, 8, "Description", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 40,  8, "Qty",         border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, "Amount",      border=1)
    for desc, qty, amount in data["items"]:
        cell(pdf, 100, 8, desc,   border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 40,  8, qty,    border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 0,   8, amount, border=1)
    pdf.ln(4)

    cell(pdf, 140, 8, "Total:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, data["total"], bold=True)

    path = OUT / f"invoice_{idx:02d}.pdf"
    pdf.output(str(path))
    return path


def make_id_form(data: dict, idx: int) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "REGISTRATION FORM", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)

    fields = [
        ("Full Name",     data["full_name"]),
        ("Date of Birth", data["date_of_birth"]),
        ("ID Number",     data["id_number"]),
        ("Nationality",   data["nationality"]),
        ("Address",       data["address"]),
    ]
    for label, value in fields:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 9, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    path = OUT / f"id_form_{idx:02d}.pdf"
    pdf.output(str(path))
    return path


def make_contract(data: dict, idx: int) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "SERVICE CONTRACT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Subject: {data['subject']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7,
        f"This contract is entered into on {data['date']} between {data['party_a']} "
        f"(hereinafter 'Party A') and {data['party_b']} (hereinafter 'Party B')."
    )
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "1. Scope of Work", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, data["scope"])
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "2. Payment", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, data["payment"])
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "3. Signatures", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(90, 7, f"Party A: {data['party_a']}", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(0,  7, f"Party B: {data['party_b']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.cell(90, 7, "________________________", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(0,  7, "________________________", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    path = OUT / f"contract_{idx:02d}.pdf"
    pdf.output(str(path))
    return path


# ---------------------------------------------------------------------------
# Ground truth
# ---------------------------------------------------------------------------

def build_ground_truth() -> list[dict]:
    cases = []
    for i, data in enumerate(INVOICES, 1):
        cases.append({
            "id": f"invoice_{i:02d}",
            "pdf": f"sample_pdfs/invoice_{i:02d}.pdf",
            "schema": "schemas/invoice_schema.json",
            "expected": {
                "sender":         data["sender"],
                "recipient":      data["recipient"],
                "date":           data["date"],
                "invoice_number": data["invoice_number"],
                "total":          data["total"],
            },
        })
    for i, data in enumerate(ID_FORMS, 1):
        cases.append({
            "id": f"id_form_{i:02d}",
            "pdf": f"sample_pdfs/id_form_{i:02d}.pdf",
            "schema": "schemas/id_form_schema.json",
            "expected": {
                "full_name":     data["full_name"],
                "date_of_birth": data["date_of_birth"],
                "id_number":     data["id_number"],
                "nationality":   data["nationality"],
            },
        })
    for i, data in enumerate(CONTRACTS, 1):
        cases.append({
            "id": f"contract_{i:02d}",
            "pdf": f"sample_pdfs/contract_{i:02d}.pdf",
            "schema": "schemas/contract_schema.json",
            "expected": {
                "party_a": data["party_a"],
                "party_b": data["party_b"],
                "date":    data["date"],
                "subject": data["subject"],
            },
        })
    return cases


# ---------------------------------------------------------------------------
# Varied / challenging PDFs
# Data has the same fields but layouts intentionally break assumptions:
#   - prose: values buried in running text, no "Label: Value" pattern
#   - reversed: recipient listed before sender
#   - multi-page: contract split across 2 pages
#   - noisy: extra legal boilerplate and irrelevant dates
#   - ambiguous labels: "Issued by" / "Bill to" instead of sender/recipient
# ---------------------------------------------------------------------------

VARIED = [
    # --- prose-style invoice: all fields embedded in a paragraph ---
    {
        "type": "prose_invoice",
        "id": "varied_01",
        "sender": "Orbit Digital GmbH",
        "recipient": "Nexus Retail AG",
        "date": "07.10.2024",
        "invoice_number": "ORB-2024-088",
        "total": "4.350,00 EUR",
        "body": (
            "Orbit Digital GmbH hereby submits invoice ORB-2024-088 dated 07.10.2024 "
            "to Nexus Retail AG for the delivery of e-commerce platform enhancements. "
            "The total amount due is 4.350,00 EUR, payable within 30 days of receipt."
        ),
    },
    # --- prose-style invoice ---
    {
        "type": "prose_invoice",
        "id": "varied_02",
        "sender": "Helix Consulting KG",
        "recipient": "Polaris Bank GmbH",
        "date": "23.10.2024",
        "invoice_number": "HLX-2024-044",
        "total": "9.800,00 EUR",
        "body": (
            "This invoice (ref. HLX-2024-044) is issued by Helix Consulting KG on "
            "23.10.2024 to Polaris Bank GmbH. Services rendered: strategic IT "
            "roadmap advisory. Total fee: 9.800,00 EUR."
        ),
    },
    # --- ambiguous labels: uses "Issued by" / "Billed to" / "Ref." / "Amount due" ---
    {
        "type": "ambiguous_invoice",
        "id": "varied_03",
        "sender": "Vega Systems UG",
        "recipient": "Draco Logistics GmbH",
        "date": "11.11.2024",
        "invoice_number": "VEG-2024-007",
        "total": "1.640,00 EUR",
    },
    # --- reversed layout: recipient block first, sender at the bottom ---
    {
        "type": "reversed_invoice",
        "id": "varied_04",
        "sender": "Sirius Software AG",
        "recipient": "Altair Media GmbH",
        "date": "30.11.2024",
        "invoice_number": "SRS-2024-019",
        "total": "2.750,00 EUR",
        "items": [("UI/UX Design", "1", "2.000,00 EUR"), ("QA Testing", "1", "750,00 EUR")],
    },
    # --- noisy invoice: multiple dates, legal boilerplate, distracting content ---
    {
        "type": "noisy_invoice",
        "id": "varied_05",
        "sender": "Pulsar Tech GmbH",
        "recipient": "Rigel Pharma AG",
        "date": "05.12.2024",
        "invoice_number": "PSR-2024-201",
        "total": "6.100,00 EUR",
        "order_date": "18.11.2024",   # distractor date
        "due_date": "05.01.2025",     # distractor date
        "items": [("Lab Software License", "1", "5.000,00 EUR"), ("Support Package", "1", "1.100,00 EUR")],
    },
    # --- ID form with unusual field labels ---
    {
        "type": "unusual_id",
        "id": "varied_06",
        "full_name": "Lena Brandt",
        "date_of_birth": "14.09.1987",
        "id_number": "DE556677889",
        "nationality": "German",
    },
    # --- ID form where name is split into first/last fields ---
    {
        "type": "split_name_id",
        "id": "varied_07",
        "full_name": "Marco Vitale",
        "date_of_birth": "02.04.1980",
        "id_number": "IT112233445",
        "nationality": "Italian",
        "first_name": "Marco",
        "last_name": "Vitale",
    },
    # --- multi-page contract (2 pages) ---
    {
        "type": "multipage_contract",
        "id": "varied_08",
        "party_a": "Zenith Labs GmbH",
        "party_b": "Aurora Ventures AG",
        "date": "01.03.2024",
        "subject": "Research and Development Partnership",
        "scope": (
            "Party A agrees to conduct joint R&D activities with Party B in the field "
            "of machine learning applied to biomedical imaging. Work packages and "
            "milestones are defined in Annex A, attached hereto."
        ),
        "clauses": [
            ("Intellectual Property", "All IP created jointly shall be co-owned equally by both parties. "
             "Neither party may license the joint IP to third parties without written consent."),
            ("Confidentiality", "Both parties agree to keep all shared data and findings strictly "
             "confidential for a period of 5 years following the end of this agreement."),
            ("Termination", "Either party may terminate this agreement with 3 months written notice. "
             "Obligations arising before termination remain in effect."),
        ],
    },
    # --- contract with data buried in preamble prose ---
    {
        "type": "prose_contract",
        "id": "varied_09",
        "party_a": "Luminar GmbH",
        "party_b": "Crestview Capital AG",
        "date": "15.06.2024",
        "subject": "Financial Advisory Services",
        "body": (
            "This agreement dated 15.06.2024 formalises the engagement between "
            "Luminar GmbH (advisor) and Crestview Capital AG (client) for the provision "
            "of ongoing financial advisory services. The subject of this contract is "
            "Financial Advisory Services. The agreement is valid for 12 months and may "
            "be renewed by mutual written consent."
        ),
    },
    # --- invoice with footer-only sender info ---
    {
        "type": "footer_invoice",
        "id": "varied_10",
        "sender": "Meridian Consulting AG",
        "recipient": "Stratos Holding GmbH",
        "date": "18.12.2024",
        "invoice_number": "MRD-2024-055",
        "total": "3.200,00 EUR",
        "items": [("Strategy Workshop", "2", "1.200,00 EUR"), ("Executive Report", "1", "800,00 EUR")],
    },
]


def make_prose_invoice(data: dict) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, data["body"])
    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_ambiguous_invoice(data: dict) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "TAX INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    rows = [
        ("Issued by",   data["sender"]),
        ("Billed to",   data["recipient"]),
        ("Ref.",        data["invoice_number"]),
        ("Issue date",  data["date"]),
        ("Amount due",  data["total"]),
    ]
    for label, value in rows:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(55, 8, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_reversed_invoice(data: dict) -> Path:
    """Recipient block first, sender only appears below the title line."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"To: {data['recipient']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"From: {data['sender']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    cell(pdf, 60, 7, "Invoice Number:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["invoice_number"])
    cell(pdf, 60, 7, "Date:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["date"])
    pdf.ln(6)

    cell(pdf, 100, 8, "Description", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 40,  8, "Qty",         border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, "Amount",      border=1)
    for desc, qty, amount in data["items"]:
        cell(pdf, 100, 8, desc,   border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 40,  8, qty,    border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 0,   8, amount, border=1)
    pdf.ln(4)
    cell(pdf, 140, 8, "Total:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, data["total"], bold=True)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_noisy_invoice(data: dict) -> Path:
    """Three dates on the page — model must pick the invoice date, not order or due date."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Original order date: {data['order_date']}   |   "
                   f"Invoice date: {data['date']}   |   Due date: {data['due_date']}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"From: {data['sender']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"To:   {data['recipient']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    cell(pdf, 60, 7, "Invoice Ref.:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["invoice_number"])
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6,
        "Please note: this invoice supersedes any previous pro-forma invoice. "
        "VAT registration: DE298374610. Payment terms: net 30 days from invoice date. "
        "Late payment interest: 8% p.a. as per §288 BGB."
    )
    pdf.ln(4)

    cell(pdf, 100, 8, "Description", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 40,  8, "Qty",         border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, "Amount",      border=1)
    for desc, qty, amount in data["items"]:
        cell(pdf, 100, 8, desc,   border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 40,  8, qty,    border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 0,   8, amount, border=1)
    pdf.ln(4)
    cell(pdf, 140, 8, "Total (excl. VAT):", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, data["total"], bold=True)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_unusual_id(data: dict) -> Path:
    """Uses non-standard labels: 'Surname, Given name', 'DoB', 'Document No.'"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "IDENTITY VERIFICATION FORM", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    fields = [
        ("Surname, Given name", data["full_name"]),
        ("DoB",                 data["date_of_birth"]),
        ("Document No.",        data["id_number"]),
        ("Country of citizenship", data["nationality"]),
    ]
    for label, value in fields:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(70, 9, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_split_name_id(data: dict) -> Path:
    """First and last name in separate fields — model must combine them."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "APPLICANT REGISTRATION", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    fields = [
        ("First Name",    data["first_name"]),
        ("Last Name",     data["last_name"]),
        ("Date of Birth", data["date_of_birth"]),
        ("ID Number",     data["id_number"]),
        ("Nationality",   data["nationality"]),
    ]
    for label, value in fields:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 9, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_multipage_contract(data: dict) -> Path:
    pdf = FPDF()

    # Page 1 — header, parties, scope
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "CONTRACT AGREEMENT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Subject: {data['subject']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7,
        f"Entered into on {data['date']} between {data['party_a']} ('Party A') "
        f"and {data['party_b']} ('Party B')."
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "1. Scope of Work", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, data["scope"])

    # Page 2 — additional clauses and signatures
    pdf.add_page()
    for i, (title, text) in enumerate(data["clauses"], 2):
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, f"{i}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, text)
        pdf.ln(3)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Signatures", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(90, 7, f"Party A: {data['party_a']}", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(0,  7, f"Party B: {data['party_b']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.cell(90, 7, "________________________", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(0,  7, "________________________", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_prose_contract(data: dict) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 10, "AGREEMENT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, data["body"])
    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


def make_footer_invoice(data: dict) -> Path:
    """Sender info only appears in small print at the bottom."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"To: {data['recipient']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    cell(pdf, 60, 7, "Invoice Number:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["invoice_number"])
    cell(pdf, 60, 7, "Date:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,  7, data["date"])
    pdf.ln(6)

    cell(pdf, 100, 8, "Description", border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 40,  8, "Qty",         border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, "Amount",      border=1)
    for desc, qty, amount in data["items"]:
        cell(pdf, 100, 8, desc,   border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 40,  8, qty,    border=1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        cell(pdf, 0,   8, amount, border=1)
    pdf.ln(4)
    cell(pdf, 140, 8, "Total:", bold=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
    cell(pdf, 0,   8, data["total"], bold=True)

    # Sender only in footer
    pdf.set_y(260)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, f"{data['sender']}  |  Registered in Germany  |  VAT: DE399012876",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_text_color(0, 0, 0)

    path = OUT / f"{data['id']}.pdf"
    pdf.output(str(path))
    return path


VARIED_BUILDERS = {
    "prose_invoice":    make_prose_invoice,
    "ambiguous_invoice": make_ambiguous_invoice,
    "reversed_invoice": make_reversed_invoice,
    "noisy_invoice":    make_noisy_invoice,
    "unusual_id":       make_unusual_id,
    "split_name_id":    make_split_name_id,
    "multipage_contract": make_multipage_contract,
    "prose_contract":   make_prose_contract,
    "footer_invoice":   make_footer_invoice,
}

VARIED_SCHEMAS = {
    "prose_invoice":    "schemas/invoice_schema.json",
    "ambiguous_invoice":"schemas/invoice_schema.json",
    "reversed_invoice": "schemas/invoice_schema.json",
    "noisy_invoice":    "schemas/invoice_schema.json",
    "footer_invoice":   "schemas/invoice_schema.json",
    "unusual_id":       "schemas/id_form_schema.json",
    "split_name_id":    "schemas/id_form_schema.json",
    "multipage_contract":"schemas/contract_schema.json",
    "prose_contract":   "schemas/contract_schema.json",
}

VARIED_EXPECTED = {
    "prose_invoice":    lambda d: {"sender": d["sender"], "recipient": d["recipient"], "date": d["date"], "invoice_number": d["invoice_number"], "total": d["total"]},
    "ambiguous_invoice":lambda d: {"sender": d["sender"], "recipient": d["recipient"], "date": d["date"], "invoice_number": d["invoice_number"], "total": d["total"]},
    "reversed_invoice": lambda d: {"sender": d["sender"], "recipient": d["recipient"], "date": d["date"], "invoice_number": d["invoice_number"], "total": d["total"]},
    "noisy_invoice":    lambda d: {"sender": d["sender"], "recipient": d["recipient"], "date": d["date"], "invoice_number": d["invoice_number"], "total": d["total"]},
    "footer_invoice":   lambda d: {"sender": d["sender"], "recipient": d["recipient"], "date": d["date"], "invoice_number": d["invoice_number"], "total": d["total"]},
    "unusual_id":       lambda d: {"full_name": d["full_name"], "date_of_birth": d["date_of_birth"], "id_number": d["id_number"], "nationality": d["nationality"]},
    "split_name_id":    lambda d: {"full_name": d["full_name"], "date_of_birth": d["date_of_birth"], "id_number": d["id_number"], "nationality": d["nationality"]},
    "multipage_contract":lambda d: {"party_a": d["party_a"], "party_b": d["party_b"], "date": d["date"], "subject": d["subject"]},
    "prose_contract":   lambda d: {"party_a": d["party_a"], "party_b": d["party_b"], "date": d["date"], "subject": d["subject"]},
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    for i, data in enumerate(INVOICES, 1):
        make_invoice(data, i)
        print(f"  invoice_{i:02d}.pdf")
    for i, data in enumerate(ID_FORMS, 1):
        make_id_form(data, i)
        print(f"  id_form_{i:02d}.pdf")
    for i, data in enumerate(CONTRACTS, 1):
        make_contract(data, i)
        print(f"  contract_{i:02d}.pdf")

    for data in VARIED:
        t = data["type"]
        VARIED_BUILDERS[t](data)
        print(f"  {data['id']}.pdf  [{t}]")

    gt = build_ground_truth()
    for data in VARIED:
        t = data["type"]
        gt.append({
            "id": data["id"],
            "pdf": f"sample_pdfs/{data['id']}.pdf",
            "schema": VARIED_SCHEMAS[t],
            "expected": VARIED_EXPECTED[t](data),
            "note": t,
        })

    GT_PATH.write_text(json.dumps(gt, indent=4, ensure_ascii=False))
    print(f"\nGround truth written: {len(gt)} cases -> {GT_PATH}")
