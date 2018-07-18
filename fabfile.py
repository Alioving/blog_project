from fabric.api import env, run
from fabric.operations import sudo


GIT_REPO = "https://github.com/Alioving/blog_project.git"

env.user = "huwenbin"
env.password = "qiancen828"

env.hosts = ['52qk8.me']


env.port = '22'


def deploy():
    source_folder = '/home/huwenbin/sites/52qk8.me/blog_project'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py makemigrations --merge &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('restart gunicorn-52qk8.me')
    sudo('service nginx reload')