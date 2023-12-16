from django.contrib import admin
from . models import Course,Skill,Instructor,User
# Register your models here.
@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'list_display','language' ,'enrolled'  ,'url'  ,'level'  ,'total_hours'  ,'type'  ,'price'  ,'description'   ,'syllabus'  ,'date_modified'  ,'certificated'  ,'rating' ,'skill']
@admin.register(Skill)
class SkillModelAdmin(admin.ModelAdmin):
    list_display = ['type']
@admin.register(Instructor)
class InstructorModelAdmin(admin.ModelAdmin):
    list_display = ['Name','organization','numberofcourse' ,'Field' ,'rating' ]
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['ID' ,'Profile_Picture','Email','Password' ,'Name' ,'cours','skill' ]