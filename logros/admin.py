from django.contrib import admin

from logros.models import Achievements

# Register your models here.

class AchievementsAdmin(admin.ModelAdmin):
    readonly_fields=('id', )

admin.site.register(Achievements, AchievementsAdmin)
