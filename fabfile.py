# -*- coding: utf-8 -*-

import os
import time

from fabric.api import cd, env, local, run, task, put
from fabric.context_managers import prefix
from fabric.contrib import project
from fabric.contrib.console import prompt

HERE = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
# os.environ.setdefault("PRODUCTION_HOSTS", "")

# env = environ.Env()
# environ.Env.read_env()

# PRODUCTION_HOSTS = env('PRODUCTION_HOSTS', None)
# django.settings_module('config.settings.local')

env.hosts = ['root@10.7.7.22']

env.excludes = (
    "*.pyc", "*.db", ".DS_Store", ".coverage", ".git", ".hg", ".tox", ".idea/",
    'assets/', 'runtime/', 'node_modules', 'db.sqlite3', '*.ipynb')

env.remote_dir = '/home/apps/bankeys'
env.local_dir = '.'
env.database = 'bankeys'


@task
def venv():
    with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
        run('mkvirtualenv bankeys')

    with prefix('workon bankeys'), cd(env.remote_dir):
        run('pip install -r requirements_dev.txt')


@task
def conf():
    put('bankeys_server.conf', '/etc/supervisor/conf.d/')
    put('bankeys_chatbot.conf', '/etc/supervisor/conf.d/')


@task
def cron(action='check'):
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('python schedule.py %s' % action)


@task
def d2u():
    local('find . -name "*.html" -exec dos2unix {} \;')
    local('find . -name "*.py" -exec dos2unix {} \;')
    local('find . -name "*.css" -exec dos2unix {} \;')
    local('find . -name "*.js" -exec dos2unix {} \;')


@task
def cert():
    local('mkdir private')
    local('mkdir server')
    local('mkdir client')
    local('openssl genrsa -out private/ca-key.pem 1024')
    local('openssl req -new -subj $SUBJECT -out private/ca-req.csr -key private/ca-key.pem')
    local('openssl x509 -req -in private/ca-req.csr -out private/ca-cert.pem -signkey private/ca-key.pem -days 3650')
    local('openssl pkcs12 -export -clcerts -in private/ca-cert.pem -inkey private/ca-key.pem -out private/ca.p12')


@task
def urls():
    local('python manage.py show_urls')


@task
def runs(script=None):
    local('python manage.py runscript %s' % script)


@task
def test(task=''):
    local('''DJANGO_SETTINGS_MODULE=config.settings.tests python manage.py test %s''' % task)


@task
def static():
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('python manage.py collectstatic --dry-run -c --noinput')


@task
def rsync(static=None):
    local_dir = os.getcwd() + os.sep
    return project.rsync_project(remote_dir=env.remote_dir, local_dir=local_dir, exclude=env.excludes, delete=True)


@task
def pull():
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('git pull')
        run('pip install -r requirements.txt')

    migrate()

    run('/usr/bin/supervisorctl stop bankeys')
    run('/usr/bin/supervisorctl start bankeys')


@task
def push(static=None):
    rsync(static)


@task
def migrate():
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('''DJANGO_SETTINGS_MODULE='config.settings.local' python manage.py migrate''')


@task(alias='rr')
def restart():
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('/usr/bin/supervisorctl restart bankeys')


@task
def stop():
    run('/usr/bin/supervisorctl stop bankeys')


@task
def ur(static=None):
    rsync(static)
    restart()


@task
def um(static=None):
    rsync(static)
    migrate()


@task
def uu(static=None):
    rsync(static)
    migrate()
    restart()


@task
def reload():
    run('/root/python/bin/supervisorctl reload')
    run('/root/python/bin/supervisorctl restart all')


@task
def prod(port=8000):
    local('''MODE=prod gunicorn --worker-class=gevent config.wsgi:application -b 0.0.0.0:%s &''' % port)


@task
def build():
    local('''python -m compileall .''')


@task
def clean(migrate=None):
    clean_temp()
    clean_static()
    migrate and clean_migrate()


@task
def clean_temp(migrate=None):
    local('find . -name "*.sql" | xargs rm -rf')
    local('find . -name "*.pyc" | xargs rm -rf')
    local('find . -name "*.bak" | xargs rm -rf')
    local('find . -name "*.log" | xargs rm -rf')
    local('find . -name ".DS_Store" | xargs rm -rf')


@task
def clean_static(migrate=None):
    local('rm -rf assets/static/*')


@task
def clean_migrate():
    local('find . -name "migrations" | xargs rm -rf')


@task
def distclean():
    clean_temp()
    clean_static()
    clean_migrate()


@task
def mm():
    local('python manage.py makemigrations')
    local('python manage.py migrate')


@task
def pack(time=None):
    local('tar zcfv ./release.tgz '
          '--exclude=.git '
          '--exclude=.tox '
          '--exclude=.svn '
          '--exclude=.idea '
          '--exclude=*.tgz '
          '--exclude=*.pyc '
          '--exclude=.vagrant '
          '--exclude=tests '
          '--exclude=storage '
          '--exclude=database '
          '--exclude=.DS_Store '
          '--exclude=.phpintel '
          '--exclude=.template '
          '--exclude=db.sqlite3 '
          '--exclude=Vagrantfile .')


@task
def setup():
    local('python manage.py migrate --settings config.settings.prod')


@task
def dumpdata(remote=None):
    num = 1

    for fixture in env.fixtures:
        if not remote:
            local('python manage.py dumpdata {} > database/fixtures/00{}_{}.json'.format(fixture, num, fixture))
        else:
            with prefix('workon bankeys'), cd(env.remote_dir):
                run('python manage.py dumpdata {} > database/fixtures/00{}_{}.json'.format(fixture, num, fixture))

        num += 1


@task
def loaddata(remote=None):
    num = 1

    for fixture in env.fixtures:
        if not remote:
            local('python manage.py loaddata database/fixtures/00{}_{}.json'.format(num, fixture))
        else:
            with (prefix('workon bankeys'), cd(env.remote_dir)):
                run(
                    'DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py loaddata database/fixtures/00{}_{}.json'.format(
                        num, fixture))

        num += 1


@task
def restdb():
    local('dropdb {database}'.format(database=env.database))
    local('createdb {database} -O {database} -E UTF8 -e'.format(database=env.database))
    local('python manage.py migrate --noinput')
    # local('python manage.py loaddata database/fixtures/*.json')
    loaddata()


@task
def deploy():
    question = '你确实要这么做？'
    prompt(question, default=True)


@task
def backdb():
    backdir = 'database/backups/%s' % time.strftime('%Y%m%d%H', time.localtime())

    if not os.path.isdir(backdir):
        os.makedirs(backdir)

    for num, fixture in enumerate(env.fixtures):
        local('python manage.py dumpdata {} > {}/00{}_{}.json'.format(fixture, backdir, num, fixture))


@task
def syncdb(action='down'):
    if action == 'up':
        remote = False
        upload = True
    else:
        remote = True
        upload = False

    if remote:
        dumpdata(remote=remote)

    project.rsync_project(
        remote_dir=env.remote_dir + '/database/fixtures',
        local_dir='./database',
        exclude=env.excludes,
        upload=upload)

    # if action == 'up':
    #     with prefix('workon bankeys'), cd(env.remote_dir):
    #         run('python manage.py loaddata database/fixtures/*.json')
    # else:
    # restdb()


@task
def dbmigrate():
    # backup data
    run('manage.py dumpdata --format=json > db.json')

    # rsync files.
    local('rsync -ave ssh rsync -ave ssh root@101.200.136.70:/home/apps/bankeys /home/apps')

    # stop service
    local('/usr/bin/supervisorctl stop bankeys')

    # migrate db
    local('dropdb {database}'.format(database=env.database))
    local('createdb {database} -O {database} -E UTF8 -e'.format(database=env.database))

    local('python manage.py migrate --noinput')
    local('python manage.py loaddata db.json')

    # start service
    local('/usr/bin/supervisorctl start bankeys')


@task
def req():
    with prefix('workon bankeys'), cd(env.remote_dir):
        run('pip install -r requirements/prod.txt')


@task
def check():
    local('python manage.py check')


@task
def init():
    setup()
    loaddata()


@task
def start(name):
    local('git flow feature start %s' % name)

@task
def publish(name):
    local('git flow feature publish %s' % name)

@task
def finish(name):
    local('git flow feature finish %s' % name)