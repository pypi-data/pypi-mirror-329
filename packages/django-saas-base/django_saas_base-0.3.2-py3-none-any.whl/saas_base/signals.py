from django.dispatch import Signal

before_create_tenant = Signal()
before_update_tenant = Signal()
before_send_mail = Signal()
after_signup_user = Signal()
after_login_user = Signal()
member_invited = Signal()


__all__ = [
    'before_create_tenant',
    'before_update_tenant',
    'before_send_mail',
    'after_signup_user',
    'after_login_user',
    'member_invited',
]
