import requests

def client():
    # token_h = "Token af746f7627786d377a57f47f5a705a568b6967f3"
    # credentials = {"username": "admin", "password": "asdasdasd"}

    data = {
        "username": "johnsnow1",
        "email": "john@snow1.com",
        "password1": "cambiami12",
        "password2": "cambiami12",
        "first_name": "rest_first_name",
        "last_name": "rest_last_name"
    }

    response = requests.post("http://127.0.0.1:8000/api/rest-auth/registration/",
                             data=data)

    # headers = {"Authorization": token_h}
    #
    # response = requests.get("http://127.0.0.1:8000/api/profiles/",
    #                         headers=headers)

    # print("Status Code: ", response.status_code)
    # response_data = response.json()
    # print(response_data)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)
    print("token = ", response_data.get("key"))
    token_h = "Token " + response_data.get("key")
    headers = {"Authorization": token_h}

    # richiamo la API per gli annunci
    data = {
        "user": {
            "username": "completa",
            "first_name": "profilo",
        },
        "indirizzo": "via rossi",
        "citta": "fermo",
        "provincia": "FM",
        "regione": "Marche",
        "telefono": "1234567890",
        "foto_profilo": "null",
        "nome_pet": "aaa",
        "pet": "Cane",
        "razza": "meticcio",
        "eta": 1,
        "caratteristiche": "morbidissimo",
        "foto_pet": "null"
    }
    response = requests.put("http://127.0.0.1:8000/api/utenti/registra/utente-normale",
                            headers=headers,
                            data=data)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
