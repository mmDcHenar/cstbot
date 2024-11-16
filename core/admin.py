from typing import Any, Optional

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Course, Link, Phone, Place, Text, TGUser
from utils.types import CourseType, UnitType, PlaceType

admin.site.unregister(User)
admin.site.unregister(Group)


class CustomModelAdmin(ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.list_display:
            first_field = self.list_display[0]
            self.list_display = ('styled_' + first_field,) + self.list_display[1:]
            setattr(self, 'styled_' + first_field, self._style_first_field(first_field))

    def _style_first_field(self, field_name):
        def _styled_field(obj):
            value = getattr(obj, field_name)
            return format_html('<b style="color:  #e67e22;">{}</b>', value)
        _styled_field.short_description = field_name.replace('_', ' ').title()
        return _styled_field


@admin.register(Text)
class TextAdmin(CustomModelAdmin):
    list_display = ("title", "text", "type")
    search_fields = ("title", "text")
    readonly_fields = ("title", "is_button")

    @display(description="Type", ordering="is_button", label={"button": "success", "message": "info"})
    def type(self, obj: Text) -> str:
        return "button" if obj.is_button else "message"

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Text] = None) -> bool:
        return False


@admin.register(TGUser)
class TGUserAdmin(CustomModelAdmin):
    list_display = ("id", "full_name", "username", "status")
    search_fields = ("id", "full_name", "username")
    readonly_fields = ("id", "full_name", "username")

    @display(description="Status", ordering="is_banned", label={"active": "success", "banned": "danger"})
    def status(self, obj: TGUser) -> str:
        return "banned" if obj.is_banned else "active"

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[TGUser] = None) -> bool:
        return False


@admin.register(Course)
class CourseAdmin(CustomModelAdmin):
    list_display = ("fa_title", "ctype", "utype")
    search_fields = ("fa_title", "course_type", "unit_type")

    @display(
        description="Course type",
        ordering="course_type",
        label={
            "general": "info",
            "foundational": "warning",
            "specialized": "danger",
            "optional": "none",
        },
    )
    def ctype(self, obj: Course):
        return CourseType(obj.course_type).label

    @display(
        description="Unit type",
        ordering="unit_type",
        label={
            "theoretical": "info",
            "practical": "warning",
        },
    )
    def utype(self, obj: Course):
        return UnitType(obj.unit_type).label

    class CourseForm(forms.ModelForm):
        class Meta:
            model = Course
            fields = "__all__"

        prerequisite_courses = forms.ModelMultipleChoiceField(
            queryset=Course.objects.all(),
            required=False,
            widget=widgets.FilteredSelectMultiple(
                verbose_name="Prerequisite Courses",
                is_stacked=False,
            ),
        )

    form = CourseForm

    def save_related(self, request: HttpRequest, form: Any, formsets: Any, change: Any) -> None:
        super().save_related(request, form, formsets, change)
        form.instance.prerequisite_courses.clear()
        form.instance.prerequisite_courses.set(form.cleaned_data["prerequisite_courses"])


@admin.register(Place)
class PlaceAdmin(CustomModelAdmin):
    list_display = ("name", "latitude", "longitude", "type")
    search_fields = ("name",)

    @display(
        description="Type",
        ordering="group",
        label={
            "gate": "danger",
            "faculty": "warning",
            "restaurant": "info",
            "office building": "success",
            "dorm": "none",
            "bank": "none",
            "other": "none",
        },
    )
    def type(self, obj: Place):
        return str(PlaceType(obj.group).label).replace("_", " ")


@admin.register(Phone)
class PhoneAdmin(CustomModelAdmin):
    list_display = ("name", "phone_number")


@admin.register(Link)
class LinkAdmin(CustomModelAdmin):
    list_display = ("name", "url_address")

    @admin.display()
    def url_address(self, obj: Link) -> str:
        return format_html(f'<a style="color:  #3498db;" href="{obj.address}">{obj.address}</a>')
