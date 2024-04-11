from django.contrib import admin

from users.models import User, Dogs


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')


admin.site.register(Dogs)
