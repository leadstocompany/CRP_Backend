from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html


class BaseSaveMixin(admin.ModelAdmin):
    """
    Mixin to handle save logic for created_by and modified_by fields in Admin classes.
    """
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date', 'username')
    list_per_page = 10  # Default number of items per page

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    def header(self):
        return format_html(
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">'
            '<h2 style="margin: 0;">Bank Types</h2>'
            '<a href="add/" style="padding: 8px 16px; background-color: #2C3E50; color: white; border-radius: 8px; text-decoration: none;">+ Create Bank Type</a>'
            '</div>'
        )
    header.short_description = " "

    def edit_button(self, obj):
        return format_html(
            '<a href="{}" style="text-decoration: none; color: green; font-weight: bold;">✏️ Edit</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/"
        )
    edit_button.short_description = "Edit"

    def delete_button(self, obj):
        return format_html(
            '<a href="{}" style="text-decoration: none; color: red; font-weight: bold;" onclick="return confirm(\'Are you sure you want to delete this item?\')">🗑️ Delete</a>',
            f"/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/delete/"
        )
    delete_button.short_description = "Delete"

    # def get_actions(self, request):
    #     return {}

    def go_back_to_paginated(self, request, queryset):
        return HttpResponseRedirect(request.path)
    go_back_to_paginated.short_description = "Back to Paginated View"
    actions = ['go_back_to_paginated']
class BaseInlineSaveMixin:
    """
    Mixin to handle save logic for created_by and modified_by fields in Inline classes.
    """
    readonly_fields = ('created_by', 'created_date', 'modified_by', 'modified_date', 'username')

    def save_formset(self, request, form, formset, change):
        """
        Save formset method to set created_by and modified_by fields for inline models.
        """
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk:  # On creation
                obj.created_by = request.user
            obj.modified_by = request.user  # On every update
            obj.save()
        formset.save_m2m()
