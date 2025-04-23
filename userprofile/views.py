from django.shortcuts import render

from django.contrib.auth import login
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from userprofile.models import UserProfile, Portfolio, Review
from tasks.models import Job
from django.db.models import Avg, Count
from .forms import ProfileEditForm, WorkExperienceFormSet, EducationFormSet, PortfolioForm, ReviewForm
from django.urls import reverse
from django.contrib import messages  # Для flash-сообщений



@login_required
def show_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)

    new_jobs = Job.objects.filter(client=profile.user, status='new')
    in_progress_jobs = Job.objects.filter(client=profile.user, status='in_progress')
    completed_jobs = Job.objects.filter(client=profile.user, status='completed')

    for job_list in [new_jobs, in_progress_jobs, completed_jobs]:
        for job in job_list:
            job.tag_list = [tag.strip() for tag in job.tags.split(',') if tag.strip()] if job.tags else []

    skills_list = [skill.strip() for skill in profile.skills.split(',') if skill.strip()] if profile.skills else []
    categories_list = [category.strip() for category in profile.categories.split(',') if category.strip()] if profile.categories else []

    portfolios = profile.portfolios.all()
    section = request.GET.get('section', 'info')

    # Инициализируем формы
    portfolio_form = PortfolioForm()
    review_form = ReviewForm()



    # Обработка форм
    if request.method == 'POST':
        # Если это владелец профиля — добавляет портфолио
        if request.user == profile.user and 'add_portfolio' in request.POST:
            portfolio_form = PortfolioForm(request.POST, request.FILES)
            if portfolio_form.is_valid():
                portfolio = portfolio_form.save(commit=False)
                portfolio.profile = profile
                portfolio.save()
                return redirect(reverse('profile:user', args=[request.user.username]) + '?section=portfolio')

        # Если это другой пользователь — добавляет отзыв
        elif request.user != profile.user and 'add_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                Review.objects.update_or_create(
                    profile=profile,
                    author=request.user,
                    defaults=review_form.cleaned_data
                )
                return redirect(reverse('profile:user', args=[profile.user.username]) + '?section=reviews')



    # Получаем отзывы
    reviews = profile.reviews.select_related('author').order_by('-created_at')

    user_review = None
    if request.user.is_authenticated and request.user != profile.user:
        try:
            user_review = profile.reviews.get(author=request.user)
        except Review.DoesNotExist:
            pass

    if request.method == 'POST':
        if 'delete_review' in request.POST and user_review:
            user_review.delete()
            return redirect(reverse('profile:user', args=[profile.user.username]) + '?section=reviews')

    # Остальные отзывы без текущего пользователя
    if user_review:
        other_reviews = profile.reviews.exclude(id=user_review.id).select_related('author').order_by('-created_at')
    else:
        other_reviews = reviews  # уже полученные ранее

    total_reviews = reviews.count()

    # Преобразуем звёзды:
    def annotate_review_stars(review):
        rating = review.rating
        full = int(rating)
        half = 1 if (rating - full) >= 0.5 else 0
        empty = 5 - full - half
        review.full_stars = full
        review.half_star = half
        review.empty_stars = empty

    if user_review:
        annotate_review_stars(user_review)
    for review in other_reviews:
        annotate_review_stars(review)

    average_rating = profile.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    rating_data = profile.reviews.values('rating').annotate(count=Count('rating'))
    rating_breakdown = {str(item['rating']): item['count'] for item in rating_data}
    full_stars = int(average_rating)
    half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star



    return render(request, 'profile/profile.html', {
        'profile': profile,
        'skills_list': skills_list,
        'categories_list': categories_list,
        'section': section,
        'new_jobs': new_jobs,
        'in_progress_jobs': in_progress_jobs,
        'completed_jobs': completed_jobs,
        'portfolios': portfolios,
        'portfolio_form': portfolio_form,
        'review_form': review_form,
        'average_rating': average_rating,
        'rating_breakdown': rating_breakdown,
        'full_stars': full_stars,
        'empty_stars': empty_stars,
        'half_star': half_star,
        'reviews': other_reviews,
        'user_review': user_review,
        'total_reviews': total_reviews,

    })


@login_required
def delete_portfolio(request):
    if request.method == 'POST':
        portfolio_id = request.POST.get('portfolio_id')
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        if portfolio.profile.user == request.user:
            portfolio.delete()
    return redirect(reverse('profile:user', args=[request.user.username]) + '?section=portfolio')

@login_required
def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, profile__user=request.user)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile:user', args=[request.user.username]) + '?section=portfolio')
    else:
        form = PortfolioForm(instance=portfolio)

    return redirect('profile:user', username=request.user.username)

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