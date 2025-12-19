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
    list_display = ("id", "status", "version_link", "submission_name", "created_at", "last_updated")

    def version_link(self, obj):
        url = reverse("admin:web_version_change", args=[obj.version.id])
        return format_html('<a href="{}">Version {} ({})</a>', url, obj.version.id, obj.version.filename)

    def submission_name(self, obj):
        return obj.version.submission.name

    version_link.short_description = "Version"
    submission_name.short_description = "Submission"

@admin.register(Submission)
class SubmissionAdmin(VersionAdmin):
    list_display = ("id", "user_link", "name", "version_count", "created_at")

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    def version_count(self, obj):
        count = obj.versions.count()
        return f"{count} version{'s' if count != 1 else ''}"

    user_link.short_description = "User"
    version_count.short_description = "Versions"


@admin.register(Version)
class VersionModelAdmin(VersionAdmin):
    list_display = ("id", "user", "submission_link", "filename", "status", "created_at")

    def submission_link(self, obj):
        url = reverse("admin:web_submission_change", args=[obj.submission.id])
        return format_html('<a href="{}">#{} - {}</a>', url, obj.submission.id, obj.submission.name)

    submission_link.short_description = "Submission"


admin.site.register([Collaborator])

admin.site.login = secure_admin_login(admin.site.login)
