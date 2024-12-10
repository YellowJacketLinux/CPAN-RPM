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

### Copyright and License

This README file is (c)2024 Michael A. Peters and licensed under the ‘GNU Free
Document License version 1.3’ as described in the `fdl-1.3.txt` file in the top
level of this project directory.

All RPM spec files in this project are licensed under Creative Commons ‘CC0 1.0
Universal’ (effectively Public Domain). See the file `LICENSE` in the `SPECS`
directory of this project.

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

The RPM spec files in this repository provide two ways to bind an RPM package
to the version of Perl the RPM was built for.

The ‘Red Hat Way’ (which I believe is also used by most other RPM-based
GNU/Linux distributions) is to put the following in the `.spec` file:

    Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))

That means the distribution `perl` package has to have that as a virtual
provide. The `.spec` files in this directory fall back to that method if the
operating system does not use the YJL method for ensuring the Perl module will
work.

The first issue I have with that method is that `perl -V:version` gives the
integer triplet version of Perl but the last part of the triplet is just the
*patch level* and a new Perl maintenance release with a higher *patch level*
should not require all add-on modules be rebuilt.

The second issue I have with the ‘Red Hat Way’ is it does not ensure the RPM
package is placing the modules within the proper Perl `@INC` directory, which
can and does vary between GNU/Linux distributions.

YJL defines the following macros, in the same place where `%perl5_vendorlib`
and `%perl5_vendorarch` are defined:

    %perl5_os_platform %{_arch}-linux-thread-multi
    %perl5_API perl(:%{perl5_version}:%{perl5_vendorlib})
    %perl5_ABI perl(:%{perl5_version}:%{perl5_os_platform}:%{perl5_vendorarch})

The latter two, `%perl5_API` and `%perl5_ABI`, expand to values provided by the
YJL `perl` RPM package, and thus can be used as module compatibility requires
in module packages.

The macro `%{perl5_version}` on YJL expands to the version of Perl *without*
the patch level (e.g. `5.36` on YJL 6.1 and `5.40` on YJL 6.6) but for others
implementing the same system, it is okay if you put the full version
*including* the patch level if implementing the same scheme in another OS
distribution.

These macros include the Perl `@INC` directory that RPM packages will put their
module files into, thus ensuring that the package only installs on systems
where it will actually be usable after installation.

For `noarch` RPM packages, I use

    Requires: %perl5_API

For `x86_64` RPM packages, I use

    Requires: %perl5_ABI

The RPM `.spec` files in this project *only* use those `Requires` if they are
defined. Otherwise, they fall back to the ‘Red Hat Way’ which works, but just
is not ideal.

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
an underscore. With CPAN packages that start with a `v`, the `v` should be
omitted from the RPM package `Version:` metadata. When a package contains an
an `_` underscore in the version, it is a test release and *probably* should
not be packaged *however* if it is packaged, the `_` should be omitted. Perl
itself ignores the underscore in its own version comparison, it is purely
decorative for humans.

Perl version (except those that start with a `v`) are floating point decimal
numbers, so for example, `3.2` is seen as newer than `3.15`. However, RPM sees
these numbers as integer fields delimited by a `.` so `3.15` is seen as newer
than `3.2`. This can cause a problem.

At this point, *most* Perl developers on CPAN are aware of this issue and will
pad their version numbers with trailing zeros (e.g. `3.20` in the previous
example) so that the version sort order works with both Perl and with packaging
systems like RPM, but the possibility of an update to a package on CPAN looking
like it is an older version to RPM still exists.

If a CPAN update looks older to RPM because of how Perl sees versions, there
are two solutions I am aware of:

1. Pad the Perl version with trailing 0s so that it becomes a larger integer
   than the previous release. This solution avoids the need for an `Epoch:`
   metadata field, but it means the `Version:` metadata field no longer
   matches the tarball.
2. Use an `Epoch:` in the RPM spec file. That allows a `Version:` metadata
   field that matches the source tarball and while I dislike having to do it,
   I think it is the cleanest way to solve the issue.

Fortunately, at the start of this project, most CPAN authors are aware of the
issue and pad the version themselves, so hopefully a remedy by the RPM packager
will rarely be needed.

When a Perl version starts with a `v`, that actually tells the Perl version
parser that the version is integer fields delimited by a `.` which is exactly
how RPM already views versions, so removing the `v` from the `Version:` field
is both safe and avoids RPM from interpreting the `v` as part of the version
which would invoke string comparisons instead of integer comparisons.

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

#### License

Most of my current spec files as they sit in my home directory do this
incorrectly. Cleanup is underway, this is important to do correctly.

When a CPAN distribution comes with a proper `LICENSE` (or related) file, life
is good. That file should be included in the `%files` section using *both* the
`%license` macro __and__ the `%doc` macro. When the license has a SPDX
identifier (see https://spdx.org/licenses/ ) that identifier should be used in
the RPM spec file `License:` field.

More than one package I have encountered have a `LICENCE` file that specifies
both ‘GPL 1.0 or later or Artistic 1.0’ but then in includes the text of the
GPL 2.0 license and the Artistic 1.0 license. Since that is the case with more
than just a few CPAN distributions I have to assume it is the result of a bug
in a program that generated the `LICENSE` file for the author.

In those cases due to the ambiguity, I pick the included license text and use:

    License: GPL-2.0-or-later or Artistic-1.0-Perl

Many distributions on CPAN specify the license terms but fail to include the
actual license text. In these cases, the actual license texts are added as a
source file (starting with `Source90`) and should be included with the
`%license` macro but they should *not* be included with the `%doc` macro as
they are not part of the original source code distribution.

Usually in these cases, the license is mention in the `README` file but in some
cases I have to hunt for it in a module POD.

What needs to happen, is in the `%prep` section of the spec file, a new file
need to created that extracts the specified license terms *and* specifies what
file the terms were extracted from that can also be packaged using the
`%license` macro.

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

When defining the `BuildRequires:` fields, I assume that the following four
modules are available on the system building the RPM spec file:

* `perl(Test)`
* `perl(Test::Harness)`
* `perl(strict)`
* `perl(warnings)`

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

    BuildRequires: perl(:VERSION) >= 5.m.n

Where `m` is the second integer in the triplet and `n` is the patch level
integer in the triplet.

Sometimes the minimum Perl version is specified as a float, so you may need
to convert it.

When described as a float, pad it with zeros to six decimal places. Then the
first three decimals after the dot correspond with `m` and the second set of
three correspond with the `n`. For example:

    use 5.00801  = use 5.008010 is the triplet 5.8.10
    use 5.04     = use 5.040000 is the triplet 5.40.0
    use 5.00504  = use 5.005040 is the triplet 5.5.40

Sometimes, the minimum Perl version is specified with a leading `v` in which
case no padding is necessary, but if it only specifies two parts of the
triplet, you should add a zero as the third. For example:

    use v5.8 is the triplet 5.8.0

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

With the noted exception of `perl(strict)` and `perl(warnings)` I believe it is
a ‘Best Practice’ to add all runtime dependencies as `BuildRequires` as well as
adding them as `Requires` even if they technically are not needed to install
and test the module.

All Perl modules that are runtime dependencies need to be specified as runtime
dependencies with a `Requires:` field. Assumptions about what is already
installed *should not be made*.

For runtime dependencies, I do include `perl(strict)` and `perl(warnings)` when
they are runtime dependencies.

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

The RPM spec file (and resulting `.src.rpm`) *hopefully* will be buildable on
most RPM based GNU/Linux distributions with the minimum required Perl version
but the installable RPM package will only work on distributions with the same
Perl version *and* `@INC` scheme for vendor packaged modules.

To avoid the installable RPM package installing on GNU/Linux distributions with
a different Perl version and/or `@INC` scheme, the RPM spec file needs to have
a conditional block.

#### `.noarch.rpm` target:

    %if 0%{?perl5_API:1} == 1
    Requires: %{perl5_API}
    %else
    Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
    Requires: %{perl5_vendorlib}
    %endif

On YJL and other system that use the previously described `%{perl5_API}` macro,
that macro limits where it can be installed. For distributions without that
macro, it falls back to the ‘Red Hat Way’ with the additional requirement of
ensuring the directory defined by `%{perl5_vendorlib}` exists for use.

#### Binary target:

    %if 0%{?perl5_API:1} == 1
    Requires: %{perl5_ABI}
    %else
    Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
    Requires: %{perl5_vendorarch}
    %endif

On YJL and other system that use the previously described `%{perl5_ABI}` macro,
that macro limits where it can be installed. For distributions without that
macro, it falls back to the ‘Red Hat Way’ with the additional requirement of
ensuring the directory defined by `%{perl5_vendorarch}` exists for use.


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


CPAN Distribution Build
-----------------------

There may be more, but there are four systems for building and installing CPAN
distributions that are commonly encountered. Listed in the order of how
frequently I encounter them:

* `perl(ExtUtils::MakeMaker)` *(part of “Perl Core”)*
* `perl(Module::Build)` *(formerly part of “Perl Core”)*
* `perl(Module::Build::Tiny)`
* `perl(inc::Module::Install)` *(A wrapper for `ExtUtils::MakeMaker`)*

When a CPAN distribution has a `Makefile.PL` script, it *probably* uses either
`ExtUtils::MakeMaker` or `inc::Module::Install` as the build system. If there
is *also* a `Build.pl` script, ignore the presence of the `Makefile.PL` script.

When a CPAN distribution has a `Build.PL` script, it uses either `Module::Build`
or `Module::Build::Tiny`.

When a CPAN distribution contains both, it uses `Module::Build` but has a
compatibility wrapper allowing `ExtUtils::MakeMaker` to be used. Do not use the
compatibility wrapper, just use `Module::Build` to build it.

The system used is easily identified at the top of the `Makefile.PL` or
`Build.PL` script. It needs to be a `BuildRequires`, I like to put it right
after the `BuildRequires: perl-devel` so that it is easy to identify the CPAN
build system used when reading the spec file. For example:

    BuildRequires: perl(:VERSION) >= 5.8.1
    BuildRequires: perl-devel
    BuildRequires: perl(Module::Build::Tiny)
    %if 0%{?!cpansigverify_skip:1} == 1
    BuildRequires: cpansign >= 0.82
    %endif
    #

All other `BuildRequires` then follow *preferably* in alphabetical order.

### The `%build` Section for `Makefile.PM`

For `ExtUtils::MakeMaker` and `inc::Module::Install` the `%build` section is
identical and *generally* should look like this:

    PERL_MM_USE_DEFAULT=1   \
    BUILDING_AS_PACKAGE=1   \
    perl Makefile.PL        \
         INSTALLDIRS=vendor \
         NO_PACKLIST=1      \
         NO_PERLLOCAL=1     \
         OPTIMIZE="$RPM_OPT_FLAGS"
    make %{?_smp_mflags}

The `PERL_MM_USE_DEFAULT=1` environmental variable tells `Makefile.PM` that you
do not want an interactive build, and to use defaults where it might ask you
questions.

The `BUILDING_AS_PACKAGE=1` environmental variable is meaningless to *most* CPAN
distributions but for a few, it tells the the script that was is being built is
a package and not to do stuff inappropriate for a package. As far as I can tell,
of all the CPAN packages I have built, only `ExtUtils::MakeMaker` itself has
cared about that setting. It *may* not be needed for any other package.

The `INSTALLDIRS=vendor` arguement tells `Makefile.PM` that the perl modules
should be installed in the vendor `@INC` directory, which is specifically for
Perl modules installed from an installation package.

The `NO_PACKLIST=1` argument tells `Makefile.PL` not create a `.packlist` file.
Those files are not meaningful to RPM managed installs, and are broken when a
`DESTDIR` is used, so they should not be generated.

The `NO_PERLLOCAL=1` argument tells `Makefile.PL` not to update the
`perllocal.pod` file, which it should not do when building a package.

The `OPTIMIZE="$RPM_OPT_FLAGS"` arguement may actually not be needed with
modern versions of Perl/MakeMaker, as it seems to get the right flags to use
from how Perl itself was configured, but it still does not hurt to have it.
Generally, `$RPM_OPT_FLAGS` tend to be a little more aggressive than default
flags with respect to security (e.g. `-D_FORTIFY_SOURCE=2` and
`-fstack-protector-strong`) and are good to use. Of course with `.noarch`
packages that option is meaningless, but it does not hurt either.

Sometimes, specific CPAN distributions will need a modification to the above
`%build` section. Typically additional options can be discovered by reading the
`INSTALL` file (if present), the `README` file, or the `Makefile.PL` file.

`make %{?_smp_mflags}` builds the package.

### The `%build` Section for `Build.PM`

For `Module::Build` and `Module::Build::Tiny` the `%build` section is *almost*
identical. For `Module::Build` it *generally* should look like this:

    %build
    PERL_MM_USE_DEFAULT=1   \
    MODULEBUILDRC=/dev/null \
    perl Build.PL --installdirs vendor
    ./Build

The `PERL_MM_USE_DEFAULT=1` environmental variable tells `Build.PL` that you do
not want an interactive build, and to use defaults where it might ask you
questions.

The `MODULEBUILDRC=/dev/null` environmental variable ensures that
`Module::Build` does not use a local configuration you might happen to have as
a result of locally building Perl modules outside of RPM.

That line is not needed for `Module::Build::Tiny` as it already does not make
use of such configuration files.

The `--installdirs vendor` option tells `Build.PL` that the perl modules should
be installed in the vendor `@INC` directory, which is specifically for Perl
modules installed from an installation package.

The final `./Build` line builds the package.

Sometimes, specific CPAN distributions will need a modification to the above
`%build` section. Typically additional options can be discovered by reading the
`INSTALL` file (if present), the `README` file, or the `Build.PL` file.

### The `%install` Section for `Makefile.PM`

For `ExtUtils::MakeMaker` and `inc::Module::Install` the `%install` section is
identical and *generally* should look like this:

    %install
    make install DESTDIR=%{buildroot}

The `DESTDIR=%{buildroot}` causes the Perl module to be installed in the RPM
build root where it can then be packaged as an installable RPM archive.

### The `%install` Section for `Build.PM`

Again, for `Module::Build` and `Module::Build::Tiny` the `%install` section is
*almost* identical. For `Module::Build` it *generally* should look like this:

    %install
    ./Build pure_install --destdir %{buildroot}
    find %{buildroot} -type f -name .packlist -delete

The `--destdir %{buildroot}` causes the Perl module to be installed in the RPM
build root where it can then be packaged as an installable RPM archive.

The `pure_install` option tells `Module::Build` to just do an install, do not
also update the `perllocal.pod` file.

With `Module::Build::Tiny` the `pure_install` option does not exist, you have
to use `install` instead of `pure_install`. It does not try to update the
`perllocal.pod` file.

The `find %{buildroot} -type f -name .packlist -delete` line removes the
unneeded (and broken) `.packlist` file that both `Module::Install` and
`Module::Build::Tiny` both install.

### The `%check` Section for `Makefile.PM`

For `ExtUtils::MakeMaker` and `inc::Module::Install` the `%check` section is
identical and *generally* should look like this:

    %check
    make test > %{name}-make.test.log 2>&1

This redirect of the `make test` output to `%{name}-make.test.log` allows the
test output to be packaged in the `%files` section using the `%doc` macros so
that users who have installed the package can inspect the test log for
themselves.

Sometimes, setting an environmental variable when running the test suite will
cause more extensive testing to take place, such as in the `Type::Tiny` CPAN
distribution where setting `EXTENDED_TESTING=1` triggers additional testing.

### The `%check` Section for `Build.PM`

For `Module::Build` and `Module::Build::Tiny` the `%check` section is
identical and *generally* should look like this:

    %check
    ./Build test > %{name}-make.test.log 2>&1

This redirect of the `make test` output to `%{name}-make.test.log` allows the
test output to be packaged in the `%files` section using the `%doc` macros so
that users who have installed the package can inspect the test log for
themselves.

Sometimes, setting an environmental variable when running the test suite will
cause more extensive testing to take place.

### DynaLoad Bootstrap Files and `Build.PM`

When building XS modules, both `Module::Build` and `Module::Build::Tiny` will
create a DynaLoad Bootstrap file that has an identical path as the binary
shared object file, and share the same filename except it uses a `.bs`
extension instead of a `.so` extension.

This bootstrap file is typically empty and should not be needed on GNU/Linux
systems. In the `%files` section of the spec file, it should be excluded from
packaging using the `%exclude` macro.


The `%files` Section
--------------------

Foo
