from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib.auth.decorators import login_required

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
