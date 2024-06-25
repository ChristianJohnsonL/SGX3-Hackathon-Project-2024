from django import forms
from django.core.validators import URLValidator

EXPERTISE_LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('all', 'All'),
]

TARGET_GROUP_CHOICES = [
    ('students', 'Students'),
    ('research_groups', 'Research Groups'),
    ('publishers', 'Publishers'),
    ('research_organizations', 'Research Organizations'),
    ('researchers', 'Researchers'),
    ('research_managers', 'Research Managers'),
    ('funders', 'Funders'),
    ('innovators', 'Innovators'),
    ('research_networks', 'Research Networks'),
    ('research_projects', 'Research Projects'),
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
