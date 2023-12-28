from django.contrib import admin
from smsapp.models import *
from smsapp.resources import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.models import LogEntry

class deliveryAdmin(admin.ModelAdmin):
     def has_add_permission(self, request, obj=None):
        return False

class RecordsAdmin(ImportExportModelAdmin):
	exclude = ('status','date_created', 'date_updated')
	list_display = ('EmpNumber', 'FirstName', 'LastName', 'OfficialEmail', 'Mobile', 'category', 'grade', 'bmc', 'status', 'date_created')
	resource_class=recordsResource   

class AudioAdmin(ImportExportModelAdmin):
	#exclude ='date_updated'
	list_display = ('name', 'description', 'file', 'uploaded_at')
	resource_class=recordsResource 
	list_filter = ['name']
	actions = ['delete_selected']


# Register your models here.
#admin.site.register(unit)
#admin.site.register(bmc)
#admin.site.register(subdistrict)
admin.site.register(district)
admin.site.register(region)
admin.site.register(project)
admin.site.register(theme)
#admin.site.register(broadcastmessage)
#admin.site.register(group)
#admin.site.register(records, RecordsAdmin)
admin.site.register(delivery, deliveryAdmin)
admin.site.register(category)
admin.site.register(AudioFile, AudioAdmin)



#LogEntry.objects.all().delete()
