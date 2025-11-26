from automacao_certificados.composition.container import Container

container = Container()

use_case = container.get_download_certificates_use_case()

use_case.run()