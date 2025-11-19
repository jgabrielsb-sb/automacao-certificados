from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core import *

class WorkflowPort:
    def __init__(
        self,
        document_downloader: DocumentDownloaderPort,
        document_persistance: DocumentPersistancePort,
    ):
        if not isinstance(document_downloader, DocumentDownloaderPort):
            raise ValueError('document_downloader must be a DocumentDownloaderPort')

        if not isinstance(document_persistance, DocumentDownloaderPort):
            raise ValueError('document_persistance must be a DocumentPersistencePort')

        self.document_downloader = document_downloader
        self.document_persistance = document_persistance

    def perform_download(self, cnpj):
        document_extracted, base64_pdf = self.document_downloader.run(cnpj)
        return document_extracted, base64_pdf

    def persist_data(self, document_persistance_input: DocumentPersistanceInput):
        self.document_persistance.run(document_persistance_input)

    def send_to_ppe(self, document_ppe_input: DocumentPPEInput):
        # to implement
        pass

    def run(self, cnpj):
        try:
            document_extracted, base64_pdf = self.perform_download(cnpj)
            self.persist_data(DocumentPersistanceInput(document_extracted, base64_pdf))
            self.send_to_ppe(DocumentPPEInput(document_extracted, base64_pdf))
        except DocumentDownloaderException as e:
            raise WorkflowException(f"Running workflow failed caused by an error on download file. Original ex: {e}")
        except DocumentPersistanceException as e:
            raise WorkflowException(f"Running workflow failed caused by an error on persist data. Original ex: {e}")
        except Exception as e:
            raise WorkflowException(f"Running workflow failed caused by an unexpected error. Original ex: {e}")


        