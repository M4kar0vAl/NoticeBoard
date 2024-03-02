from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class AdvertAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'created']
    ordering = ('-created',)
    list_per_page = 20
    list_filter = ['category']
    search_fields = ['title', 'user__username', 'text']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['advert', 'text', 'is_accepted', 'user', 'created']
    ordering = ('-created',)
    list_display_links = ('text',)
    list_per_page = 20
    list_filter = ['is_accepted']
    search_fields = ('advert__title', 'text', 'user__username')
    actions = ['accept', 'reject']

    @admin.action(description="Accept chosen responses")
    def accept(self, request, queryset):
        for response in queryset.filter(is_accepted=False):
            response.accept()

    @admin.action(description="Reject chosen responses")
    def reject(self, request, queryset):
        for response in queryset:
            response.reject()


admin.site.register(User, UserAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Response, ResponseAdmin)
