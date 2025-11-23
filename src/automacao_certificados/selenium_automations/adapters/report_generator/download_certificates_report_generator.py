from typing import Any, Sequence

import pandas as pd
import plotly.graph_objects as go

from automacao_certificados.selenium_automations.core.models import *

class DownloadCertificatesReportGenerator():

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

    def _build_row_display(
        self,
        rows: Sequence[DownloadCertificatesRow],
    ) -> list[dict[str, Any]]:
        display_rows: list[dict[str, Any]] = []

        for r in rows:
            def status_text(ok: bool, msg: str | None) -> str:
                if ok:
                    return "✅ SUCCESS"
                if msg:
                    # second line with the error
                    return f"❌ FAIL<br><span style='font-size:11px'>{msg}</span>"
                return "❌ FAIL"

            display_rows.append(
                {
                    "cnpj": r.cnpj,
                    "document_type": r.document_type,
                    "error_selection": r.error_selection,
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
        error_selection_hover: list[str] = []
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

        return fig



    def run(
        self,
        certificates: list[DownloadCertificatesUseCaseOutput],
    ) -> DownloadCertificatesTable:
        rows = self._convert_elements_to_rows(certificates)
        table = self._make_plotly_table(rows)
        table.show()
        return table
