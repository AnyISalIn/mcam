import os
import pathlib

from flask import current_app


def generate_plan_files(path, providers, resources, outputs, variables, datasources):
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, 'providers.tf'), 'wb') as f:
        data = '\n'.join([_.config for _ in providers])
        f.write(data.encode())

    with open(os.path.join(path, 'resources.tf'), 'wb') as f:
        f.write(resources.encode())

    with open(os.path.join(path, 'outputs.tf'), 'wb') as f:
        f.write(outputs.encode())

    with open(os.path.join(path, 'variables.tf'), 'wb') as f:
        f.write(variables.encode())

    with open(os.path.join(path, 'datasources.tf'), 'wb') as f:
        f.write(datasources.encode())


class TerraformManagerService(object):
    def __init__(self, terraform_bin=None, plan_template_dir=None):
        self.terraform_bin = terraform_bin or current_app.config['TERRAFORM_BIN']
        self.plan_template_dir = pathlib.Path(plan_template_dir or current_app.config['PLAN_DIR'])

    def validate(self, *args):
        return [self.terraform_bin, 'validate'] + list(args)

    def apply(self, *args):
        return [self.terraform_bin, 'apply', '-auto-approve'] + list(args)

    def init(self, *args):
        return [self.terraform_bin, 'init'] + list(args)

    def show(self, *args):
        return [self.terraform_bin, 'show', '-json'] + list(args)

    def refresh(self, *args):
        return [self.terraform_bin, 'refresh'] + list(args)

    def destroy(self, *args):
        return [self.terraform_bin, 'destroy', '-auto-approve'] + list(args)

    def graph(self, *args):
        return [self.terraform_bin, 'graph'] + list(args)

    def plan(self, *args):
        return [self.terraform_bin, 'plan'] + list(args)
