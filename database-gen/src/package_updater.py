import ast

from src.model_updater import create_or_update_class


class PackageUpdater:

    def __init__(self, database_uri: str, target_folder: str):
        self.database_uri = database_uri
        self.target_folder = target_folder

    def create_or_update(self):
        filename = f'{self.target_folder}/__init__.py'
        package_module = ast.parse('"""Partially autogenerated - edit only inside manual sections"""\n'
                                   'from flask_sqlalchemy import SQLAlchemy\n\n\n'
                                   'db = SQLAlchemy()\n')
        with open(filename, 'w') as target_file:
            target_file.write(ast.unparse(package_module))
        self._generate_and_update_models()

    def _generate_and_update_models(self):
        flask_sqlacodegen_module = _build_flask_sqlacodegen_module(self.database_uri)
        for node in ast.walk(flask_sqlacodegen_module):
            if isinstance(node, ast.ClassDef):
                create_or_update_class(self.target_folder, node)


def _build_flask_sqlacodegen_module(database_uri) -> ast.Module:
    import subprocess
    command = ["flask-sqlacodegen", "--flask", "--noinflect", database_uri]
    completed_process = subprocess.run(command, capture_output=True, text=True)
    return ast.parse(completed_process.stdout)
