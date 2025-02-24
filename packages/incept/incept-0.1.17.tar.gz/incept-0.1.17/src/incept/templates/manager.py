# src/incept/templates/manager.py
import re
import shutil
from pathlib import Path
from platformdirs import user_documents_dir
from incept.utils.file_utils import sync_templates

CONFIG_DIR = Path.home() / ".incept"
TEMPLATE_DIR = CONFIG_DIR / "folder_templates"

# For example, define placeholder folder names or a pattern:
PLACEHOLDER_PATTERN = re.compile(r'^\{\#\#_.+\}$')

def get_default_documents_folder() -> Path:
    """
    Returns the cross-platform 'Documents' directory using platformdirs.
    On Windows, this typically points to:  C:\\Users\\<YourName>\\Documents
    On macOS:    /Users/<YourName>/Documents
    On Linux:    /home/<YourName>/Documents (or similar, if configured).
    """
    return Path(user_documents_dir())

def builtin_templates_dir() -> Path:
    """Points to the built-in `.config/folder_templates` in the installed package."""
    return (Path(__file__).parent.parent / ".config" / "folder_templates").resolve()

def ensure_templates_from_package():
    """
    Merges built-in templates (from the installed package) into
    ~/.incept/folder_templates, overwriting only the 'default'
    folders and leaving custom user folders alone.
    """
    # ... same as before ...
    pass  # shortened for brevity

def get_default_documents_folder() -> Path:
    """
    Returns the user's cross-platform 'Documents' directory 
    (Windows: C:\\Users\\<user>\\Documents, macOS/Linux: ~/Documents, etc.)
    """
    from platformdirs import user_documents_dir
    return Path(user_documents_dir())

def create_course_structure(
    course_name: str,
    template: str = "default",
    force_init: bool = True,
    base_path: Path | None = None
) -> Path:
    """
    Create a local course folder structure by copying the template from:
    ~/.incept/folder_templates/courses/<template>/

    - Automatically replaces `{course_name}` in the template folder structure.
    - Copies all files/folders **except** `{##_chapter_name}` and `{##_lesson_name}`.
    - Preserves user flexibility in defining hierarchical structures.

    :param course_name: The sanitized name of the course.
    :param template: The template folder to use (default="default").
    :param force_init: Ensures templates are synced before use.
    :param base_path: The destination directory for the course.
    :return: The created course path.
    """
    if force_init:
        ensure_templates_from_package()

    # Find the template path
    template_base_path = TEMPLATE_DIR / "courses" / template
    if not template_base_path.exists():
        raise ValueError(f"Template '{template}' not found at: {template_base_path}")

    if base_path is None:
        base_path = Path(user_documents_dir()) / "courses"

    # **Find `{course_name}` occurrence inside the template structure**
    detected_course_name_path = None
    for root, dirs, _ in os.walk(template_base_path):
        for directory in dirs:
            if directory == "{course_name}":
                detected_course_name_path = Path(root) / directory
                break
        if detected_course_name_path:
            break  # Stop as soon as we find `{course_name}`

    # **If `{course_name}` exists inside template, replace it**
    if detected_course_name_path:
        relative_path_from_template = detected_course_name_path.relative_to(template_base_path)
        destination_course_path = base_path / relative_path_from_template.parent / course_name
    else:
        # Otherwise, just create the course at the base path
        destination_course_path = base_path / course_name

    if destination_course_path.exists():
        raise FileExistsError(f"Course folder already exists: {destination_course_path}")

    def ignore_placeholder_folders(folder: str, items: list[str]) -> list[str]:
        """
        Called by shutil.copytree for each directory.
        Returns a list of item names to 'ignore' (i.e., skip copying).
        """
        ignored = []
        for item in items:
            if PLACEHOLDER_PATTERN.match(item):  # Ignore {##_chapter_name} or {##_lesson_name}
                ignored.append(item)
        return ignored

    # **Copy template contents while skipping `{##_chapter_name}` and `{##_lesson_name}`**
    shutil.copytree(
        src=template_base_path,
        dst=destination_course_path,
        dirs_exist_ok=False,
        ignore=ignore_placeholder_folders
    )

    return destination_course_path


def get_available_templates() -> list[str]:
    """Lists subfolders in ~/.incept/folder_templates/courses."""
    courses_dir = TEMPLATE_DIR / "courses"
    if not courses_dir.exists():
        return []
    return [folder.name for folder in courses_dir.iterdir() if folder.is_dir()]
