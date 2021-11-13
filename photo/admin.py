from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):  # 5.3.5 절에서 추가
    list_display = ['id', 'author', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['created', 'updated', 'author']
    search_fields = ['text', 'created']
    ordering = ['-updated', '-created']


# admin.site.register(Photo)
admin.site.register(Photo, PhotoAdmin)  # 5.3.5 절에서 수정
