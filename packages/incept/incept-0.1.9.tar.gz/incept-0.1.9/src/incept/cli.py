# src/incept/cli.py

import os
import click
import shutil
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
from incept.templates.manager import ensure_templates_from_package, TEMPLATE_DIR
from incept.courses import getCourses

CONFIG_DIR = Path.home() / ".incept"
CONFIG_SUBDIR = CONFIG_DIR / "config"
ENV_FILE = CONFIG_DIR / ".env"

@click.group()
def main():
    """
    Incept CLI: A command-line interface for managing courses, templates, etc.
    """
    pass

@main.command("init-templates")
def cli_init_templates():
    """
    Ensure user-level templates are up to date with the built-in templates.
    Also create a placeholder .env file and config JSON files if not present.
    """
    click.echo("Initializing Incept templates...")
    ensure_templates_from_package()  # existing code for folder_templates
    click.echo(f"Templates ready in: {TEMPLATE_DIR}")

    # 1) Create ~/.incept/.env if it doesn't exist
    if not ENV_FILE.exists():
        # Assume we have an env.example in src/incept/.config/config_templates/env.example
        builtin_env_example = Path(__file__).parent.parent / ".config" / "config_templates" / "env.example"
        if builtin_env_example.exists():
            shutil.copy2(builtin_env_example, ENV_FILE)
            click.echo(f"Created .env at {ENV_FILE}")
        else:
            click.echo("No env.example found in package; skipping .env creation.")
    else:
        click.echo(".env file already exists; not overwriting.")

    # 2) Create ~/.incept/config/ and copy JSON config if missing
    CONFIG_SUBDIR.mkdir(parents=True, exist_ok=True)
    builtin_config_dir = Path(__file__).parent.parent / ".config" / "config_templates"

    for json_file in ["course.json", "chapter.json", "lesson.json", "full_course.json"]:
        dest_path = CONFIG_SUBDIR / json_file
        source_path = builtin_config_dir / json_file
        if not dest_path.exists():
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                click.echo(f"Created config file: {dest_path}")
            else:
                click.echo(f"Missing {source_path}, skipping.")
        else:
            click.echo(f"{dest_path.name} already exists; not overwriting.")

    click.echo("init-templates complete.")

@main.command("get-courses")
@click.option("--api-key", default=None, help="Notion API Key. If not provided, uses .env or environment variable.")
@click.option("--database-id", default=None, help="Notion Database ID. If not provided, uses .env or environment variable.")
@click.option("--filter", default=None, help="Optional filter: name of course to fetch.")
def cli_get_courses(api_key, database_id, filter):
    """
    Fetch courses from the specified Notion database.
    If --api-key or --database-id are not passed, we try .env or system env vars.
    """
    # 1) Load ~/.incept/.env if it exists
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)

    # 2) If user didn't pass --api-key, see if environment has API_KEY
    if not api_key:
        api_key = os.getenv("API_KEY")  # from .env or system
    # 3) If user didn't pass --database-id, see if environment has DATABASE_ID
    if not database_id:
        database_id = os.getenv("DATABASE_ID")

    # 4) If still missing, raise error
    if not api_key or not database_id:
        raise click.ClickException("API_KEY or DATABASE_ID not found. Provide via CLI options or .env file.")

    # 5) Call getCourses
    df = getCourses(
        db="notion",
        api_key=api_key,
        database_id=database_id,
        filter=filter
    )
    if df.empty:
        click.echo("No courses found.")
        return

    # 6) Print the DataFrame of courses
    click.echo("Courses found:")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        click.echo(df)

# Future subcommands: add-course, update-course, etc.

if __name__ == "__main__":
    main()
