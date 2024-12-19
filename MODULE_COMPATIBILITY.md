Module Compatibility
====================

### Copyright and License

This `MODULE_COMPATIBILITY.md` file is (c)2024 Michael A. Peters and licensed
under the ‘GNU Free Document License version 1.3’ as described in the
[`fdl-1.3.txt`](fdl-1.3.txt) file in the top level of this project directory.


RPM and Perl Module Compatibility
---------------------------------

An RPM package is basically an archive of the files to be installed with their
location on the file system, scripts that may need to automatically run when
that archive is installed, updated, or removed, and metadata about that archive
that includes information related to dependencies the package requires to
function and dependencies the package provides.

The Linux Standards Base (LSB) does not specify how an RPM package is supposed
to ensure a packaged Perl module will properly function within the Perl
environment of the GNU/Linux distribution it is being installed in.

For a Perl module to properly function, in addition to having the right Perl
version and Perl module dependencies met, the module must be installed within a
`@INC` directory that the operating system `perl` interpreter is configured to
use. The `@INC` path is a compile-time option that can and does differ between
GNU/Linux distributions even when the Perl version and architecture is the same.


Perl `@INC` Directories
-----------------------

When Perl is compiled, six *system-wide* `@INC` directories are defined with
compile-time options:

* __`-Dprivlib`__ defines where *architecture independent* Perl modules that are
  installed as part of ‘Perl Core’ are installed. In some cases, including in
  YJL, this is a sub-directory within `/usr/lib/perl5` but some GNU/Linux
  distributions put it in `/usr/share/perl5`.
* __`-Darchlib`__ defines where *architecture dependent* Perl modules that are
  installed as part of ‘Perl Core’ are installed. With some GNU/Linux
  distributions, including YJL, this is the same directory used for `-Dprivlib`
  but in the majority of RPM based GNU/Linux distributions it differs. On 64-bit
  systems it often is a sub-directory of `/usr/lib64/perl5` but on 32-bit and
  other non-multilib systems (including YJL) it *usually* is a sub-directory of
  `/usr/lib/perl5`.
* __`-Dvendorlib`__ defines where *architecture independent* Perl modules that
  are provided in a vendor package but are not installed with ‘Perl Core’ are
  installed. This is the correct location for RPM packaging of *architecture
  independent* CPAN distributions even when the RPM package updates a Perl
  module that was installed as part of ‘Perl Core’. In some cases, including in
  YJL, this is a sub-directory within `/usr/lib/perl5` but some GNU/Linux
  distributions put it in `/usr/share/perl5`.
* __`-Dvendorarch`__ defines where *architecture dependent* Perl modules that
  are provided in a vendor package but are not installed with ‘Perl Core’ are
  installed. This is the correct location for RPM packaging of *architecture
  dependent* CPAN distributions even when the RPM package updates a Perl
  module that was installed as part of ‘Perl Core’. With some GNU/Linux
  distributions, including YJL, this is the same directory used for
  `-Dvendorlib` but in the majority of RPM based GNU/Linux distributions it
  differs. On 64-bit systems it often is a sub-directory of `/usr/lib64/perl5`
  but on 32-bit and other non-multilib systems (including YJL) it *usually*
  is a sub-directory of `/usr/lib/perl5`.
* __`-Dsitelib`__ defines where *architecture dependent* Perl modules that are
  installed from source by the system administrator are installed. RPM packages
  have absolutely no business installing Perl modules in this `@INC` directory.
  Many GNU/Linux distributions define this directory to be within `/usr/local`
  but some may not.
* __`-Dsitearch`__ defines where *architecture dependent* Perl modules that are
  installed from source by the system administrator are installed. RPM packages
  have absolutely no business installing Perl modules in this `@INC` directory.
  Many GNU/Linux distributions define this directory to be within `/usr/local`
  but some may not.

In Yellow-Jacket GNU/Linux, the following compile-time arguments are used when
compiling the `perl` package:

* __`-Dsitelib=/usr/lib/perl5/perl5.x/core_perl`__
* __`-Dsitearch=/usr/lib/perl5/perl5.x/core_perl`__
* __`-Dvendorlib=/usr/lib/perl5/perl5.x/vendor_perl`__
* __`-Dvendorarch=/usr/lib/perl5/perl5.x/vendor_perl`__
* __`-Dsitelib=/usr/local/lib/perl5/perl5.x/site_perl`__
* __`-Dsitearch=/usr/local/lib/perl5/perl5.x/site_perl`__

This gives YJL three different site-wide `@INC` directories:

* `/usr/lib/perl5/perl5.x/core_perl`
* `/usr/lib/perl5/perl5.x/vendor_perl`
* `/usr/local/lib/perl5/perl5.x/site_perl`

The `5.x` represents the Perl version *without* the patch level. For example, in
YJL 6.6 which uses Perl 5.40, `5.40` would be used. Some GNU/Linux distributions
do include the patch level in their system-wide `@INC` directory definitions.

Other `@INC` can be defined by the user or by the Perl script to define
additional places for the Perl interpreter to search for Perl modules. For
example, it is very common for users to install additional Perl modules in their
home directory for their own use. Some third party vendors *may* define their
own system-wide `@INC` directory within `/opt` though that seems to be generally
be avoided by third-party vendors and I suspect with good reason.


The RPM Module Compatibility Problem
------------------------------------

Different GNU/Linux distributions define those compile-time options differently
and I do not believe the LSB *or any other generic specification* has any
business dictating what those compile-time options should be.

Thanks to the power of RPM Macros, it is possible to write generic RPM spec
files that will install the modules in the proper location for the GNU/Linux
distribution the RPM spec file is built on. However once the RPM is built, the
installable RPM must be restricted to systems that use the same `@INC` scheme
at least for `-Dvendorlib` or `-Dvendorarch` depending upon whether or not
the package is architecture independent or not.

Unfortunately the LSB does not specify a mechanism for ensuring that an
installable Perl RPM was built using a suitable `@INC` scheme for the system the
RPM is being installed on.

The method most commonly used is what I call the ‘Red Hat Way’ although I do not
know if Red Hat was the first to use it. All Red Hat systems I have used and
most other RPM distributions support this method. YJL supports it too for the
sake of compatibility but it is not the method implemented by YJL for YJL
Perl modules.


The ‘Red Hat Way’
-----------------

The ‘Red Hat Way’ of dealing with the issue is pretty standard across RPM based
GNU/Linux distributions but I believe is insufficient.

With the ‘Red Hat Way’ the main `perl` RPM has the following `Provides:`:

    Provides: perl(:MODULE_COMPAT_%{version})

where `%{version}` __MUST__ be the ‘three-part’ version number variant. The
reason why it __MUST__ be the ‘three-part’ version number variant is because
Perl module RPM spec files will then have the following `Requires:`

    Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))

The expression

    %(eval `perl -V:version`; echo $version)

*always* evaluates to the ‘three-part’ version number variant of Perl on the
build system.

This restricts the RPM to the same maintenance patch level of Perl used to build
the RPM but there are two problems with that method:

1. It does not verify that the same `@INC` scheme was used. This can result in
   an RPM that installs but for which the module is installed in a directory
   that `perl` does not search.
2. It means that every single package that includes a Perl module must be
   updated every time a new patch level maintenance release of Perl is
   provided.

The way that most RPM based GNU/Linux distributions deal with the second issue
is they rarely provide new patch level maintenance releases, instead opting to
backport bug fixes into the ‘three-part’ version number they originally
shipped. It works, but it certainly is not KISS, and it means that there is an
inconsistency in how a particular ‘three-part’ version behaves across different
operating systems. This can cause a problem when a Perl module requires a
specific patch level because it depends upon a fix that took place in a specific
patch level. It may be a current ‘defacto’ standard practice among GNU/Linux
distributions but it is dirty and I do not like it.


The ‘YJL Way’
-------------

YJL defines two macros that currently are YJL specific but they do not have to
be.

### `%perl5_API`

The `perl5_API` macro is defined as:

    perl(:%{perl5_version}:%{perl5_vendorlib})

The `%{perl5_version}` macro on YJL expands to `5.x` (e.g. 5.40) but if a
distribution wants to force a rebuild of every single RPM containing a Perl
module every time a new patch level maintenance release is made available,
that distribution is free to do so.

The `%{perl5_vendorlib}` macro is a standard vendor independent macro that
expands to the `@INC` directory defined by the `-Dvendorlib` Perl compile-time
flag.

The YJL `perl` package has the following `Provides:`

    Provides: %{perl5_API} = %{triplet}

The `%{triplet}` macro is the ‘three-part’ version number variant of Perl.

Architecture independent Perl modules then can have the following:

    Requires: %{perl5_API}

That ties the RPM to both the version of perl and the proper `@INC` scheme for
architecture independent Perl modules.

It is generally okay to leave the `Requires:` versionless but it can be set to
specify the minimum version of Perl. For example:

    Requires: %{perl5_API} >= 5.8.1

### `@perl5_ABI`

The `perl5_ABI` macro is defined as:

    perl(:%{perl5_version}:%{perl5_os_platform}:%{perl5_vendorarch})

The `%{perl5_os_platform}` macro expands to `%{_arch}-linux-thread-multi`
(`x86_64-linux-thread-multi` on 64-bit systems) and `%{perl5_vendorarch}` is a
standard vendor independent macro that expands to the `@INC` directory defined
by the `-Dvendorarch` Perl compile-time flag.

The YJL `perl` package has the following `Provides:`

    Provides: %{perl5_API} = %{triplet}

Architecture dependent Perl modules then can have the following:

    Requires: %{perl5_ABI}

That ties the RPM the the version of perl, the operating system platform, and
the proper `@INC` scheme for architecture dependent Perl modules.

It is generally okay to leave the `Requires:` versionless but it can be set to
specify the minimum version of Perl. For example:

    Requires: %{perl5_ABI} >= 5.8.1


