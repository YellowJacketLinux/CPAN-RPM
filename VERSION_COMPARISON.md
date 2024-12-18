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

RPM likes to view a version as fields delimited by a period. This version
number `2.54` to RPM is a version with two fields, the first field being `2` and
the second field being `54`.

Unless specifically signalled to do otherwise with a leading `v`, Perl likes to
view a version as a floating point number.

In RPM, the version `2.54` is seen as a newer version than the version `2.6`
becaise with the first field (`2`) being equal for both, `54` is larger than `6`
so `2.54` corresponds with the newer version.

With Perl however, the float `2.6` is larger than the float `2.54` so `2.6` is
seen as the newer version.

This difference in version comparison methods can cause problems.


