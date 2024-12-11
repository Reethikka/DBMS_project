# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now(),choice__isnull=False).distinct().order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    template_name="polls/detail.html"
    model=Question
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    template_name="polls/results.html"
    model=Question
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        question=self.object
        datapoints = [
            {"label": choice.choice_text, "y": choice.votes}
            for choice in question.choice_set.all()
        ]
        context['datapoints'] = datapoints
        return context

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render(request,"polls/detail.html",{"question":question,"error_message":"You didn't select a choice.",})
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
def about(request):
    return render(request,"polls/about.html")

def login_page(request):
    return render(request,"polls/login.html")

def register_page(request):
    return render(request,"polls/register.html")

def logout_page(request):
    return render(request,"polls/logout.html")
