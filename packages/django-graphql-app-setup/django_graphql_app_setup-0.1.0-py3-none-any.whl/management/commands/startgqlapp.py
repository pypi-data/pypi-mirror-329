import os
from django.core.management.commands.startapp import Command as StartAppCommand
from django.core.management.base import CommandError


class Command(StartAppCommand):
    help = "Creates a Django app directory structure with additional schema, mutations, queries, types, inputs, and management/commands folders. Also updates INSTALLED_APPS in settings."

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
        custom_directory = options.get("custom_directory")

        # Determine the target directory
        if custom_directory:
            target = os.path.join(os.getcwd(), custom_directory, app_name)
        else:
            target = os.path.join(os.getcwd(), app_name)

        # Ensure the parent directory exists
        parent_dir = os.path.dirname(target)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f"Created parent directory: {parent_dir}"))

        # Call the original startapp command to create the default Django app structure
        super().handle(**options)

        # Define the additional folders and files to create
        schema_structure = {
            "schema": {
                "__init__.py": "",
                "mutations": {
                    "__init__.py": "",
                    f"{app_name}_mutations.py": (
                        "from graphene import Mutation\n\n"
                        f"class {app_name.capitalize()}Mutation(Mutation):\n"
                        "    pass\n"
                    ),
                },
                "queries": {
                    "__init__.py": "",
                    f"{app_name}_queries.py": (
                        "from graphene import ObjectType\n\n"
                        f"class {app_name.capitalize()}Query(ObjectType):\n"
                        "    pass\n"
                    ),
                },
                "types": {
                    "__init__.py": "",
                    f"{app_name}_types.py": (
                        "from graphene import ObjectType, String\n\n"
                        f"class {app_name.capitalize()}Type(ObjectType):\n"
                        "    example_field = String()\n"
                    ),
                },
                "inputs": {
                    "__init__.py": "",
                    f"{app_name}_inputs.py": (
                        "from graphene import InputObjectType, String\n\n"
                        f"class {app_name.capitalize()}Input(InputObjectType):\n"
                        "    example_field = String()\n"
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
        app_import_path = self.get_app_import_path(target)

        # Update INSTALLED_APPS in settings.py
        self.update_installed_apps(app_import_path)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created app '{app_name}' with default Django files, schema, mutations, queries, types, inputs, and management/commands folders. Also updated INSTALLED_APPS with '{app_import_path}'."
            )
        )

    def create_structure(self, target, structure):
        """
        Recursively create folders and files based on the given structure.
        """
        for name, content in structure.items():
            path = os.path.join(target, name)
            if isinstance(content, dict):
                # Create a directory
                os.makedirs(path, exist_ok=True)
                self.create_structure(path, content)
            else:
                # Create a file with the given content
                with open(path, "w") as f:
                    f.write(content)

    def get_app_import_path(self, target):
        """
        Determine the Python import path for the app based on its location.
        """
        # Get the absolute path of the app directory
        app_abs_path = os.path.abspath(target)

        # Get the absolute path of the project root (where manage.py is located)
        project_root = os.path.abspath(os.getcwd())

        # Calculate the relative path of the app from the project root
        relative_path = os.path.relpath(app_abs_path, project_root)

        # Convert the relative path to a Python import path
        # Replace slashes with dots and remove leading/trailing slashes
        app_import_path = relative_path.replace(os.sep, ".").strip(".")

        return app_import_path

    def find_settings_path(self):
        """
        Dynamically find the path to settings.py by traversing up the directory tree.
        """
        current_dir = os.path.abspath(os.getcwd())
        while current_dir != os.path.dirname(current_dir):  # Stop at the root directory
            settings_path = os.path.join(current_dir, "config", "settings.py")
            if os.path.exists(settings_path):
                return settings_path
            # Move up one directory
            current_dir = os.path.dirname(current_dir)
        return None

    def update_installed_apps(self, app_import_path):
        """
        Update the INSTALLED_APPS setting in settings.py to include the new app.
        """
        # Dynamically find the settings.py path
        settings_path = self.find_settings_path()
        if not settings_path:
            self.stdout.write(
                self.style.WARNING(
                    "Could not find settings.py in any parent directory. Skipping INSTALLED_APPS update."
                )
            )
            return

        # Read the settings file
        with open(settings_path, "r") as f:
            lines = f.readlines()

        # Find the INSTALLED_APPS list
        installed_apps_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("INSTALLED_APPS"):
                installed_apps_index = i
                break

        if installed_apps_index == -1:
            self.stdout.write(
                self.style.WARNING(
                    "Could not find INSTALLED_APPS in settings file. Skipping update."
                )
            )
            return

        # Check if the app is already in INSTALLED_APPS
        for line in lines[installed_apps_index:]:
            if f"'{app_import_path}'" in line or f'"{app_import_path}"' in line:
                self.stdout.write(
                    self.style.WARNING(
                        f"App '{app_import_path}' is already in INSTALLED_APPS. Skipping update."
                    )
                )
                return

        # Insert the new app into INSTALLED_APPS
        for i in range(installed_apps_index, len(lines)):
            if lines[i].strip().endswith("]"):
                # Insert the new app before the closing bracket
                lines.insert(i, f"    '{app_import_path}',\n")
                break

        # Write the updated settings file
        with open(settings_path, "w") as f:
            f.writelines(lines)

        self.stdout.write(
            self.style.SUCCESS(
                f"Added '{app_import_path}' to INSTALLED_APPS in settings."
            )
        )