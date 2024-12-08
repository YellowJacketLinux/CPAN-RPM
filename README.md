RPM Spec Files for CPAN distributions
=====================================

### Document Note

This document does not exceed 80 characters in width *however* it does use a
few multi-byte characters (all from ISO-8859-15) that may cause some lines to
exceed 80 characters in width on systems without native font support for those
glyphs in their console font.

### Copyright and License

All RPM spec files in this project a Creative Commons ‘CC0 1.0 Universal’
(effectively Public Domain). See the file `LICENSE` at the top level of this
project. However some files in the `SOURCES` directory are not.

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
the Perl version integer triplet (e.g. `5.8.1` opposed to the float `5.008001`).

Due to the epoch mess caused by Perl’s use of a float for their version
number (pun intended), the `perl(:VERSION)` virtual provide is the *only* way
to check the version of Perl in an RPM-compatible way. As far as I know, every
RPM-based GNU/Linux distribution defines that virtual provides in the RPM
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

Foo


    



