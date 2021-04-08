from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django import forms
from . import util
import re
import secrets


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
    if request.method == "GET":
        empty_list=[]
        query=request.GET.get('q')
        queries=util.list_entries()
        for x in queries:
            entry_variable=util.get_entry(x)
            print(x)
            if query.lower() == x.lower():
                entry_variable=util.get_entry(x)
                return render(request, "encyclopedia/entry.html", {
                        "title_entry": query,
                        "entry_variable": entry_variable
                        })

            if query.lower() in x.lower():
                entry_variable=util.get_entry(x)
                empty_list.append(x)
                # continue

                return render(request, "encyclopedia/search.html", {
                        "results": empty_list,
                        "title_entry": x,
                        "entry_variable": entry_variable
                        })

        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

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
                    })
        else: 
            return render(request, "encyclopedia/create.html", {
            "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": CreateForm()
    })

def edit(request, title):
    if request.method == "POST":
        entries=util.list_entries()
        form=Edit(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            for entrie in entries:
                if title.lower()==entrie.lower():
                    return render(request, "encyclopedia/error.html")
            if title.lower() != entrie.lower():
                save=util.save_entry(title,text)
                return render(request, "encyclopedia/entry.html",{
                "title_entry": title,
                "entry_variable": text
                })

        else:
            text=util.get_entry(title)
            form=Edit(initial={'title': title, 'text':text})
            return render(request, "encyclopedia/edit.html", {
            'text_edit': form,
            })

    elif request.method == "GET":
        text=util.get_entry(title)
        form=Edit(initial={'title': title, 'text':text})
        return render(request, "encyclopedia/edit.html", {
        'text_edit': form,
        })
    

def random_page(request):
    entries=util.list_entries()
    title=secrets.choice(entries)
    title_entry=util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title_entry": title,
        "entry_variable": title_entry
    })