from typing import Any, Sequence

import pandas as pd
import plotly.graph_objects as go
import textwrap
from pathlib import Path
from datetime import datetime

from automacao_certificados.selenium_automations.core.models import *

class DownloadCertificatesReportGenerator():
    
    def __init__(
        self,
        save_path: Path = Path("data/certificates_report"),
        MAX_ERROR_LINES: int = 20,
        ERROR_LINE_WIDTH: int = 40,
    ):
        self.save_path = save_path
        self.max_error_lines = MAX_ERROR_LINES
        self.error_line_width = ERROR_LINE_WIDTH

    def _is_step_sucess(self, step_result: StepResult):
        return step_result.sucess if step_result is not None else False

    def _get_error_message(self, step_result: StepResult):
        return step_result.error_message if step_result is not None else None

    def _convert_element_to_row(
        self,
        certificate: DownloadCertificatesUseCaseOutput
    ) -> DownloadCertificatesRow:
        return DownloadCertificatesRow(
            cnpj=certificate.certificate.cnpj,
            document_type=certificate.certificate.document_type,
            error_selection=certificate.error_selection,
            download_step_is_sucess=self._is_step_sucess(certificate.workflow_output.download_output_result),
            download_step_error_message=self._get_error_message(certificate.workflow_output.download_output_result),
            persistance_step_is_sucess=self._is_step_sucess(certificate.workflow_output.persistance_output_result),
            persistance_step_error_message=self._get_error_message(certificate.workflow_output.persistance_output_result),
            ppe_step_is_sucess=self._is_step_sucess(certificate.workflow_output.ppe_output_result),
            ppe_step_error_message=self._get_error_message(certificate.workflow_output.ppe_output_result),
        )

    def _convert_elements_to_rows(
        self, 
        elements: list[DownloadCertificatesUseCaseOutput]
    ) -> list[DownloadCertificatesRow]:
        return [self._convert_element_to_row(element) for element in elements]

    def _format_error_for_cell(self, msg: str | None) -> str:
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
        display_rows = self._build_row_display(rows)
        df = pd.DataFrame(display_rows)

        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=list(df.columns), align="left"),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        align="left",
                        # no hoverinfo/hovertext here – Table cells don't support it
                    ),
                )
            ]
        )

        fig.update_layout(
            title=f"Relatório de Certificados - {date.strftime('%d/%m/%Y')}"
        )
        return fig

    def run(
        self,
        certificates: list[DownloadCertificatesUseCaseOutput],
        date: datetime
    ) -> Path:
        rows = self._convert_elements_to_rows(certificates)
        table = self._make_plotly_table(date, rows)
        file_path = self.save_path / f"certificates_report_{date.strftime('%d-%m-%Y-%H-%M-%S')}.html"
        table.write_html(file_path)
        return file_path
