import subprocess

from harvest.models import Job
from web.settings import BASE_DIR


def harvest_cron_job():
    process_job = Job.objects.filter(status='PROCESS').count()
    if process_job >= 4:
        return

    job = Job.objects.filter(status='WAITING').order_by('id').first()
    print(job)
    if not job:
        return

    job.status = 'PROCESS'
    job.save()

    start = int(job.start_time.timestamp())
    end = int(job.end_time.timestamp())
    command = (f'npx --yes tweet-harvest@latest -o "{start}_{end}.csv" -s "{job.keyword} '
               f'lang:id since_time:{start} until_time:{end}" -l {job.limit} --token '
               f'"{job.account.auth_token}"')

    _output_log = BASE_DIR / f'harvest/logs/{start}_{end}.log'
    with open(_output_log, 'w') as output_log:
        process = subprocess.Popen(command, shell=True, stdout=output_log, stderr=output_log)
        process.communicate()

    job.status = 'DONE'
    job.save()
