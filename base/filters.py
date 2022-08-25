import django_filters

from .models import *
from django.forms.widgets import TextInput

class StoreFilter(django_filters.FilterSet):

    CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest')
    )
    
   
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='', widget=TextInput(
            attrs={'size': '10',
                   'class': 'form-control',
                   'placeholder': 'Search'}))
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image', 'price']
        
    def filter_by_order(self, queryset, name, value):
        expression = 'user' if value == 'oldest' else '-user'
        return queryset.order_by(expression)
