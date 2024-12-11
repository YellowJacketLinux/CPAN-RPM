%global cpanname Algorithm-Diff

Name:     perl-%{cpanname}
Version:  1.201
Release:  %{?repo}0.rc1%{?dist}
Summary:  Compute 'intelligent' differences between two files / lists
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz
Source90: PERL-Artistic
Source91: PERL-Copying

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Carp)
BuildRequires: perl(Exporter)
BuildRequires: perl(integer)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(integer)
Requires: perl(strict)
Requires: perl(vars)
Provides: perl(Algorithm::Diff) = %{version}
Provides: perl(Algorithm::DiffOld) = %{version}

%description
This module provides an intelligent algorithm for describing data
differences.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .


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
%license PERL-Artistic PERL-Copying
%doc %{name}-make.test.log
%doc PERL-Artistic PERL-Copying Changes README



%changelog
* Sun Nov 24 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.201-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
