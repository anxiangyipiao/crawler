import os
import ast
import json
import random
import pandas as pd
import requests


json_data_template = {
    'enabled': True,
    'mode': 'random',
    'name': '',
    'param': '',
    'cron': '1 12 * * *',
    'cmd': 'scrapy crawl',
    'spider_id': '676e4fe0d08b88e0bb9c1ced'
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
    return class_name, site_name


def extract_from_directory(directory):
    data_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(directory, filename)
            name, site_name = extract_name_and_site_name(file_path)
            json_data_copy = json_data_template.copy()
            json_data_copy['name'] = site_name
            json_data_copy['param'] = name
            json_data_copy['cron'] = random_cron()
            data_list.append(json_data_copy)

    return data_list


def upload_data(data_list):

    num = 0
    url = "http://47.100.34.178:8080//api/schedules"
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MTg3NWZjZTU0NDMxYzgyNjdjZDAzOSIsIm5iZiI6MTcyOTczMTA2MywidXNlcm5hbWUiOiJhZG1pbiJ9.J0wtk_QO_U28_tGlcQqOwdt1JWL3LQ11R_niUXGfxNo',
        'Content-Type': 'application/json'
    }
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

    cron = '{minute} 13 * * *'
    minute = random.randint(0, 59)
    
    return cron.format(minute=minute)



if __name__ == "__main__":


    path = '0225'
    directory_path = os.path.abspath(os.path.dirname(__file__)) + "/" + path


    mode = 2
    if mode == 1:
        data_list = extract_from_directory(directory_path)
        to_csv(data_list)

    if mode == 2:
        data_list = read_csv()
        upload_data(data_list)

