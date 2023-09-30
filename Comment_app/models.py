from django.db import models
from User_app.models import User
from Blog_app.models import Posts


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.PROTECT, related_name="comment_post", verbose_name="Post")
    content = models.TextField(verbose_name="Comment Content")
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name="Publication Date&Time")
    auther = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comment_auther",
                               verbose_name="Comment Auther", null=True)
    soft_delete = models.BooleanField(default=False, verbose_name="Soft Delete")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.post.title
