from django.contrib import admin

from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "description")
	search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "completed", "due_date")
	list_filter = ("completed", "category")
	search_fields = ("title", "description")