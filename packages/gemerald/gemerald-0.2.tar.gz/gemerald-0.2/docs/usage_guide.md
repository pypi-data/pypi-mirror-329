
# Usage guild

### Compatibility ###

 - Python 3.12

### Basic directory structure ###

To start building your site you will need 3 directories:
 - templates
 - static
 - content

`static` directory will hold all your assets for the website.
This catalog will be copied to every output format under the path `/static`.
Please put your images there.

`content` directory contains all your markdown files.
These will be translated into output formats.
It can contain subfolders.
Subfolders will apear in output as well.

`templates` is a directory that contains only other subdirectories.
All subdirectories must be named just like needed output formats.
As an example, if you need to produce HTML output, all your HTML templates will be placed under
`templates/html`.

### Config files ###

Each format's template directory must contain additional file named `config.yaml`.
This file contains all configuration for given format.
This is a list of mandatory keys that need to be present:

 - `enabled` (boolean) - Prevent output for given format by setting this to false.
 - `addStatic` (boolean) - Copy static folder contents into `/contents` path of given output.

### Templating ###

Each template has a given file extension.
As an example HTML output has an `.html` file extension.
All your templates will have to end with that extension.
Other files (except `config.yaml`) will be ignored.

All templates reside with a folder named like given file extension.
This folder must be a subfolder of a `templates` folder.

Here is a list of file extensions:
 - gmi
 - html
 - txt
 - debug

If your markdown file is named `hello.md`, your file needs template `hello.<file_extension>`.

There is a special template file named `_entries.<file_extension>` that can match multiple files.
That can be useful for blog entries.
Any file that does not have it's own template (named exactly like the file) will look for `_entries`
template.
A `_entries` template must be placed in the same folder as a dedicated template should be placed.

### Available templating values ###

Templates use Jinja2 templating language.
To insert dynamic value use double curly braces (`{{ value }}`).

Gemerald passes 2 values to templates:
 - `Context`
 - `Site`

Site is just a shorthand for `Context.site`.
It contains `content` - that is generated via transformation of Markdown into requested format.
You can access it via `Site.content`

`Content` is wider object that encapsulates:
 - `href` of a page
 - `title`
 - `dateReleased`
 - `siblings` which is a list-like object that contins other files from the same directory. Use `.by_date()` to sort them.
 - `utils` which is a python dict contining only `now` key. A datetime object of a current time.

