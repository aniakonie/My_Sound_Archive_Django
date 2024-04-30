from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def create_archive(request):
    if request.method == "POST":
        if request.form["create_library"] == "Changed my mind":
            pass
            #return redirect to archive
        else:
            create_library()
            #return redirect to archive
    return render(request, "create_archive.html")



def create_library():
    print('create library')
    pass