from typing import Any, Sequence
import html
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
        of the report generator port that uses HTML/CSS to generate a report 
        of the certificates.
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

    def _format_document_type_with_municipio(
        self,
        document_type: str,
        municipio: str | None
    ) -> str:
        """
        Formats the document type with municipality information for municipal certificates.

        :param document_type: The document type.
        :type document_type: str
        :param municipio: The municipality name if it's a municipal certificate.
        :type municipio: str | None
        :return: The formatted document type.
        :rtype: str
        """
        if municipio:
            return f"{document_type} - {municipio}"
        return document_type

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
        # Format document type with municipality if available
        document_type_str = str(download_certificate_result.certificate.document_type.value)
        formatted_document_type = self._format_document_type_with_municipio(
            document_type_str,
            download_certificate_result.municipio
        )
        
        return DownloadCertificatesRow(
            cnpj=download_certificate_result.certificate.cnpj,
            document_type=formatted_document_type,
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
        :return: The formatted error message as HTML.
        :rtype: str
        """
        if not msg:
            return ""

        # Escape HTML entities to prevent breaking HTML structure
        escaped_msg = html.escape(msg)

        # Break message into multiple lines
        wrapped = textwrap.wrap(escaped_msg, width=self.error_line_width)

        # Limit number of lines
        if len(wrapped) > self.max_error_lines:
            wrapped = wrapped[:self.max_error_lines]
            wrapped[-1] += "..."

        # Convert to HTML with <br> tags for line breaks
        return "<br>".join(wrapped)

    def _format_status_cell(self, ok: bool, msg: str | None) -> str:
        """
        Formatting the status cell with success/failure indicator and error message.

        :param ok: Whether the step was successful.
        :type ok: bool
        :param msg: The error message if any.
        :type msg: str | None
        :return: HTML formatted status cell.
        :rtype: str
        """
        if ok:
            return '<span class="status-success">✅ SUCCESS</span>'
        
        formatted_error = self._format_error_for_cell(msg)
        if formatted_error:
            return f'<span class="status-fail">❌ FAIL</span><div class="error-details">{formatted_error}</div>'
        return '<span class="status-fail">❌ FAIL</span>'

    def _generate_html_table(
        self,
        date: datetime,
        rows: list[DownloadCertificatesRow]
    ) -> str:
        """
        Generating an HTML table from the rows.

        :param date: The date for the report.
        :type date: datetime
        :param rows: The rows to display.
        :type rows: list[DownloadCertificatesRow]
        :return: HTML table string.
        :rtype: str
        """
        table_html = ['<table class="certificates-table">']
        
        # Header
        table_html.append('<thead>')
        table_html.append('<tr>')
        table_html.append('<th>CNPJ</th>')
        table_html.append('<th>Tipo de Documento</th>')
        table_html.append('<th>Erro de Seleção</th>')
        table_html.append('<th>Download</th>')
        table_html.append('<th>Persistência</th>')
        table_html.append('<th>PPE</th>')
        table_html.append('</tr>')
        table_html.append('</thead>')
        
        # Body
        table_html.append('<tbody>')
        for r in rows:
            table_html.append('<tr>')
            
            # CNPJ
            table_html.append(f'<td class="cell-cnpj">{html.escape(r.cnpj)}</td>')
            
            # Document Type
            table_html.append(f'<td class="cell-doc-type">{html.escape(str(r.document_type))}</td>')
            
            # Error Selection
            error_selection_html = self._format_error_for_cell(r.error_selection)
            table_html.append(f'<td class="cell-error-selection">{error_selection_html if error_selection_html else "—"}</td>')
            
            # Download
            table_html.append(f'<td class="cell-download">{self._format_status_cell(r.download_step_is_sucess, r.download_step_error_message)}</td>')
            
            # Persistance
            table_html.append(f'<td class="cell-persistance">{self._format_status_cell(r.persistance_step_is_sucess, r.persistance_step_error_message)}</td>')
            
            # PPE
            table_html.append(f'<td class="cell-ppe">{self._format_status_cell(r.ppe_step_is_sucess, r.ppe_step_error_message)}</td>')
            
            table_html.append('</tr>')
        table_html.append('</tbody>')
        table_html.append('</table>')
        
        return '\n'.join(table_html)

    def generate_report(
        self,
        input: DownloadCertificatesUseCaseOutput,
    ) -> str:
        """
        Running the report generator by converting the input to rows and generating an HTML report.

        :param input: The input.
        :type input: DownloadCertificatesUseCaseOutput
        :return: The HTML content of the report.
        :rtype: str
        """
        rows = self._convert_elements_to_rows(input.output)
        date = datetime.now()
        table_html = self._generate_html_table(date, rows)
        
        # Generate complete HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Certificados - {date.strftime('%d/%m/%Y')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, Helvetica, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #333;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .report-container {{
            max-width: 100%;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 24px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .certificates-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            table-layout: fixed;
        }}
        
        .certificates-table thead {{
            background-color: #3498db;
            color: white;
        }}
        
        .certificates-table th {{
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #2980b9;
            word-wrap: break-word;
        }}
        
        .certificates-table td {{
            padding: 10px;
            border: 1px solid #ddd;
            vertical-align: top;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: normal;
        }}
        
        .certificates-table tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .certificates-table tbody tr:hover {{
            background-color: #f0f0f0;
        }}
        
        .cell-cnpj {{
            width: 12%;
        }}
        
        .cell-doc-type {{
            width: 18%;
        }}
        
        .cell-error-selection {{
            width: 20%;
        }}
        
        .cell-download,
        .cell-persistance,
        .cell-ppe {{
            width: 16.67%;
        }}
        
        .status-success {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .status-fail {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .error-details {{
            margin-top: 5px;
            font-size: 11px;
            color: #7f8c8d;
            line-height: 1.4;
        }}
        
        .error-details br {{
            display: block;
            margin: 2px 0;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <h1>Relatório de Certidões - {date.strftime('%d/%m/%Y')}</h1>
        {table_html}
    </div>
</body>
</html>"""
        
        return html_content

