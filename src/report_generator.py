import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:

    @staticmethod
    def generate(data, critical_screenshot=None):

        filename = datetime.now().strftime(
            "Driver_Report_%Y%m%d_%H%M%S.pdf"
        )

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        # ---------------------------------
        # TITLE
        # ---------------------------------

        story.append(
            Paragraph(
                "<font size=24><b>NeuroGuard X</b></font>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "<font size=16>AI Driver Monitoring Report</font>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 20))

        # ---------------------------------
        # DATE & TIME
        # ---------------------------------

        story.append(
            Paragraph(
                f"<b>Date & Time :</b> "
                f"{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        # ---------------------------------
        # DRIVER DATA TABLE
        # ---------------------------------

        table_data = [
            ["Parameter", "Value"]
        ]

        for key, value in data.items():

            table_data.append(
                [key, str(value)]
            )

        table = Table(
            table_data,
            colWidths=[200, 220]
        )

        table.setStyle(
            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ])
        )

        story.append(table)

        story.append(Spacer(1, 20))

        # ---------------------------------
        # OVERALL DRIVER STATUS
        # ---------------------------------

        status = data.get(
            "Status",
            "SAFE"
        )

        if status == "SAFE":

            status_text = (
                "<font color='green'>"
                "<b>Overall Driver Status : SAFE</b>"
                "</font>"
            )

            recommendation = (
                "Driver remained alert throughout the session."
            )

        elif status == "WARNING":

            status_text = (
                "<font color='orange'>"
                "<b>Overall Driver Status : WARNING</b>"
                "</font>"
            )

            recommendation = (
                "Driver showed signs of drowsiness. "
                "A short break is recommended."
            )

        else:

            status_text = (
                "<font color='red'>"
                "<b>Overall Driver Status : CRITICAL</b>"
                "</font>"
            )

            recommendation = (
                "Driver reached a critical drowsiness level. "
                "Stop the vehicle immediately and take adequate rest."
            )

        story.append(
            Paragraph(
                status_text,
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 15))

        # ---------------------------------
        # RECOMMENDATION
        # ---------------------------------

        story.append(
            Paragraph(
                f"<b>Recommendation :</b>"
                f"<br/><br/>"
                f"{recommendation}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        # ---------------------------------
        # CRITICAL SCREENSHOT
        # ---------------------------------

        story.append(
            Paragraph(
                "<b>Critical Event Screenshot</b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))

        if (
            critical_screenshot
            and os.path.exists(critical_screenshot)
        ):

            img = Image(
                critical_screenshot,
                width=350,
                height=200
            )

            story.append(img)

        else:

            story.append(
                Paragraph(
                    "<i>"
                    "No critical event screenshot "
                    "recorded in this session."
                    "</i>",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1, 20))

        # ---------------------------------
        # FOOTER
        # ---------------------------------

        story.append(
            Paragraph(
                "<i>"
                "Generated Automatically by "
                "NeuroGuard X v1.0"
                "</i>",
                styles["Normal"]
            )
        )

        # ---------------------------------
        # BUILD PDF
        # ---------------------------------

        doc.build(story)

        return filename