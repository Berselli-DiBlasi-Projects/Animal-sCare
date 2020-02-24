import requests

def client():
    # token_h = "Token 6f9ce6a2bc0f738362b8c0a02d15d6e6ceb94a26"
    credentials = {"username": "pippo", "password": "pippo"}
    
    response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data=credentials)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)

    #richiamo la API per gli annunci
    response = requests.get("http://127.0.0.1:8000/api/annunci/", data=credentials)
    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
