from __future__ import with_statement
import os
from fabric.api import *
import sys
import time


env['base_directory'] = os.path.dirname(os.path.abspath(__file__))
env['deployment_branch'] = 'master'

packages = {
    'pip':[
        'python-dateutil==1.5',
        'feedparser==5.1',
        'raven==1.4.6',
        'pyyaml',
        '-U distribute',
        'nltk',
        'tablib==0.9.11',
        'chardet',
        'numpy',
        'google-api-python-client==1.0c2'
    ],
    'apt-get':[
        'python-memcache',
        'python-dev'
    ]
}

def _update_deployment_timestamp():
    import fileinput
    for line in fileinput.input('settings.py', inplace=1):
        if line.startswith('DEPLOYMENT_TIMESTAMP'):
            print 'DEPLOYMENT_TIMESTAMP = %i \n' % int(time.time()),
        else:
            print line,

def dev():
    env.hosts = ['root@me.dev']
    env['deployment_branch'] = 'dev'

def stage():
    pass

def demo():
    env.hosts = ['root@me.clienttest.web.01']
    env['deployment_branch'] = 'master'

def prod():
    env.hosts = ['root@me.prod.wwp.01']

def git():
    _update_deployment_timestamp()
    for dir in ['metalayercore', 'thedashboard', '.']: #'compressor', 'chargifyapi',
        with settings(warn_only=True):
            local('cd %s/%s && git add --all' % (env['base_directory'], dir))
            local('cd %s/%s && git commit' % (env['base_direcotry'], dir))
            local('cd %s/%s && git push' % (env['base_directory'], dir))

def git_tag(tag, message=None):
    for dir in ['metalayercore', 'thedashboard', '.']: #'compressor', 'chargifyapi',
        local('cd %s/%s && git tag -a %s -m "%s"' % (env['base_directory'], dir, tag, message or tag))
        local('cd %s/%s && git push --tags' % (env['base_directory'], dir))

def create_story_branch(story_name):
    for dir in ['metalayercore', 'thedashboard', '.']:
        local('cd %s/%s && git checkout -b %s' % (env['base_directory'], dir, story_name))

def commit_story_branch():
    for dir in ['metalayercore', 'thedashboard', '.']:
        local('cd %s/%s && git add --all' % (env['base_directory'], dir))
        with settings(warn_only=True):
            local('cd %s/%s && git commit' % (env['base_directory'], dir))

def rebase_story_branch(base='dev'):
    for dir in ['metalayercore', 'thedashboard', '.']:
        local('cd %s/%s && git fetch' % (env['base_directory'], dir))
        local('cd %s/%s && git rebase origin/%s' % (env['base_directory'], dir, base))

def squash_and_close_story_branch(story_name, base='dev'):
    _update_deployment_timestamp()
    for dir in ['metalayercore', 'thedashboard', '.']:
        if dir == '.':
            local('cd %s/%s && git add --all' % (env['base_directory'], dir))
            with settings(warn_only=True):
                local('cd %s/%s && git commit -m "final merge of story branch %s"' % (env['base_directory'], dir, story_name))
        local('cd %s/%s && git rebase -i %s' % (env['base_directory'], dir, base))
        local('cd %s/%s && git checkout %s' % (env['base_directory'], dir, base))
        local('cd %s/%s && git merge %s' % (env['base_directory'], dir, story_name))
        local('cd %s/%s && git push origin %s' % (env['base_directory'], dir, base))

def fetchall(branch='master'):
    for dir in ['metalayercore', 'thedashboard',  '.']: #'compressor=develop', 'chargifyapi',
        with settings(warn_only=True):
            this_branch = dir.split('=')[1] if '=' in dir else branch
            local('cd %s/%s && git fetch && git merge origin/%s' % (env['base_directory'], dir.split('=')[0], this_branch))

def deploy(install_packages=False):
    if install_packages:
        for package in packages['apt-get']:
            run('apt-get install %s' % package)
        for package in packages['pip']:
            run('pip install %s' % package)

    with cd('/usr/local/metaLayer-enterprise/enterprise'):
        run("git fetch")
        run("git merge origin/%s" % env['deployment_branch'])
        run("git submodule init && git submodule update")
        run("git status")
    with settings(warn_only=True):
        run("service apache2 restart")
        run("service nginx restart")

def recycle():
    run('service apache2 restart')

def runcommand():
    #methd used for ad hoc commands that need to be run
    #run('pip uninstall django_compressor')
    #run('mkdir /var/log/metalayer')
    #run('touch /var/log/metalayer/errors.log')
    #run('chmod a+rw /var/log/metalayer/errors.log')
    #run('ln -s /usr/local/metaLayer-dashboard/dashboard/imaging/CACHE /usr/local/metaLayer-dashboard/dashboard/static/CACHE/images')
    #run('rm /usr/local/metaLayer-dashboard/dashboard/static/CACHE/images')
    """
    with cd('/usr/local/metaLayer-dashboard/dashboard'):
        with settings(warn_only=True):
            run('rm actions -r')
            run('rm aggregator -r')
            run('rm dashboards -r')
            run('rm datapoints -r')
            run('rm outputs -r')
            run('rm visualizations -r')
            run('rm search -r')
    """
    #run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/css /usr/local/metaLayer-enterprise/enterprise/static/css/thedashboard')
    #run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/images /usr/local/metaLayer-enterprise/enterprise/static/images/thedashboard')
    #run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/html /usr/local/metaLayer-enterprise/enterprise/static/html/thedashboard')
    #run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/js /usr/local/metaLayer-enterprise/enterprise/static/js/thedashboard')
    #run('mkdir /usr/local/metaLayer-enterprise/enterprise/static/CACHE')
    #run('rm /usr/local/metaLayer-enterprise/enterprise/static/CACHE/images')
    #run('ln -s /usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE /usr/local/metaLayer-enterprise/enterprise/static/CACHE/images')
    #run('chmod a+rw /usr/local/metaLayer-enterprise/enterprise/static/CACHE')
    #run('chmod a+rw /usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE')
    #run('service apache2 restart')
    #put('~/Documents/metaLayer/DraftFBC/Data/20120516/processing/processing.tar.gz', '/tmp')
    pass

def serversetup(server_ip=None, git_managed=False):
    apachesetup()
    codebasesetup(server_ip, git_managed)
    solrsetup()

def apachesetup():
    ####################################################################################################################
    # APACHE2 SETUP
    ####################################################################################################################
    run('apt-get update')
    run('apt-get install apache2 libapache2-mod-wsgi')
    run('rm /etc/apache2/sites-enabled/*')
    run('a2enmod headers')
    run('service apache2 restart')
    put('%s/assets/apache2/vhost' % os.path.dirname(__file__), '/etc/apache2/sites-enabled/metaLayer-enterprise', mode=0755)

def codebasesetup(server_ip=None, git_managed=False):
    ####################################################################################################################
    # CODEBASE SETUP
    ####################################################################################################################
    run('apt-get update')
    run('apt-get install git-core mercurial mongodb python-cairo python-rsvg python-pip curl')
    run('pip install --upgrade pip')
    for package in packages['apt-get']:
        run('apt-get install %s' % package)
    for package in packages['pip']:
        run('pip install %s' % package)
    with settings(warn_only=True):
        system_packages = run('pip freeze -l').splitlines()
        system_packages = [p.split('==')[0] for p in system_packages]
        if 'Django' not in system_packages:
            run('pip install hg+https://bitbucket.org/wkornewald/django-nonrel')
        if 'djangotoolbox' not in system_packages:
            run('pip install hg+https://bitbucket.org/wkornewald/djangotoolbox')
        if 'django-mongodb-engine' not in system_packages:
            run('pip install git+git://github.com/django-nonrel/mongodb-engine')
    with settings(warn_only=True):
        run('ssh-keygen -t rsa')
    run('more ~/.ssh/id_rsa.pub')
    run('read -p "Press ENTER once ssh key is installed"')
    with settings(warn_only=True):
        run('rm /tmp/metaLayer-enterprise -r')
        run('rm /usr/local/metaLayer-enterprise -r')
        run('mkdir /tmp/metaLayer-enterprise')
        run('mkdir /usr/local/metaLayer-enterprise')
        run('mkdir /usr/local/metaLayer-enterprise/enterprise')
    put('%s/assets/apache2/wsgi' % os.path.dirname(__file__), '/usr/local/metaLayer-enterprise/enterprise.wsgi', mode=0755)
    put('%s/assets/users/create_users' % os.path.dirname(__file__), '/tmp/create_users', mode=0755)

    with settings(warn_only=True):
        run('rm /usr/share/nltk_data -r')
    run('mkdir /usr/share/nltk_data')
    run("python -c \"import nltk;nltk.download('brown', download_dir='/usr/share/nltk_data')\"")

    if git_managed:
        run('git clone git@github.com:metaLayer/metaLayer-enterprise.git /usr/local/metaLayer-enterprise/enterprise')
        with cd('/usr/local/metaLayer-enterprise/enterprise'):
            run('git checkout master')
            run('git submodule init && git submodule update')
        run('cd /usr/local/metaLayer-enterprise/enterprise && python manage.py syncdb')
        with cd('/usr/local/metaLayer-enterprise/enterprise'):
            run('more /tmp/create_users | python manage.py shell')
        run('rm /tmp/create_users')
    else:
        run('git clone git@github.com:metaLayer/metaLayer-enterprise.git /tmp/metaLayer-enterprise')
        with cd('/tmp/metaLayer-enterprise'):
            run('git checkout master')
            run('git submodule init && git submodule update')
        run('cp /tmp/metaLayer-enterprise/* /usr/local/metaLayer-enterprise/enterprise/ -r')
        run('sed -i \'s/ENTER_SITE_HOST/%s/g\' /usr/local/metaLayer-enterprise/enterprise/settings.py' % server_ip)
        run('cd /usr/local/metaLayer-enterprise/enterprise && python manage.py syncdb')
        run('python -c "import compileall; compileall.compile_dir(\'/usr/local/metaLayer-enterprise/enterprise\', force=1);"')
        #run('find /usr/local/metaLayer-enterprise/enterprise -name "*.py" -delete')
        with cd('/usr/local/metaLayer-enterprise/enterprise'):
            run('more /tmp/create_users | python manage.pyc shell')
        run('rm /tmp/create_users')

    run('rm /tmp/metaLayer-enterprise -r')
    run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/css /usr/local/metaLayer-enterprise/enterprise/static/css/thedashboard')
    run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/images /usr/local/metaLayer-enterprise/enterprise/static/images/thedashboard')
    run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/html /usr/local/metaLayer-enterprise/enterprise/static/html/thedashboard')
    run('ln -s /usr/local/metaLayer-enterprise/enterprise/thedashboard/static/js /usr/local/metaLayer-enterprise/enterprise/static/js/thedashboard')
    run('mkdir /usr/local/metaLayer-enterprise/enterprise/static/CACHE')
    run('ln -s /usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE /usr/local/metaLayer-enterprise/enterprise/static/CACHE/images')
    run('chmod a+rw /usr/local/metaLayer-enterprise/enterprise/static/CACHE')
    run('chmod a+rw /usr/local/metaLayer-enterprise/enterprise/metalayercore/imaging/CACHE')
    run('service apache2 restart')
    run('curl http://localhost')

def solrsetup():
    ####################################################################################################################
    # SOLR SETUP
    ####################################################################################################################
    run('apt-get update')
    run('apt-get install tomcat6')
    with settings(warn_only=True):
        run('rm /var/solr -r')
        run('rm /etc/tomcat6/Catalina/localhost/solr.xml')
        #run('rm /tmp/solr -r')
    #run('mkdir /tmp/solr')
    run('mkdir /var/solr')
    #    with cd('/tmp/solr'):
    #        run('wget http://mirror.cc.columbia.edu/pub/software/apache/lucene/solr/3.6.1/apache-solr-3.6.1.tgz')
    #        run('tar xzf apache-solr-3.6.1.tgz')
    #        run('cp apache-solr-3.6.1/dist/apache-solr-3.6.1.war /var/solr/solr.war')
    #        run('cp apache-solr-3.6.1/example/solr/* /var/solr -r')
    #    run('rm /var/solr/conf/schema.xml')
    put('%s/assets/solr/solr_3_4_0/*' % os.path.dirname(__file__), '/var/solr/', mode=0755)
    run('chown -R tomcat6 /var/solr/')
    run("echo -e '<Context docBase=\"/var/solr/solr.war\" debug=\"0\" privileged=\"true\" allowLinking=\"true\" crossContext=\"true\">\n<Environment name=\"solr/home\" type=\"java.lang.String\" value=\"/var/solr\" override=\"true\" />\n</Context>' | tee -a /etc/tomcat6/Catalina/localhost/solr.xml")
    run("echo 'TOMCAT6_SECURITY=no' | sudo tee -a /etc/default/tomcat6")
    run('sed -i \'s/set -e/set -e\\nJAVA_OPTS="$JAVA_OPTS -Dsolr.home=\/var\/solr"/g\' /etc/init.d/tomcat6')
    run('service tomcat6 restart')
    run('curl http://localhost:8080/solr/select/?q=*')
    run('read -p "PLEASE CHECK THE SOLR OUTPUT ABOVE"')

