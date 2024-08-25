from django.contrib import admin

from store.models import Category, Keeper, Operation


@admin.register(Keeper)
class KeeperAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    list_filter = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    list_filter = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ["giver", "taker", "tool", "quantity", "created"]
    list_filter = ["giver", "created", "taker"]
