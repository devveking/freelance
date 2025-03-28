from django.shortcuts import render

from django.contrib.auth import login
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from userprofile.models import UserProfile

from django.contrib import messages  # Для flash-сообщений



# @login_required
# def show_profile(request, username):
#     profile = get_object_or_404(UserProfile, user__username=username)
#     section = request.GET.get('section', 'info')
#     return render(request, 'profile/profile.html', {
#         'profile': profile,
#         'section': section
#     })

@login_required
def show_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)

    # Разделяем навыки и категории перед передачей в шаблон

    skills_list = [skill.strip() for skill in profile.skills.split(',') if skill.strip()] if profile.skills else []
    categories_list = [category.strip() for category in profile.categories.split(',') if category.strip()] if profile.categories else []

    section = request.GET.get('section', 'info')

    return render(request, 'profile/profile.html', {
        'profile': profile,
        'skills_list': skills_list,
        'categories_list': categories_list,
        'section': section
    })

