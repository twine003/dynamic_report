from django.db import models

# Create your models here.
PARAMETER_TYPES = [
        ('text', 'Text'),
        ('integer', 'Integer'),
        ('decimal', 'Decimal'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
        ('choice_list', 'Choice List'),
        ('multiple_choice', 'Multiple Choice'),
        ('json', 'JSON or Dict'),
    ]

class ReportParameter(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name="parameters")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=PARAMETER_TYPES)
    required = models.BooleanField(default=False)
    data = models.CharField(max_length=500, null=True, blank=True, 
        help_text="List of data to select from in case of choice list or multiple choice, " \
        "use the convention app.model to generate data from an existing model")

    def __str__(self):
        return self.name

class Report(models.Model):
    name = models.CharField(max_length=255)
    sql_query = models.TextField(null=True, blank=True)
    bi_url = models.URLField(null=True, blank=True)

    def __str__(self):
            return self.name