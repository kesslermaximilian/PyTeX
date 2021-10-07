# PyTeX

Some hacky python scripts to simplify my LaTeX package writing.

## Usage

Write packages in `.pytex` format. The `PackageFormatter` class will then - given author and name of the package - read in and format the file to produce a ready to use LaTeX package `.sty` file.

As an example, see the [LatexPackages](https://github.com/kesslermaximilian/LatexPackages) repository where this is used.

## Macros
Here is a (possibly incomplete) list of the PyTeX macros currently supported. The examples assume that we create a package called `example.sty`, written by myself:

| macro name | explanation | example |
---|---|---
`__HEADER__(< package description>)` | inserts package header, including license and LaTeX package header | `\NeedsTexFormat{LaTeX2e}`<br/>`\ProvidesPackage{mkessler-example}[2021/10/07 - <description>]`
`__PACKAGE_NAME__` | inserts package name | `mkessler-example`
`__PACKAGE_PREFIX__` | inserts package prefix | `mkessler@example@`
`__PACKAGE_MACRO__(<macro-name>)`| declares internal package macro | `\mkessler@example@<macro-name>`
`__FILE_NAME__`| inserts package file name | `mkessler-example.sty`
`__AUTHOR__`| inserts package author | `Maximilian Keßler`
`__DATE__`| inserts compilation date in format `%Y/%m/%d` | `2021/10/07`
`__NEW_IF__(<name>,<value>)`| declares a new LaTeX if | `\ifmkessler@example@<name>\mkessler@example@<name><value>`
`__SET_IF__(<name>,<value>)`| sets the value of a LaTeX if | `\mkessler@example@<name><value>`
`__IF__(<name>)`| starts conditional | `\ifmkessler@example@<name>`
`__LANGUAGE_OPTIONS__`| inserts default language options | `\newif\mkessler@example@english\mkessler@example@englishtrue`<br/>`\DeclareOption{german}{\mkessler@example@englishfalse}`<br/>`\DeclareOption{ngerman}{\mkessler@example@englishfalse}`<br/>`\DeclareOption{english}{\mkessler@example@englishtrue}`
`__LANGUAGE_OPTIONS_X__`| inserts default language options with `xkeyval` | `\newif\mkessler@example@english\mkessler@example@englishtrue`<br/>`\DeclareOptionX{german}{\mkessler@example@englishfalse}`<br/>`\DeclareOptionX{ngerman}{\mkessler@example@englishfalse}`<br/>`\DeclareOptionX{english}{\mkessler@example@englishtrue}`
`__END_OPTIONS__`| process options and handle wrong options | `\DeclareOption*{\PackageWarning{mkessler-example}{Unknown '\CurrentOption'}`<br/>`\ProcessOptions\relax`
`__END_OPTIONS_X__`| process options with `xkeyval` | `\DeclareOptionX*{\PackageWarning{mkessler-example}{Unknown '\CurrentOption'}`<br/>`\ProcessOptionsX\relax`
`__ERROR__(<message>)` | output package error | `\PackageError{mkessler-example}{<message>}`
`__WARNING__(<message>)`| output package warning | `\PackageWarning{mkessler-example}{<message>}`
`__INFO__(<message>)`| output package info | `\PackageInfo{mkessler-example}{<message>}`