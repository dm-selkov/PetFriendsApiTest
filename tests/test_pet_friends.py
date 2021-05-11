import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест проверяет статус ответа и наличие ключа в теле ответа при отправке валидных данных"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter='my_pets'):
    """Тест запрашивает список всех питомцев и проверяет статус ответа и размер списка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_photo(name: str = 'Test pet', animal_type: str = 'test', age: str = '1',
                                pet_photo: str = 'images/meerkat.jpg'):
    """Проверка выполнения запроса на добавление нового питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_info_of_first_existing_pet(name: str = 'Test name', animal_type: str = 'test type', age: str = '5'):
    """Проверка обновления информации о питомце. Обновляет информацию о первом питомце в списке.
    Проверяется статус ответа, а также сверяются отправленные данные и данные полученные при повторном запросе
    информации о первом питомце в списке"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        status, result = pf.update_info_of_pet(auth_key, pet_id, name, animal_type, age)
        _, new_list = pf.get_list_of_pets(auth_key, 'my_pets')
        new_pet = new_list['pets'][0]
        new_name, new_animal_type, new_age = new_pet['name'], new_pet['animal_type'], new_pet['age']
        assert status == 200
        assert new_name == name and new_animal_type == animal_type and new_age == age
    else:
        raise Exception('There is no pets in list')


def test_delete_first_pet_in_list():
    """Проверка удаления питомца из списка. Удаляется первый питомце в списке.
    Если список пуст - генерируется исключение"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        status = pf.delete_pet(auth_key, pet_id)
        _, list_of_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert pet_id not in list_of_pets.values()
    else:
        raise Exception('There is no pets in list')


def test_create_pet_simple_with_valid_data(name: str = 'Test create simple', animal_type: str = 'test type', age: str = '5'):
    """Проверка выполнения запроса на добавление нового питомца без фото с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_set_photo_of_pet_with_valid_photo(pet_photo: str = 'images/fry.jpg'):
    """Проверка обновления фото питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        status, result = pf.set_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['id'] == pet_id
        assert len(result['pet_photo']) > 0
    else:
        raise Exception('There is no pets in list')
