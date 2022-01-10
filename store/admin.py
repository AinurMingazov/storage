from django.contrib import admin

from store.models import Tool, Keeper, Operation


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'keeper', 'slug',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Keeper)
class KeeperAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['giver', 'taker', 'tool',
                    'quantity', 'created']
    list_filter = ['giver', 'created', 'taker']



