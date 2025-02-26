# Generic formatter and linter

This package provides formatters and linters for CMake, C++, and Python, making it ideal for developers who work with both C++ and Python.

# Getting Started

## Installation

```sh
pip install lhy-formatter-linter
```

## Usage

The formatter or linter will recursively scan your project directory, formatting or linting all CMake, C++, and Python code using third-party tools.

| third-party tool | cmake        | C++             | python       | 
|------------------|--------------|-----------------|--------------|
| formatter        | cmake-format | clang-format    | yapf, isort  | 
| linter           | cmake-lint   | clang-tidy      | flake8       | 

```sh
lhy -h
usage: lhy [-h] {format,lint} ...

code formatter and linter.

positional arguments:
  {format,lint}
    format       Format code
    lint         Lint code
```

### format code in yout project

```sh
lhy format -p <project-root-dir> 
```
### lint code in yout project

```sh
lhy lint -p <project-root-dir> 
```

## Optional arguments

### Choose languages 

Users can choose to format or lint one or more languages by using the `-l` or `--language` option.


```sh
lhy format -p <project-root-dir> -l cmake
```

```sh
lhy lint -p <project-root-dir> -l python
```

```sh
lhy lint -p <project-root-dir> -l cmake cxx
```

### Ignore no-source directories

In a project, there are typically subdirectories that do not contain source code.

By default, `lhy-formatter-linter` ignores the following directories at the top level under the project root directory:

* `.git`
* `build`
* `.vscode`
* `.cache`
* `.pytest_cache`

Users can add custom subdirectories to ignore using the optional argument `-id` or `--ignore-dirs`. The format of the subdirectories to ignore can be either an absolute path or a relative path to the project root directory.


```sh
lhy format -p <project-root-dir> --ignore-dirs .github py_venv <project_root_dir>/docs
```

```sh
lhy lint -p <project-root-dir> --ignore-dirs <project_root_dir>/.github  <project_root_dir>/py_venv docs
```
Alternatively, users can specify a text file that contains the directories to ignore, with one directory per line.

For example, a file named `dirs-to-ignore.txt` could have the following content:

```
<project_root_dir>/.github
<project_root_dir>/py_venv
docs
```
Then, use the optional argument `-ig` or `--ignore-file` to specify the file containing the directories to ignore, which will be parsed by the formatter or linter.

```sh
lhy format -p <project-root-dir> --ignore-file dirs-to-ignore.txt
```

### Format or lint config files

By default, the formatter or linter will use the format or lint configuration files located directly under the project root directory.

Users can place their own custom format and lint configuration files directly under the project root directory to override the default settings and apply their own custom formatting or linting rules.


```sh

└── user
    ├── project_root_dir
    │   ├── src
    │   ├── .clang-format
    │   ├── .clang-tidy
    │   ├── .cmake-format
    │   ├── .flake8
    │   ├── .style.yapf
    │   └── .isort.cfg

```
Alternatively, users can specify the configuration file paths using the following optional arguments:

#### formatter config file path arguments
```sh
optional cmake format arguments:
  --cmake-format-config CMAKE_FORMAT_CONFIG
                        Path of cmake format custom config file (default: None)

optional c++ format arguments:
  --clang-format-config CLANG_FORMAT_CONFIG
                        Path of clang format custom config file (default: None)

optional python format arguments:
  --yapf-config YAPF_CONFIG
                        Path of yapf custom config file (default: None)
  --isort-config ISORT_CONFIG
                        Path of isort custom config file

```

```sh

lhy format -p <project-root-dir> \
    --cmake-format-config <cmake-format-config-absolute-file-path> \
    --clang-format-config <clang-format-config-absolute-file-path> \
    --yapf-config <yapf-config-absolute-file-path> \
    --isort-config <isort-config-absolute-file-path>
```

#### linter config file path arguments
```sh
optional cmake lint arguments:
  --cmake-lint-config CMAKE_LINT_CONFIG
                        Path of cmake lint custom config file (default: None)

optional c++ format arguments:
  --clang-tidy-config CLANG_TIDY_CONFIG
                        Path of clang tidy custom config file (default: None)

optional python format arguments:
  --flake8-config FLAKE8_CONFIG
                        Path of flake8 custom config file (default: None)
```

```sh

lhy format -p <project-root-dir> \
    --cmake-lint-config <cmake-lint-config-absolute-file-path> \
    --clang-tidy-config <clang-tidy-config-absolute-file-path> \
    --flake8-config <flake8-config-absolute-file-path>
```

## Integrate to CI

This package can be integrated into a Continuous Integration (CI) pipeline to ensure that all code on the remote repository conforms to the specified norms and standards.


### jenkins example.
```jenkins

stage('Check code') {
    agent any
    steps {
        sh 'lhy lint -p <project_root_dir>'
        sh 'lhy format -p <project_root_dir>'
        sh 'git diff --exit-code'
    }
}

```

# License

This project is licensed under the MIT License. For more information, please refer to the [LICENSE.md](https://github.com/sygslhy/coding_tools/blob/main/LICENSE.md) file.