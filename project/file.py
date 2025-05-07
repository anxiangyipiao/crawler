import os
import ast
import json
import random
import pandas as pd
import requests


spider_id = '680b1c7676684571850e79b1'
url = "http://121.37.171.89:18080/api/schedules"

headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4MGIwZGE1NzY2ODQ1NzE4NTBlNzkzMCIsIm5iZiI6MTc0NTU1OTczNSwidXNlcm5hbWUiOiJ6YXgifQ.qauWkkNQZZPZpvhnHDPOGA13rTCyY6JIMXLW1ROMMwY',
        'Content-Type': 'application/json'
    }


json_data_template = {
    'enabled': True,
    'mode': 'random',
    'name': '',
    'param': '',
    'cron': '1 12 * * *',
    'cmd': 'scrapy crawl',
    'spider_id': spider_id
}


def extract_name_and_site_name(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    class_name = None
    site_name = None
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for class_node in node.body:
                if isinstance(class_node, ast.Assign):
                    for target in class_node.targets:
                        if isinstance(target, ast.Name):
                            if target.id == 'name':
                                class_name = class_node.value.s
                            elif target.id == 'site_name':
                                site_name = class_node.value.s
    
    if class_name is not None or site_name is not None:
        # raise ValueError(f"Could not find 'name' or 'site_name' in {file_path}")
        return class_name, site_name

    else:
        return None, None
    
def extract_from_directory(directory):
    data_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(directory, filename)
            name, site_name = extract_name_and_site_name(file_path)

            if name is None or site_name is None:
                continue

            json_data_copy = json_data_template.copy()
            json_data_copy['name'] = site_name
            json_data_copy['param'] = name
            json_data_copy['cron'] = random_cron()
            data_list.append(json_data_copy)

    return data_list

def upload_data(data_list):

    num = 0
    for form_data in data_list:
        payload=json.dumps(form_data)
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            num+=1
        else:
            print(response.text)
    print("total upload_data is " + str(num))

def to_csv(data_list):
    df = pd.DataFrame(data_list)
    headers = ['enabled', 'mode', 'name', 'param', 'cron', 'cmd', 'spider_id']

    if os.path.exists('./upload_data.csv'):
        os.remove('./upload_data.csv')
    df.to_csv('./upload_data.csv', index=False, columns=headers)

def read_csv():

    data_list = []
    df = pd.read_csv('upload_data.csv')

    for i in range(len(df)):
        row = df.iloc[i].to_dict()
        data_list.append(row)

    return data_list

def random_cron():

    hour1 = 9
    hour2 = 12
    hour3 = 16
    hour4 = 20
    # hour4 = random.randint(22, 23)

    minute = random.randint(0, 45)

    corn = '{minute} {hour1},{hour2},{hour3},{hour4} * * *'
    
    
    return corn.format(minute=minute, hour1=hour1, hour2=hour2, hour3=hour3, hour4=hour4)

def get_all_job(spider_id):


    params = {
        "page": "1",
        "size": "1000",
        "conditions": "[{\"key\":\"spider_id\",\"op\":\"eq\",\"value\":\""+spider_id+"\"}]",
        "sort": "[]"
    }

    res = requests.get(url, params=params, headers=headers)

    id_list = []

    if res.status_code == 200:

        list_data = res.json()['data']

        for data in list_data:

            id_list.append(data['_id'])


    return id_list

def delete_job(job_id_list):

    param = {
        "ids": job_id_list
    }

    res = requests.delete(url, json=param,headers=headers)

    if res.status_code == 200:
        print("delete success")
    else:
        print("delete failed")
        print(res.text)



if __name__ == "__main__":


    path = 'spiders/zhaopin'
    directory_path = os.path.abspath(os.path.dirname(__file__)) + "/" + path


    mode = 2
    if mode == 1:
        data_list = extract_from_directory(directory_path)
        to_csv(data_list)

    if mode == 2:
        data_list = read_csv()
        upload_data(data_list)

    if mode == 3:
        spider_id = '680b1c7676684571850e79b1'
        job_id_list = get_all_job(spider_id)
        delete_job(job_id_list)