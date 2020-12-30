from django.contrib import admin

from rendaz.production.models import (
    Character,
    Location,
    Project,
    Screenplay,
    Shot,
)


class ProjectAdmin(admin.ModelAdmin):
    fields = ("name", "slug", "title", "artifacts_folder")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Project, ProjectAdmin)
admin.site.register(Character)
admin.site.register(Location)
admin.site.register(Screenplay)
admin.site.register(Shot)
