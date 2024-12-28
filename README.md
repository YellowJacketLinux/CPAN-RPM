RPM Spec Files for CPAN distributions
=====================================

### Document Note

This document does not exceed 80 characters in width *however* it does use a
few multi-byte characters (all from ISO-8859-15) that may cause some lines to
exceed 80 characters in width on systems without native font support for those
glyphs in their console font. The actual character encoding of this document is
UTF8, but it can be converted to ISO-8859-15 (or Windows/CP-1252) without glyph
changes. Converting this document to ISO-8859-15 *may* fix the display of those
multi-byte characters (curly apostrophe, single and double quotes) in GNU/Linux
consoles without a proper UTF-8 font available, as is sometimes the case when
booting without a GUI where bitmap fonts are used.

A Table of Contents and some structural cleanup is needed.

### Copyright and License

This `README.md` file is (c)2024 Michael A. Peters and licensed under the ‘GNU
Free Document License version 1.3’ as described in the
[`fdl-1.3.txt`](fdl-1.3.txt) file in the top level of this project directory.

All RPM spec files in this project are licensed under Creative Commons ‘CC0 1.0
Universal’ (effectively Public Domain). See the file [`LICENSE`](SPECS/LICENSE)
in the `SPECS` directory of this project.

Note that Files in the `SOURCES` directory however typically do not fall under
either of those licenses.

Any patches in the `SOURCES` directory fall under the same license as the CPAN
distribution they patch, and license files within that directory (for CPAN
distributions that mention a license but do not include it) are copyright by
their respective owners.


Git Purpose Description
-----------------------

In Yellow Jacket GNU/Linux, Perl module distributions from CPAN will be
provided from a separate package repository from the main operating system
package repository.

This separate package repository will require the main operating system package
repository (for Perl itself, and for shared libraries some XS modules link
against, and even occasionally an executable) and likewise, some packages in
the main operating system RPM package repository will require the CPAN package
repository (such as `git`, for its Perl modules and for its `/usr/libexec/git`
Perl scripts).

In some cases, RPM packages in this package repository will replace modules
that are installed as part of “Perl Core” packages. There are two reasons for
this:

1. CPAN has a newer version that fixes some issue.

2. In the “Perl Core” package, I can only *recommend* packages from CPAN that
   are not in core, but in this package repository, I can *require* them. For
   example, the CPAN distribution ‘libwww-perl’ is in “Perl Core” but there
   is no TLS functionality in “Perl Core”. The ‘libwww-perl’ distribution can
   make use of TLS functionality if the right CPAN distributions are
   installed, and TLS is critically important to have, so the RPM spec file
   for ‘libwww-perl’ in this package repository *requires* them and will
   replace the ‘libwww-perl’ provided by “Perl Core” even though they are the
   same version and functionally equivalent.

Most of the CPAN distributions in this repository however are *not* in “Perl
Core”.

Primarily I want to make sure everything Perl is needed for YJL core packages
to properly work (e.g. the previously mentioned dependencies for `git` to fully
function) and for proper TLS to be available.

Secondarily, I want to make things as painless as possible for users who need
to use `cpanm` or a related tool to install distributions from CPAN that are
not available in YJL as RPM packages. That means all four of the primarily used
installer (`ExtUtils::MakeMaker`, `Module::Build`, `Module::Build::Tiny`, and
`inc::Module::Install`) as well as `Alien`, `Moose` (and derivatives), and a
plethora of `Test::` and `Test2::` related distributions.

Finally but at the lowest priority, commonly used distributions from CPAN that
are not included by the previously mentioned objectives, to reduce how often a
user needs to use `cpanm` to install something they need.


RPM SPEC FILE SPECIFICATION
---------------------------

Please note that not all of RPM spec files currently meet my own specification.
This is because my own specification has evolved while creating them. Part of
the reason for this git repository is to allow myself to create issues I can
use to remind myself of what packages need adjusting.

### Build System Prerequisites

The following Perl-specific RPM macros are expected to be defined on the system
building the spec file:

* `%perl5_vendorlib` (base `@INC` directory for RPM-packaged non-core `noarch`
  Perl modules)
* `%perl5_vendorarch` (base `@INC` directory for RPM-packaged non-core
  hardware-specific Perl modules)

Those macro definitions are *traditionally* defined in an RPM macro file that is
owned by the `perl-devel` package. However I can not guarantee that all RPM
based GNU/Linux distributions do that. There *may* be a way to detect correct
settings for those if not defined (they correspond with Perl compile options)
but unless I am made aware that it is an issue, I assume those RPM macros are
defined on the system building one the RPM spec files in this project.

The `perl` package __MUST__ have the virtual `perl(:VERSION)` provide defined to
the Perl version integer triplet (e.g. `5.8.1` or `5.40.0` opposed to the float
`5.008001` or `5.040`).

Due to the epoch mess caused by Perl’s use of a float for their version
number (pun intended), the `perl(:VERSION)` virtual provide is the *only* way
to check the version of Perl in an RPM-compatible way. As far as I know, every
RPM-based GNU/Linux distribution defines that virtual provide in the RPM
package that contains the `%{_bindir}/perl` executable. That *should* be part
of the LSB standard but the LSB seems to be dead, with no new release since
2015.

#### Module Compatibility

So-called ‘Module Compatibility’ is to ensure that the packaged RPM will only
install on systems where it actually will work.

The `perl` RPM itself needs to provide for ‘Module Compatibility’.

The LSB unfortunately does not specify how this is to be done. The ‘defacto’
standard way is what I call the ‘Red Hat Way’ and all of the CPAN Perl RPM spec
files will work with the ‘Red Hat Way’ in the interest of compatibility.

However I have invented a new way I call the ‘YJL Way’ which does not have the
same limitations as the ‘Red Hat Way’. Please see the document
[`MODULE_COMPATIBILITY.md`](MODULE_COMPATIBILITY.md) for a detailed description
of the ‘Red Hat Way’, the ‘YJL Way’, and how RPM spec files can accomodate both
methods of ensuring ‘Module Compatibility’.

Even though the LSB does not require it, it is my *strong opinion* that all RPM
packaging of `perl` should accomodated the ‘Red Hat Way’ of providing ‘Module
Compatibility’ even if they also provide for the ‘YJL Way’. That way, end users
who need to rebuild a Fedora (or whatever) `src.rpm` will have an easier time
getting what they need.

### RPM Spec File Requirements

#### `%{cpanname}` related metadata

The very top (first) line of the RPM spec file should define the CPAN name of
the CPAN distribution being built. This is the name used in the source tarball.
The CPAN name is defined in the `cpanname` macro. For example:

    %global cpanname Math-Random-ISAAC

The `Name:` field of the main package *must* be defined as:

    Name:     perl-%{cpanname}

The RPM `.spec` file name should match. In the above example, the RPM file name
would be `perl-Math-Random-ISAAC.spec` to match the main package name.

The `URL:` field of the main package *must* be defined as:

    https://metacpan.org/dist/%{cpanname}

Many projects on CPAN have their own project homepage. However the CPAN link is
much less likely to change or vanish over time.

#### Version metada

The `Version:` field *must* match the version number in the source tarball
*unless* the version number in the source tarball starts with `v` or contains
an underscore.

Detailed information on how to handle the Perl versioning scheme in RPM is
documented in the file [`VERSION_COMPARISON.md`](VERSION_COMPARISON.md).

#### Release Metadata

This is the scheme used by Yellow Jacket GNU/Linux:

    Release:  %{?repo}0.rc1%{?dist}

The `%{?repo}` macro *if defined* must end with a `.` and the fairly standard
`%{?dist}` macro *if defined* must begin with a `.`. When defined, those macros
are defined on the build system, not in the RPM spec file.

In YJL, for the CPAN repository, `%{?repo}` expands to `3.cpan.` and for
YJL 6.6, %{?dist} expands to `.yjl606`. Obviously if building the RPM spec
files elsewhere, if those macros expand at all they will expand to something
different.

Between those build-system defined macros, non-test releases will have a non-
negative odd integer such as a `1`, `3`, `5`, etc.

Test releases will have a non-negative even integer such as a `0`, `2`, `4`,
etc. followed by a `.` which is then followed by either `dev` (Development) or
`rc` (Release Candidate) followed directly by a positive integer.

The way RPM evaluates strings, a leading `rc` will always be viewed as newer
than a leading `dev` so there is no need to increment the leading even integer
when moving from a `dev` release to a `rc` release of the same version.

In the `%changelog`, only the part of the `Release:` tag *between* the
`%{?repo}` and `%{?dist}` are used to identify the changelog entry.

#### Source Metadata

The `Source0:` field needs to point to the full URL of the source tarball from
CPAN. The ‘tarball’ part of the link should be expressed in terms of macros.
In most cases, it will be:

    %{cpanname}-%{version}.tar.gz

In the few cases where the version on CPAN starts with a `v` then instead:

    %{cpanname}-v%{version}.tar.gz

Note that the full link on CPAN includes the current maintainer of the CPAN
distribution as part of the hyperlink. Sometimes the current maintainer
changes, so that needs to be checked every time a spec file is updated to a
different version of the distribution.

#### Summary and Description

The `Summary:` field should generally not contain a summary that is longer than
70 characters in width.

The `%description` section should target lines that are at most 65 characters in
width and *never* exceed 70 characters in width.

For English `Summary:` and `%description` fields, it is best to only use
characters that are single-byte in UTF-8 (basically the ISO-8859-1 set of
glyphs) but sometimes using multi-byte glyphs is not avoidable.

For `Summary:` and `%description` fields in other languages, it often is not
possible to avoid the use of multi-byte glyphs.

Within the `%description` section, module names and functions and executables
should be encased within back-ticks and items of emphasis should be encased
with asterisks. For example:

    %description
    `Fubar::Foo::Bar` is a module that only exports the `fubar()`
    function. This module is very effective at messing up your Perl
    program, so only use it when you *want* things to seriously break.

Presently, *most* of the RPM spec files in this git project take their summary
and description directly from the POD for the main module in the distribution.
Sometimes that is appropriate but in other cases, it it not.

The summaries and descriptions need to be properly cleaned up before they can be
translated into other languages, which is something I hope to see happen. Call
me woke, but I really wish more people who do not speak English as their primary
language could read RPM package metadata in their preferred language.

#### Group Metadata

What to do with the `Group:` field in an RPM spec file is something I am still
pondering.

My present scheme is outlined in the file [GROUPS.md](GROUPS.md). Consider that
file subject to radical future change.

#### License

Most of my current spec files as they sit in my home directory do this
incorrectly. Cleanup is underway, this is important to do correctly.

When a CPAN distribution comes with a proper `LICENSE` (or related) file, life
is good. That file should be included in the `%files` section using *both* the
`%license` macro __and__ the `%doc` macro. When the license has a [SPDX
identifier](https://spdx.org/licenses/) that identifier should be used in
the RPM spec file `License:` field.

RPM itself does not specify that SPDX needs to be used but at least for ‘Free
Libre Open Source Software’ (FLOSS) using the SPDX identifier has become the
fairly standard mechanism for identifying the license, and with very good
reason: It greatly reduces confusion *when done correctly*.

More than one package I have encountered have a `LICENCE` file that specifies
both ‘GPL 1.0 or later or Artistic 1.0’ but then in includes the text of the
GPL 2.0 license and the Artistic 1.0 license. Since that is the case with more
than just a few CPAN distributions I have to assume it is the result of a bug
in a program that generated the `LICENSE` file for the author.

In those cases due to the ambiguity, I pick the included license text and use:

    License: Artistic-1.0-Perl or GPL-2.0-or-later

Many distributions on CPAN specify the license terms but fail to include the
actual license text. In these cases, the actual license text should be added as
a source file (starting with `Source90`) and should be included with the
`%license` macro but they should *not* be included with the `%doc` macro as
they are not part of the original source code distribution.

Usually in these cases, the license is mention in the `README` file but in some
cases I have had to hunt for it in a module POD. I wish more CPAN maintainers
understood the importance of including the actual license text as a file in
their CPAN distribution but I suppose it is what it is.

What needs to happen in cases where the license is referenced in a README or
module POD file: in the `%prep` section of the spec file, a new file needs to
be created that extracts the specified license terms *and* specifies what file
the terms were extracted from that can also be packaged using the `%license`
macro so that future lawyers etc. who need to know precisely what terms were
specified and where can easily find them in the source of the original CPAN
distribution.

BuildRequires, Requires, and Provides
-------------------------------------

Many GNU/Linux distributions have scriptlets that attempt to auto-detect what
Perl modules a package provides and depends upon. My experience with those
scriptlets is they *mostly* work but even though it is incredibly time
consuming, it is better to manually define Perl module dependencies. This does
result in some mistakes but I honestly think it is better.

The modules required to run the installer while creating the package always
need to be manually defined.

A difference in how Perl compares versions (as floats) with how RPM compares
versions can also be an issue, but rarely so these days and the solution is
generally easy.

When defining the `BuildRequires:` fields, I assume that the following two
modules are available on the system building the RPM spec file:

* `perl(Test)`
* `perl(Test::Harness)`

Any other modules that are needed to run the installer or the tests *must* be
explicitly specified with a `BuildRequires:` field.

### System Defined Perl Macros

All spec files must *explicitly* require the `perl-devel` package:

    BuildRequires: perl-devel

That ensures that the `%perl5_vendorlib` and `%perl5_vendorarch` macros are
defined.

### Minimum Perl Version

When the Perl module has a minimum Perl version that is needed, the spec file
*must* have

    BuildRequires: perl(:VERSION) >= 5.x.y

Where `x` is the second integer in the triplet and `y` is the patch level
integer in the triplet.

See the file [`VERSION_COMPARISON.md`](VERSION_COMPARISON.md) for information
on the ‘three-part’ (triplet) version number variant for Perl.

### Signature Verification

When a CPAN distribution has a `SIGNATURE` file, the RPM spec file *must*
contain the following conditional `BuildRequires:`

    %if 0%{?!cpansigverify_skip:1} == 1
    BuildRequires: cpansign >= 0.82
    %endif

That is so the `cpansign` can be used to verify the integrity of the CPAN
distribution. Build systems without an Internet connection will need to
define the `%{cpansigverify_skip}` macro so that verification is skipped. This
is the case with build systems like
[Mock](https://rpm-software-management.github.io/mock/). However for end-user
builds of a spec file or source RPM, signature verification should take place
and the `cpansign` utility is needed for that. End users who really do not
want to verify the integrity of the source tarball can define that macro in
their `~/.rpmmacros` file. They also should get their head examined.

Hopefully in the future, a mechanism for verifying signatures even in build
systems like Mock will be achievable. For now, the RPM packager will have to
make sure the signature is verified when the packager creates the `src.rpm`
that is then built by Mock.

### Tests

With a very few exceptions, all modules needed for running tests should have a
corresponding `BuildRequires:` field defined. The only exceptions are cases
where the module is broken or seriously deprecated or simply not applicable to
the operating system.

CPAN modules are developed by many different developers often years apart and
using vastly different versions of Perl on different operating systems. Running
as many of the test suites as possible is the best way to find potential issues
with running the module in your version of Perl in your operating system.

While it does not hurt to add them as `BuildRequires`, I do assume that both
`perl(Test)` and `perl(Test::Harness)` are available on the build system and do
not explicitly `BuildRequires` them.

The CPAN distributions *usually* specify what modules are needed to run the
test suite but often the list is incomplete. Manually checking is the only way
to be sure all needed modules for the tests have an appropriate `BuildRequires`
defined.

### Runtime Dependencies

I believe it is a ‘Best Practice’ to add all runtime dependencies as
`BuildRequires` as well as adding them as `Requires` even if they technically
are not needed to install and test the module.

All Perl modules that are runtime dependencies need to be specified as runtime
dependencies with a `Requires:` field. Assumptions about what is already
installed *should not be made*.

The CPAN distribution `META.yml` *usually* specify what non-Core runtime
dependencies are needed but they quite frequently make assumptions that modules
distributed as part of “Perl Core” are present. Sometimes they forget to specify
a module. The best thing to do, despite it being very time consuming, is to
manually check each module installed by the CPAN distribution for its
dependencies.

Sometimes a dependency is a fall-back dependency that is only needed if another
dependency is not met. If that other dependency already has a `Requires` in the
RPM spec file, there is not a need to also `Requires` the fall-back.

### Dependency Versions

When a dependency requires a specific version (or newer) of a Perl module, the
version is almost always a float. RPM however will interpret the version as
two integer fields delimited by a `.`. Most CPAN developers are aware of this
but it can sometimes be an issue.

When it is an issue, the solution is to pad the version in the `Provides` with
zeros and for any spec file that requires it, pad them with zeros as needed, so
that all `Requires` and `Provides` have the same number of decimal places.

A list of what modules need that treatment and how many decimals of padding are
needed will need to be maintained. At this point in time, it is quite rare. In
most historic cases, the CPAN developers have resolved it by incriminating the
number *before* the `.` and then being mindful to always use a fixed number of
decimal places so that the version sorts the same whether evaluated as a float
or as integer fields.

A small number of Perl modules use a `v` at the beginning of their version. In
those cases, the `v` should not be included in the `BuildRequires` or in the
`Requires`. Those modules have their version sorted the same way by Perl as by
RPM but including the `v` in the RPM versioning breaks that.

### Module Provides

In most cases, a Perl module will be of the same version as the CPAN
distribution it comes from. That can not however be assumed, sometimes they
differ *even when there is only one module*.

For each module that a CPAN distribution provides, you have to look at the
module itself for the defined version to use in the RPM spec file in the
associated `Provides:` field.

When that version starts with a `v`, do not use the `v` in the module version
that the RPM spec file specifies with a `Provides:` field. When that version
contains a `_`, do not use the `_` in the module version that the RPM spec file
specifies with a `Provides:` field.

In some cases, a module will not specify a version. Sometimes that is the case
with a module that should not be called by modules or scripts outside the
distribution but sometimes that is the case with modules that can be called by
modules or scripts outside the distribution.

When a module without a version is installed by a distribution, I usually do
have a `Provides:` field for it in the spec file, but I do not assign a version
to it.

Generally the assigned version in the `Provides:` field should match what is
specified in the source file containing the module, but in rare cases where the
version is a float that causes RPM to misidentify the module as older than a
previous release, it may be necessary to pad the end of the assigned version in
the RPM spec file with one or more zeros at the end.

Sometimes a single source file provides more than one module (more than one
`package` defined in the file). In such cases, I only create a single
`Provides:` that matches what is expected for the source file name.

### Module Install Compatibility

To ensure module compatibility with the installed version of Perl, see the
document [`MODULE_COMPATIBILITY.md`](MODULE_COMPATIBILITY.md) at the top
level of this directory.


The `%prep` section
-------------------

The first line of the `%prep` section uses the RPM `%setup` macro unpacks the
source tarball. Most of the time this is the proper command to use:

    %setup -q -n %{cpanname}-%{version}

In cases where the CPAN distribution version starts with a `v` use this instead:

    %setup -q -n %{cpanname}-v%{version}

If the CPAN distribution contains a `SIGNATURE` file, the spec file __MUST__
contain this conditional to verify the integrity of the distribution:

    %if 0%{?!cpansigverify_skip:1} == 1
    cpansign verify
    %endif

That way the `SIGNATURE` file is used to verify the integrity of the source
*unless* the `%{cpansigverify_skip}` macro has been defined.

If there are any patches to apply (which should be quite rare), patches should
only be applied *after* signature verification or the signature validation will
obviously fail.

If the CPAN distribution does not include the text of the license it specifies,
copy the source containing the license file into the unpacked source.

The `%prep` section of a CPAN distribution that includes a `SIGNATURE` file and
specifies the license as either GPL 1.0 or Artistic but does not include the
texts of those licenses would thus start like thus:

    %prep
    %setup -q -n %{cpanname}-%{version}
    %if 0%{?!cpansigverify_skip:1} == 1
    cpansign verify
    %endif
    cp %{SOURCE90} .
    cp %{SOURCE91} .


The `%build`, `%install`, and `%check` Sections
-----------------------------------------------

Please see the separate document
[`BUILD_INSTALL_CHECK.md`](BUILD_INSTALL_CHECK.md)


The `%files` Section
--------------------

For the main package (the Perl modules), the default file attributes are set to
to read only for all users. Many moons ago when I wanted to test an update by
installing locally from source in the ‘site’ `@INC` directory, I accidentally
used the ‘vendor’ `@INC` directory which over-wrote the RPM managed version of
the CPAN distribution. I do not know if denying write permission would actually
protect systems from that kind of mistake, but it might.

The `%files` section thus *always* begins like this:

    %files
    %defattr(0444,root,root,-)

Any file listed will then have `0444` permissions *unless* another attribute is
specifically set for the file.

XS modules need the execution bit set. It is possible they actually do not, but
at least historically with RPM, debug symbols would not be properly stripped
from binary files that did not have the execution bit set. So for any XS
modules, `%attr(0555,root,root)` is specified.

Manual pages could be installed with the default `0444` permissions but it is
customary for manual pages to have `0644` permissions so for manual pages, I do
set `%attr(0644,root,root)` to conform with traditional RPM packages of manual
pages.

The output of the tests during the build process is packaged with the following
line in the `%files` section:

    %doc %{name}-make.test.log

That allows the output of the test suite to be viewed at any point in the
future.


Sub-Packages
------------

At this time I am not allowing the Perl module part of a CPAN distribution to be
broken up into multiple sub-packages, although perhaps for some packages such as
`Alien` an argument could be made for breaking it up.

Executable scripts however *must* be put into a separate sub-package.

The main package *usually* should then use an RPM `Suggest:` field to suggest
that the executable script sub-package be installed, but sometimes it is better
to use `Requires:` and sometimes it is okay to do neither.

An executable script sub-package *usually* should either be named using the name
of the script it installs, or use the CPAN distribution name *without* the
`perl-` prefix.

An executable script sub-package *must* require the same same version and
release main package, and also should require any perl modules it uses and if
specified, the minimum version of Perl.

The executable scripts themselves should have `%attr(0755,root,root)` set and
should be installed in `%{_bindir}`.


End-Notes
---------

Not being satisfied with other Perl RPM packaging guidelines I have come across,
specifically their use of automatic filtering of `Provides:` and `Requires:`
and their use of `perl(:MODULE_COMPAT_<perl_version>)` which is patch-level
specific and does not bind the RPM to `@INC` structure, these packaging
guidelines are a __rough draft__ of my own set of Perl packaging guidelines for
CPAN distributions that I wish to enforce for Yellow-Jacket GNU/Linux.

There may be changes made in the future, but I figured it is better to at least
have *something* in the present I can use to validate my RPM spec files against.

The plan is also test whether or not these RPM spec files properly build in
Fedora 41 without modification.

Generally users of Fedora or any other GNU/Linux distribution should use the
packages their distribution provides *however* sometimes those packages are out
of date and sometimes they may not exist and sometimes there are other reasons
why a user might not want their OS vendor-provided packages. In those cases, the
users of those distributions *should* be able to build these spec files with
little or no modification needed.

### Importing Spec Files

Presently I have over 300 CPAN distribution spec files written, and more to
write. The intent is to import them ten at a time into the `incoming` branch of
this git repository where I will then make sure they meet the specification I
have provided here, and when they do, pull request them into the main git.

This will take a long time and I suspect will not be finished until some time
in February.
