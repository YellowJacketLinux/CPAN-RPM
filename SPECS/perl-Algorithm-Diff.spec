%global cpanname Algorithm-Diff

Name:     perl-%{cpanname}
Version:  1.201
Release:  %{?repo}0.rc2%{?dist}
Summary:  Compute 'intelligent' differences between two files / lists
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Carp)
BuildRequires: perl(Exporter)
BuildRequires: perl(integer)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(integer)
Requires: perl(strict)
Requires: perl(vars)
#
Provides: perl(Algorithm::Diff) = %{version}
Provides: perl(Algorithm::DiffOld) = %{version}

%description
This module provides an intelligent algorithm for describing data
differences.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from embedded pod
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{perl5_vendorlib}/Algorithm/Diff.pm


EOF

START=`grep -n "^=head1 LICENSE" lib/Algorithm/Diff.pm |cut -d":" -f1`
END=`grep -n "^=head1 MAILING LIST" lib/Algorithm/Diff.pm |cut -d":" -f1`
DIFF="$((${END}-${START}))"
REND="$((${END}-1))"

head -${REND} lib/Algorithm/Diff.pm |tail -${DIFF} >> Perl-License-Extracted.txt


%build
PERL_MM_USE_DEFAULT=1   \
BUILDING_AS_PACKAGE=1   \
perl Makefile.PL        \
     INSTALLDIRS=vendor \
     NO_PACKLIST=1      \
     NO_PERLLOCAL=1     \
     OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorlib}/Algorithm
%{perl5_vendorlib}/Algorithm/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license Artistic-1.0-Perl.txt GPL-1.0.txt Perl-License-Extracted.txt
%doc %{name}-make.test.log
%doc Changes README Perl-License-Extracted.txt



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.201-0.rc2
- Fix up License, spec file cleanup

* Sun Nov 24 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.201-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
