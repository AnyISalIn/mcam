import os

from mcam import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def profile():
    app.run()


@app.shell_context_processor
def make_shell_context():
    from mcam.instance.models import Instance
    from mcam.template.models import Template
    from mcam.provider.models import Provider
    from mcam.user.models import User
    return dict(
        db=db,
        Instance=Instance,
        Template=Template,
        Provider=Provider,
        User=User
    )


@app.cli.command()
def init_data():
    from mcam.user.models import User
    if not User.objects.count():
        user = User(username='admin', password='admin', is_admin=True).save()
