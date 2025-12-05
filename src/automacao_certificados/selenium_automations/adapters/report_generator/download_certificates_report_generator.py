from typing import Any, Sequence

import pandas as pd
import plotly.graph_objects as go
import textwrap
from datetime import datetime

from automacao_certificados.selenium_automations.core.models import *

class DownloadCertificatesReportGenerator:
    
    def __init__(
        self,
        MAX_ERROR_LINES: int = 20,
        ERROR_LINE_WIDTH: int = 40,
    ):
        """
        The download certificates report generator is an implementation 
        of the report generator port that uses the pandas and plotly libraries 
        to generate a report of the certificates.
        """
        if not isinstance(MAX_ERROR_LINES, int):
            raise ValueError("MAX_ERROR_LINES must be an integer")
        
        self.max_error_lines = MAX_ERROR_LINES
        self.error_line_width = ERROR_LINE_WIDTH

    def _is_step_sucess(self, step_result: StepResult):
        """
        Checking safely if the step is  succesfull by returning False if the step result is None.

        :param step_result: The step result.
        :type step_result: StepResult
        :return: True if the step is successful, False otherwise.
        :rtype: bool
        """
        return step_result.sucess if step_result is not None else False

    def _get_error_message(self, step_result: StepResult):
        """
        Getting the error message from the step result by returning None if the step result is None.

        :param step_result: The step result.
        :type step_result: StepResult
        :return: The error message.
        :rtype: str | None
        """
        return step_result.error_message if step_result is not None else None

    def _convert_element_to_row(
        self,
        download_certificate_result: DownloadCertificateResult
    ) -> DownloadCertificatesRow:
        """
        Converting the certificate use case output to a row of the report.

        :param download_certificate_result: The download certificate result.
        :type certificate: DownloadCertificateResult
        :return: The row.
        :rtype: DownloadCertificatesRow
        """
        return DownloadCertificatesRow(
            cnpj=download_certificate_result.certificate.cnpj,
            document_type=download_certificate_result.certificate.document_type,
            error_selection=download_certificate_result.error_selection,
            download_step_is_sucess=self._is_step_sucess(download_certificate_result.workflow_output.download_output_result),
            download_step_error_message=self._get_error_message(download_certificate_result.workflow_output.download_output_result),
            persistance_step_is_sucess=self._is_step_sucess(download_certificate_result.workflow_output.persistance_output_result),
            persistance_step_error_message=self._get_error_message(download_certificate_result.workflow_output.persistance_output_result),
            ppe_step_is_sucess=self._is_step_sucess(download_certificate_result.workflow_output.ppe_output_result),
            ppe_step_error_message=self._get_error_message(download_certificate_result.workflow_output.ppe_output_result),
        )

    def _convert_elements_to_rows(
        self, 
        elements: list[DownloadCertificatesUseCaseOutput]
    ) -> list[DownloadCertificatesRow]:
        """
        Converting the certificate use case outputs to rows of the report.

        :param elements: The certificate use case outputs.
        :type elements: list[DownloadCertificatesUseCaseOutput]
        :return: The rows of the report.
        :rtype: list[DownloadCertificatesRow]
        """
        return [self._convert_element_to_row(element) for element in elements]

    def _format_error_for_cell(self, msg: str | None) -> str:
        """
        Formatting the error message for the cell

        :param msg: The error message.
        :type msg: str | None
        :return: The formatted error message.
        :rtype: str
        """
        if not msg:
            return ""

        # Break message into multiple lines
        wrapped = textwrap.wrap(msg, width=self.error_line_width)

        # Limit number of lines
        if len(wrapped) > self.max_error_lines:
            wrapped = wrapped[:self.max_error_lines]
            wrapped[-1] += "..."

        # Convert to HTML with <br> so Plotly breaks lines
        return "<br>".join(wrapped)

    def _build_row_display(
        self,
        rows: Sequence[DownloadCertificatesRow],
    ) -> list[dict[str, Any]]:
        """
        Building the row display.

        :param rows: The rows.
        :type rows: Sequence[DownloadCertificatesRow]
        :return: The row display.
        :rtype: list[dict[str, Any]]
        """
        display_rows: list[dict[str, Any]] = []

        for r in rows:
            def status_text(ok: bool, msg: str | None) -> str:
                if ok:
                    return "✅ SUCCESS"
                formatted_error = self._format_error_for_cell(msg)
                if formatted_error:
                    return f"❌ FAIL<br><span style='font-size:11px'>{formatted_error}</span>"
                return "❌ FAIL"

            display_rows.append(
                {
                    "cnpj": r.cnpj,
                    "document_type": r.document_type,
                    "error_selection": self._format_error_for_cell(r.error_selection),
                    "download": status_text(r.download_step_is_sucess, r.download_step_error_message),
                    "persistance": status_text(r.persistance_step_is_sucess, r.persistance_step_error_message),
                    "ppe": status_text(r.ppe_step_is_sucess, r.ppe_step_error_message),
                }
            )

        return display_rows



    def _build_hover_text(
        self,
        rows: Sequence[DownloadCertificatesRow],
    ) -> list[list[str]]:
        """
        Returns a list-of-lists with hovertext for each column in the same
        order as the table columns: [cnpj, document_type, download, persistance, ppe]

        :param rows: The rows.
        :type rows: Sequence[DownloadCertificatesRow]
        :return: The hover text.
        :rtype: list[list[str]]
        """
        cnpj_hover: list[str] = []
        doc_type_hover: list[str] = []
        download_hover: list[str] = []
        persistance_hover: list[str] = []
        ppe_hover: list[str] = []

        for r in rows:
            # For these columns, hover = same as cell text
            cnpj_hover.append(r.cnpj)
            doc_type_hover.append(r.document_type)

            # For step columns:
            def step_hover(ok: bool, msg: str | None) -> str:
                if ok:
                    return "SUCCESS"
                # Tooltip will show the error message if exists, otherwise just 'FAIL'
                return msg or "FAIL"

            download_hover.append(
                step_hover(r.download_step_is_sucess, r.download_step_error_message)
            )
            persistance_hover.append(
                step_hover(r.persistance_step_is_sucess, r.persistance_step_error_message)
            )
            ppe_hover.append(
                step_hover(r.ppe_step_is_sucess, r.ppe_step_error_message)
            )

        return [cnpj_hover, doc_type_hover, download_hover, persistance_hover, ppe_hover]

    def _make_plotly_table(
        self,
        date: datetime,
        rows: list[DownloadCertificatesRow]
    ) -> go.Figure:
        """
        Getting the plotly figure of the table.

        :param date: The date.
        :type date: datetime
        :param rows: The rows.
        :type rows: list[DownloadCertificatesRow]
        :return: The plotly figure.
        :rtype: go.Figure
        """
        display_rows = self._build_row_display(rows)
        df = pd.DataFrame(display_rows)

        # Define column widths to prevent overlapping
        # Adjust widths based on content type
        column_widths = {
            "cnpj": 120,
            "document_type": 200,
            "error_selection": 250,
            "download": 300,
            "persistance": 300,
            "ppe": 300
        }
        
        # Get widths in the same order as columns
        widths = [column_widths.get(col, 200) for col in df.columns]

        fig = go.Figure(
            data=[
                go.Table(
                    columnwidth=widths,
                    header=dict(
                        values=list(df.columns),
                        align="left",
                        fill_color="paleturquoise",
                        font=dict(size=12, color="black"),
                        height=40
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        align="left",
                        fill_color="white",
                        font=dict(size=11, color="black"),
                        # Remove fixed height to allow cells to expand based on content
                        line=dict(width=1, color="gray")
                    ),
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text=f"Relatório de Certificados - {date.strftime('%d/%m/%Y')}",
                font=dict(size=16)
            ),
            autosize=True,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        return fig

    def generate_report(
        self,
        input: DownloadCertificatesUseCaseOutput,
    ) -> str:
        """
        Running the report generator by converting the input to rows, making the plotly table and saving the file.

        :param input: The input.
        :type input: DownloadCertificatesUseCaseOutput
        :return: The HTML content of the report.
        :rtype: str
        """
        rows = self._convert_elements_to_rows(input.output)
        date = datetime.now()
        table = self._make_plotly_table(date, rows)
        html_content = table.to_html(full_html=True, include_plotlyjs="cdn")
        
        # Add CSS to ensure proper text wrapping and prevent overlapping
        css_style = """
        <style>
            .js-plotly-plot .plotly .modebar {
                display: none;
            }
            .js-plotly-plot .plotly table {
                table-layout: auto;
                width: 100%;
            }
            .js-plotly-plot .plotly table td {
                white-space: normal !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                max-width: 0;
                padding: 8px !important;
                vertical-align: top !important;
            }
            .js-plotly-plot .plotly table th {
                white-space: normal !important;
                word-wrap: break-word !important;
                padding: 8px !important;
            }
        </style>
        """
        
        # Insert CSS before closing head tag or after opening body tag
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", css_style + "</head>")
        elif "<body>" in html_content:
            html_content = html_content.replace("<body>", "<body>" + css_style)
        else:
            # If no head/body tags, prepend to html content
            html_content = css_style + html_content
        
        return html_content

