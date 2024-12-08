RPM Spec Files for CPAN distributions
=====================================

### Document Note

This document does not exceed 80 characters in width *however* it does use a
few multi-byte characters (all from ISO-8859-15) that may cause some lines to
exceed 80 characters in width on systems without native font support for those
glyphs in their console font.

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







