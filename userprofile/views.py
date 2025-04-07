from django.shortcuts import render

from django.contrib.auth import login
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from userprofile.models import UserProfile
from tasks.models import Job
from .forms import ProfileEditForm, WorkExperienceFormSet, EducationFormSet

from django.contrib import messages  # Для flash-сообщений



@login_required
def show_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)

    active_jobs = Job.objects.filter(client=profile.user, status__in=['new', 'in_progress'])

    # Разделяем теги перед передачей в шаблон
    for job in active_jobs:
        job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []

    # Разделяем навыки и категории перед передачей в шаблон
    skills_list = [skill.strip() for skill in profile.skills.split(',') if skill.strip()] if profile.skills else []
    categories_list = [category.strip() for category in profile.categories.split(',') if category.strip()] if profile.categories else []

    section = request.GET.get('section', 'info')

    return render(request, 'profile/profile.html', {
        'profile': profile,
        'skills_list': skills_list,
        'categories_list': categories_list,
        'section': section,
        'active_jobs': active_jobs,
    })


@login_required
def edit_profile(request):
    profile = request.user.profile # Получаем профиль текущего пользователя
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:user', username=request.user.username)  # Перенаправление на страницу профиля
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "profile/edit-profile.html", {"form": form})


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        work_experience_formset = WorkExperienceFormSet(request.POST, instance=profile)
        education_formset = EducationFormSet(request.POST, instance=profile)

        if form.is_valid() and work_experience_formset.is_valid() and education_formset.is_valid():
            form.save()
            work_experience_formset.save()
            education_formset.save()
            return redirect('profile:user', username=request.user.username)  # Заменить на URL профиля

    else:
        form = ProfileEditForm(instance=profile)
        work_experience_formset = WorkExperienceFormSet(instance=profile)
        education_formset = EducationFormSet(instance=profile)

    return render(request, 'profile/edit-profile.html', {
        'form': form,
        'work_experience_formset': work_experience_formset,
        'education_formset': education_formset
    })