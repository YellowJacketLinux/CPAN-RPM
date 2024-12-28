CPAN Distribution Build
=======================

### Copyright and License

This `BUILD_INSTALL_CHECK.md` file is (c)2024 Michael A. Peters and licensed
under the ‘GNU Free Document License version 1.3’ as described in the
[`fdl-1.3.txt`](fdl-1.3.txt) file in the top level of this project directory.


Build Systems
-------------

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

The `INSTALLDIRS=vendor` argument tells `Makefile.PM` that the Perl modules
should be installed in the vendor `@INC` directory, which is specifically for
Perl modules installed from an installation package.

The `NO_PACKLIST=1` argument tells `Makefile.PL` not create a `.packlist` file.
Those files are not meaningful to RPM managed installs, and are broken when a
`DESTDIR` is used, so they should not be generated.

The `NO_PERLLOCAL=1` argument tells `Makefile.PL` not to update the
`perllocal.pod` file, which it should not do when building a package.

The `OPTIMIZE="$RPM_OPT_FLAGS"` argument may actually not be needed with
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

The `--installdirs vendor` option tells `Build.PL` that the Perl modules should
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
shared object file, and share the same file name except it uses a `.bs`
extension instead of a `.so` extension.

This bootstrap file is typically empty and should not be needed on GNU/Linux
systems. In the `%files` section of the spec file, it should be excluded from
packaging using the `%exclude` macro. For example:

    %attr(0555,root,root) %{perl5_vendorarch}/auto/Class/Plain/Plain.so
    %exclude %{perl5_vendorarch}/auto/Class/Plain/Plain.bs

If a Perl XS module needs to link to shared library in a non-standard location,
the *proper* solution is for that non-standard location to be configured in a
`/etc/ld.so.conf.d/` file rather than using a DynaLoad bootstrap file.


