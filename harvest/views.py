from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from web.settings import BASE_DIR
from .forms import CreateJobForm
from .models import Account, Job


# Create your views here.
def index(request):
    jobs = Job.objects.all()
    return render(request, 'crawler/index.html', {'jobs': jobs})


def create(request):
    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('harvest:index')
        else:
            return HttpResponse('Error Validation: ' + str(form.errors))
    else:
        accounts = Account.objects.all()
        return render(request, 'crawler/form.html', {
            'accounts': accounts
        })


def show(request, job_id):
    job = Job.objects.filter(id=job_id).first()
    if not job:
        return HttpResponse('Error: Job Not Found', status='404')

    start = int(job.start_time.timestamp())
    end = int(job.end_time.timestamp())
    output_log = BASE_DIR / f'harvest/logs/{start}_{end}.log'

    with open(output_log, 'r') as file:
        latest_content = ''

        if request.headers.get('Accept') == 'application/json':
            if job.status == 'PROCESS':
                last_position = int(request.GET.get('last_position', 0))
                file.seek(last_position)
                latest_content = file.read()
                return JsonResponse({'latest_content': latest_content, 'pos': file.tell(), 'complete': False})
            else:
                return JsonResponse({'latest_content': '', 'pos': None, 'complete': True})
        else:
            lines = file.readlines()
            for line in lines[-20:]:
                latest_content += line

            return render(request, 'crawler/show.html', {
                'job': job,
                'pos': file.tell(),
                'latest_content': latest_content,
            })
