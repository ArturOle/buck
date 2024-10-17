
import buck_aws
import click
import os


@click.group()
@click.option('--bucket_name', default='developer-task2', help='Bucket name')
@click.option('--directory', default='TIE-sa', help='Directory')
@click.pass_context
def cli(ctx, bucket_name, directory):
    ctx.ensure_object(dict)
    ctx.obj["bucket_name"] = bucket_name
    ctx.obj["directory"] = directory


@cli.command("list_all")
@click.pass_context
def list_all(ctx):
    print(buck_aws.list_all_in_bucket(
        ctx.obj["bucket_name"],
        ctx.obj["directory"])
    )


@cli.command("find")
@click.option('--pattern', required=True, help='Pattern')
@click.pass_context
def find(ctx, pattern):
    print(buck_aws.find_in_bucket(
        ctx.obj["bucket_name"],
        ctx.obj["directory"],
        pattern
    ))


@cli.command("upload")
@click.option('--file_path', required=True, help='File path')
@click.pass_context
def upload(ctx, file_path):
    print(buck_aws.upload_file_to_bucket(
        file_path,
        ctx.obj["bucket_name"],
        ctx.obj["directory"]
    ))


@cli.command("delete")
@click.option('--pattern', default='\b\B', help='Pattern')
@click.pass_context
def delete(ctx, pattern):
    print(buck_aws.delete_matching_files(
        ctx.obj["bucket_name"],
        ctx.obj["directory"],
        pattern
    ))


if __name__ == '__main__':
    cli(obj={})
