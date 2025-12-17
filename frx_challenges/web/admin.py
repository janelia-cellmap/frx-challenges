from allauth.account.decorators import secure_admin_login
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from reversion.admin import VersionAdmin

from .models import Collaborator, ContentFile, Evaluation, Page, Submission, Version


@admin.register(Page)
class PageAdmin(VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContentFile)
class ContentFileAdmin(VersionAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Evaluation)
class EvaluationAdmin(VersionAdmin):
    list_display = ("id", "status", "created_at", "last_updated")

@admin.register(Submission)
class SubmissionAdmin(VersionAdmin):
    list_display = ("id", "user_link", "name")

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"


@admin.register(Version)
class VersionModelAdmin(VersionAdmin):
    list_display = ("id", "user", "submission__name", "filename", "status")


admin.site.register([Collaborator])

admin.site.login = secure_admin_login(admin.site.login)
