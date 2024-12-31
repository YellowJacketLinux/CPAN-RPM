Perl License Ambiguity Issues
=============================

When there is a legal question about a license, ALWAYS ask a lawyer who is
qualified to give legal advice on ‘Free Libre Open Source Software’ license
issues. The purpose of this file is *not* to provide legal guidance but merely
to attempt to explain decisions I made with the RPM packaging of CPAN software
distributions with what I consider to be license ambiguities.

The RPM Package Format has a `License` metadata field that is typically used
to specify the applicable software licenses using a string, typically the
SPDX Indentifier. Additionally, RPM provides a `%license` macro that should be
used to include license text files in the package.

Unfortunately software projects are not always very precise with respect to
license terms, coders are generally not lawyers.

There are several ambiguities in many CPAN modules. It appears that these are
primarily caused by bugs in software meant to automate the generation of LICENSE
files as the ambiguities tend to be identical across many different CPAN
distributions by different authors/maintainers.

Most of the ambiguities occur in cases where a `LICENSE` (or `LICENCE`) file
exists in the CPAN source that specifies ‘Perl 5 Terms’ but then includes text
of licenses that differ from ‘Perl 5 Terms’ licenses.

Some of the time, seemingly less than half, a `LICENSE` (or `LICENCE`) file
exists in the CPAN source that specifies ‘Perl 5 Terms’ and includes text that
does match the ‘Perl 5 Terms’ licenses. In those cases, there is no ambiguity.



Perl 5 Terms
------------

Many CPAN modules include text similar to the following:

    > This is free software; you can redistribute it and/or modify it under
    > the same terms as the Perl 5 programming language system itself.
    > 
    > Terms of the Perl programming language system itself
    > 
    > a) the GNU General Public License as published by the Free
    >    Software Foundation; either version 1, or (at your option) any
    >    later version, or
    > b) the "Artistic License"

This *should* translate to SPDX identifiers of ‘GPL-1.0-or-later’ (for case
`a)`) and ‘Artistic-1.0-Perl’ (for case `b)`) as those SPDX identifiers are
the proper identifiers for the versions of those licenses included with Perl 5.

When a CPAN distribution identifies ‘Perl 5 Terms’ but does not include the
license text, I feel comfortable specifying ‘Artistic-1.0-Perl’ and
‘GPL-1.0-or-later’ as SPDX dual-license terms, and including the text files
that correspond with those SPDX identifiers.

When a CPAN distribution identifies ‘Perl 5 Terms’ and then includes license
terms that differ, I feel it necessary to include this file and use SPDX
identifiers that reflect the included license, sometimes also including the
text of the ‘Artistic-1.0-Perl’ in a separate file.


Artistic 1.0
------------

There are three different commonly encountered versions of the Artistic 1.0
license.

What seems to be the ‘Original’ “Artistic 1.0” license has a SPDX identifier of
‘Artistic-1.0’ and is *different* than the version of the “Artistic 1.0”
license that ships with Perl 5, which has the SPDX identifier
‘Artistic-1.0-Perl’.

When a CPAN modules claims the same license terms as Perl but then includes the
text of the SPDX ‘Artistic-1.0’ license instead of the ‘Artistic-1.0-Perl’
license, I *suspect* the intent was ‘Artistic-1.0-Perl’ but if there is a
question, only the CPAN maintainer can properly clarify the situation, Yellow
Jacket GNU/Linux does not have the authority to clarify the situation.

YJL RPM spec files will specify both ‘Artistic-1.0’ and ‘Artistic-1.0-Perl’ as
SPDX identifiers as an argument can be made for either case. The original
`LICENSE` (or `LICENCE`) filr is packaged in the RPM with both the RPM
`%license` and `%doc` macros and the text of the ‘Artistic-1.0-Perl’ is included
in a file called `Artistic-1.0-Perl.txt` but is only packaged with the RPM
`%license` macro as it is not part of the original CPAN source distribution.

### ‘Artistic-1.0’ vs ‘Artistic-1.0-Perl’

The difference between ‘Artistic-1.0’ and ‘Artistic-1.0-Perl’ includes two
changes:

1. The latter has an expanded ‘Clause 7’ that adds some specificity:

    Artistic-1.0 Clause 7:

    7. C or perl subroutines supplied by you and linked into this Package shall
       not be considered part of this Package.

    Artistic-1.0-Perl Clause 7:

    7. C subroutines (or comparably compiled subroutines in other languages)
       supplied by you and linked into this Package in order to emulate
       subroutines and variables of the language defined by this Package shall
       not be considered part of this Package, but are the equivalent of input
       as in Paragraph 6, provided these subroutines do not change the language
       in any way that would cause it to fail the regression tests for the
       language.

2. The latter adds ‘Clause 8’:

    8. Aggregation of this Package with a commercial distribution is always
       permitted provided that the use of this Package is embedded; that is,
       when no overt attempt is made to make this Package’s interfaces visible
       to the end user of the commercial distribution. Such use shall not be
       construed as a distribution of this Package. 

In the event those differences impact your use of a CPAN distribution, please
contact the maintainer of the CPAN distribution for clarification. Yellow Jacket
GNU/Linux can not provide clarification for you.

### ‘Artistic-1.0-cl8’

There is a third variant of the “Artistic 1.0” license with a SPDX identifier of
‘Artistic-1.0-cl8’ but I have not *yet* seen that license used with CPAN
distributions. It has the added ‘Clause 8’ but lacks the expanded ‘Clause 7’.


Artistic 2.0
------------

As far as I can tell, there is only one variation of the “Artistic 2.0” license
in common use and it has an SPDX identifier of ‘Artistic-2.0’.

So far when the text of the “Artistic 2.0” license has been included in a CPAN
distribution, the intent has been pretty clear that the ‘Artistic-2.0’ SPDX
identifier is the license the module author wants used rather than one of the
three variations of the “Artistic 1.0” license.

When the text of the “Artistic 2.0” license is included, it is fairly safe to
assume that the CPAN author/maintainer meant “Artistic 2.0” and to in fact use
the ‘Artistic-2.0’ SPDX identifier.


GNU Public License
------------------

Many CPAN distributions specifically reference ‘GPL 1.0 or later’ but then they
include the text of the ‘GPL 2.0’ license.

In those cases, YJL uses ‘GPL-2.0-or-later’ as the SPDX identifier to match the
included license text.

If someone wants to use such a CPAN distribution under the terms of the GPL 1.0
license, that is between them and the CPAN author/maintainer, YJL does not care.
Specifying ‘GPL-2.0-or-later’ meets both ‘GPL 1.0 or later’ and the license text
included with the CPAN distribution, so that is the SPDX identifier we use in
these common cases.


__EOF__
