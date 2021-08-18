from django.db import models

class Post(models.Model):
    """Post Model
    Fields:
        title (CharField): title of the post
        category (ForeignKey): id of the category the post is in
        content (CharField): The post caption
        publication_date (Date): Date the post was published
        image_url (CharField): url for the post image
        user (ForeignKey): id of the author of the post
        approved (Boolean): if approved or not by admin
    """

    title = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    image_url = models.CharField(max_length=500)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    approved = models.BooleanField()

def __str__(self):
    return self.name