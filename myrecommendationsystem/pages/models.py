from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

class Book(models.Model):
	name   	= models.CharField(blank=False,max_length=100)
	author = models.CharField(blank=False,max_length=100,default="Mr.Rukesh Shrestha")
	descriptions  = models.TextField(null=False,default="Four teenagers in detention discover an old video game console with a game they’ve never heard of. When they decide to play, they are immediately sucked into the jungle world of Jumanji in the bodies of their avatars (Dwayne Johnson, Jack Black, Kevin Hart, and Karen Gillan). They’ll have to complete the adventure of their lives filled with fun, thrills and danger or be stuck in the game forever!",max_length=500)
	genre = models.CharField(max_length=50,default="Biography and Memoirs")
	image = models.ImageField(upload_to='')
	num_visits = models.IntegerField(default=0)
	last_visits = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('detailhome',args=[str(self.id)])


		


class Myrating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE)
	places 	= models.ForeignKey(Book,on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

	def __str__(self):
		return str(self.user)


# Create your models here.

class Contactus(models.Model):
    name = models.CharField(max_length=50,null=True,blank=False)
    emails = models.EmailField(max_length=200,null=True,blank=False)
    subjects = models.CharField(max_length=100,null=True,blank=False)
    descriptions = models.TextField(max_length=400,null=True,blank=False)



class Aboutus(models.Model):
	descriptions_page  = models.TextField(null=False,default="This is the amazing  book. You must read it.")
	descriptions_person  = models.TextField(null=False,default="People vary in terms of their physical appearance and personalities, and the words that are used to describe them are just as varied. Some words are better suited to describing the physical appearance of someone, some are best used to describe the person’s style, and others are ideal for describing the person’s character traits.")
	footerdetail = models.TextField(null=False,default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
	quotes = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
	facebook = models.URLField(max_length=500,default="https://www.facebook.com/rukesh.shrestha.94651/")
	linkedin = models.URLField(max_length=500,default="https://www.linkedin.com/in/rukesh-shrestha-07914b1a3/")
	instragram = models.URLField(max_length=500,default="https://www.instagram.com/____rukesh____/")
	image = models.ImageField(upload_to='')









	
	