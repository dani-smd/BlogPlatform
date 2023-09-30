
from django.contrib import admin
# ---
from Blog_app.models import (Posts, PostRate)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "auther_name", "publication_date")

    def auther_name(self, obj):
        return obj.auther.username


admin.site.register(Posts, PostAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ("post_title", "auther_name", "rate", "created")

    def post_title(self, obj):
        return obj.post.title

    def auther_name(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return "Anonymous User"


admin.site.register(PostRate, RateAdmin)


