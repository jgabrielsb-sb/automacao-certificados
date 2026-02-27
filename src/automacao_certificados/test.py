from automacao_certificados.selenium_automations.composition.container import Container

container = Container()

api_requester = container.adapter_factory.create_receita_api_requester()
company = api_requester.get_company(cnpj='12243697000100')
print(company)