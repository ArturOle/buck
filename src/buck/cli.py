import click
import os

import buck


@click.group()
def cli():
    pass


@cli.command()
@click.option('--bucket_name', default='developer-task', help='Bucket name')
@click.option('--directory', default='TIE-sa', help='Directory')
def list_all(bucket_name, directory):
    return buck.list_all_in_bucket(bucket_name, directory)