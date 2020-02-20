import requests

def client():
    # token_h = "Token af746f7627786d377a57f47f5a705a568b6967f3"
    # credentials = {"username": "admin", "password": "asdasdasd"}

    data = {
        "username": "resttest",
        "email": "test@rest.com",
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

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
