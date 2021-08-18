from django.db import models

class User(models.Model):
    """User Model
    Fields:
        first_name (CharField): Users first name
        last_name (CharField): Users last name
        email (CharField): Users email
        username (Charfield): Username for the user
        password (CharField): Users Password
        is_staff (BooleanField): If the user is a staff member or not
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)

def __str__(self):
    return self.name

