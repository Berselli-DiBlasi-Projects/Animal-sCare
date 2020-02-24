import requests

def client():
    token_h = "Token bce7ded8c7ac6d9c9e97725741983882b967fb1b"


    headers = {"Authorization": token_h}
    
    response = requests.get("http://127.0.0.1:8000/API/utenti/profilo/",
                            headers=headers)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
