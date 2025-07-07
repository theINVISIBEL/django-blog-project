from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
import hashlib
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.name


User = get_user_model()


TYPE_CHOICES = [
        ('audios','audio'),
        ( 'videos','video'),
        ( 'texts','text'),
    ]

def validate_audio_extension(file):
        allowed_extensions = ('mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a')
        ext = str(file.name).split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(f"امتداد الملف '{ext}' غير مدعوم.")

def validate_video_extension(file):
        allowed_extensions = ('mov', 'avi', 'mp4', 'webm', 'mkv')
        ext = str(file.name).split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(f"امتداد الفيديو '{ext}' غير مدعوم.")
        
class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='authorspic/', blank=True)
    bio = models.TextField()
    work = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
        
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


ARTICLE_TYPES = (
    ('standard', 'Standard'),
    ('video', 'Video'),
    ('audio', 'Audio'),
)




class Article(models.Model):
    ARTICLE_TYPES = (
    ('standard', 'Standard'),
    ('video', 'Video'),
    ('audio', 'Audio'),)
    title    = models.CharField(max_length=200)
    summary = models.TextField(max_length=200 ,blank=True, null=True)
    slug    = models.SlugField(max_length=200, unique=True)         
    author = models.ForeignKey(AuthorProfile, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField()
    updated_at  = models.DateTimeField(auto_now=True)
    published   = models.BooleanField(default=False)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags   =  models.ManyToManyField(Tag, blank=True)
    posttype = models.CharField(max_length=10, choices=ARTICLE_TYPES, default='standard')
    video = models.URLField(blank=True, null=True)
    audio = models.FileField(upload_to='audios_uploaded',blank=True,validators=[validate_audio_extension])
    def __str__(self):
        return self.title    
    

              
class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    Name = models.CharField(max_length=100, verbose_name="الاسم")
    Email = models.EmailField()
    comment = models.TextField()

    @property
    def gravatar_url(self):
        email = self.Email.strip().lower().encode('utf-8')
        email_hash = hashlib.md5(email).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=identicon"

    def __str__(self):
        return f"{self.Name} - {self.Email}"







   
                         
                            
                            
  
                 



       


