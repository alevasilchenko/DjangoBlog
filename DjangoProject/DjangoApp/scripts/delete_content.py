from ..models import Post

# Удаление объектов Post, соответствующих параметрам поиска, задаваемым в диалоговом режиме.


def input_date_value(string: str):  # функция, следящая за корректностью задаваемого года (целое число)
    while True:
        try:
            year_str = input(f'{string}: ')
            if year_str == '':
                return None
            else:
                result = int(year_str)
        except Exception as exc:
            print(exc)
        else:
            return result


def input_status(string: str):  # функция, следящая за корректностью статуса публикации
    while True:
        result = input(f'{string}: ')
        if (result == '') or (result == 'draft') or (result == 'published'):
            return result
        else:
            print('Некорректный ввод! Надо повторить...')


print('Задайте параметры соответствия для фильтрации записей (для пропуска поля просто нажмите Enter):')
title = input('Заголовок: ')
author = input('Автор: ')
body = input('Содержание (проверка включения текстового фрагмента): ')
created_year = input_date_value('Год создания')
updated_year = input_date_value('Год изменения')
publish_year = input_date_value('Год публикации')
status = input_status('Статус ("draft" или "published")')

posts = Post.objects.all()  # берём список всех объектов и последовательно применяем к нему заданные фильтры
# далее используем print'ы для контроля начального количества объектов и его изменения по мере применения фильтров

post_id = []

posts_len_begin = len(posts)
print('posts_len_begin =', posts_len_begin)

if title:
    posts = posts.filter(title=title)
    print('filter_title:', len(posts))
if author:
    posts = posts.filter(author__username=author)
    print('filter_author:', len(posts))
if body:
    for post in posts:
        if body in post.body:
            post_id.append(post.id)
    posts = posts.filter(id__in=post_id)
    print('filter_body:', len(posts))
if created_year:
    posts = posts.filter(created__year=created_year)
    print('filter_created:', len(posts))
if updated_year:
    posts = posts.filter(updated__year=updated_year)
    print('filter_updated:', len(posts))
if publish_year:
    posts = posts.filter(publish__year=publish_year)
    print('filter_publish:', len(posts))
if status:
    posts = posts.filter(status=status)
    print('filter_status:', len(posts))

print(f'Отфильтрованные посты: {posts}')

posts_len_to_delete = len(posts)

if posts_len_to_delete:
    print('posts_len_to_delete =', posts_len_to_delete)
    action = input('Для удаления введите "delete" (в противном случае программа просто завершит работу): ')
    if action == 'delete':
        posts.delete()
        posts_len_end = posts_len_begin - posts_len_to_delete
        print(f'Удаление выполнено. Количество оставшихся записей: {posts_len_end}')
        assert Post.objects.count() == posts_len_end  # небольшой тест )
