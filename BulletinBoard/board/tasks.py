from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

from .models import Response, Advert


@shared_task
def response_created_notify(pk):
    instance = Response.objects.get(pk=pk)
    user_to_notify = instance.advert.user
    subject = 'Новый отклик!'
    text_content = (
        f'''Здравствуйте, {user_to_notify.username}!\n
У вашего объявления {instance.advert.title} новый отклик!\n
Посмотреть все отклики на ваши объявления можно по ссылке http://127.0.0.1:8000{reverse('response_list')}'''
    )
    html_content = (
        f'''Здравствуйте, <b>{user_to_notify.username}</b>!<br>
У вашего объявления <b><i>{instance.advert.title}</i></b> новый отклик!<br>
Посмотреть все отклики на ваши объявления можно по \
<a href="http://127.0.0.1:8000{reverse('response_list')}">ссылке</a>'''
    )

    send_mail(
        subject=subject,
        message=text_content,
        html_message=html_content,
        from_email=None,
        recipient_list=[user_to_notify.email]
    )


@shared_task
def response_accepted_notify(pk):
    instance = Response.objects.get(pk=pk)
    user_to_notify = instance.user
    subject = 'Ваш отклик принят!'
    text_content = (
        f'''Здравствуйте, {user_to_notify.username}!\n
Ваш отклик на объявление {instance.advert.title} был принят!
Ссылка на объявление: http://127.0.0.1:8000{instance.advert.get_absolute_url()}'''
    )
    html_content = (
        f'''Здравствуйте, <b>{user_to_notify.username}</b>!<br>
Ваш отклик на <a href="http://127.0.0.1:8000{instance.advert.get_absolute_url()}">объявление</a> был принят!'''
    )

    send_mail(
        subject=subject,
        message=text_content,
        html_message=html_content,
        from_email=None,
        recipient_list=[user_to_notify.email]
    )


@shared_task
def advert_created_notify(pk):
    instance = Advert.objects.get(pk=pk)
    emails_n_usernames = get_user_model().objects.filter(
        subscriptions__contains=[instance.category]
    ).values_list('email', 'username')
    subject = f'Новое объявление в категории {instance.get_category_display()}'

    for email, username in emails_n_usernames:
        text_content = (
            f"""Здравствуйте, {username}!\n
На сайте появилось новое объявление в категории {instance.get_category_display()}.\n\n
{instance.title}\n
Возможно, это объявление Вас заинтересует.\n
Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}"""
        )
        html_content = (
            f"""Здравствуйте, <b>{username}</b>!<br>
На <a href="http://127.0.0.1:8000{reverse('advert_list')}">сайте</a> появилось новое \
<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">объявление</a> в категории \
{instance.get_category_display()}.<br><br>
{instance.title}<br>
Возможно, это объявление Вас заинтересует."""
        )
        send_mail(
            subject=subject,
            message=text_content,
            html_message=html_content,
            from_email=None,
            recipient_list=[email]
        )


@shared_task
def adverts_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(days=7)
    adverts = Advert.objects.filter(created__gt=one_week_ago)
    categories = adverts.order_by('category').distinct('category').values_list('category', flat=True)
    users = get_user_model().objects.filter(subscriptions__overlap=categories)

    subject = 'Объявления за неделю'
    br = '\n'
    for user in users:
        cur_ads = adverts.filter(category__in=user.subscriptions)
        text_content = (
            f"""Здравствуйте, {user.username}!\n
Собрали для Вас объявления за прошедшую неделю!\n\n
{f"{br}{br}".join([f'{ad.title}{br}Категория: {ad.get_category_display()}{br}Ссылка: http://127.0.0.1:8000{ad.get_absolute_url()}' for ad in cur_ads])}\n\n
Если вы хотите отписаться от рассылки или подписаться на другие категории, пожалуйста, \
перейдите по этой ссылке: http://127.0.0.1:8000{reverse('subscriptions')}"""
        )
        html_content = (
            f"""Здравствуйте, <b>{user.username}</b>!<br>
Собрали для Вас объявления за прошедшую неделю!<br><br>
{"<br><br>".join([f'<a href="http://127.0.0.1:8000{ad.get_absolute_url()}">{ad.title}</a><br>Категория: {ad.get_category_display()}' for ad in cur_ads])}<br><br>
Если вы хотите отписаться от рассылки или подписаться на другие категории, пожалуйста, \
перейдите по этой <a href="http://127.0.0.1:8000{reverse('subscriptions')}"><i>ссылке</i></a>"""
        )

        send_mail(
            subject=subject,
            message=text_content,
            html_message=html_content,
            from_email=None,
            recipient_list=[user.email]
        )
