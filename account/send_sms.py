import requests

def send_sms(phone_number,text):
    url = "http://notify.eskiz.uz/api/message/sms/send"

    payload = {'mobile_phone': phone_number,
               'message': text,
               'from': '4546',
               'callback_url': 'http://0000.uz/test.php'}
    files = [

    ]
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vbm90aWZ5LmVza2l6LnV6L2FwaS9hdXRoL2xvZ2luIiwiaWF0IjoxNjQ3MDgyMTE2LCJleHAiOjE2NDk2NzQxMTYsIm5iZiI6MTY0NzA4MjExNiwianRpIjoiaEtVbG5sZG1PVFMybzZpdyIsInN1YiI6IjUiLCJwcnYiOiI4N2UwYWYxZWY5ZmQxNTgxMmZkZWM5NzE1M2ExNGUwYjA0NzU0NmFhIn0.Gg1RtDpo1i38Pr3jD16kS8ZhagJciUw0A_p0VY9bdVk'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)