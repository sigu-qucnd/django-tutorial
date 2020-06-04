from django.http import HttpResponse,HttpResponseRedirect
# from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choise, Question
from django.views import generic  

# Create your views here.

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     content = {
#         'latest_question_list': latest_question_list,
#     }
    
#     # return HttpResponse(template.render(content,request))
#     return render(request, 'polls/index.html', content)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list' 

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


# def detail(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request, 'polls/details.html', {'question':question})

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/result.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

def vote(request, question_id):  
    question = get_object_or_404(Question, pk=question_id)  
    try:  
        selected_choise = question.choise_set.get(pk=request.POST['choise'])  
    except (KeyError, Choise.DoesNotExist):  
        # Redisplay the question voting form.  
        return render(request, 'polls/detail.html', {  
            'question': question,  
            'error_message': "You didn't select a choice.",  
        })  
    else:  
        selected_choise.votes += 1  
        selected_choise.save()  
        # Always return an HttpResponseRedirect after successfully dealing  
        # with POST data. This prevents data from being posted twice if a  
        # user hits the Back button.  
        return HttpResponseRedirect(reverse('results', args=(question.id,)))