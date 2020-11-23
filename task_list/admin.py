from django.contrib import admin
from .models import Task, User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'complete_date')
    list_editable = ('completed',)
    exclude = ()
    readonly_fields = ('id',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)


