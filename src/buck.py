
import buck_aws
import click

from pprint import pprint


@click.group()
@click.option('--bucket_name', default='developer-task2', help='Bucket name')
@click.option('--directory', default='TIE-sa', help='Directory')
@click.pass_context
def cli(ctx, bucket_name, directory):
    ctx.ensure_object(dict)
    ctx.obj["bucket_name"] = bucket_name
    ctx.obj["directory"] = directory


@cli.command("list-all")
@click.pass_context
def list_all(ctx):
    result = buck_aws.list_all_in_bucket(
        ctx.obj["bucket_name"],
        ctx.obj["directory"]
    )
    pprint(result)


@cli.command("find")
@click.option('--pattern', required=True, help='Pattern')
@click.pass_context
def find(ctx, pattern):
    reslut = buck_aws.find_in_bucket(
        ctx.obj["bucket_name"],
        ctx.obj["directory"],
        pattern
    )
    pprint(reslut)


@cli.command("upload")
@click.option('--file-path', required=True, help='File path')
@click.pass_context
def upload(ctx, file_path):
    result = buck_aws.upload_file_to_bucket(
        file_path,
        ctx.obj["bucket_name"],
        ctx.obj["directory"]
    )
    pprint(result)


@cli.command("delete")
@click.option('--pattern', required=True, help='Pattern')
@click.pass_context
def delete(ctx, pattern):
    result = buck_aws.delete_matching_files(
        ctx.obj["bucket_name"],
        ctx.obj["directory"],
        pattern
    )
    pprint(result)


if __name__ == '__main__':
    cli(obj={})
