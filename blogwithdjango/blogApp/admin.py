from django.contrib import admin
from .models import *
from .models import Article
from django.contrib import admin
from .models import Article



admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(AuthorProfile)

