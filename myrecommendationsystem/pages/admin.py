from django.contrib import admin
from django.db import models
from .models import Contactus,Book,Myrating,Aboutus


# Register your models here.

class CustomBook(admin.ModelAdmin):
    list_display=('name','author','genre',)


class CustomContact(admin.ModelAdmin):
    list_display=('name','emails','subjects','descriptions')


class CustomRating(admin.ModelAdmin):
    list_display=('user','places','rating')

class CustomAbout(admin.ModelAdmin):
    list_display=('quotes','facebook','linkedin','instragram','descriptions_page','descriptions_person',)

admin.site.register(Contactus,CustomContact),
admin.site.register(Book,CustomBook),
admin.site.register(Myrating,CustomRating),
admin.site.register(Aboutus,CustomAbout)
