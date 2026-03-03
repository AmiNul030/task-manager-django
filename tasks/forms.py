from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Study Django"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional notes..."}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }