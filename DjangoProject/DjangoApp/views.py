from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


def post_list(request):
    objects_list = Post.published.all()
    paginator = Paginator(objects_list, 3)  # 3 статьи на странице
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # если страница не является целым числом, возвращаем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # если номер страницы больше, чем общее количество страниц, возвращаем последнюю страницу
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'post\\list.html', {'page_num': page_num, 'page_obj': page_obj})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    # список активных комментариев для этой статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # создаём комментарий, но пока не сохраняем в базе данных
            new_comment = comment_form.save(commit=False)
            #  привязываем комментарий к текущей статье
            new_comment.post = post
            # сохраняем комментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'post\\detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def post_share(request, post_id):
    # получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # форма была отправлена на сохранение
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # все поля формы прошли валидацию
            cd = form.cleaned_data
            # отправка элнетронной почты
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post\\share.html', {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'post\\list.html'
