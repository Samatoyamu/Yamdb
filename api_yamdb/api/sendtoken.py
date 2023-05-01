from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def make_token(user):
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()


def registration(user):
    send_mail('Регистрация на сайте',
              message=f'Код подтверждения: '
                      f'{user.confirmation_code}',
              from_email=settings.FROM_MAIL,
              recipient_list=[user.email],
              )
