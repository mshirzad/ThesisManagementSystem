from django.contrib import admin
from main.models import StudentsInfo

class StudentsInfoAdmin(admin.ModelAdmin):
	
	list_display = ('name', 'father_name', 'department', 'monograph_title', 'graduation_year')


admin.site.register(StudentsInfo, StudentsInfoAdmin)
admin.site.site_header = 'Thesis Management & Plagiarism Detection System'