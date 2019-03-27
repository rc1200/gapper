from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import  FormView
from .models import Carousel
from .forms import ContactMeForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .utilities import def_1_val, def_list, p1, Person



from django.http import JsonResponse

def myAjax(request, ticker):
    j1 = 'test J1'
    j2 = 'test J2'
    j3 = 'test J3 xx'
    # test = [{"id": 1}, {"id": 2}, {"id": 3}]

    a1 = Person(ticker, 55)
    print(p1)
    print(p1.name)
    print(p1.age)
    print(p1.jsonReturn())
    test = a1.jsonReturn()
    # test = {"id": 1}
    # data = request.GET.get['value']

    print('name................', request.method)
    print('data................', request)
    print('data................', ticker)
    sampleJson = 	{'color': "red"}
        # ,{'color': "green"}

    return JsonResponse(test, safe=False)
    # stuff_for_frontend = {'def_1_val': def_1_val, 'def_list': def_list, 'p1': p1}
    # return render(request, "portfolio/index3.html", stuff_for_frontend)




# use content mixin instead since we are expanding the base and just need to call the template vs having to explictly
# call the dictionary
class GetContentMixin(object):
    mixin_model = Carousel

    def get_context_data(self, **kwargs):
        Carousel.objects.all().update(is_active=None)
        Carousel.objects.filter(carousel_num=0).update(is_active='active')
        context = super(GetContentMixin, self).get_context_data(**kwargs)
        context['carousel_model'] = self.mixin_model.objects.all().order_by('carousel_num')
        return context


# since the template extends the base which requires a form, we need to create a mixin to define the form
# so the form data can be passed since we hid them and only display them when they try contact them because it is a modal form
class FormMixin(forms.Form):
    form_class = ContactMeForm


# class instead to speed up production
# NOTE: using the mixin for the form and content
class IndexView(GetContentMixin, FormMixin, FormView):
    template_name = "portfolio/index2.html" # define the template to use


class GalleryView(GetContentMixin, FormMixin, FormView):
    template_name = "portfolio/gallery.html" # define the template to use


# Function Based views

def thankyou(request):
    form = ContactMeForm(request.POST or None)

    if form.is_valid():  # ensure the form has clean data passed
        save_it = form.save(commit=False)

        # save_it.save() # since we are not storing this in the DB no need to save

        # send email
        subject = 'Message from Client'
        message = form.cleaned_data['message']
        from_email = settings.EMAIL_HOST_USER
        to_list = [save_it.senderEmail, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=False,)

        return HttpResponseRedirect('/', {'form': ContactMeForm()})


def index(request):
    return render(request, "portfolio/index.html", {'form': ContactMeForm()})


def index2(request):
    # ensure that the only active record is the one where carousel_num = 1
    Carousel.objects.all().update(is_active=None)
    Carousel.objects.filter(carousel_num=0).update(is_active='active')
    carousel_model = Carousel.objects.all().order_by('carousel_num')
    stuff_for_frontend = {'carousel_model': carousel_model, 'form': ContactMeForm()}
    return render(request, "portfolio/index2.html", stuff_for_frontend)
    # return render(request, "portfolio/index2.html",  {'form': ContactMeForm()})


def gallery(request):
    return render(request, "portfolio/gallery.html", {'form': ContactMeForm()})

def index3(request):
    stuff_for_frontend = {'def_1_val': def_1_val, 'def_list': def_list, 'p1': p1}
    return render(request, "portfolio/index3.html", stuff_for_frontend)
    # return render(request, "portfolio/index3.html")
