from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import URL
from .forms import URLForm  # You'll need to create a form for URL submission
from django.utils import timezone


def home(request):
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data["original_url"]
            url_instance, created = URL.objects.get_or_create(original_url=original_url)
            if created:
                url_instance.save()
            short_url = request.build_absolute_uri(
                reverse("redirect", args=[url_instance.short_code])
            )
            return render(request, "home.html", {"form": form, "short_url": short_url})

    else:
        form = URLForm()

    return render(request, "home.html", {"form": form})


def redirect_url(request, short_code):
    url_instance = get_object_or_404(URL, short_code=short_code)

    if url_instance.expiration_date and timezone.now() > url_instance.expiration_date:
        return HttpResponse("This URL has expired", status=410)

    return HttpResponseRedirect(url_instance.original_url)
