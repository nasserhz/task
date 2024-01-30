from django.urls import path

from . import views


urlpatterns = [
    path(
        "delay",
        views.AddDelayReport.as_view(),
        name="delay-report"
    ),
    path(
        "assign",
        views.AssignAgent.as_view(),
        name="assign-agent"
    ),
    path(
        "report",
        views.VendorReports.as_view(),
        name="vendor-reports"
    ),
]
