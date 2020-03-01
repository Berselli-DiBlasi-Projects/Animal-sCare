import requests

def client():

    credentials = {"username": "werther", "password": "pass123"}
    
    response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data=credentials)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)
    print("token = ", response_data.get("key"))
    token_h = "Token " + response_data.get("key")
    headers = {"Authorization": token_h}

    #richiamo la API per gli annunci
    response = requests.get("http://127.0.0.1:8000/api/annunci/calendario/", headers=headers)
    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
