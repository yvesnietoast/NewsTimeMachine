from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from pages import views
from news.models import newsBit
from news.tasks import request_summary
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from ninja.security import django_auth

from chat.api import router as chat_router
api = NinjaAPI()
api.add_router("/chat/", chat_router, auth=django_auth)


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/summarize/{newsbit_id}")
def summarize_newsbit(request, newsbit_id: int):
    newsbit = get_object_or_404(newsBit, id=newsbit_id)
    print(newsbit.transcript)
    
    if not newsbit.summary:
        request_summary.delay(newsbit_id)  # Using Celery to handle the summarization asynchronously
        return {"message": "Summary request has been queued"}
    
    return {"title": newsbit.title, "summary": newsbit.summary}


urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("latest/",views.latest),
    path('chat/', TemplateView.as_view(template_name="chat/chat.html")),
    
]