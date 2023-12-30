from django.shortcuts import render

from dashboard.models import Sentiment


# Create your views here.
def index(request):
    sentiment = Sentiment.objects.all()
    total_negative = sum(entry.total for entry in sentiment if entry.label == 'negative')
    total_neutral = sum(entry.total for entry in sentiment if entry.label == 'neutral')
    total_positive = sum(entry.total for entry in sentiment if entry.label == 'positive')

    return render(request, 'index.html', {
        'total_negative': total_negative,
        'total_neutral': total_neutral,
        'total_positive': total_positive
    })


def tools(request):
    return render(request, 'tools.html')
