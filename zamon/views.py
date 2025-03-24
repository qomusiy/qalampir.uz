from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from habar.models import Habar, Bolim, Sponsor, Contact
from habar.forms import ContactForm, CommentForm
from django.contrib import messages
from user.models import Comment, CommentLike
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import datetime

def get_date():
    return datetime.datetime.today()

def get_category():
    return Bolim.objects.all()

def index(request):
    context = {
        'habar': Habar.objects.all().order_by('-date'),
        'habar2': Habar.objects.all().order_by('-view'),
        'bolim': get_category(),
        'sponsor': Sponsor.objects.all(),
        'uzb': Habar.objects.filter(bolim__name="O'zbekiston").order_by('-date'),
        'jah': Habar.objects.filter(bolim__name="Jahon").order_by('-date'),
        'iqt': Habar.objects.filter(bolim__name="Iqtisodiyot").order_by('-date'),
        'spo': Habar.objects.filter(bolim__name="Sport").order_by('-date'),
        'date': get_date(),
        'user': request.user,
    }
    return render(request, 'index.html', context=context)

def about(request):
    context = {
        'habar2': Habar.objects.all().order_by('-view'),
        'habar': Habar.objects.all().order_by('-date'),
        'bolim': get_category(),
        'sponsor': Sponsor.objects.all(),
        'date': get_date(),
        'user': request.user,
    }
    return render(request, '404.html', context=context)

def detail(request, pk):
    habar0 = get_object_or_404(Habar, pk=pk)
    habarlar = Habar.objects.filter(bolim=habar0.bolim).exclude(id=habar0.id).order_by('-date')
    popular_news = Habar.objects.all().exclude(id=habar0.id).order_by('-view')
    sponsor = Sponsor.objects.all()
    comments = Comment.objects.filter(post__title=habar0.title).order_by('-created_at')[:3][::-1]
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = habar0
                comment.save()
                return redirect('detail', pk=habar0.id)
            except:
                return redirect('login')
    else:
        form = CommentForm()

    habar0.view += 1
    habar0.save()

    # Add like data for each comment
    comment_data = []
    for comment in comments:
        user_liked = request.user.is_authenticated and CommentLike.objects.filter(user=request.user, comment=comment).exists()
        like_count = comment.likes.count()
        comment_data.append({
            'comment': comment,
            'user_liked': user_liked,
            'like_count': like_count,
        })

    context = {
        'ctg': get_category(),
        'habar0': habar0,
        'habarlar': habarlar[:3],
        'popular_news': popular_news[:6],
        'date': get_date(),
        'sponsor': sponsor,
        'habar': Habar.objects.all().order_by('-date'),
        'bolim': get_category(),
        'comments': comment_data,  # Updated to use comment_data
        'form': form,
        'user': request.user,
    }
    return render(request, 'single_page.html', context)

@login_required
@require_POST
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    user = request.user

    # Check if the user already liked the comment
    like = CommentLike.objects.filter(user=user, comment=comment).first()
    
    if like:
        # Unlike: Remove the like
        like.delete()
        liked = False
    else:
        # Like: Add a new like
        CommentLike.objects.create(user=user, comment=comment)
        liked = True

    like_count = comment.likes.count()
    return JsonResponse({'status': 'success', 'liked': liked, 'like_count': like_count})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'bolim': get_category(),
        'habar': Habar.objects.all().order_by('-date'),
        'habar2': Habar.objects.all().order_by('-view')[:6],
        'date': get_date(),
        'form': form,
        'user': request.user,
    }
    return render(request, 'contact.html', context)

def category_detail(request, pk):
    bolim0 = get_object_or_404(Bolim, id=pk)
    habarlar = Habar.objects.filter(bolim=bolim0).order_by('-date')
    context = {
        'bolim': get_category(),
        'habarlar': habarlar,
        'date': get_date(),
        'bolim0': bolim0,
        'habar': Habar.objects.order_by('-date'),
        'user': request.user,
    }
    return render(request, 'category.html', context)

def interface(request):
    habar = Habar.objects.all().order_by('-date')
    context = {
        'bolim': get_category(),
        'habar': habar,
        'habarlar': habar,
        'date': get_date(),
        'user': request.user,
    }
    return render(request, 'interface.html', context)

@require_POST
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        f = form.save(commit=False)
        f.updated_at = get_date()
        form.save()
        return JsonResponse({'status': 'success', 'post_id': comment.post.id})  # Add post_id to response
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user != comment.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    comment.delete()
    return JsonResponse({'status': 'success'})