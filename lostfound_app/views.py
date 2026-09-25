from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import PetReportForm
from .models import PetReport


@login_required
def report_overview(request):

    report_filter = request.GET.get(
        "type",
        "ALL",
    )

    reports = (
        PetReport.objects
        .filter(
            report_status=PetReport.ReportStatus.OPEN
        )
        .select_related(
            "reporter",
            "pet",
        )
    )

    if report_filter == "LOST":
        reports = reports.filter(
            report_type=PetReport.ReportType.LOST
        )

    elif report_filter == "FOUND":
        reports = reports.filter(
            report_type=PetReport.ReportType.FOUND
        )

    search = request.GET.get(
        "q",
        "",
    ).strip()

    if search:
        reports = reports.filter(
            Q(location__icontains=search)
            | Q(description__icontains=search)
            | Q(pet__name__icontains=search)
            | Q(pet__breed__icontains=search)
        )

    lost_count = PetReport.objects.filter(
        report_status=PetReport.ReportStatus.OPEN,
        report_type=PetReport.ReportType.LOST,
    ).count()

    found_count = PetReport.objects.filter(
        report_status=PetReport.ReportStatus.OPEN,
        report_type=PetReport.ReportType.FOUND,
    ).count()

    my_open_count = PetReport.objects.filter(
        reporter=request.user,
        report_status=PetReport.ReportStatus.OPEN,
    ).count()

    return render(
        request,
        "lostfound_app/report_overview.html",
        {
            "reports": reports,
            "report_filter": report_filter,
            "search": search,
            "lost_count": lost_count,
            "found_count": found_count,
            "my_open_count": my_open_count,
        },
    )


@login_required
def my_reports(request):

    reports = (
        PetReport.objects
        .filter(reporter=request.user)
        .select_related("pet")
        .order_by(
            "-created_at",
            "-report_id",
        )
    )

    return render(
        request,
        "lostfound_app/my_reports.html",
        {
            "reports": reports,
        },
    )


@login_required
def report_add(request):

    initial_type = request.GET.get("type")

    if initial_type not in {
        PetReport.ReportType.LOST,
        PetReport.ReportType.FOUND,
    }:
        initial_type = None

    if request.method == "POST":

        form = PetReportForm(
            request.POST,
            request.FILES,
            user=request.user,
        )

        if form.is_valid():

            report = form.save(
                commit=False
            )

            report.reporter = request.user

            report.report_status = (
                PetReport.ReportStatus.OPEN
            )

            report.save()

            messages.success(
                request,
                "Your report has been published.",
            )

            return redirect(
                "report_detail",
                report_id=report.report_id,
            )

    else:

        form = PetReportForm(
            user=request.user,
            initial={
                "report_type": initial_type
            },
        )

    return render(
        request,
        "lostfound_app/report_form.html",
        {
            "form": form,
            "page_title": "Create pet report",
            "button_text": "Publish report",
        },
    )


@login_required
def report_detail(request, report_id):

    report = get_object_or_404(
        PetReport.objects.select_related(
            "reporter",
            "pet",
        ),
        report_id=report_id,
    )

    return render(
        request,
        "lostfound_app/report_detail.html",
        {
            "report": report,
        },
    )


@login_required
def report_edit(request, report_id):

    report = get_object_or_404(
        PetReport,
        report_id=report_id,
        reporter=request.user,
    )

    if request.method == "POST":

        form = PetReportForm(
            request.POST,
            request.FILES,
            instance=report,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Report updated successfully.",
            )

            return redirect(
                "report_detail",
                report_id=report.report_id,
            )

    else:

        form = PetReportForm(
            instance=report,
            user=request.user,
        )

    return render(
        request,
        "lostfound_app/report_form.html",
        {
            "form": form,
            "report": report,
            "page_title": "Edit report",
            "button_text": "Save changes",
        },
    )


@login_required
def report_resolve(request, report_id):

    report = get_object_or_404(
        PetReport,
        report_id=report_id,
        reporter=request.user,
    )

    if request.method == "POST":

        report.report_status = (
            PetReport.ReportStatus.RESOLVED
        )

        report.save(
            update_fields=[
                "report_status"
            ]
        )

        messages.success(
            request,
            "Report marked as resolved.",
        )

    return redirect(
        "report_detail",
        report_id=report.report_id,
    )


@login_required
def report_reopen(request, report_id):

    report = get_object_or_404(
        PetReport,
        report_id=report_id,
        reporter=request.user,
    )

    if request.method == "POST":

        report.report_status = (
            PetReport.ReportStatus.OPEN
        )

        report.save(
            update_fields=[
                "report_status"
            ]
        )

        messages.success(
            request,
            "Report reopened.",
        )

    return redirect(
        "report_detail",
        report_id=report.report_id,
    )


@login_required
def report_delete(request, report_id):

    report = get_object_or_404(
        PetReport,
        report_id=report_id,
        reporter=request.user,
    )

    if request.method == "POST":

        report.delete()

        messages.success(
            request,
            "Report deleted.",
        )

        return redirect(
            "my_reports"
        )

    return render(
        request,
        "lostfound_app/report_delete.html",
        {
            "report": report,
        },
    )