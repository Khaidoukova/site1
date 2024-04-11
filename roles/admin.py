from django.contrib import admin

from roles.models import Competitor, Judge, Conductor

# Register your models here.
admin.site.register(Competitor)
admin.site.register(Judge)
admin.site.register(Conductor)
