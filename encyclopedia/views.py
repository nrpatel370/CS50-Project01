from django.shortcuts import render, redirect
from django.contrib import messages
import random

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(req, title):
    content = util.get_entry(title)
    
    if not content:
        return render(req, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    
   
    return render(req, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(req):
    query = req.GET.get("q", "").strip()
    
    if query:
        entry_content = util.get_entry(query)
        if entry_content:
            return redirect("title", title=query)
        
        entries = util.list_entries()
        results = [entry for entry in entries if query.lower() in entry.lower()]

        return render(req, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })
    else:
        return redirect("index")
    
def new_page(req):
    if req.method == "POST":
        title = req.POST.get("title").strip()
        content = req.POST.get("content").strip()

        if util.get_entry(title):
            messages.error(req, f"An entry with the title '{title}' already exists.")
            return redirect("newpage")

        util.save_entry(title, content)

        return redirect("title", title=title)

    return render(req, "encyclopedia/create_new_page.html")

def edit(req, title):
    content = util.get_entry(title)
    if content is None:
        return render(req, "encyclopedia/error.html", {"message": "Page not found."})
    
    if(req.method == "POST"):
        content = req.POST.get("content").strip()
        util.save_entry(title, content)
        return redirect("title", title=title)
    
    return render(req, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(req):
    title_rand = random.choice(util.list_entries())
    return redirect("title", title=title_rand)