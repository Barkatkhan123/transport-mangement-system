from django import forms
from django.utils import timezone
from .models import City, Route, Trip

INPUT_CLASS = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500'
SELECT_CLASS = 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white'


class TripSearchForm(forms.Form):
    origin = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label='From City',
        widget=forms.Select(attrs={'class': SELECT_CLASS, 'id': 'id_origin'})
    )
    destination = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label='To City',
        widget=forms.Select(attrs={'class': SELECT_CLASS, 'id': 'id_destination'})
    )
    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': INPUT_CLASS,
            'type': 'date',
            'id': 'id_travel_date',
        })
    )
    passengers = forms.IntegerField(
        min_value=1, max_value=10, initial=1,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'id': 'id_passengers',
            'min': 1, 'max': 10,
        })
    )

    def clean_travel_date(self):
        date = self.cleaned_data['travel_date']
        if date < timezone.now().date():
            raise forms.ValidationError('Travel date cannot be in the past.')
        return date

    def clean(self):
        cleaned = super().clean()
        origin = cleaned.get('origin')
        destination = cleaned.get('destination')
        if origin and destination and origin == destination:
            raise forms.ValidationError('Origin and destination cannot be the same.')
        return cleaned


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['route', 'bus', 'driver', 'departure_datetime', 'arrival_datetime', 'base_price']
        widgets = {
            'route': forms.Select(attrs={'class': SELECT_CLASS}),
            'bus': forms.Select(attrs={'class': SELECT_CLASS}),
            'driver': forms.Select(attrs={'class': SELECT_CLASS}),
            'departure_datetime': forms.DateTimeInput(attrs={'class': INPUT_CLASS, 'type': 'datetime-local'}),
            'arrival_datetime': forms.DateTimeInput(attrs={'class': INPUT_CLASS, 'type': 'datetime-local'}),
            'base_price': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Price (PKR)', 'min': 0, 'step': '0.01'}),
        }

    def __init__(self, agency=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if agency:
            self.fields['bus'].queryset = agency.buses.filter(status='active')
            self.fields['driver'].queryset = agency.drivers.filter(status='active')

    def clean(self):
        cleaned = super().clean()
        departure = cleaned.get('departure_datetime')
        arrival = cleaned.get('arrival_datetime')
        bus = cleaned.get('bus')
        driver = cleaned.get('driver')

        if departure and arrival and arrival <= departure:
            raise forms.ValidationError('Arrival time must be after departure time.')

        if bus and departure and arrival:
            conflict = Trip.objects.filter(
                bus=bus,
                departure_datetime__lt=arrival,
                arrival_datetime__gt=departure,
                status__in=['scheduled', 'boarding', 'departed']
            )
            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                raise forms.ValidationError(f'Bus {bus.registration_number} is already scheduled during this time.')

        if driver and departure and arrival:
            conflict = Trip.objects.filter(
                driver=driver,
                departure_datetime__lt=arrival,
                arrival_datetime__gt=departure,
                status__in=['scheduled', 'boarding', 'departed']
            )
            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                raise forms.ValidationError(f'Driver {driver.full_name} is already assigned during this time.')

        return cleaned


class RouteForm(forms.ModelForm):
    estimated_duration_hours = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=2,
        min_value=0.1,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Duration in hours (e.g. 18 or 2.5)',
            'step': 'any',
            'min': '0.1'
        }),
        label='Duration (hours)'
    )

    class Meta:
        model = Route
        fields = ['origin', 'destination', 'distance_km', 'estimated_duration_hours']
        widgets = {
            'origin': forms.Select(attrs={'class': SELECT_CLASS}),
            'destination': forms.Select(attrs={'class': SELECT_CLASS}),
            'distance_km': forms.NumberInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Distance in KM', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.estimated_duration_minutes:
            hours = self.instance.estimated_duration_minutes / 60
            self.fields['estimated_duration_hours'].initial = int(hours) if hours.is_integer() else round(hours, 2)

    def clean(self):
        cleaned = super().clean()
        origin = cleaned.get('origin')
        destination = cleaned.get('destination')
        if origin and destination and origin == destination:
            raise forms.ValidationError('Origin and destination cannot be the same city.')
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        hours = self.cleaned_data.get('estimated_duration_hours')
        if hours is not None:
            instance.estimated_duration_minutes = int(round(float(hours) * 60))
        else:
            instance.estimated_duration_minutes = None
        if commit:
            instance.save()
        return instance
