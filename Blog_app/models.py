from django.db import models
from User_app.models import User


class Posts(models.Model):
    title = models.CharField(max_length=500, verbose_name="Post Title")
    content = models.TextField(verbose_name="Post Content")
    auther = models.ForeignKey(User, on_delete=models.PROTECT, related_name="post_auther", verbose_name="Auther")
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name="Publication Date&Time")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ('-publication_date',)

    def __str__(self):
        return str(self.title)


class PostRate(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.PROTECT, related_name="post_rate", verbose_name="Post")
    rate = models.IntegerField(verbose_name="Rate")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_Rater", verbose_name="Rater", null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date&Time")

    class Meta:
        verbose_name = "PostRate"
        verbose_name_plural = "PostRates"

    def __str__(self):
        return self.post.title
