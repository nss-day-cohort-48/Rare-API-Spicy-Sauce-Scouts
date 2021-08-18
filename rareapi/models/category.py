from django.db import models

class Category(models.Model):
    """Category Model
    Fields:
        label (CharField): name of the category 
    """

    label = models.CharField(max_length=50)

def __str__(self):
    return self.name
