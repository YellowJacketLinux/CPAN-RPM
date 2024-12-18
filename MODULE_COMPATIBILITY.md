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
* __`Dsitearch`__ defines where *architecture dependent* Perl modules that are
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

Other `@INC` can be defined by the user or by the Perl script to define
additional places for the Perl interpreter to search for Perl modules. For
example, it is very common for users to install additional Perl modules in their
home directory for their own use. Some third party vendors *may* define their
own system-wide `@INC` directory within `/opt` though that seems to be generally
be avoided by third-party vendors and I suspect with good reason.


The RPM Module Compatibility Problem
------------------------------------

Foo


The ‘Red Hat Way’
-----------------

The ‘Red Hat Way’ of dealing with the issue is pretty standard across RPM based
GNU/Linux distributions but I believe is insufficient.
