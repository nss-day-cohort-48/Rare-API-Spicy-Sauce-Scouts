from django.db import models
from django.contrib.auth.models import User # pylint:disable=imported-auth-user


class RareUser(models.Model):
    """"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.TextField()

    @property

    def first_name(self):
        """"""
        return self.user.first_name

    @property

    def last_name(self):
        """"""
        return self.user.last_name

    @property

    def email(self):
        """"""
        return self.user.email

    @property

    def username(self):
        """"""
        return self.user.username