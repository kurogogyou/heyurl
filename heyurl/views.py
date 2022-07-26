from django.shortcuts import render
from django.http import HttpResponse
import string, random
from django.utils import timezone
from .models import Url
from .forms import UrlForm
from django.core.validators import URLValidator
import re


def index(request):
    urls = Url.objects.order_by('-created_at')
    form = UrlForm()
    context = {'urls': urls, 'form': form}
    return render(request, 'heyurl/index.html', context)

def store(request):
    # FIXME: Insert a new URL object into storage
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            o_url = form.cleaned_data['original_url']
            val = URLValidator()
            try:
                val(o_url)
            except:
                return HttpResponse("Invalid input.")
            
            base = string.ascii_letters + string.digits
            s_url = ''
            while(s_url == '' or Url.objects.filter(short_url=s_url)):
                s_url=''.join(random.choice(base) for i in range(5))
            u = Url(short_url=s_url, original_url = o_url, created_at = timezone.now(), updated_at = timezone.now())
            u.save()

            return HttpResponse("Storing a new URL object into storage. New url is: {}".format(u))
    else:
        return HttpResponse("Invalid input.")

def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    print(request.headers)
    browser = request.headers['Sec-Ch-Ua']
    platform = request.headers['Sec-Ch-Ua-Platform']
    print(browser + ' ' + platform)
    return HttpResponse("You're looking at url %s" % short_url)
