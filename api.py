import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> tuple:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filter: str = '') -> tuple:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком всех найденных питомцев, совпадающих с фильтром. На данный момент поддерживаются
        следующие значения фильтра: пустое значение - первые 100 питомцев на сайте,
        'my_pets' - только питомцы данного пользователя"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_with_photo(self, auth_key: dict, name: str, animal_type: str, age: str, pet_photo: str) -> tuple:
        """Метод принимает данные для нового питомца (имя, тип, возраст и фото), делает запрос на создание
        нового питомца и возвращает статус запроса и результат с данными созданного питомца в формате JSON"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_info_of_pet(self, auth_key: dict, pet_id: str, name: str, animal_type: str, age: str) -> tuple:
        """Метод принимает id питомца и новые данные (имя, тип, возраст) и возвращает статус ответа и
        информацию с новыми данными питомца в формате JSON"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, pet_id: str) -> int:
        """Метод принимает id питомца, которого нужно удалить и возвращает статус ответа"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        return status

    def create_pet_simple(self, auth_key: dict, name: str, animal_type: str, age: str):
        """Метод принимает имя, тип питомца и возраст, делает запрос к API сервера для
        создания питомца без фотографии и
        возвращает статус ответа и данные о созданном питомце в формате JSON"""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def set_photo_of_pet(self, auth_key: dict, pet_id: str, pet_photo: str):
        """Метод приминает id питомца и путь к фото к питомца. Возвращает статус ответа
        и информацию о питомце в формате JSON"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
