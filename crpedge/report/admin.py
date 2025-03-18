import csv
from io import BytesIO
from django.urls import path, reverse
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from reportlab.pdfgen import canvas
from .models import ReportConfiguration


@admin.register(ReportConfiguration)
class ReportConfigurationAdmin(admin.ModelAdmin):
    list_filter = ("company", "project")
    search_fields = ("report_name",)

    fieldsets = (
        ("Report Details", {
            "fields": ("company", "report_name"),
        }),
        ("Filter Settings", {
            "classes": ("collapse",),
            "fields": (
                "main_category", "sub_category", "project", "party", "gl_coa", "bank",
                "bank_branch", "credit_facility", "filter1", "sub_filter1",
                "filter2", "sub_filter2", "curr_code", "curr_rate"
            ),
        }),
    )

    def get_list_display(self, request):
        """Dynamically list non-empty fields plus action and download links."""
        # Get the first report to determine filled fields
        first_report = ReportConfiguration.objects.first()
        if not first_report:
            # Fallback if no records exist
            return ("id", "download_links", "action_buttons")

        filled_fields = []
        for field in first_report._meta.fields:
            # Exclude the 'id' field to avoid duplication
            if field.name == "id":
                continue
            value = getattr(first_report, field.name, None)
            if value:  # Add field to list_display only if it has a value
                filled_fields.append(field.name)

        # Add the action and download links at the end
        filled_fields.extend(["action_buttons", "download_links"])
        return tuple(filled_fields)

    def action_buttons(self, obj):
        """Render edit and delete buttons on the right side."""
        edit_url = reverse('admin:report_reportconfiguration_change', args=[obj.pk])
        delete_url = reverse('admin:report_reportconfiguration_delete', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">Edit</a> &nbsp; <a class="button" href="{}">Delete</a>',
            edit_url, delete_url
        )
    action_buttons.short_description = "Actions"

    def download_links(self, obj):
        """Generate download links for CSV and PDF on the right side."""
        csv_url = reverse('admin:report_download_csv', args=[obj.pk])
        pdf_url = reverse('admin:report_download_pdf', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">CSV</a> | <a class="button" href="{}">PDF</a>',
            csv_url, pdf_url
        )
    download_links.short_description = "Download Report"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'download/csv/<int:report_id>/',
                self.admin_site.admin_view(self.download_csv),
                name='report_download_csv',
            ),
            path(
                'download/pdf/<int:report_id>/',
                self.admin_site.admin_view(self.download_pdf),
                name='report_download_pdf',
            ),
        ]
        return custom_urls + urls

    def download_csv(self, request, report_id):
        """Download the report as a CSV file."""
        try:
            report = ReportConfiguration.objects.get(pk=report_id)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{report.report_name}.csv"'
            writer = csv.writer(response)

            # Add header
            writer.writerow(['Field', 'Value'])

            # Add non-empty fields to the CSV
            for field in report._meta.fields:
                field_name = field.verbose_name.capitalize()
                value = getattr(report, field.name, '')
                if value:
                    writer.writerow([field_name, value])

            return response
        except ReportConfiguration.DoesNotExist:
            return HttpResponse("Report not found.", status=404)

    def download_pdf(self, request, report_id):
        """Download the report as a PDF file."""
        try:
            report = ReportConfiguration.objects.get(pk=report_id)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report.report_name}.pdf"'

            buffer = BytesIO()
            p = canvas.Canvas(buffer)

            y = 800
            p.drawString(100, y, f"Report: {report.report_name}")
            y -= 20
            p.drawString(100, y, f"Company: {report.company}")
            y -= 20

            # Add non-empty fields to the PDF
            for field in report._meta.fields:
                field_name = field.verbose_name.capitalize()
                value = getattr(report, field.name, '')
                if value:
                    y -= 20
                    p.drawString(100, y, f"{field_name}: {value}")

            p.showPage()
            p.save()

            buffer.seek(0)
            response.write(buffer.getvalue())
            buffer.close()
            return response
        except ReportConfiguration.DoesNotExist:
            return HttpResponse("Report not found.", status=404)
