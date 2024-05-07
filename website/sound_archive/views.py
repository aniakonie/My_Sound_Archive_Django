from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def archive(request):

    return render(request, "archive.html")
