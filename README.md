RPM Spec Files for CPAN distributions
=====================================

### Document Note

This document does not exceed 80 characters in width *however* it does use a
few multi-byte characters (all from ISO-8859-15) that may cause some lines to
exceed 80 characters in width on systems without native font support for those
glyphs in their console font. The actual character encoding of this document is
UTF8, but it can be converted to ISO-8859-15 (or Windows/CP-1252) without glyph
changes.

### Copyright and License

All RPM spec files in this project are licensed under Creative Commons ‘CC0 1.0
Universal’ (effectively Public Domain). See the file `LICENSE` at the top level
of this project. Files in the `SOURCES` directory however typically do not fall
under that license.

Any patches in the `SOURCES` directory fall under the same license as the CPAN
distribution they patch, and license files within that directory (for CPAN
distributions that mention a license but do not include it) are copyright by
their respective owners.

Git Purpose Description
-----------------------

In Yellow Jacket GNU/Linux, perl module distributions from CPAN will be
provided from a separate package repository from the main operating system
package repository.

This separate package repository will require the main operating system package
repository (for perl itself, and for shared libraries some XS modules link
against, and even occassionally an executable) and likewise, some packages in
the main operating system RPM package repository will require the CPAN package
repository (such as `git`, for its perl modules and for its `/usr/libexec/git`
perl scripts).

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

The following perl-specific RPM macros are expected to be defined on the system
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
package is placing the modules within the proper perl `@INC` directory, which
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

1. Pad the perl version with trailing 0s so that it becomes a larger integer
   than the previous release. This solution avoids the need for an `Epoch:`
   metadata field, but it means the `Version:` metadata field no longer
   matches the tarball.
2. Use an `Epoch:` in the RPM spec file. That allows a `Version:` metadata
   field that matches the source tarball and while I dislike having to do it,
   I think it is the cleanest way to solve the issue.

Fortunately, at the start of this project, most CPAN authors are aware of the
issue and pad the version themselves, so hopefully a remedy by the RPM packager
will rarely be needed.

When a perl version starts with a `v`, that actually tells the Perl version
parser that the version is integer fields delimited by a `.` which is exactly
how RPM already views versions, so removing the `v` from the `Version:` field
is both safe and avoids RPM from interpreting the `v` as part of the version
which would invoke string comparisons instead of ingeger comparisons.

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
















    



