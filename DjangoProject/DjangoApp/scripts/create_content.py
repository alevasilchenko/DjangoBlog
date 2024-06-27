from django.contrib.auth.models import User
from ..models import Post
from random import randint, choice
from datetime import datetime, timedelta

# Создадим некоторое количество объектов в базе данных, наполнив их рандомным контентом.
# Но сначала добавим несколько пользователей (авторов) (user2, user3, user4 ...) в дополнение к суперпользователю admin.
# При этом, учитывая, что в процессе отладки запускать этот скрипт придётся неоднократно,
# а также имея желание "набить руку" в области QuerySet-запросов, сначала проверяем количество пользователей,
# и, если оно больше одного, то удаляем всех пользователей, кроме суперпользователя admin.

if User.objects.count() > 1:
    User.objects.all().exclude(username='admin').delete()

NUMBER_OF_USERS = 3  # количество добавляемых пользователей (авторов)

for i in range(NUMBER_OF_USERS):
    user = User.objects.create_user(f'user{i+2}')

# Сначала выполним очистку таблицы Posts:

Post.objects.all().delete()

NUMBER_OF_OBJECTS_MIN = 10  # минимальное количество добавляемых объектов
NUMBER_OF_OBJECTS_MAX = 99  # максимальное количество добавляемых объектов
NUMBER_OF_OBJECTS = randint(NUMBER_OF_OBJECTS_MIN, NUMBER_OF_OBJECTS_MAX)  # количество записей в базу данных

NUMBER_OF_WORDS_IN_TITLE_MIN = 1  # минимальное количество "слов" в заголовке статьи
NUMBER_OF_WORDS_IN_TITLE_MAX = 9  # максимальное количество "слов" в заголовке статьи

NUMBER_OF_WORDS_IN_BODY_MIN = 10  # минимальное количество "слов" в содержании статьи
NUMBER_OF_WORDS_IN_BODY_MAX = 99  # максимальное количество "слов" в содержании статьи

NUMBER_OF_LETTERS_MIN = 1  # минимальное количество букв в генерируемых "словах"
NUMBER_OF_LETTERS_MAX = 9  # максимальное количество букв в генерируемых "словах"

DATE_MIN = '2020-01-01 00:00:00'  # самое раннее допустимое значение "дата-время", используемое в полях DataTimeField

STATUS_LIST = ('draft', 'published')  # возможные варианты статуса публикации


def create_word(cap=False):  # функция, создающая рандомным способом "слово" и возвращающая его
    # в качестве аргумента передаётся признак необходимости сделать первую букву слова заглавной

    number_of_letters = randint(NUMBER_OF_LETTERS_MIN, NUMBER_OF_LETTERS_MAX)  # количество символов в "слове"

    result = ''
    for _ in range(number_of_letters):
        result += chr(randint(ord('a'), ord('z')))  # добавляем очередной символ слова из диапазона 'a'-'z'
    if cap:
        result = result.capitalize()

    return result


def create_some_words(number=1, only_first=True):  # функция, создающая последовательность из "слов" и возвращающая её
    # в качестве аргументов передаётся требуемое количество слов в последовательности
    # и признак заглавной буквы только для первого слова (по умолчанию) или для всех слов

    result = create_word(cap=True)  # первое слово последовательности всегда с заглавной буквы
    for _ in range(1, number):
        result += ' '  # добавляем пробел между словами
        if only_first:
            result += create_word(cap=False)
        else:
            result += create_word(cap=True)

    return result


def create_title():  # функция, создающая рандомным способом заголовок поста и возвращающая его

    number_of_words = randint(NUMBER_OF_WORDS_IN_TITLE_MIN, NUMBER_OF_WORDS_IN_TITLE_MAX)  # количество слов в заголовке
    result = create_some_words(number_of_words, only_first=False)  # все слова заголовка - с заглавной буквы

    return result


def create_body():  # функция, создающая рандомным способом текст поста и возвращающая его

    number_of_words = randint(NUMBER_OF_WORDS_IN_BODY_MIN, NUMBER_OF_WORDS_IN_BODY_MAX)  # количество слов в содержании
    result = create_some_words(number_of_words, only_first=True)

    return result


def create_date(date_min=DATE_MIN):  # функция, создающая рандомным способом корректное значение "дата-время"
    # в качестве аргумента передаётся самая ранняя допустимая дата

    datetime_min = datetime.strptime(date_min, '%Y-%m-%d %H:%M:%S')
    duration_seconds = (datetime.now() - datetime_min).total_seconds()
    interval_seconds = randint(1, int(duration_seconds))  # случайный интервал от самой ранней даты в секундах
    result = datetime_min + timedelta(seconds=interval_seconds)

    return result


def create_status():  # функция, выбирающая рандомным способом статус публикации и возвращающая его

    result = choice(STATUS_LIST)

    return result


list_of_objects = []  # список объектов для записи в базу данных

for _ in range(NUMBER_OF_OBJECTS):  # наполняем список объектов для последующего их сохранения в базе данных

    object_title = create_title()  # формируем заголовок поста
    object_slug = object_title.replace(' ', '-')  # значение slug копирует заголовок с заменой пробелов дефисами
    object_author_number = randint(1, NUMBER_OF_USERS+1)  # выбираем рандомным способом порядковый номер автора
    if object_author_number == 1:
        object_author_name = 'admin'
    else:
        object_author_name = f'user{object_author_number}'  # получаем соответствующее имя автора
    object_author = User.objects.get(username=object_author_name)  # по имени автора получаем соответствующий объект
    object_body = create_body()  # формируем содержание статьи
    object_created = create_date()  # формируем дату создания статьи
    object_updated = create_date(str(object_created))  # формируем дату редактирования статьи
    object_publish = create_date(str(object_updated))  # формируем дату публикации статьи
    object_status = create_status()  # формируем статус публикации

    list_of_objects.append(Post(title=object_title,
                                slug=object_slug,
                                author=object_author,
                                body=object_body,
                                created=object_created.astimezone(),
                                updated=object_updated.astimezone(),
                                publish=object_publish.astimezone(),
                                status=object_status))

Post.objects.bulk_create(list_of_objects)  # добавляем список объектов в базу данных

print('NUMBER_OF_OBJECTS =', NUMBER_OF_OBJECTS)  # для контроля

assert Post.objects.count() == NUMBER_OF_OBJECTS  # небольшой тест )
