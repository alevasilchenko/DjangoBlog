from ..models import Post
from random import randint

# Внесём изменения в некоторые объекты базы данных, заменив рандомный контент заголовка или содержания фиксированным
# (для наглядности внесённых изменений). Пусть новый текст заголовка будет 'NEW TITLE', а содержания - 'NEW BODY'.
# Количество изменяемых объектов определим как половину от имеющихся (с округлением в сторону увеличения при нечётном
# количестве последних). Сами же объекты выберем рандомным способом, а заголовок и содержание в них будем изменять
# по очереди.

number_objects_in_table = Post.objects.count()  # количество записей в таблице Posts
number_objects_to_modify = number_objects_in_table // 2 + number_objects_in_table % 2  # количество изменяемых записей

objects_list = Post.objects.all()  # список всех объектов таблицы Posts

objects_to_modify = set()  # множество индексов объектов (в списке всех объектов), подлежащих изменению

while len(objects_to_modify) < number_objects_to_modify:
    object_number = randint(0, number_objects_to_modify - 1)  # рандомный выбор индекса изменяемого объекта в списке
    objects_to_modify.add(object_number)

title_or_body = True
for object_index in objects_to_modify:
    post = objects_list[object_index]
    if title_or_body:
        post.title = 'NEW TITLE'
    else:
        post.body = 'NEW BODY'
    post.save()
    title_or_body = not title_or_body

# определяем количество объектов, в которых должен был быть заменён заголовок:
number_objects_to_modify_title = number_objects_to_modify // 2 + number_objects_to_modify % 2
print('number_objects_to_modify_title =', number_objects_to_modify_title)  # для контроля

# и количество объектов, в которых должно было быть заменено содержание:
number_objects_to_modify_body = number_objects_to_modify - number_objects_to_modify_title
print('number_objects_to_modify_body =', number_objects_to_modify_body)  # для контроля

assert Post.objects.filter(title='NEW TITLE').count() == number_objects_to_modify_title  # небольшой тест )
assert Post.objects.filter(body='NEW BODY').count() == number_objects_to_modify_body  # и ещё один ))
