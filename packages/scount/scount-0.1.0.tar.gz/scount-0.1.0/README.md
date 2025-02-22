# A source code line counter

## A tool to count the real number of lines in the source code.

We sometimes desperately want a tool that will count the total "real" line count of an opensource project or the projects we are working in. It should not count the blank lines and the comments so that we know how big is the code base.

Simpler the tool, better it is. Here is a simple tool I wrote which will do the job. Currently it supports C, C++, Java, Scala, Python, PHP, Perl, Go and Lua. But you may add other types as well by providing a comment syntax file (explained later).

How do we run the tool? Let us install the tool and print the helps.
```
# Install scount
pip install scount
# Check the help text
scount --help
```
It will print the below:
```
Usage: scount [options]

Options:
  -h, --help            show this help message and exit
  -c COMMENT_FILE, --comment-file=COMMENT_FILE
                        comment syntrax description file
  -d SOURCE_ROOT_DIR, --root-source-dir=SOURCE_ROOT_DIR
                        root directory for source code
  -s SKIP_DIR_REGEX, --skip_dirs=SKIP_DIR_REGEX
                        regular expression for directory name to be skipped
  -f SKIP_FILE_REGEX, --skip_files=SKIP_FILE_REGEX
                        regular expression for file names to be skipped
                        
```
Below is an output form a test run:

```
$ scount -d /mnt/disk0/nipun/repos/NipunTalukdarExamples/

File-type:       C++  Line-count:    4091
File-type:    Python  Line-count:    7319
File-type:      Perl  Line-count:      70
File-type:         C  Line-count:    2692
File-type:      Java  Line-count:    6578
File-type:        Go  Line-count:    3558

```
The tool determines the file type by looking at the extension of the files and doesn't do any other magic for that. All the files with extension .pl will be assumed to be Perl files, all the files with extension .java will be assumed to be Java files etc.

Now the tool doesn't know about Haskell files and how Haskell code is commented. It also doesn't know about Javascript files. So, we instruct the tool by providing it a Json file that describes how commenting is done in Haskell and Javascript files.

Below is content from the sample Json file  (let us name it as syntax_haskell_js.json):
```
{
    "hs": {
        "output_as": "Haskell",
        "other_extns": ["haskell", "hask"],
        "start": "{-",
        "end": "-}",
        "whole_line": ["--"],
    },
    "js": {
        "output_as": "Javascript",
        "other_extns": ["javascript"],
        "start": "/*",
        "end": "*/",
        "whole_line": ["//"],
    },
}
```
The Json file describes how the Haskell and Javascript files are commented. The top level keys denote the languages. So, hs and js are denoting Haskell and Javascript languages. Files with extension .hs are output as "Haskell" files.  Also, files with extensions .haskell and .hask will be treated as Haskell files. 
"start" tag denotes the start tag of a comment. For Haskell, it is '{-'. 
"end" tag denotes the end of a comment. For Haskell, it is '-}'.  
"whole_line" tag denotes the commenting tag which indicates the rest of the line to be a comment. For Haskell it is '--', for Javascript it is '//'.

A sample test run output is shown below:
```
$ scount -d /mnt/disk0/nipun/testdir - -c syntax_haskell_js.json
File-type:    Python  Line-count:     173
File-type:   Haskell  Line-count:      49
```

