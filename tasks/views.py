from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timesince import timesince

from .forms import JobForm
from django.contrib.auth.decorators import login_required
from .models import Job

from userprofile.models import UserProfile
from django.db.models import Q
from datetime import date, timedelta
from django.urls import reverse


# @login_required
# def find_task(request):
#     jobs = Job.objects.filter(status='new').order_by('-created_at')
#
#     # Получаем профили клиентов для заданий
#     profiles = {profile.user.id: profile for profile in UserProfile.objects.filter(user__in=[job.client for job in jobs])}
#
#     for job in jobs:
#         job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []
#         job.time_since_created = timesince(job.created_at)
#         job.is_owner = job.client == request.user
#         job.profile = profiles.get(job.client.id)
#
#     return render(request, 'tasks/find_task.html', {
#         'jobs': jobs
#     })

from django.db.models import Count

@login_required
def find_task(request):
    search_query = request.GET.get('q', '')
    selected_categories = request.GET.getlist('category')
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    deadline_filter = request.GET.get('deadline')
    tag_query = request.GET.get('tags', '')

    # Базовый queryset
    jobs = Job.objects.filter(status='new')

    # Категории с количеством задач (до фильтрации по категориям)
    category_counts = Job.objects.filter(status='new') \
        .values('category') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if selected_categories:
        jobs = jobs.filter(category__in=selected_categories)

    if min_budget:
        jobs = jobs.filter(budget__gte=min_budget)
    if max_budget:
        jobs = jobs.filter(budget__lte=max_budget)

    if deadline_filter == 'within last day':
        jobs = jobs.filter(deadline__lte=date.today() + timedelta(days=1))
    elif deadline_filter == 'within last week':
        jobs = jobs.filter(deadline__lte=date.today() + timedelta(days=7))
    elif deadline_filter == 'flexible':
        jobs = jobs.filter(deadline__gt=date.today() + timedelta(days=7))
    # 'all' — без фильтрации

    if tag_query:
        tags = [tag.strip() for tag in tag_query.split(',') if tag.strip()]
        for tag in tags:
            jobs = jobs.filter(tags__icontains=tag)

    jobs = jobs.order_by('-created_at')

    profiles = {profile.user.id: profile for profile in UserProfile.objects.filter(user__in=[job.client for job in jobs])}

    for job in jobs:
        job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []
        job.time_since_created = timesince(job.created_at)
        job.is_owner = job.client == request.user
        job.profile = profiles.get(job.client.id)

    return render(request, 'tasks/find_task.html', {
        'jobs': jobs,
        'search_query': search_query,
        'selected_categories': selected_categories,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'deadline_filter': deadline_filter,
        'tag_query': tag_query,
        'category_counts': category_counts,
    })


@login_required
def task_detail(request, id):
    job = get_object_or_404(Job, id=id)  # Получаем задание по id или 404, если не найдено

    job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []

    is_owner = job.client == request.user

    time_since_created = timesince(job.created_at)

    profile = get_object_or_404(UserProfile, user=job.client)

    return render(request, 'tasks/task-details.html', {
        'job': job,
        'profile': profile,
        'time_since_created':time_since_created,
        'is_owner': is_owner,
        'client': job.client
    })


@login_required
def create_task(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return redirect(reverse('profile:user', args=[request.user.username]) + '?section=tasks')
    else:
        form = JobForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def edit_task(request, id):
    job = get_object_or_404(Job, id=id, client=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('task_detail', id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'tasks/edit_task.html', {'form': form, 'job': job})

@login_required
def delete_task(request, id):
    job = get_object_or_404(Job, id=id, client=request.user)
    if request.method == "POST":
        job.delete()
        return redirect('job_list')
    return redirect('task_detail', id=id)

@login_required
def archive_task(request, id):
    job = get_object_or_404(Job, id=id, client=request.user)
    if request.method == "POST":
        job.status = 'in_progress'  # или 'in_progress', как тебе удобнее
        job.save()
    return redirect('task_detail', id=id)
