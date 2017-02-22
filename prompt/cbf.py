import click
from click_repl import register_repl

class CmdGlobal(object):

    def __init__(self):
        self.current_resource_type = None
        self.current_resource = None

    def __str__(self):
        return u'CmdGlobal(current_resource_type={}, current_resource={})'.format(self.current_resource_type, self.current_resource)


class CmdConfig(object):

    def __init__(self):
        self.verbose = None
        self.resource_type = None
        self.resource = None

    def __str__(self):
        return u'CmdConfig(verbose={}, resource_type={}, resource={})'.format(self.verbose, self.resource_type, self.resource)


global_cfg = CmdGlobal()


@click.group()
@click.option(
    '--verbose',
    is_flag=True,
    default=False
)
@click.pass_context
def cli(ctx, verbose):
    print(ctx)
    cfg = CmdConfig()
    cfg.verbose = verbose
    ctx.obj = cfg


@cli.command(name='say')
@click.option(
    '--message',
    default=u'Hello, world!',
    help='Set the message to say hello',
)
@click.pass_obj
def cmd_say(cfg, message):
    click.echo(message)




@cli.group(name='cd', help='change current resource')
@click.pass_obj
def cmd_cd(cfg):
    pass


@cmd_cd.command(name='node', help='change current resource')
@click.argument('resource')
@click.pass_obj
def cmd_cd_node(cfg, resource):
    """
    Change current resource
    """
    global_cfg.current_resource_type = u'node'
    global_cfg.current_resource = resource
    click.echo(cfg)
    click.echo(global_cfg)

@cmd_cd.command(name='worker')
@click.argument('resource')
@click.pass_obj
def cmd_cd_worker(cfg, resource):
    global_cfg.current_resource_type = u'worker'
    global_cfg.current_resource = resource
    click.echo(cfg)
    click.echo(global_cfg)

@cmd_cd.command(name='transport')
@click.argument('resource')
@click.pass_obj
def cmd_cd_transport(cfg, resource):
    global_cfg.current_resource_type = u'transport'
    global_cfg.current_resource = resource
    click.echo(cfg)
    click.echo(global_cfg)


@cli.group(name='stop', help='Stop a resource.')
@click.pass_obj
def cmd_stop(cfg):
    pass


@cmd_stop.command(name='transport', help='Stop a router transport.')
@click.argument('resource')
@click.option(
    '--mode',
    help=u'graceful: wait for all clients to disconnect before stopping\n\nimmediate: stop transport forcefully disconnecting all clients',
    type=click.Choice([u'graceful', u'immediate']),
    default=u'graceful'
)
@click.pass_obj
def cmd_stop_transport(cfg, resource, mode):
    cfg.resource_type = u'transport'
    cfg.resource = resource
    click.echo(cfg)
    click.echo(global_cfg)


#@cmd_stop.command(name='worker')
#@click.argument('node')
#@click.argument('worker')
#@click.pass_obj
#def cmd_stop_worker(cfg, node, worker):
#    pass
#
#
#@cmd_stop.command(name='realm')
#@click.argument('node')
#@click.argument('worker')
#@click.argument('realm')
#@click.pass_obj
#def cmd_stop_realm(cfg, node, worker, realm):
#    pass






@cli.group(name='start')
@click.pass_obj
def cmd_start(cfg):
    pass


@cmd_start.command(name='worker')
@click.argument('resource')
@click.option(
    '--type',
    required=True
)
@click.pass_obj
def cmd_start_worker(cfg, resource, type):
    pass


@cmd_start.command(name='realm')
@click.argument('resource')
@click.option(
    '--name',
    required=True
)
@click.pass_obj
def cmd_start_realm(cfg, resource, name):
    pass




#@click.command()
#@click.option('--count', default=1, help='Number of greetings.')
#@click.option('--name', prompt='Your name',
#              help='The person to greet.')
#def hello(count, name):
#    """Simple program that greets NAME for a total of COUNT times."""
#    for x in range(count):
#        click.echo('Hello %s!' % name)

register_repl(cli)

if __name__ == '__main__':
    cli()
