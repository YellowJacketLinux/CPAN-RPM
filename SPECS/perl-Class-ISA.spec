%global cpanname Class-ISA

Name:     perl-%{cpanname}
Version:  0.36
Release:  %{?repo}0.rc2%{?dist}
Summary:  Report the search path for a class's ISA tree
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl(:VERSION) >= 5.4.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(if)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.4.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(if)
Requires: perl(strict)
Requires: perl(vars)
#
Provides: perl(Class::ISA) = %{version}

%description
Suppose you have a class (like `Food::Fish::Fishstick`) that is
derived, via its `@ISA`, from one or more superclasses (as
`Food::Fish::Fishstick` is from `Food::Fish`, `Life::Fungus`, and
`Chemicals`), and some of those superclasses may themselves each
be derived, via its `@ISA`, from one or more superclasses (as
above).

When, then, you call a method in that class (`$fishstick->calories`),
Perl first searches there for that method, but if it's not there, it
goes searching in its superclasses, and so on, in a depth-first (or
maybe "height-first" is the word) search. In the above example, it'd
first look in `Food::Fish`, then `Food`, then `Matter`, then
`Life::Fungus`, then `Life`, then `Chemicals`.

This library, `Class::ISA`, provides functions that return that list
-- the list (in order) of names of classes Perl would search to find
a method, with no duplicates.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from README
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README


EOF

START=`grep -n "^COPYRIGHT AND LICENSE" README |cut -d":" -f1`
END=`grep -n "^AUTHOR" README |cut -d":" -f1`
DIFF="$((${END}-${START}))"
REND="$((${END}-1))"

head -${REND} README |tail -${DIFF} >> Perl-License-Extracted.txt


%build
PERL_MM_USE_DEFAULT=1   \
BUILDING_AS_PACKAGE=1   \
perl Makefile.PL        \
     INSTALLDIRS=vendor \
     NO_PACKLIST=1      \
     NO_PERLLOCAL=1
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorlib}/Class
%{perl5_vendorlib}/Class/ISA.pm
%attr(0644,root,root) %{_mandir}/man3/Class::ISA.3*
%license Artistic-1.0-Perl.txt GPL-1.0.txt Perl-License-Extracted.txt
%doc %{name}-make.test.log
%doc README ChangeLog Perl-License-Extracted.txt



%changelog
* Sun Dec 29 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.36-0.rc2
- Spec file and license cleanup

* Sat Nov 23 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.36-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
