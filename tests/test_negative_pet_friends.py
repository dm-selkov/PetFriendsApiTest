import os

from api import PetFriends
from settings import valid_email, valid_password, not_valid_password

pf = PetFriends()


def test_get_api_key_with_invalid_data_forbidden(email=valid_email, password=not_valid_password):
    """Тест проверяет статус ответа при вводе невалидного пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_list_of_pets_with_invalid_key_forbidden(filter=''):
    """Проверка невозможности получить данные питомцев без ввода валидного ключа"""
    auth_key = {'key': '12345'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_create_pet_simple_with_invalid_key_forbidden(name: str = 'Test', animal_type: str = 'Test', age: str = '4'):
    """Проверка невозможности создать питомца без валидного ключа"""
    auth_key = {'key': '12345'}
    status, _ = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 403


def test_create_pet_simple_with_emtpy_fields_impossible(name: str = '', animal_type: str = '', age: str = ''):
    """Проверка невозможности создать питомца с пустыми полями имени, типа и возраста с помощью
    валидного ключа"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_create_pet_simple_with_negative_age_impossible(name: str = 'Test pet', animal_type:
                                                        str = 'just pet', age: str = '-2'):
    """Тест проверяет невозможность создания питомца с отрицательным возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_delete_pet_without_valid_key_forbidden():
    """Проверка невозможности удалить существующего питомца без валидного ключа"""
    # используем валидный ключ для получения существующего id питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']
        # меняем ключ на невалидный и пытаемся удалить питомца
        auth_key = {'key': '1234567890'}
        status = pf.delete_pet(auth_key, pet_id)
        assert status == 403
    else:
        raise Exception('There is no pets in list')


def test_delete_pet_of_another_user_with_valid_key_forbidden():
    """Проверяем невозможность удалить питомца с помощью валидного ключа другого пользователя."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # используем пустой фильтр для получения списка питомцев всех пользователей
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='')
    if len(list_of_pets['pets']) > 0:
        # берем питомца, который не принадлежит владельцу ключа
        pet_id = list_of_pets['pets'][50]['id']
        status = pf.delete_pet(auth_key, pet_id)
        assert status == 403
    else:
        raise Exception('There is no pets in list')


def test_update_info_of_pet_of_another_user_with_valid_key_forbidden(name: str = 'Test name',
                                                                     animal_type: str = 'test type', age: str = 'test'):
    """Проверяем невозможность изменения информации о питомце не принадлежащем данному пользователю"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')
    pet_id = list_of_pets['pets'][50]['id']
    status, result = pf.update_info_of_pet(auth_key, pet_id, name, animal_type, age)
    _, new_list = pf.get_list_of_pets(auth_key, '')
    new_pet = new_list['pets'][50]
    new_name, new_animal_type, new_age = new_pet['name'], new_pet['animal_type'], new_pet['age']
    assert status == 403
    assert new_name != name and new_animal_type != animal_type and new_age != age


def test_set_photo_of_pet_of_another_user_forbidden(pet_photo: str = 'images/fry.jpg'):
    """Проверяем невозможность поменять фотографию питомца принадлежащего другому пользователю
    с помощью валидного ключа"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')
    pet_id = list_of_pets['pets'][20]['id']
    status, result = pf.set_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status != 200


def test_add_new_pet_with_gif_as_photo_impossible(name: str = 'Test pet', animal_type: str = 'test', age: str = '1',
                                                  pet_photo: str = 'images/cat.gif'):
    """Проверка невозможности загрузить gif в качестве фотографии питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
