from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse

from dynamic_report.forms import ShowReportForm
from dynamic_report.models import ReportParameter

# Register your models here.
class ReportParameterInline(admin.TabularInline):
        model = ReportParameter
        extra = 0

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ReportParameterInline]
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.62.0/codemirror.min.css',
                'https://codemirror.net/5/theme/darcula.css', # theme dracula for sql editor
                )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.62.0/codemirror.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.62.0/mode/sql/sql.js',
            'dynamic_report/reporte.js',  # ajust the path for your custom js
        )
        
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = [
            path('select_report/', self.admin_site.admin_view(self.select_report), name='%s_%s_select_report' % info),
        ]
        return custom_urls + urls
    
    def construct_sql_query(self, original_sql_query, form_data):
        from django.db import connection
        parameters_in_sql = [parameter.split('@')[1] for parameter in original_sql_query.split() if '@' in parameter]

        for parameter in parameters_in_sql:
            original_sql_query = original_sql_query.replace(f"@{parameter}", f"%({parameter})s")
            
        with connection.cursor() as cursor:
            cursor.execute(original_sql_query, form_data)
            results = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            results_with_headers = [dict(zip(headers, result)) for result in results]

        return results_with_headers

    def select_report(self, request):
        from django.core.serializers.json import DjangoJSONEncoder
        import json

        context = {}
        form_type = ShowReportForm
        
        form = form_type(request.POST or None,
                         request.FILES or None)
        
        if request.POST and form.is_valid():
            report = form.cleaned_data['name']
            if report.bi_url:
                context['uri_dashboard'] = report.bi_url
            else:
                result = self.construct_sql_query(report.sql_query, form.cleaned_data)
                context['results'] = json.dumps(result, cls=DjangoJSONEncoder)
            
        context['title'] = _("Report")
        context['form'] = form
        context['opts'] = self.model._meta
        
        return TemplateResponse(request, "admin/dynamic_report/select.html", context)