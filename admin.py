from django.contrib import admin

from .models import Professor,Impactfactor,Journal,Scholar # 모델에서 Resource를 불러온다

# Register your models here

class ProfessorAdmin(admin.ModelAdmin):
  list_display = ('professor_id', 'professor_name', 'professor_homepage', 'depart_name')
class ImpactfactorAdmin(admin.ModelAdmin):
  list_display = ('impactfactor_id', 'impactfactor_value', 'journal_id')
class JournalAdmin(admin.ModelAdmin):
  list_display = ('journal_id', 'journal_name', 'professor_id', 'year', 'scholar_id')
class ScholarAdmin(admin.ModelAdmin):
  list_display = ('scholar_id', 'scholar_name', 'professor_id')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Impactfactor, ImpactfactorAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Scholar, ScholarAdmin)