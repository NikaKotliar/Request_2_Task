import requests
from pathlib import Path

with open('token.txt', 'r') as file_object:
    TOKEN = file_object.read().strip()

class Yadisk:
    def __init__(self, token):
        self.token = TOKEN

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'Accept': 'application/json'
        }

    def get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        headers = self.get_headers()
        result = requests.get(upload_url, headers=headers, params=params)
        print(result.json())
        return result.json()

    def upload_file_to_disk(self, disk_file_path, file_path):
        href = self.get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Загрузка успешна")


file_name = 'test_file.txt'
file_path = Path("file_for_download/", file_name)
disk_file_path = str("Test_for_api/" + file_name)

ya = Yadisk(TOKEN)
ya.upload_file_to_disk(disk_file_path, file_path)
