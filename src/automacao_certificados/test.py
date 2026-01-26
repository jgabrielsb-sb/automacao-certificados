from automacao_certificados.selenium_automations.composition.container import Container

container = Container()


municipio_getter_port = container.adapter_factory.create_receita_api_municipio_getter()
cnpj = '17503314000100'
if __name__ == "__main__":
    municipio = municipio_getter_port.run(cnpj=cnpj)
    print(municipio)