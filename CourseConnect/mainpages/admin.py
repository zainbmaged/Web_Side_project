from django.contrib import admin
from . models import Course, Skill

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    pass

class SkillAdmin(admin.ModelAdmin):
    pass

class InstructorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)
admin.site.register(Skill, SkillAdmin)
#admin.site.register(Instructor, InstructorAdmin)
