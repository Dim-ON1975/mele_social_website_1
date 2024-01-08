from django.db import models
from django.conf import settings


class Profile(models.Model):
    # Извлекаем модель пользователя и настроечный параметр AUTH_USER_MODEL, чтобы ссылаться на
    # него при определении связи модели с моделью пользователя (один-к-одному), не ссылаясь на
    # модель пользователя auth напрямую, т.е. осуществляется ассоцирование профилей с пользователями.
    # С по мощью параметра on_delete=models.CASCADE мы принудительно удаляем связанный объект Profile
    # при удалении объекта User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Дата рождения пользователя.
    date_of_birth = models.DateField(blank=True, null=True)
    # Фотография пользователя.
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
