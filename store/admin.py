from django.contrib import admin

from store.models import Tool, Keeper, Operation, Category
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class ToolResource(resources.ModelResource):

    class Meta:
        model = Tool
        fields = ('id', 'name', 'quantity', 'category', 'keeper',
                    'available', 'price', 'slug')


class ToolAdmin(ImportExportActionModelAdmin):
    resource_class = ToolResource
    list_display = [field.name for field in Tool._meta.fields if field.name != "id"]
    # inlines = [ToolImageInline]
admin.site.register(Tool, ToolAdmin)

# @admin.register(Tool)
# class ToolAdmin(admin.ModelAdmin):
#     list_display = ['name', 'quantity', 'category', 'keeper',
#                     'available', 'created', 'updated', 'price', 'slug']
#     list_filter = ['available', 'created', 'updated']
#     list_editable = ['available']
#     prepopulated_fields = {'slug': ('name',)}


@admin.register(Keeper)
class KeeperAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_filter = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_filter = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['giver', 'taker', 'tool',
                    'quantity', 'created']
    list_filter = ['giver', 'created', 'taker']



