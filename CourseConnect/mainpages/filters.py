import django_filters
from django_filters import DateFilter
from .models import Course

"""
from django.db.models import CharField

CharField.register_lookup(Lower)
"""

class OrderFilter(django_filters.FilterSet):
    class Meta:
         model = Course
         #fields = '__all__'
         fields = {
              'Title': ['icontains'],
              'Price': ['icontains'],
              'Rating': ['icontains'],
              'Level': ['icontains'],
              'Language': ['icontains'],
              'Platform': ['icontains'],
          }
         exclude = ['URL','Description', 'Certificate',
                    'Skill','Instructors', 'Reviews',
                    'Enrolled', 'Learning_Type',
                    'Last_Updated','Duration']
         
    def exclude_case_insensitive(self, queryset, name, value):
         return queryset.exclude(**{f"{name}__lower__in": [e.lower() for e in value]})
    