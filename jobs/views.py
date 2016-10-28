# -*- coding: utf-8 -*-

from digg_paginator import DiggPaginator
from django.db.models import Q
from django.views.generic import ListView

from jobs.models import JobItem


class JobList(ListView):
    """Лента новостей."""
    template_name = 'jobs_list.html'
    context_object_name = 'jobs'
    paginate_by = 20
    paginator_class = DiggPaginator
    model = JobItem

    def get_queryset(self):
        jobs = super(JobList, self).get_queryset()
        search = self.request.GET.get('q')
        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        jobs = jobs.order_by('-created_at')
        return jobs

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'jobs'
        return context
