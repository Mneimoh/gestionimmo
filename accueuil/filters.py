import django_filters

from main.models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = '__all__'