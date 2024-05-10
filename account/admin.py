from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User

# Register your models here.
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    # list_filter=('created_at',)
    search_fields=('title',)

admin.site.register(User,UserAdmin)