RPM Spec Files for CPAN distributions
=====================================

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

1.) CPAN has a newer version that fixes some issue.

2.) In the “Perl Core” package, I can only *recommend* packages from CPAN that
    are not in core, but in this package repository, I can *require* them. For
    example, the CPAN distribution ‘libwww-perl’ is in “Perl Core” but there
    is no TLS functionality in “Perl Core”. The ‘libwww-perl’ distribution can
    make use of TLS functionality if the right CPAN distributions are
    installed, and TLS is critically important to have, so the RPM spec file
    for ‘libwww-perl’ in this package repository *requires* them and will
    replace the ‘libwww-perl’ provided by “Perl Core” even though they are the
    same version and functionally equivalent.



