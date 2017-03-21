from django import forms


class SearchForm(forms.Form):
    """
    Home research form
    """
    CHOICES = (('Gene family name', 'Gene family name'),
               ('Gene Ensembl ID', 'Gene Ensembl ID'),
               ('Gene name', 'Gene name'),
               ('Species', 'Species'))
    search = forms.CharField(max_length=80, required=True)
    type = forms.ChoiceField(choices=CHOICES)


