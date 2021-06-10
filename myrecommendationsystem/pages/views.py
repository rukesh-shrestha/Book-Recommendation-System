from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm,ContactUsForm
from django.db.models import Q
from django.contrib import messages
from .models import Contactus,Book,Myrating,Aboutus
import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from ast import literal_eval as make_tuple
from myrecommendationsystem.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json
from datetime import datetime
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import sigmoid_kernel
from django.views.generic import DetailView



# Create your views here.
def home(request):
    context = Book.objects.all()
    book = Book.objects.all().order_by('-num_visits')[0:3]
    recent = Book.objects.all().order_by('-last_visits')[0:3] 
    paginator = Paginator(context, 2)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
           
        post_list = paginator.page(1)
    except EmptyPage:
        
        post_list = paginator.page(paginator.num_pages)
    query = request.GET.get('q')
    if query:

        contexts = Book.objects.filter(Q(name__icontains=query) | Q(genre__icontains=query) | Q(author__icontains=query)).distinct()
        return render(request, 'home.html', {'context': contexts, 'query':query})

    return render(request,"home.html",{'context': post_list,'page': page,'book':book,'recent':recent})



def rating(request, place_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    book = get_object_or_404(Book, id=place_id)
    book.num_visits +=1
    book.last_visits = datetime.now()
    book.save()
   

    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Myrating()
        ratingObject.user = request.user
        ratingObject.places = book
        ratingObject.rating = rate
        ratingObject.save()

        return redirect("home")
    return render(request, 'rating.html', {'place': book})

def about(request):
    context = Aboutus.objects.all()
    return render(request,"aboutus.html",{'context':context})

def contact(request):
    
    my_form = ContactUsForm(request.GET)
    if request.method=="POST":
        my_form = ContactUsForm(request.POST)
        if my_form.is_valid():
            Contactus.objects.create(**my_form.cleaned_data)
            name = request.POST.get('name')
            email = request.POST.get('emails')
            subject = request.POST.get('subjects')
            message = request.POST.get('descriptions')
            recepient = ("asd@yopmail.com",)
            template = render_to_string('email_template.html',{'name':name,'description':message,'mail':email})
            email=EmailMessage(
                subject,
                template,
                EMAIL_HOST_USER,
                recepient

            )

            email.fail_silently=False
            if email!=None:

                email.send()

            
            return redirect("contact")


    context = {"form":my_form}
    return render(request,"contactus.html",context)

def register(request):
    form = UserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully.')
            return redirect('login')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")

            return render(request,"register.html",context)
   
    return render(request,"register.html",context)

def loginuser(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"username or password is incorrect.")
    context = {}
    return render(request,"login.html",context)

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def recommend(request):
    context = Book.objects.all()
    user_id = request.user.id
    users = request.user
    
    contexts = {
        'message':"Please rate the book first."

    }
    
    
    objectss = Myrating.objects.filter(user=users)
    if len(objectss) != 0:
        
        url = "http://127.0.0.1:5000/recommend"
        payload = {'user_id':user_id}
        headers = {
            'content-type': "multipart/form-data",
            'cache-control': "no-cache",

        }

        responses = requests.request("POST",url,data=payload)

        response = json.loads(responses.text)
        respnses_tuple = make_tuple(response)
        context = list()

        for user_id in respnses_tuple:
            try:
                recommended = Book.objects.get(id=user_id)
                context.append(recommended)
            except:
                pass


        
        return render(request,"recommendcollaborative.html",{'context': context})
    else:
        return render(request,"recommendcollaborative.html",contexts)
  

@login_required(login_url='login')
def recommended(request):
    headers = {
            'content-type': "multipart/form-data",
            'cache-control': "no-cache",

            }
            
    query = request.GET.get('q')
    
    if query:
        url = "http://127.0.0.1:5000/recommending"
        payload = {'query':query}
        responses = requests.request("POST",url,data=payload)
        
        try:
            json.loads(responses.text)
            response = json.loads(responses.text)
            print(response)
            value = tuple(response.keys())
            context = list()
            
            for x in value:
                try:
                    recommend = Book.objects.get(id=x)
                    context.append(recommend)
                except:
                    pass
        
            
            return render(request, 'recommendcontent.html', {'context': context})
        except:
            return render(request,"recommendcontent.html",{'name':'Please enter the correct name of the book.'})
            
    else:
        
        
        return render(request,"recommendcontent.html",{'name':'Please search the book name from the above search bar.'})

    return render(request,"recommendcontent.html",{})


def detail(request):
    context = Aboutus.objects.all()
    return render(request,"detail.html",{'context':context})





class Detail(DetailView):
    model = Book   
    template_name = 'detailhome.html'

def Footer(request):
    footer = Aboutus.objects.all()
    return render(request,"footer.html",{'social':footer})