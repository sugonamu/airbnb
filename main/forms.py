from django import forms
from .models import Reservation, Review  # Import your Reservation and Review models

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'number_of_guests']  # Adjust fields as needed

        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError("Check-out date must be after check-in date.")

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Adjust fields as needed

        widgets = {
            'rating': forms.Select(choices=[
                (1, '1 Star'), 
                (2, '2 Stars'), 
                (3, '3 Stars'), 
                (4, '4 Stars'), 
                (5, '5 Stars')
            ]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment:
            raise forms.ValidationError("Comment cannot be empty.")
        return comment
