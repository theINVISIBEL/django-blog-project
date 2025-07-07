from .models import Category

def categories_processor(request):
    return {
        'categorys': Category.objects.all()
    }
