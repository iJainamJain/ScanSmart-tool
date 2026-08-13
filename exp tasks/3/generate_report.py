"""Generate a PDF report for Task 3: Image Enhancement in the Spatial Domain.

Creates a professional lab-report-style PDF embedding all generated figures,
observations, and documentation.

Run from the project root:
    .venv\\Scripts\\python.exe "exp tasks/3/generate_report.py"
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.lib import colors

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
REPORT_PATH = Path(__file__).resolve().parent / "Task3_Report.pdf"


def build_styles():
    """Create custom paragraph styles for the report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontSize=28,
        leading=34,
        spaceAfter=6 * mm,
        textColor=HexColor("#1a1a2e"),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontSize=14,
        leading=18,
        textColor=HexColor("#16213e"),
        alignment=TA_CENTER,
        spaceAfter=4 * mm,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=10 * mm,
        spaceAfter=4 * mm,
        textColor=HexColor("#0f3460"),
        borderWidth=0,
        borderPadding=0,
    ))
    styles.add(ParagraphStyle(
        name="SubHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        spaceBefore=6 * mm,
        spaceAfter=3 * mm,
        textColor=HexColor("#16213e"),
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=3 * mm,
    ))
    styles.add(ParagraphStyle(
        name="Caption",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=HexColor("#555555"),
        spaceAfter=6 * mm,
        spaceBefore=2 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BulletItem",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        leftIndent=12 * mm,
        bulletIndent=6 * mm,
        spaceAfter=2 * mm,
    ))
    return styles


def add_cover_page(story, styles):
    """Add a title/cover page."""
    story.append(Spacer(1, 60 * mm))
    story.append(Paragraph("Semester Mini Project - Task 3", styles["CoverTitle"]))
    story.append(Paragraph(
        "Image Enhancement in the Spatial Domain",
        styles["CoverSubtitle"],
    ))
    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(
        width="60%", thickness=1.5, color=HexColor("#0f3460"),
        spaceAfter=10 * mm, spaceBefore=4 * mm,
    ))
    story.append(Paragraph(
        "<b>Course:</b> Digital Image Processing", styles["CoverSubtitle"]
    ))
    story.append(Paragraph(
        "<b>Project:</b> SmartScan AI - Intelligent Document Scanner",
        styles["CoverSubtitle"],
    ))
    story.append(Spacer(1, 8 * mm))

    # Team table
    team_data = [
        ["Team Member", "Contribution"],
        ["Jainam Jain", "Core pipeline, boundary detection, GUI, OCR"],
        ["Dhanush", "Dataset collection (148 photos)"],
        ["Vivek", "Dataset collection (104 photos)"],
    ]
    team_table = Table(team_data, colWidths=[6 * cm, 10 * cm])
    team_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f0f0f0"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(team_table)
    story.append(PageBreak())


def add_aim(story, styles):
    """Section: Aim."""
    story.append(Paragraph("1. Aim", styles["SectionHeading"]))
    story.append(Paragraph(
        "To implement and analyse spatial-domain image enhancement techniques "
        "- intensity transformations, histogram operations, and image arithmetic "
        "- and integrate them as pre-processing capabilities in the SmartScan AI "
        "document scanner. These techniques serve as the foundation for the "
        "segmentation module that follows.",
        styles["BodyText2"],
    ))


def add_task2(story, styles):
    """Section: Task 2 - Intensity Transformations."""
    story.append(Paragraph("2. Intensity Transformation Techniques", styles["SectionHeading"]))
    story.append(Paragraph(
        "Four classical intensity transformations were implemented and tested on "
        "document images from our self-captured dataset:",
        styles["BodyText2"],
    ))

    # Techniques table
    tech_data = [
        ["Technique", "Formula", "Purpose"],
        ["Image Negative", "s = 255 - r", "Invert intensity; enhance bright details in dark regions"],
        ["Log Transform", "s = c * log(1 + r)", "Compress highlights, expand shadows; good for dark images"],
        ["Gamma (Power-Law)", "s = c * r^gamma", "gamma<1 brightens, gamma>1 darkens; exposure correction"],
        ["Contrast Stretching", "Piecewise linear", "Stretch a narrow band to full [0,255] range"],
    ]
    tech_table = Table(tech_data, colWidths=[3.8 * cm, 4 * cm, 8.5 * cm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f0f0f0"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 4 * mm))

    # Add the figure
    img_path = OUTPUT_DIR / "task2_intensity_transforms.png"
    if img_path.exists():
        story.append(Image(str(img_path), width=17 * cm, height=8.5 * cm))
        story.append(Paragraph(
            "Figure 1: All intensity transformations applied to jainam_doc_02.jpg. "
            "Note how Gamma=0.4 brightens the document while Gamma=2.5 darkens it. "
            "The log transform compresses highlights significantly.",
            styles["Caption"],
        ))


def add_task3(story, styles):
    """Section: Task 3 - Histogram Analysis."""
    story.append(Paragraph("3. Histogram Analysis", styles["SectionHeading"]))
    story.append(Paragraph(
        "Histograms visualise the distribution of pixel intensities in an image. "
        "A narrow, peaked histogram indicates low contrast, while a broad spread "
        "indicates high contrast. By comparing histograms before and after "
        "enhancement, we can quantitatively verify that a technique actually "
        "improved the image rather than relying on subjective visual judgement.",
        styles["BodyText2"],
    ))

    img_path = OUTPUT_DIR / "task3_histogram_analysis.png"
    if img_path.exists():
        story.append(Image(str(img_path), width=15 * cm, height=10.7 * cm))
        story.append(Paragraph(
            "Figure 2: Histogram comparison before and after Gamma=0.5 enhancement. "
            "The original histogram is clustered in the mid-range; after enhancement, "
            "the distribution shifts rightward (brighter) and broadens.",
            styles["Caption"],
        ))


def add_task4(story, styles):
    """Section: Task 4 - Histogram Equalization."""
    story.append(PageBreak())
    story.append(Paragraph("4. Histogram Equalization", styles["SectionHeading"]))
    story.append(Paragraph(
        "Histogram equalization transforms pixel intensities so that the output "
        "histogram is approximately uniform (flat). This maximises image contrast "
        "by spreading intensity values across the full [0, 255] range.",
        styles["BodyText2"],
    ))

    img_path = OUTPUT_DIR / "task4_histogram_equalization.png"
    if img_path.exists():
        story.append(Image(str(img_path), width=15 * cm, height=10.7 * cm))
        story.append(Paragraph(
            "Figure 3: Original vs histogram-equalized image with their histograms. "
            "Standard deviation increased from 63.5 to 74.0, confirming improved contrast.",
            styles["Caption"],
        ))

    story.append(Paragraph("Observation", styles["SubHeading"]))
    story.append(Paragraph(
        "The original image's histogram is clustered in a narrow intensity band "
        "(low contrast). After equalization, the histogram spreads across the full "
        "[0, 255] range (std dev 63.5 -> 74.0), improving contrast especially in "
        "regions that were previously indistinguishable. However, histogram "
        "equalization can amplify sensor noise in already-bright regions, which is "
        "why our main pipeline uses CLAHE (Contrast Limited Adaptive Histogram "
        "Equalization) instead - it applies equalization locally per tile, avoiding "
        "global over-amplification.",
        styles["BodyText2"],
    ))


def add_task5(story, styles):
    """Section: Task 5 - Image Arithmetic."""
    story.append(Paragraph("5. Image Arithmetic Operations", styles["SectionHeading"]))

    ops_data = [
        ["Operation", "Formula", "Practical Application"],
        ["Addition", "alpha*I1 + (1-alpha)*I2",
         "Image fusion - combining multi-sensor data (e.g., visible + infrared)"],
        ["Subtraction", "|I1 - I2|",
         "Change/motion detection - subtracting a reference frame reveals moving objects"],
        ["Averaging", "(1/N) * sum(Ik)",
         "Noise reduction - averaging N noisy captures reduces noise by sqrt(N)"],
    ]
    ops_table = Table(ops_data, colWidths=[3 * cm, 4.5 * cm, 8.8 * cm])
    ops_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f0f0f0"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(ops_table)
    story.append(Spacer(1, 4 * mm))

    img_path = OUTPUT_DIR / "task5_arithmetic_operations.png"
    if img_path.exists():
        story.append(Image(str(img_path), width=16 * cm, height=10 * cm))
        story.append(Paragraph(
            "Figure 4: Top row - two source images and their weighted addition. "
            "Bottom row - absolute subtraction highlighting differences, "
            "one of five noisy copies, and the averaged result showing noise reduction.",
            styles["Caption"],
        ))


def add_task6(story, styles):
    """Section: Task 6 - Comparison."""
    story.append(PageBreak())
    story.append(Paragraph("6. Comparative Enhancement Analysis", styles["SectionHeading"]))
    story.append(Paragraph(
        "All enhancement techniques were applied to three different images from our "
        "dataset, chosen to represent different lighting conditions and camera setups. "
        "The comparison grid below shows the visual results, and the table provides "
        "quantitative brightness (mean) and contrast (std dev) measurements.",
        styles["BodyText2"],
    ))

    img_path = OUTPUT_DIR / "task6_comparison_grid.png"
    if img_path.exists():
        story.append(Image(str(img_path), width=17 * cm, height=10.5 * cm))
        story.append(Paragraph(
            "Figure 5: All 7 enhancement techniques applied across 3 different document images.",
            styles["Caption"],
        ))

    # Metrics table
    metrics_data = [
        ["Image", "Orig mean/std", "Negative", "Log", "Gamma=0.4", "Gamma=2.0", "Contrast Str.", "Hist. Eq."],
        ["jainam_doc_02", "128/63.5", "127/63.5", "213/36.6", "184/48.6", "80/55.0", "151/107.7", "129/74.0"],
        ["dhanush_doc_003", "167/56.5", "88/56.5", "230/26.1", "210/38.4", "122/56.7", "205/93.1", "129/74.1"],
        ["vivek_doc_010", "178/19.2", "77/19.2", "238/5.5", "220/10.1", "125/25.3", "234/31.6", "130/74.4"],
    ]
    metrics_table = Table(metrics_data, colWidths=[2.6*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f0f0f0"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("Best Technique per Image", styles["SubHeading"]))
    story.append(Paragraph(
        "<b>Image 1 (jainam_doc_02):</b> Histogram Equalization - provides the best "
        "contrast spread for an indoor document with moderate lighting.",
        styles["BulletItem"],
    ))
    story.append(Paragraph(
        "<b>Image 2 (dhanush_doc_003):</b> Gamma=0.4 - effectively brightens the "
        "underexposed capture without harsh redistribution artefacts.",
        styles["BulletItem"],
    ))
    story.append(Paragraph(
        "<b>Image 3 (vivek_doc_010):</b> Contrast Stretching - balances detail "
        "enhancement without over-amplifying noise in an already-bright image.",
        styles["BulletItem"],
    ))


def add_challenges_and_conclusion(story, styles):
    """Section: Challenges and Conclusion."""
    story.append(Paragraph("7. Challenges Faced", styles["SectionHeading"]))
    challenges = [
        "<b>Parameter sensitivity:</b> Log and gamma transforms require careful "
        "tuning of c and gamma; wrong values either wash out or crush the image.",
        "<b>Noise amplification:</b> Histogram equalization amplifies sensor noise "
        "alongside useful detail. This is why our main pipeline uses CLAHE "
        "(localised equalization) instead of global equalization.",
        "<b>Arithmetic dimension mismatch:</b> Real dataset images have different "
        "resolutions, so arithmetic operations require explicit resizing before "
        "computation.",
    ]
    for ch in challenges:
        story.append(Paragraph(ch, styles["BulletItem"]))

    story.append(Paragraph("8. Conclusion", styles["SectionHeading"]))
    story.append(Paragraph(
        "Spatial-domain enhancement techniques are powerful tools for improving "
        "document image quality before segmentation. Through quantitative measurement "
        "(histogram analysis, std dev comparison), we confirmed that histogram "
        "equalization and gamma correction are the most impactful for our document "
        "scanning use case. These techniques are now available as reusable modules in "
        "our project (src/enhancement/intensity.py, src/enhancement/arithmetic.py) and "
        "integrated into both the CLI and Streamlit GUI pipelines.",
        styles["BodyText2"],
    ))
    story.append(Paragraph(
        "The key takeaway is that enhancement technique selection is image-dependent: "
        "no single transform is universally best. Histogram equalization works well for "
        "low-contrast indoor documents, gamma correction excels at exposure compensation, "
        "and contrast stretching provides controlled enhancement without noise amplification.",
        styles["BodyText2"],
    ))


def main():
    print(f"Generating PDF report: {REPORT_PATH}")

    doc = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = build_styles()
    story = []

    add_cover_page(story, styles)
    add_aim(story, styles)
    add_task2(story, styles)
    add_task3(story, styles)
    add_task4(story, styles)
    add_task5(story, styles)
    add_task6(story, styles)
    add_challenges_and_conclusion(story, styles)

    doc.build(story)
    print(f"Done! Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
