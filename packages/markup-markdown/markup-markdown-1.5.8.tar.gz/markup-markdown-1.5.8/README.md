# Markup-Markdown

Stack up markdown files with `!INCLUDE` directives.

## Installation

```
pip install markup-markdown
```

Project on [pypi](https://pypi.org/project/markup-markdown/).

Download the source code, navigate to [GitHub Repo](https://github.com/hailiang-wang/markup-markdown).

There are two components to the project: a Python module, `markup`, and a
Python script that acts as a simple command line interface to the module,
`markup`.

## Commands

### `markup`

Assuming you have a file named `foo.m.md`, you can generate the preprocessed
file `foo.md` by running the following command:

```
markup foo.m.md -o foo.md
```

If you do not specify an output file name, the results will be printed to
stdout, enabling them to be piped to another command.

By default, all available modules are enabled. You can specify a list of
modules to exclude:

```
markup foo.m.md -o foo.md -e youtubembed
```

To watch directory and subdirectories:

```
markup -w PATH
```

Where PATH is a directory path, e.g. `.`, `/home/user`.

To generate docx file, use the [specified file as a style reference](https://pandoc.org/MANUAL.html) in producing a docx or ODT file.

```
markup foo.m.md -o index.md # well defined index.md for pandoc with Toc, Captions, etc.
pandoc --from markdown+footnotes --wrap=none --reference-doc=styles/refs.docx -i index.md -o file.docx
```

To see usage instructions, including a list of enabled modules, supply the
-h or --help arguments:

```
markup --help
```

### `headingsup`

Modify all headings by promote level.

```
headingsup -a 1 -i input.md -o output.md
```

With above command, all `H1` headings are changed to `H2` headings.

Get more hints.

```
headingsup -h
```

### `headingsdown`

Modify all headings by apppend levels.

```
headingsdown -a 1 -i input.md -o output.md
```

With above command, all `H2` headings are changed to `H1` headings.

Get more hints.

```
headingsdown -h
```

### `canvas`

Convert Obsidian canvas file into markup markdown, details in issue [#9](https://github.com/hailiang-wang/markup-markdown/issues/9).

```
canvas -i INPUT.canvas -o OUTPUT.m.md [-r ROOT_CARD_TEXT]
e.g.
    canvas -i xxx.canvas -o xxx.m.md -r root
```

* `INPUT.canvas` is relative path against PWD(Current Working Dir)
* `OUTPUT.m.md` is relative path against PWD(Current Working Dir)
* `-r` is for text of ROOT of the generated file in input canvas, default `root`
* `canvas` command must run inside an Obsidian vault, means at least one dir contains `.obsidian` for the parents of PWD

More information, check out issue [#9](https://github.com/hailiang-wang/markup-markdown/issues/9).

## Modules

### Includes

In order to facilitate large documentation projects, MarkdownPP has an Include
module that will replace a line of the form `!INCLUDE "path/to/filename"` with
the contents of that file, recursively including other files as needed.

File `foo.m.md`:

```
Hello
```

File `bar.m.md`:

```
World!
```

File `yoo.m.md`:

```
## World!
## Who
```

File `index.m.md`:

```
!INCLUDE "foo.m.md"
!INCLUDE "[Bar](bar.m.md)"
!INCLUDE "[[yoo.m.md#World!]]"
```

Compiling `index.m.md` with the Include module will produce the following:

```
Hello
World!
## World!
```

Furthermore, the Include module supports the shifting of headers in the
file to be included. For example,

File `foo.m.md`:

```
# Foo
## Bar
```

File `index.m.md`:

```
# Title
## Subtitle
!INCLUDE "foo.m.md", 2
```

Compiling `index.m.md` with the Include module and using `2` as shift
parameter will yield:

```
# Title
## Subtitle
### Foo
#### Bar
```

### Markers

| Module | Marker | Required | Description |
| --- | --- | --- | --- |
| Skip Blocks | `<!-- markup:markdown-begin -->` | No |  If present, skip above lines in the included file, add following line in the file. |
| Skip Blocks | `<!-- markup:markdown-end -->` | No | If present, bypass following lines in the included file, add following line in the file. |
| Skip Line | `<!-- markup:skip-line -->`  | No | When you want to skip a specific line, use this marker by the end of the line _or_ in the begining.|
| Skip Obsidian Comment | `%%`YOUR COMMENT`%%` | No | Skip content with [Obsidian Comment Syntax](https://github.com/hailiang-wang/markup-markdown/issues/6) |
| Page Break of Office Word | `<!-- markup:page-break-xml -->` | No | Insert a page break for rendering Office Word. |
| Blank Line | `<!-- markup:blank-line -->` | No | Resolve for a blank line purposely. |
| Skip Header Metadata | `---` |  No | if `---` present as 1st line, then lines are skipped until next `---` come into place  |
| EnvVariableReplacements | %MBN_`xxx`% | No | Replace variable in content by Env variable awareness, [more](https://github.com/hailiang-wang/markup-markdown/issues/7) |

More examples -

```
YOUR MESSAEG <!-- markup:skip-line -->
some thing . <!-- markup:skip-line -->
```

### IncludeURLs

Facilitates the inclusion of remote files, such as files kept in a subversion
or GitHub repository. Like Include, the IncludeURL module can replace a line of
the form `!INCLUDEURL "http://your.domain/path/to/filename"` with the contents
returned from that url, recursively including additional remote urls as needed.

IncludeURL runs immediately after the Include module finishes executing. This
means that is it possible to include local files that then require remote files,
but impossible parse !INCLUDE statements found in remote files. This is prevent
ambiguity as to where the file would be located.

Remote file `http://your.domain/foo.m.md`:

```
Hello
```

Remote file `http://your.domain/bar.m.md`:

```
Remote World!
```

Local file `index.m.md`:

```
!INCLUDEURL "http://your.domain/foo.m.md"
!INCLUDEURL "http://your.domain/bar.m.md"
```

Compiling `index.m.md` with the IncludeURL module will produce the following:

```
Hello
Remote World!
```

### IncludeCode

Facilitates the inclusion of local code files. GFM fences will be added
around the included code.

Local code file `hello.py`:

```
    def main():
        print "Hello World"


    if __name__ == '__main__':
        main()
```

Local file `index.m.md`:

```
# My Code

!INCLUDECODE "hello.py"
Easy as that!
```

Compiling `index.m.md` with IncludeCode module wil produce the following:

    # My Code

    ```
    def main():
        print "Hello World"


    if __name__ == '__main__':
        main()
    ```
    Easy as that!

Furthermore the IncludeCode module supports line extraction and language
specification. The line extraction is like python list slicing (e.g. 3:6; lines
three to six). Please note that line counting starts at one, not at zero.

Local file `index.m.md`:

    # My Code

    !INCLUDECODE "hello.py" (python), 1:2
    Easy as that!

Compiling `index.m.md` with IncludeCode module will produce the following:

    # My Code

    ```python
    def main():
        print "Hello World"
    ```
    Easy as that!

### Include image

Insert a image with links as HTML, Markdown, Wikilink.

```
<img src="xxx.png"/>
![caption](xxx.png)
![[xxx.png|caption]]
```


### Table of Contents

The biggest feature provided by MarkdownPP is the generation of a table of
contents for a document, with each item linked to the appropriate section of the
markup. The table is inserted into the document wherever the preprocessor finds
`!TOC` at the beginning of a line. Named `<a>` tags are inserted above each
Markdown header, and the headings are numbered hierarchically based on the
heading tag that Markdown would generate.

```
!TOC DEPTH H1_LANG MODE
```

Where DEPTH is [1-6], H1_LANG is language for h1 header in TOC, [en|cn] , e.g. `!TOC 5 cn`.
Available MODE are `section_only`,`top_and_section`. `top_and_section` would generate the index list on top of the file, `section_only` would omit the top index list.
Image caption is generated as well with ToC prefix.

```
![image catption](URL)
```

Table caption is generated with marker `<!-- markup:table-caption CAPTION -->` under the table.

```
| foo    | bar    |
| ------ | ------ |
| table1 | tabtl2 |
<!-- markup:table-caption xx foo s22 中文 -->
```

### Reference

Similarly, MarkdownPP can generate a list of references that follow Markdown's
alternate link syntax, eg `[name]: <url> "Title"`. A list of links will be
inserted wherever the preprocessor finds a line beginning with `!REF`. The
generated reference list follows the same alternate linking method to ensure
consistency in your document, but the link need not be referenced anywhere in
the document to be included in the list.

```
Document to be included [in the list][Reference11]：

[Reference11]: <https://github.com/hailiang-wang/markup-markdown#reference> "Similarly, MarkdownPP can generate a list of reference"

!REF
```

### Footnote

```
FOO[^f1] Bar

[^f1]: This is a footnote
```

### Skip Header Metadata

```
---
page-title: "Foo bar"
url: https://readingoutpost.com/zettelkasten-6-steps/
date: "2023-03-03 16:50:23"
mindmap-plugin: basic
tags: ["fooo"]
---

Above lines skipped.
```

### YouTube Embeds

As GitHub-flavored Markdown does not allow embed tags, each line of the form
`!VIDEO "[youtube url]"` is converted into a screenshot that links to the video,
roughly simulating the look of an embedded video player.

For example,

```
!VIDEO "http://www.youtube.com/embed/7aEYoP5-duY"
```

becomes

```
[![Link to Youtube video](images/youtube/7aEYoP5-duY.png)](http://www.youtube.com/watch?v=7aEYoP5-duY)
```

## Examples

Example file.m.md:

```
# Document Title

!TOC

## Header 1

### Header 1.a

## Header 2

!REF

[github]: http://github.com "GitHub"

```

The preprocessor would generate the following Markdown-ready document file.md:

```
# Document Title

1\. [Header 1](#header1)
1.1\. [Header 1.a](#header1a)
2\. [Header 2](#header2)

<a name="header1"></a>

## Header 1

<a name="header1a"></a>

### Header 1.a

<a name="header2"></a>

## Header 2

- [GitHub][github]

[github]: http://github.com "GitHub"

```

## Keyboard Shortcuts

Use `mkc`, `img`, `lk`, etc as shortcuts to generate Markdown blocks.

- Insert `mkc` then tab.

### Visual Studio Code

Press `Ctrl + Shift + P` for Commands palette, select `Configure User Snippets`, next select `Markdown.json`, then paste below lines.

```json
{
    "Table Caption for markup": {
        "prefix": "mkc",
        "body": [
            "<!-- markup:table-caption $1 -->"
        ],
        "description": "Generate table caption for markup-markdown"
    },
    "Insert image": {
        "prefix": "img",
        "body": [
            "![$2]($1)"
        ],
        "description": "Generate image with caption"
    },
    "Insert link": {
        "prefix": "lk",
        "body": [
            "[$2]($1)"
        ],
        "description": "Generate link"
    },
    "Insert reference": {
        "prefix": "ref",
        "body": [
            "[^$2]: see Appendix $1，page XXX"
        ],
        "description": "Generate reference"
    },
    "Insert reference in Chinese": {
        "prefix": "refc",
        "body": [
            "[^$1]: 见附录 《$2》，第 $3 页"
        ],
        "description": "Generate reference"
    },
    "Insert footnote": {
        "prefix": "fn",
        "body": [
            "[^]"
        ],
        "description": "Generate footnote"
    },
    "Markup include begins": {
        "prefix": "mkb",
        "body": [
            "<!-- markup:markdown-begin -->"
        ],
        "description": "Skip above lines in the included file, add following lines in the file."
    },
    "Markup include ends": {
        "prefix": "mke",
        "body": [
            "<!-- markup:markdown-end -->"
        ],
        "description": "Bypass lines in the included file."
    },
    "Skip current line": {
        "prefix": "mks",
        "body": [
            "<!-- markup:skip-line -->"
        ],
        "description": "Bypass lines in the included file, add following line in the file."
    },
    "Insert a blank line": {
        "prefix": "mkbl",
        "body": [
            "<!-- markup:blank-line -->"
        ],
        "description": "Insert a blank line."
    },
    "Insert a page break for Office Word": {
        "prefix": "mkpb",
        "body": [
            "<!-- markup:page-break-xml -->"
        ],
        "description": "Insert a page break for Office Word."
    },
    "Insert Comment": {
        "prefix": "ic",
        "body": [
            "<!-- $1 -->"
        ],
        "description": "Insert comment"
    }
}
```

## Contribute

### Install locally and watch

Watch dirs.

```
python setup.py sdist && pip install -U dist/markup-1.0.3.tar.gz && markup -w .
```

### Publish new version

```
./scripts/publish.sh
```

## Known Issues

- file encoding only support UTF-8
- TOC not support punctuations

## Support

If you find any problems with MarkdownPP, or have any feature requests, please
report them to [GitHub][repo], and I will respond when possible. Code
contributions are _always_ welcome, and ideas for new modules, or additions to
existing modules, are also appreciated.

Markup-Markdown is based on Markdown Preprocessor ([MarkdownPP](https://github.com/jreese/markdown-pp)).

**NOTICE: MarkdownPP is no longer actively maintained. MarkdownPP will not receive any future releases.**

The Markup-Markdown is a Python module designed to add extended features
on top of the excellent Markdown syntax defined by John Gruber. These additions
are mainly focused on creating larger technical documents without needing to use
something as heavy and syntactically complex as Docbook.

MarkdownPP uses a set of selectable modules to apply a series of transforms to
the original document, with the end goal of generating a new Markdown document
that contains sections or features that would be laborious to generate or
maintain by hand.

Documents designed to be preprocessed by Markup-Markdown should try to follow the
convention of naming files with a .m.md extension(m.md is Markup Markdown for short, ".md" as end so we can leverage Editor's highlight), so that Markup-Markdown can
generate a document with the same name, but with the standard .md extension.
As an example, this document in raw format is named "readme.m.md", and the
generated document from Markup-Markdown is named "readme.md" so that GitHub can find
and process that document when viewing the repository.

## References

!REF

[repo]: http://github.com/jreese/markdown-pp "Markdown Preprocessor on GitHub"
