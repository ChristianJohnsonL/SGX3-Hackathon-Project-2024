from django import forms
from django.core.validators import URLValidator

# Refer to the following site for the field names and values from Globus:
# https://github.com/HPC-ED/HPC-ED.github.io/wiki/Metadata-Description

# ('Sent to python', 'displayed in form')
EXPERTISE_LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
    ('All', 'All'),
]

TARGET_GROUP_CHOICES = [
    ('Researchers', 'Researchers'),
    ('Research groups', 'Research Groups'),
    ('Research communities', 'Research Communities'),
    ('Research projects', 'Research Projects'),
    ('Research networks', 'Research Networks'),
    ('Research managers', 'Research Managers'),
    ('Research organizations', 'Research Organizations'),
    ('Students', 'Students'),
    ('Innovators', 'Innovators'),
    ('Providers', 'Providers'),
    ('Funders', 'Funders'),
    ('Research Infrastructure Managers', 'Research Infrastructure Managers'),
    ('Resource Managers', 'Resource Managers'),
    ('Publishers', 'Publishers'),
    ('Other', 'Other'),
]

OUTCOMES_CHOICES = [
    ('proficient', 'Proficiency'),
    ('basic_understanding', 'Basic Understanding'),
    ('deep_knowledge', 'Deep Knowledge'),
    ('apply', 'Apply'),
]

URL_TYPE_CHOICES = [
    ('url', 'URL'),
    ('doi', 'DOI')
]


class MetadataForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    abstract = forms.CharField(widget=forms.Textarea, label='Abstract')
    authors = forms.CharField(label='Authors', required=False)
    expertise_level = forms.ChoiceField(label='Expertise Level', choices=EXPERTISE_LEVEL_CHOICES, widget=forms.RadioSelect)
    learning_outcome = forms.ChoiceField(label='Learning Outcome', choices=OUTCOMES_CHOICES, widget=forms.RadioSelect)
    learning_resource_type = forms.CharField(label='Learning Resource Type')
    target_group = forms.ChoiceField(label='Target Group', choices=TARGET_GROUP_CHOICES, widget=forms.RadioSelect)
    keywords = forms.CharField(label='Keywords')
    version_date = forms.DateTimeField(
        label='Version Date',
        input_formats=['%Y-%m-%dT%H:%M'],  # Ensure this matches the HTML5 datetime-local format
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )   
    language = forms.CharField(label='Language', max_length=10)
    url = forms.CharField(label='URL', validators=[URLValidator()], max_length=200)
    resource_url_type = forms.ChoiceField(label='Resource URL Type', choices=URL_TYPE_CHOICES, widget=forms.RadioSelect)
    license = forms.CharField(label='License', required=False)
    cost = forms.CharField(label='Cost', required=False)
    start_datetime = forms.DateTimeField(
        label='Start Datetime',
        input_formats=['%Y-%m-%dT%H:%M'],  # Ensure this matches the HTML5 datetime-local format
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )    
    duration = forms.IntegerField(label='Duration', min_value=1)
    provider_id = forms.CharField(label='Provider ID', max_length=100)
    rating = forms.DecimalField(label='Rating', max_digits=2, decimal_places=1)


class SearchForm(forms.Form):
    Search_Query = forms.CharField(label='Search Query', max_length=200)
    Expertise_Level = forms.MultipleChoiceField(label='Expertise Level', choices=EXPERTISE_LEVEL_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    Learning_Outcome = forms.MultipleChoiceField(label='Learning Outcome', choices=OUTCOMES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    Target_Group = forms.MultipleChoiceField(label='Target Group', choices=TARGET_GROUP_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)