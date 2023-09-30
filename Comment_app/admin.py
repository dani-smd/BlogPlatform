from django.contrib import admin
# ---
from Comment_app.models import Comments


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post_name", "comment_auther", "publication_date", "soft_delete")

    def post_name(self, obj):
        return obj.post.title

    def comment_auther(self, obj):
        return obj.auther.username


admin.site.register(Comments, CommentAdmin)
