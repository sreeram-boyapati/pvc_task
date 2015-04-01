from django.contrib import admin
from core.models import FetchTask, PhotoCategory, Photo, Job


class PhotoAdmin(admin.ModelAdmin):
    pass


class PhotoCategoryAdmin(admin.ModelAdmin):
    pass


class JobAdmin(admin.ModelAdmin):
    pass


class FetchTaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoCategory, PhotoCategoryAdmin)
admin.site.register(FetchTask, FetchTaskAdmin)
admin.site.register(Job, JobAdmin)
