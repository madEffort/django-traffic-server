import os
import shutil

apps_path = "apps"

for app in os.listdir(apps_path):

    app_migrations_path = os.path.join(apps_path, app, "migrations")

    if os.path.exists(app_migrations_path):
        # Delete all files except __init__.py
        for filename in os.listdir(app_migrations_path):
            file_path = os.path.join(app_migrations_path, filename)
            if filename != "__init__.py":
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                elif os.path.isdir(file_path) and filename == "__pycache__":
                    shutil.rmtree(file_path)
                    print(f"Deleted directory: {file_path}")
    else:
        print(f"No migrations directory found for {app}")
