from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timesince import timesince

from .forms import JobForm
from django.contrib.auth.decorators import login_required
from .models import Job

from userprofile.models import UserProfile

@login_required
def task_detail(request, id):
    job = get_object_or_404(Job, id=id)  # Получаем задание по id или 404, если не найдено

    job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []

    time_since_created = timesince(job.created_at)

    profile = get_object_or_404(UserProfile, user=job.client)

    return render(request, 'tasks/task-details.html', {
        'job': job,
        'profile': profile,
        'time_since_created':time_since_created
    })


@login_required
def create_task(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return redirect('job_list')  # перенаправление на список заданий
    else:
        form = JobForm()
    return render(request, 'tasks/create_task.html', {'form': form})
