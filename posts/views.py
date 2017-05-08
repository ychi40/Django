from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from .models import Incident

from .forms import IncidentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
#from django.contrib.auth.decorators import  login_required


#@login_required(login_url='/login/')
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = IncidentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
             "form": form,

    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None): #retrieve
    instance = get_object_or_404(Incident, id=id) #filter by attribute
    context = {
        "title": instance.crime,
        "instance": instance,
    }
    return render(request, "post_details.html", context)


def post_list(request): #list items
    queryset_list = Incident.objects.all()
    if request.user.is_staff or request.user.is_superuser:
         queryset_list = Incident.objects.all()
         # .order_by("-timestamp")
    query = request.GET.get("q")
    if query :
        queryset_list = queryset_list.filter(
            Q(crime__icontains=query)|
            Q(crimedesc__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 5) # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
    "object_list": queryset,
    "title": "List",
    "page_request_var" : page_request_var
    }

    return render(request, "post_list.html", context)
    #return HttpResponse("<h1>list</h1>")







def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Incident, id=id) #filter by attribute
    form = IncidentForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("crime"))
        instance.save()
        #message success
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.crime,
        "instance": instance,
        "form":form,
    }
    return render(request, "post_form.html", context)



def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Incident, id=id)  # filter by attribute
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")

