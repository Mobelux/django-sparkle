from django.contrib import admin
from sparkle.models import Application, Version, SystemProfileReport, SystemProfileReportRecord

admin.site.register(Application)
admin.site.register(Version)
admin.site.register(SystemProfileReport)
admin.site.register(SystemProfileReportRecord)
