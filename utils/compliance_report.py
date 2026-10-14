"""
Compliance Report Generation Engine.
Exports WCAG 2.2, Section 508, and EN 301 549 compliance audit results in
PDF, DOCX, CSV, and JSON formats without altering existing reporting engines.
"""

import io
import json
from typing import Dict, Any, List
import pandas as pd

# Safe ReportLab PDF imports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Safe python-docx imports
try:
    import docx
    from docx.shared import Pt, RGBColor
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


def generate_compliance_json_report(compliance_data: Dict[str, Any], doc_title: str = "WCAG Compliance Report") -> str:
    """Generate structured JSON compliance audit report."""
    payload = {
        "report_title": doc_title,
        "standard": "WCAG 2.2 / Section 508 / EN 301 549",
        "overall_tier": compliance_data.get("overall_tier", "Unknown"),
        "badge_text": compliance_data.get("badge_text", ""),
        "compliance_score": compliance_data.get("compliance_score", 0.0),
        "total_criteria": compliance_data.get("total_criteria", 0),
        "passed_criteria": compliance_data.get("passed_criteria", 0),
        "failed_criteria": compliance_data.get("failed_criteria", 0),
        "level_counts": compliance_data.get("level_counts", {}),
        "criteria_results": compliance_data.get("criteria_results", []),
        "enriched_issues": compliance_data.get("enriched_issues", [])
    }
    return json.dumps(payload, indent=2)


def generate_compliance_csv_report(compliance_data: Dict[str, Any]) -> str:
    """Generate CSV spreadsheet string of criteria evaluation and issue breakdown."""
    rows = []
    for crit in compliance_data.get("criteria_results", []):
        rows.append({
            "Criterion": crit.get("criterion", ""),
            "Name": crit.get("name", ""),
            "Level": crit.get("level", ""),
            "Status": crit.get("status", ""),
            "Violations Count": crit.get("violations_count", 0),
            "WCAG Principle": crit.get("principle", ""),
            "Section 508 Standard": crit.get("section_508", ""),
            "EN 301 549 Reference": crit.get("en_301_549", "")
        })
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)


def generate_compliance_docx_report(compliance_data: Dict[str, Any], doc_title: str = "WCAG 2.2 Compliance Audit") -> bytes:
    """Generate Word DOCX compliance audit document bytes."""
    if not DOCX_AVAILABLE:
        return b"DOCX library (python-docx) is missing."
        
    doc = docx.Document()
    
    # Document Title
    heading = doc.add_heading(doc_title, level=0)
    if heading.runs:
        heading.runs[0].font.color.rgb = RGBColor(99, 102, 241)
        
    doc.add_paragraph("Standards: WCAG 2.2 (Levels A / AA / AAA) • US Section 508 • European EN 301 549")
    doc.add_paragraph(f"Overall Certification Status: {compliance_data.get('badge_text', 'Evaluated')}")
    doc.add_paragraph(f"Compliance Pass Rate: {compliance_data.get('compliance_score', 0)}%")
    
    # KPI Scorecard Table
    doc.add_heading("1. Executive Compliance Scorecard", level=1)
    table_kpi = doc.add_table(rows=6, cols=2)
    table_kpi.style = 'Table Grid'
    
    kpis = [
        ("Certification Tier", compliance_data.get("overall_tier", "N/A")),
        ("Total Criteria Evaluated", str(compliance_data.get("total_criteria", 0))),
        ("Passed Criteria", str(compliance_data.get("passed_criteria", 0))),
        ("Failed Criteria", str(compliance_data.get("failed_criteria", 0))),
        ("Level A Status", "PASSED" if compliance_data.get("level_a_passed") else "FAILED"),
        ("Level AA Status", "PASSED" if compliance_data.get("level_aa_passed") else "FAILED")
    ]
    
    for idx, (lbl, val) in enumerate(kpis):
        table_kpi.cell(idx, 0).text = lbl
        table_kpi.cell(idx, 1).text = val
        
    doc.add_paragraph()
    
    # Success Criteria Breakdown Table
    doc.add_heading("2. Success Criteria Audit Matrix", level=1)
    criteria = compliance_data.get("criteria_results", [])
    
    if criteria:
        table_crit = doc.add_table(rows=len(criteria) + 1, cols=5)
        table_crit.style = 'Table Grid'
        
        headers = ["Criterion", "Name", "Level", "Status", "Violations"]
        for col_idx, h_text in enumerate(headers):
            cell = table_crit.cell(0, col_idx)
            cell.text = h_text
            if cell.paragraphs and cell.paragraphs[0].runs:
                cell.paragraphs[0].runs[0].bold = True
                
        for row_idx, crit in enumerate(criteria, start=1):
            table_crit.cell(row_idx, 0).text = str(crit.get("criterion", ""))
            table_crit.cell(row_idx, 1).text = str(crit.get("name", ""))
            table_crit.cell(row_idx, 2).text = str(crit.get("level", ""))
            table_crit.cell(row_idx, 3).text = str(crit.get("status", ""))
            table_crit.cell(row_idx, 4).text = str(crit.get("violations_count", 0))
            
    doc.add_paragraph()
    
    # Detailed Violations & Remediation Section
    doc.add_heading("3. Detailed Violations & Actionable Remediation", level=1)
    enriched_issues = compliance_data.get("enriched_issues", [])
    
    if not enriched_issues:
        doc.add_paragraph("Congratulations! No cognitive or accessibility violations were detected. The copy complies with all evaluated criteria.")
    else:
        for idx, iss in enumerate(enriched_issues, 1):
            p = doc.add_paragraph()
            p.add_run(f"#{idx}. {iss.get('title', 'Violation')} [{iss.get('severity', 'Medium')}]").bold = True
            p.add_run(f"\nCriterion: {iss.get('wcag_criterion')} {iss.get('wcag_name')} ({iss.get('wcag_level')})")
            p.add_run(f"\nSection 508: {iss.get('section_508')}")
            p.add_run(f"\nEN 301 549: {iss.get('en_301_549')}")
            p.add_run(f"\nExplanation: {iss.get('explanation')}")
            if iss.get("snippet"):
                p.add_run(f"\nSnippet: \"{iss.get('snippet')}\"")
            if iss.get("wcag_remediation"):
                p.add_run(f"\nRemediation: {iss.get('wcag_remediation')}")
            doc.add_paragraph()
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def generate_compliance_pdf_report(compliance_data: Dict[str, Any], doc_title: str = "WCAG 2.2 Compliance Audit") -> bytes:
    """Generate high-quality PDF compliance audit report bytes using ReportLab."""
    if not REPORTLAB_AVAILABLE:
        return b"PDF library (reportlab) is missing."
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=12,
        spaceAfter=6
    )
    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor(compliance_data.get("badge_color", "#10b981")),
        fontName='Helvetica-Bold'
    )
    normal_style = styles['Normal']
    
    elements = []
    
    # Title & Metadata
    elements.append(Paragraph(doc_title, title_style))
    elements.append(Paragraph("Standards Audit: WCAG 2.2 • U.S. Section 508 • European EN 301 549", normal_style))
    elements.append(Paragraph(f"Status: {compliance_data.get('badge_text', '')}", badge_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=8, spaceAfter=12))
    
    # Scorecard Table
    elements.append(Paragraph("Executive Compliance Scorecard", h2_style))
    scorecard_data = [
        ["Standard Metric", "Evaluation Result"],
        ["Overall Certification Tier", compliance_data.get("overall_tier", "N/A")],
        ["Compliance Pass Rate", f"{compliance_data.get('compliance_score', 0)}%"],
        ["Total Criteria Evaluated", str(compliance_data.get("total_criteria", 0))],
        ["Passed Criteria", str(compliance_data.get("passed_criteria", 0))],
        ["Failed Criteria", str(compliance_data.get("failed_criteria", 0))],
        ["Level A Compliance (Must Have)", "PASSED (100%)" if compliance_data.get("level_a_passed") else "FAILED (Violations Present)"],
        ["Level AA Compliance (Standard)", "PASSED" if compliance_data.get("level_aa_passed") else "FAILED"]
    ]
    
    t_score = Table(scorecard_data, colWidths=[240, 260])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    elements.append(t_score)
    elements.append(Spacer(1, 10))
    
    # Criteria Matrix Table
    elements.append(Paragraph("Success Criteria Audit Breakdown", h2_style))
    criteria_data = [["Criterion", "Name", "Level", "Status", "Issues"]]
    
    for crit in compliance_data.get("criteria_results", []):
        criteria_data.append([
            crit.get("criterion", ""),
            crit.get("name", ""),
            crit.get("level", ""),
            crit.get("status", ""),
            str(crit.get("violations_count", 0))
        ])
        
    t_crit = Table(criteria_data, colWidths=[65, 210, 75, 75, 75])
    t_crit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    elements.append(t_crit)
    elements.append(Spacer(1, 10))
    
    # Detailed Violations
    elements.append(Paragraph("Actionable Findings & Standard Remediation", h2_style))
    enriched_issues = compliance_data.get("enriched_issues", [])
    if not enriched_issues:
        elements.append(Paragraph("No accessibility violations detected. The document meets cognitive inclusion benchmarks.", normal_style))
    else:
        for idx, iss in enumerate(enriched_issues[:15], 1):
            detail_text = (
                f"<b>#{idx}. {iss.get('title')}</b> [{iss.get('severity')}]<br/>"
                f"<i>Criterion:</i> {iss.get('wcag_criterion')} - {iss.get('wcag_name')} ({iss.get('wcag_level')})<br/>"
                f"<i>Section 508:</i> {iss.get('section_508')}<br/>"
                f"<i>Remediation:</i> {iss.get('wcag_remediation')}"
            )
            elements.append(Paragraph(detail_text, normal_style))
            elements.append(Spacer(1, 6))
            
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
