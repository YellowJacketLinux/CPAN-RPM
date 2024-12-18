Version Comparison
==================

### Copyright and License

This `VERSION_COMPARISON.md` file is (c)2024 Michael A. Peters and licensed
under the ‘GNU Free Document License version 1.3’ as described in the
[`fdl-1.3.txt`](fdl-1.3.txt) file in the top level of this project directory.


Version Comparison Issue
------------------------

When dealing with numeric version numbers, the RPM Package Manager (RPM) sorts
versions differently than the *typical* Perl version sorting scheme. In the
past this has caused issues, which is why all RPM based GNU/Linux distributions
have a non-zero `Epoch:` assigned to the `perl` RPM.

RPM likes to view a version as fields delimited by a period. The version number
`2.54` to RPM is a version with two fields, the first field being `2` and the
second field being `54`.

Unless specifically flagged to do otherwise with a leading `v`, Perl likes to
view a version as a floating point number.

In RPM, the version `2.54` is seen as a newer version than the version `2.6`
because with the first field (`2`) being equal for both, `54` is larger than `6`
so `2.54` corresponds with the newer version.

With Perl however, the float `2.6` is larger than the float `2.54` so `2.6` is
seen as the newer version.

This difference in version comparison methods can cause problems.

At this point in time, most CPAN maintainers are aware of the issue and will do
their best to avoid triggering the issue. For example, rather than update a
version from `2.54` to `2.6` they will instead update the version to `2.60` so
that it is seen as a newer version using either version comparison scheme.
However the issue can still crop up from time to time.


CPAN Distribution Version
-------------------------

When a CPAN distribution is packaged as an RPM package, the `Version:` metadata
field of the RPM __MUST__ match the CPAN version number in the CPAN tarball.
It is not allowed (by best practices, RPM itself does not really care) to pad
the `Version:` field in the RPM spec file with trailing zeros if the CPAN
distribution does not do so.

If the hypothetical CPAN distribution `Fubar-2.54.tar.gz` source tarball is
updated to `Fubar-2.6.tar.gz` then the only acceptable solution in the RPM
spec file is to use an `Epoch:` metadata tag to let RPM know that it is a newer
version of the `Fubar` distribution.

Hopefully that never needs to be done but the possibility exists that at some
point it may be needed. If the need arises, the CPAN maintainer should be
contacted first, they may be willing to push an update that pads the decimal
part of the version number with zeros to accommodate distribution packagers.

### Version with a leading `v`

A few CPAN distributions have version numbers with a leading `v`. That leading
`v` is not actually part of the distribution version but is a signal to Perl
that the distribution does not use floats for the version but instead uses a
period as a field delimiter, just like what RPM does natively. In those cases,
the `v` __*SHOULD NOT*__ be part of the RPM `Version:` metadata or else RPM
will use string comparisons for that field.


Perl Module Version
-------------------

In addition to the CPAN distribution version number, modules within a CPAN
distribution will *usually* also have a version number. More often than not,
this module number will match the CPAN distribution version number, but it does
not have to and sometimes it will be different.

The version of a Perl module provides is specified in the RPM spec file using
the `Provides:` metadata tag. For example:

    Provides: perl(Fubar::Foo::Bar) = 2.54

When a Perl module is updated to a newer version that does not look newer to
RPM, then you *must* pad with zeros to compensate, __NEVER__ use an epoch to
resolve the issue.

If `Fubar::Foo::Bar` is updated from `2.54` to `2.6` then the correct
`Provides:` tag to compensate is:

    Provides: perl(Fubar::Foo::Bar) = 2.60

Similarly, anything that has `Fubar::Foo::Bar` version `2.6` as a dependency
will need to require the padded number in the RPM spec file:

    Requires: perl(Fubar::Foo::Bar) >= 2.60

When padding is needed for RPM to understand the Perl versioning and do the
right thing, the module that requires the padding will have to have that padding
need noted. At present, I am only aware of it being an issue with a single core
module but I have to look up which module it is.


Underscore in Version Number
----------------------------

Some Perl modules, and perhaps even some CPAN distributions, have a single
underscore as part of the version. Ignore the underscore. It is there as a
visual indication that the module (or distribution) is a test release. For
version comparison purposes, pretend it does not exist.


Perl Version
------------

When the version of Perl itself needs to be specified in an RPM spec file
(usually as a `BuildRequires:` but on some occasions as a `Requires:` then the
so-called ‘three-part’ version number variant for Perl __*MUST*__ be used rather
than the float version number.

In the rare cases where a Perl script specifies the Perl version it wants using
a version that starts with a lower case `v` then the version number is already
in the ‘three-part’ version number variant. For example:

    use v5.8.1

That means `5.8.1` is the minimum ‘three-part’ version number variant for Perl
that is required. To require that version of Perl as a minimum `BuildRequires:`
it would be specified like this:

    BuildRequires: perl(:VERSION) >= 5.8.1

Note that sometimes the third part is not specified if zero:

    use v5.8

That means `5.8.0` is the minimum ‘three-part’ version number variant for Perl
that is required.

When a Perl version is specified by a Perl script, *usually* the float variant
of the Perl version is specified and RPM packagers have to convert the float
variant to the ‘three-part’ version number. This conversion method applies to
Perl itself, not to CPAN modules.

For Perl5, the float variant of the version number will be a `5` followed by a
dot and then followed by 1–6 decimal places. First pad it out (if needed) to
six decimal places. For example:

    use 5.00405

There are five decimal places, so the float would be padded out to `5.004050`.

The `5` represents the first number in the ‘three-part’ version number variant.
The first three decimal places *without the leading zeros* represent the second
number in the ‘three-part’ version number variant. The last three decimal places
*without the leading zeros* represent the third number in the ‘three-part’
version number variant.

Thus `5.008001` is equivalent to `5.8.1`, `5.04` is equivalent to `5.40.0`, and
`5.00405` is equivalent to `5.4.50`.

As far as I can tell, the Linux Standards Base (LSB) does not specifically
require the distribution `perl` RPM to provide `perl(:VERSION) = 5.x.y` but it
should, and every RPM based distribution I have looked at does in fact do that.



















