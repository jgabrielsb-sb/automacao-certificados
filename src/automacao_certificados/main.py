from automacao_certificados.selenium_automations.adapters.http import HttpxClient

if __name__ == "__main__":
    client = HttpxClient()
    
    response = client.get(
        "http://localhost:8000/api/v1/documents//",
    )

    print(response)
    