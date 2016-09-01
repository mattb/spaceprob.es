from __future__ import print_function
import sys
from fabric.api import lcd, local, abort, prompt
from fabric.contrib.console import confirm
from secrets import GIT_REPO, LOCAL_TEMP_DIR, DEV_USER, DEV_URL, DEV_PATH, STAGING

DEPLOY_DIR_NAME = 'spaceprobes_deploy'  # extra dir inside of LOCAL_TEMP_DIR just in case conflicts

def deploy():
    """ this method checks out the repo into a local temp directory,
        builds the jekyll _site folder there, and then rsyncs _site folder to remote server """
    print("checking out codebase...")

    try: 
        if sys.argv[2] == 'production':
            checkout_codebase('production', 'master')
        else: 
            branch = prompt("What branch should we deploy?")
            checkout_codebase('staging', branch)

    except IndexError:
        print("""
                Hello! Things have changed a bit. 

                Please say:

                fab deploy staging 

                or

                fab deploy production
                """)

def production():
    print("deploying to production")
    with lcd("%s%s/%s/" % (LOCAL_TEMP_DIR, DEPLOY_DIR_NAME, 'spaceprob.es')):
        local("jekyll _2.5.2_ build")
        rsync_call = "rsync -r -vc -e ssh --exclude .git --exclude venv _site/ %s@%s:%s" % (DEV_USER, DEV_URL,DEV_PATH)
        local(rsync_call)

def staging():
    print("deploying to staging")
    print("%s%s/%s/" % (LOCAL_TEMP_DIR, DEPLOY_DIR_NAME, 'spaceprob.es'))
    with lcd("%s%s/%s/" % (LOCAL_TEMP_DIR, DEPLOY_DIR_NAME, 'spaceprob.es')):
        local("jekyll _2.5.2_ build")
        rsync_call = "rsync -r -vc -e ssh --exclude .git --exclude venv _site/ %s@%s:%s" % (STAGING['DEV_USER'], STAGING['DEV_URL'], STAGING['DEV_PATH'])
        local(rsync_call)

def checkout_codebase(server, branch):
    """ remove any old checked out repo and grab the latest
        build the _site directory and rsync it """
    with lcd(LOCAL_TEMP_DIR):
        local('rm -rf %s' % DEPLOY_DIR_NAME)  #
        local('mkdir %s' % DEPLOY_DIR_NAME)  # this extra directory makes it a lil safer futzing around

    with lcd("%s%s/" % (LOCAL_TEMP_DIR, DEPLOY_DIR_NAME)):
        print("cloning into %s%s/" % (LOCAL_TEMP_DIR, DEPLOY_DIR_NAME))
        clone_cmd = "git clone -b %s %s" % (branch, GIT_REPO)
        print(clone_cmd)
        local(clone_cmd)

