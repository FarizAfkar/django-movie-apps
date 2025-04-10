from django import forms
from .models import Genre, MPAA_Rating, Movie, MovieGenre

class GenreForm(forms.ModelForm):
    """Form for creating or updating a Genre."""
    name = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'id':'Name'
                            }),
                        label='')

    class Meta:
        model = Genre
        fields = ['name']


class MPAA_RatingForm(forms.ModelForm):
    """Form for creating or updating MPAA Rating."""
    type_mpaa = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control col-2',
                            'id':'type_mpaa'
                            }),
                        label='')
    label = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control col-2',
                            'id':'label_mpaa'
                            }),
                        label='')

    class Meta:
        model = MPAA_Rating
        fields = ['type_mpaa', 'label']


class MovieForm(forms.ModelForm):
    """Form for creating or updating a Movie."""
    name = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'id':'name',
                            'placeholder':'Name'
                            }),
                        label='Name')
    description = forms.CharField(
                        widget=forms.Textarea(
                        attrs={
                            'class':'form-control',
                            'id':'description',
                            'placeholder':'Description',
                            'rows': 3, 'cols': 30
                            }),
                        label='Description')
    imgPath = forms.FileField(
                        widget=forms.ClearableFileInput(
                        attrs={
                            'class':'form-control',
                            'id':'imgPath',
                            'placeholder':'imgPath',
                            'multiple': False
                            }),
                        label='Poster')
    duration = forms.IntegerField(
                        widget=forms.NumberInput(
                        attrs={
                            'class':'form-control',
                            'id':'duration',
                            'placeholder':'Duration',
                            'min':'0',
                            }),
                        label='Duration')
    language = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'id':'language',
                            'placeholder':'Language',
                            }),
                        label='Language')
    userRating = forms.DecimalField(
                        widget=forms.NumberInput(
                        attrs={
                            'class':'form-control',
                            'id':'userRating',
                            'placeholder':'User Rating',
                            'max':'5',
                            'min':'0',
                            'step':'0.1',
                            }),
                        label='User Rating')
    # Adding MPAA Rating select one mpaa rating
    mpaaRating = forms.ChoiceField(
                        widget=forms.Select(
                        attrs={
                            'class':'form-select',
                            'id':'mpaaRating',
                            'placeholder':'MPAA Rating',
                            }),
                        label='MPAA Rating')
    # Adding genre as a Many-to-Many field (select multiple genres)
    genre = forms.MultipleChoiceField(  # All available genres
                        widget=forms.SelectMultiple(
                            attrs={'class': 'form-select',
                                   'id':'genre',
                                   'placeholder':'Genre',
                                   }),  # You can add bootstrap classes here for styling
                            label='Genre')

    class Meta:
        model = Movie
        fields = [
            'name', 'description', 'imgPath', 'duration',
            'language', 'userRating', 'mpaaRating', 'genre'
        ]
