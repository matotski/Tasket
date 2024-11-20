from django_filters import rest_framework as filters
from .models import Task, User


class TaskFilter(filters.FilterSet):
    due_date = filters.DateTimeFromToRangeFilter(field_name='due_date')
    assigned_to = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['due_date', 'assigned_to']
