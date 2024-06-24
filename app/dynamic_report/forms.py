from django import forms

from dynamic_report.models import Report, ReportParameter


class ShowReportForm(forms.Form):
        class Meta:
            fields = ['name',]
    
        def __init__(self, *args, **kwargs):
            super(ShowReportForm, self).__init__(*args, **kwargs)
            
            self.fields['name'] = forms.ModelChoiceField(
                queryset=Report.objects.all(),
                empty_label="Select the report name",
                help_text="Select the name of the report",
            )
            if self.data and 'name' in self.fields:
                parameters = ReportParameter.objects.filter(report=self.data.get('name'))
                for parameter in parameters:
                    if parameter.type == 'text':
                        self.fields[parameter.name] = forms.CharField(label=parameter.name, required=parameter.required)
                    elif parameter.type == 'integer':
                        self.fields[parameter.name] = forms.IntegerField(label=parameter.name, required=parameter.required)
                    elif parameter.type == 'decimal':
                        self.fields[parameter.name] = forms.DecimalField(label=parameter.name, required=parameter.required)
                    elif parameter.type == 'date':
                        self.fields[parameter.name] = forms.DateField(label=parameter.name,
                                                                        required=parameter.required,
                                                                        widget=forms.DateInput(attrs={'type': 'date'}))
                    elif parameter.type == 'boolean':
                        self.fields[parameter.name] = forms.BooleanField(label=parameter.name)
                    elif parameter.type == 'option_list':
                        # Selection field for option list
                        choices = self._get_choices_from_data(parameter.data)
                        self.fields[parameter.name] = forms.ChoiceField(
                            label=parameter.name,
                            choices=choices,
                            required=parameter.required
                        )
                    elif parameter.type == 'multiple_selection':
                        # Multiple selection field
                        choices = self._get_choices_from_data(parameter.data)
                        self.fields[parameter.name] = forms.MultipleChoiceField(
                            label=parameter.name,
                            choices=choices,
                            required=parameter.required,
                            widget=forms.CheckboxSelectMultiple
                        )
                    
        def _get_choices_from_data(self, data):
            from django.apps import apps
    
            # Retrieve options from ParametroReporte model data
            if data:
                # If format is 'app.model', load options from the specified model
                if '.' in data:
                    app_label, model_name = data.split('.')
                    model = apps.get_model(app_label, model_name)
                    choices = [(obj.pk, str(obj)) for obj in model.objects.all()]
                else:
                    # If format is a comma-separated list of options
                    choices = [option.strip() for option in data.split(',')]
                    choices = [(option, option) for option in choices]
                return choices
            return []