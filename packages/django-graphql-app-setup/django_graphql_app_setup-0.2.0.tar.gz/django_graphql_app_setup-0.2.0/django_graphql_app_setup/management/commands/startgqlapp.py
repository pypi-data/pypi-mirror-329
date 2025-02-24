import os
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = "Creates a Django app directory structure with additional schema, mutations, queries, types, inputs, and management/commands folders. Also updates INSTALLED_APPS in settings and modifies apps.py."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--custom-directory",
            type=str,
            help="Specify the directory where the app should be created.",
        )

    def handle(self, **options):
        # Get the app name and custom directory
        app_name = options["name"]
        custom_directory = options.get("custom_directory", None)

        # Determine the target directory
        target = os.path.join(os.getcwd(), app_name)

        # Call the original startapp command to create the default Django app structure
        super().handle(**options)

        # Define the additional folders and files to create
        schema_structure = {
            "schema": {
                "__init__.py": "",
                "mutations": {
                    "__init__.py": "",
                    f"{app_name}_mutations.py": (
                        "import graphene\n\n"
                        f"class {app_name.capitalize()}Mutation(graphene.Mutation):\n"
                        "    pass\n"
                    ),
                },
                "queries": {
                    "__init__.py": "",
                    f"{app_name}_queries.py": (
                        "import graphene\n\n"
                        f"class {app_name.capitalize()}Query(graphene.ObjectType):\n"
                        "    pass\n"
                    ),
                },
                "types": {
                    "__init__.py": "",
                    f"{app_name}_types.py": (
                        "import graphene\n\n"
                        "class ExampleType(graphene.ObjectType):\n"
                        "    example_field = graphene.String()\n"
                    ),
                },
                "inputs": {
                    "__init__.py": "",
                    f"{app_name}_inputs.py": (
                        "import graphene\n\n"
                        "class ExampleInput(graphene.InputObjectType):\n"
                        "    example_field = graphene.String()\n"
                    ),
                },
            },
            "management": {
                "__init__.py": "",
                "commands": {
                    "__init__.py": "",
                    "example_command.py": (
                        "from django.core.management.base import BaseCommand\n\n"
                        "class Command(BaseCommand):\n"
                        "    help = 'Example custom management command for this app.'\n\n"
                        "    def handle(self, *args, **kwargs):\n"
                        "        self.stdout.write(self.style.SUCCESS('Hello from the custom command!'))\n"
                    ),
                },
            },
        }

        # Create the additional folders and files
        self.create_structure(target, schema_structure)

        # Determine the app's Python import path
        app_import_path = self.get_app_import_path(target, custom_directory)

        # Update INSTALLED_APPS in settings.py
        self.update_installed_apps(app_import_path)

        # Update apps.py
        self.update_apps_py(target, app_import_path, app_name)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created app '{app_name}' with default Django files, schema, mutations, queries, types, inputs, and management/commands folders. Also updated INSTALLED_APPS with '{app_import_path}' and modified apps.py."
            )
        )

    def create_structure(self, target, structure):
        for name, content in structure.items():
            path = os.path.join(target, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self.create_structure(path, content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    def get_app_import_path(self, target, directory=None):
        app_abs_path = os.path.abspath(target)
        project_root = os.path.abspath(os.getcwd())
        relative_path = os.path.relpath(app_abs_path, project_root)
        app_import_path = relative_path.replace(os.sep, ".").strip(".")
        if directory:
            directory = directory.replace("/", ".").strip(".")
            app_import_path = f"{directory}.{app_import_path}"
        return app_import_path

    def find_settings_path(self):
        current_dir = os.path.abspath(os.getcwd())
        while current_dir != os.path.dirname(current_dir):
            settings_path = os.path.join(current_dir, "config", "settings.py")
            if os.path.exists(settings_path):
                return settings_path
            current_dir = os.path.dirname(current_dir)
        return None

    def update_installed_apps(self, app_import_path):
        settings_path = self.find_settings_path()
        if not settings_path:
            self.stdout.write(
                self.style.WARNING(
                    "Could not find settings.py. Skipping INSTALLED_APPS update."
                )
            )
            return

        with open(settings_path, "r") as f:
            lines = f.readlines()

        installed_apps_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("INSTALLED_APPS"):
                installed_apps_index = i
                break

        if installed_apps_index == -1:
            self.stdout.write(
                self.style.WARNING("Could not find INSTALLED_APPS. Skipping update.")
            )
            return

        for line in lines[installed_apps_index:]:
            if f"'{app_import_path}'" in line or f'"{app_import_path}"' in line:
                self.stdout.write(
                    self.style.WARNING(
                        f"App '{app_import_path}' is already in INSTALLED_APPS."
                    )
                )
                return

        for i in range(installed_apps_index, len(lines)):
            if lines[i].strip().endswith("]"):
                lines.insert(i, f"    '{app_import_path}',\n")
                break

        with open(settings_path, "w") as f:
            f.writelines(lines)

        self.stdout.write(
            self.style.SUCCESS(f"Added '{app_import_path}' to INSTALLED_APPS.")
        )

    def update_apps_py(self, target, app_import_path, app_name):
        apps_py_path = os.path.join(target, "apps.py")
        if not os.path.exists(apps_py_path):
            return

        with open(apps_py_path, "w") as f:
            f.write(
                f"from django.apps import AppConfig\n\n"
                f"class {app_name.capitalize()}Config(AppConfig):\n"
                f"    name = '{app_import_path}'\n"
                f"    label = '{app_name}'\n"
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {apps_py_path} with name='{app_import_path}' and label='{app_name}'."
            )
        )
