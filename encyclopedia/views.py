from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django import forms
from . import util
import re


class SearchForm(forms.Form):
    queries = forms.CharField(label="")

class CreateForm(forms.Form):
    title=forms.CharField(label="")
    text=forms.CharField(widget=forms.Textarea(attrs={'rows':3 , 'placeholder':"Content"}))

class Edit(forms.Form):
    title=forms.CharField(label="")
    text=forms.CharField(widget=forms.Textarea(attrs={'rows':3 , 'placeholder':"Content"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_variable=util.get_entry(title)
    if title is None:
        return render(request, "encyclopedia/error.html")
    else :
        return render(request, "encyclopedia/entry.html", {
            "title_entry": title,
            "entry_variable": entry_variable
        })

def search(request):
    if request.method=="POST":
        empty_list=[]
        posts=util.list_entries()
        query=request.POST.get('q') #sa ovim kreiramo varijablu "query" da uzmemo sta smo napisali u search
        form=SearchForm(request.POST)
        if form.is_valid():
            queries=form.cleaned_data["queries"]
        for post in posts:          # kreiramo for loop "post" zato sto za listu "posts" ne mozemo da definisemo lower slova, pa ih moramo svaki razdovik
            if query.lower() == post.lower():
                query=util.get_entry(query)
                return render(request, "encyclopedia/search.html", {
                "query": query
                })
            if query.lower() in post.lower():   # parcijalno trazenje odnosno ukoliko ukucamo samo dva slova treba da izadje predlozena pretraga koja se mathcuje
                empty_list.append(post)
                return render(request, "encyclopedia/search.html", {
                "results": empty_list,
                "post":post
            })
        else:
            return render(request, "encyclopedia/error.html")


def create(request):
    if request.method=="POST":
        entries=util.list_entries()
        form=CreateForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            for entrie in entries:
                if title.lower()==entrie.lower():
                    return render(request, "encyclopedia/error.html")
            if title.lower() != entrie.lower():
                entries.append(title)
                save=util.save_entry(title,text)
                return render(request, "encyclopedia/search.html",{
                "title": title,
                "text": text
                # "entries": entries                                    #'entries' je iz def index(request)
                    })
        else: 
            return render(request, "encyclopedia/create.html", {
            "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": CreateForm()
    })


#prikazivanje edit stranice
def edit(request, title):
        text=util.get_entry(title)
        editt=Edit(initial={'title': title, 'text':text})
        return render(request, "encyclopedia/edit.html", {
                'text_edit': editt
            })



def submit_edit(request,title):
    if request.method=="POST":
        title=util.get_entry(title)
        entries=util.list_entries()
        form=Edit(initial={'title': title, 'text':text})
        if form.is_valid(): 
            title=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            entries.append(title)
            
            # entries.append(title)
            # save=util.save_entry(title,text)
            return render(request, "encyclopedia/error.html", {
                'text_edit': form,
                'title':title
            } )


        else:
            return render(request, "encyclopedia/index.html", {
                            "entries": util.list_entries()
                        })
    



