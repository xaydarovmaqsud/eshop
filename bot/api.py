import requests
import shutil
import os

def get_categories():
    response = requests.get('http://127.0.0.1:8000/api/category/')
    return response.json()['results']

def get_cat_id(name):
    res=dict()
    for c in get_categories():
        res[c['name']] = c['id']
    print(res)
    return res[name]

def get_products(cat,page=1,per_page=6):
    response = requests.get(f'http://127.0.0.1:8000/api/product/?category={cat}&page={page}&per_page={per_page}')
    response_data=response.json()['results']
    for data in response_data:
        img_url = data.get('image')
        if img_url:
            file_format=img_url.split('.')[-1]
            path=f"downloads/images/"
            file_name=f"img.{data['id']}.{file_format}"
            r=requests.get(img_url,stream=True)
            if r.status_code == 200 and not(file_name in os.listdir('downloads/images')):
                with open(path+file_name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
    return response_data

def bot_login(data):
    response = requests.request('POST', 'http://127.0.0.1:8000/api/login/', data=data)
    return response

def get_my_cart():
    response=requests.get(
        f'http://127.0.0.1:8000/api/cart/',
        headers={
            'Authorization':f'Token 94bcb7a49d44b4db505d3e032d2a2bbba3b06e9931ae1bcf0e8ac15b6d263bdd'
        })
    name=[]
    for i in range(len(response.json()['items'])):
        res=response.json()['items'][i]['product']
        name.append(res)
    return name

