from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect 
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views import View
# from .email import send_welcome_email
# from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from .forms import RegisterForm, LoginForm
from .models import Comment, Photo


# Create your views here.
def home(request):
    photos = Photo.objects.all()
    comments= Comment.objects.all()
    form = RegisterForm(request.POST)
    if request.method == 'POST':
       
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = RegisterRecipients(name = name,email =email)
            recipient.save()
            # send_welcome_email(name,email)
            str= 'sign up notification'
            subject = 'Welcome to instagram clone web app'
            sender = 'faisoabdirisak@gmail.com'
            

    #passing in the context vairables
            text_content = render_to_string('email/newsemail.txt',{"name": name})
            html_content = render_to_string('email/newsemail.html',{"name": name})

            # msg = EmailMultiAlternatives(subject,text_content,sender,[email])
            # msg.attach_alternative(html_content,'text/html')
            send_mail(str,subject,sender, [receiver],fail_silently=False)
            # msg.send()
            HttpResponseRedirect('auth/home')

    context ={'comments':comments, 'photos': photos, "form":form}
    return render(request, 'auth/home.html',context)


def viewPhoto(request,pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'auth/viewphoto.html', {'photo': photo})


def addPhoto(request):

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
      

        photo = Photo.objects.create(
                description=data['description'],
                image=image,
            )

        return redirect('users-home')
    context ={}
    return render(request, 'auth/addpost.html', context)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'auth/register.html'


    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='login')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})    

# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)




@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'auth/profile.html', {'user_form': user_form, 'profile_form': profile_form})




def search_results(request):
    if 'photo' in request.GET and request.GET["photo"]:
        search_term = request.GET.get("photo")
        searched_profiles = profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"photos": searched_profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'auth/search.html',{"message":message})
