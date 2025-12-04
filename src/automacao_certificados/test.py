import base64

from automacao_certificados.selenium_automations.application.workflow.factories.federal_workflow_factory import FederalWorkflowFactory
from automacao_certificados.selenium_automations.composition.container import Container

container = Container()
api_requester = container.adapter_factory.create_direct_data_api_requester()
httpx_client = container.infrastructure.http_client

if __name__ == "__main__":
    cnpj = '14876384000115'
    #cnpj = '17086031000100'
    # # response = api_requester.get_certificado_base64(cnpj)
    # # print(response)

    # # url = 'https://apiv3.directd.com.br/api/Historico?ConsultaUid=direct-f1ee8774-2448-4957-a46e-a1f74ea2dd02&Extensao=pdf'

    # # response = httpx_client.get(url)
    # # base64_pdf = base64.b64encode(response.content).decode("utf-8")
    # # print(base64_pdf)
    # workflow = FederalWorkflowFactory().get_workflow()
    # output = workflow.run(cnpj)
    # print(output)

    receita_api_getter = container.adapter_factory.create_receita_api_requester()
    company = receita_api_getter.get_company(cnpj)
    print(company)


    