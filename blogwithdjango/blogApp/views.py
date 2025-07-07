from django.shortcuts import render ,get_object_or_404 , redirect
from .models import *
from PIL import Image
from .forms import CommentForm 
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator


from PIL import Image
from .models import Article
import os
from django.conf import settings

def editImage():
    articles = Article.objects.all()
    for article in articles:
        if article.image:
            image_path = article.image.path  # المسار الكامل للصورة على القرص
            try:
                with Image.open(image_path) as img:
                    img = img.resize((302, 347))
                    img.save(image_path)  # حفظ الصورة المعدلة فوق الأصلية

            except Exception as e:
                print(f"خطأ أثناء تعديل الصورة: {e}")



def summarytext():
    articles = Article.objects.all()
    try:
        for article in articles:
            raw_text = strip_tags(article.content)
            short_text = ' '.join(raw_text.split()[:24])
            article.summary = short_text
            article.save()
        print("تم إنشاء ملخص لجميع المقالات.")

    except:
        print("erors")
        



def index(request):
    categories = Category.objects.all()
    article_list = Article.objects.exclude(slug='').order_by('-created_at')
    last5articles = Article.objects.exclude(slug='').order_by('-created_at')[:5]
    paginator = Paginator(article_list, 6)  # عدد المقالات في كل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'categories': categories,
        'page_obj': page_obj,
        'last5articles': last5articles,
    }
    return render(request, "Calvin/index.html", context)


def about(request):
    return render(request, "Calvin/about.html")

def contact(request):
    return render(request, "Calvin/contact.html")




def category(request, slug):
    # 1. جلب التصنيف (Category) المطلوب
    category = get_object_or_404(Category, slug=slug)

    # 2. جلب جميع المقالات التابعة لهذا التصنيف
    article_list = Article.objects.filter(categories=category).order_by('-created_at')

    # 3. تطبيق الترقيم (Pagination)
    paginator = Paginator(article_list, 6)  # عدد المقالات لكل صفحة
    page_number = request.GET.get('page')   # رقم الصفحة من الرابط
    page_obj = paginator.get_page(page_number)  # استرجاع صفحة المقالات

    # 4. تمرير البيانات إلى القالب
    context = {
        'category': category,  # اسم التصنيف
        'page_obj': page_obj,  # المقالات المرقمة
    }

    return render(request, "Calvin/category.html", context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():  
           Name  = form.cleaned_data["Name"]
           Email = form.cleaned_data["Email"]
           comment = form.cleaned_data["comment"]
   
           comment = form.save(commit=False)
           comment.article = article  # نربط التعليق بالمقال
           comment.save()
    
    else:
        form = CommentForm()

    comments = article.comments.all()
    return render(request, 'Calvin/article_detail.html', {'article': article ,'form': form,'comments': comments })



def singleaudio(request, slug):
    article = get_object_or_404(Article, slug=slug ,posttype='audio')
    comments = Comment.objects.filter(article=article)
    videos = Article.objects.exclude(video__exact='')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('singleaudio', slug=article.slug)
    else:
        form = CommentForm()

    # (اختياري) احصل على المقال السابق واللاحق
    previous_article = Article.objects.filter(id__lt=article.id).order_by('-id').first()
    next_article = Article.objects.filter(id__gt=article.id).order_by('id').first()

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'previous_article': previous_article,
        'next_article': next_article,
    }

    return render(request, 'Calvin/single-audio.html', context)







def singlevideo(request ,slug):
    article = get_object_or_404(Article, slug=slug,posttype='video')
    comments = Comment.objects.filter(article=article)
    videos = Article.objects.exclude(video__exact='')



    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('single-video', slug=article.slug)
    else:
        form = CommentForm()

    # (اختياري) احصل على المقال السابق واللاحق
    previous_article = Article.objects.filter(id__lt=article.id).order_by('-id').first()
    next_article = Article.objects.filter(id__gt=article.id).order_by('id').first()
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'previous_article': previous_article,
        'next_article': next_article,
    }
    return render(request, "Calvin/single-video.html", context )

def video_articles(request):
    videos = Article.objects.filter(posttype='video').order_by('-created_at')
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, "Calvin/video_list.html", context)


def audio_articles(request):
    audios = Article.objects.filter(posttype='audio').order_by('-created_at')
    paginator = Paginator(audios, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, "Calvin/audio_list.html", context)

def search_view(request):
    query = request.GET.get('q')
    results = Article.objects.filter(title__icontains=query) if query else []
    return render(request, 'Calvin/search_results.html', {'results': results, 'query': query})



def Standard_articles(request ):
    blogs =  Article.objects.filter(posttype='standard').order_by('-created_at')
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, "Calvin/standard_articles.html", context)


def styles(request):
    return render(request, "Calvin/styles.html")
 