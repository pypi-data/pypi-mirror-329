import sys
import os
from shutil import copytree
from pathlib import Path
from jinja2 import Template
from typing import Tuple, Any
from gemerald.markdown_file import MarkdownFile
from gemerald.navigator import NavigatorFile, TemplateNavigator, MarkdownNavigator
from gemerald.strategies import find_strategy


def find_formats(templates_path):
    subfolders = [Path(f.path) for f in os.scandir(templates_path) if f.is_dir()]
    template_dirs = [TemplateNavigator(subfolder) for subfolder in subfolders]
    return [tpl for tpl in template_dirs if tpl.config.get("enabled")]


def main():
    try:
        dirs = get_dirs(Path(sys.argv[1]))
    except IndexError:
        print("Nope!")
        usage()
        sys.exit(1)

    markdown_nav = MarkdownNavigator(dirs["input_dir"])
    tpls = find_formats(dirs["templates_dir"])

    files_in_dirs: dict[str, list[MarkdownFile]] = {}
    files: list[Tuple[MarkdownFile, NavigatorFile]] = []
    for md_file in markdown_nav:
        md = MarkdownFile(
            path=md_file.relative_path,
            contents=md_file.contents,
        )
        files.append((md, md_file))
        add_to_group(files_in_dirs, md_file.relative_folder_path, md)

    add_siblings(files_in_dirs)

    for tpl in tpls:
        for md, _ in files:
            md.set_formatter(find_strategy(tpl.name))

        for md, md_file in files:
            template_path = tpl.get_template_for(md_file).absolute_path

            if tpl.config.get("addStatic"):
                copytree(
                    src=dirs["static_dir"],
                    dst=dirs["output_dir"] / tpl.name,
                    dirs_exist_ok=True,
                )

            with open(template_path, encoding="utf-8") as tpl_f:
                template = Template(tpl_f.read())
                template.filename = template_path
                content = md.template(template)

            save_location = (
                dirs["output_dir"] / tpl.name / md.get_path_changed_extension(tpl.name)
            )

            save_dir = os.path.dirname(save_location)
            os.makedirs(save_dir, exist_ok=True)

            with open(save_location, "w+", encoding="utf-8") as savefile:
                savefile.write(content)
                savefile.write("\n")


def add_to_group(d: dict, k: str, v: Any):
    if d.get(k) is None:
        d[k] = [v]
    else:
        d[k].append(v)


def add_siblings(dict_of_folders: dict):
    for files in dict_of_folders.values():
        for file in files:
            # We need a copy of that list
            other_files = [other_file for other_file in files if other_file != file]
            file.set_siblings(other_files)


def get_dirs(source_dir: Path):
    dirs = {
        "output_dir": source_dir / "public",
        "input_dir": source_dir / "content",
        "static_dir": source_dir / "static",
        "templates_dir": source_dir / "templates",
    }
    if not source_dir.is_dir():
        print("This is not a valid project structure")
        sys.exit(1)
    if not dirs["input_dir"].is_dir():
        print("All sources must be in an 'content' directory")
        sys.exit(1)
    if not dirs["static_dir"].is_dir():
        print("You're missing a static dir")
        sys.exit(1)
    if not dirs["templates_dir"].is_dir():
        print("All templates must be in a directory")
        sys.exit(1)
    if dirs["output_dir"].exists():
        print("Please delete current public dir before")
        sys.exit(1)
    return dirs


def usage():
    print(
        """
            Usage:
            gemerald <SOURCE_DIR>
        """
    )


if __name__ == "__main__":
    main()
