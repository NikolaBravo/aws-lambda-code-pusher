# -*- coding: utf-8 -*-
"""
Main Github Pusher Code.
Copyright 2017-infinity @Gergely Brautigam
"""
import os
import git
import boto3

# First create a Github instance:
TOKEN = os.environ.get("GITHUB_TOKEN")
S3_CLIENT = boto3.client('s3')
BUCKET = os.environ.get("BUCKET")

def donwload_built_artifacts():
    """
    Downloads the blog's built source from the bucket.
    """
    s3_client = boto3.resource('s3')

    bucket = s3_client.Bucket(name=BUCKET)
    for obj in bucket.objects.filter(Prefix='datamunger/'):
        print('{0}.{1}'.format(bucket.name, obj.key))
        path, _ = os.path.split(obj.key)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        s3_client.meta.client.download_file(bucket.name, obj.key, obj.key)


def handler(event, context):
    """
    Lambda handler which gets called when a lambda executes.
    """

    # Pull S3 artifact here and apply it to blog folder
    donwload_built_artifacts()

    """
    git init
    git remote add origin PATH/TO/REPO
    git fetch
    git reset origin/master
    git checkout master
    git commit -a
    git push
    """
    source = git.Repo.init(path=os.path.join(os.getcwd(), 'blog'))
    origin = source.create_remote('origin', 'https://%s@github.com/Skarlso/blogsource.git' % TOKEN)
    origin.fetch()
    source.head.reset(commit='origin/master')
    source.heads.master.checkout()
    source.git.add(A=True)
    source.index.commit('Added new content.')
    source.git.push()
    return None
