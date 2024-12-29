%global cpanname Canary-Stability

Name:     perl-%{cpanname}
Version:  2013
Release:  %{?repo}0.rc1%{?dist}
Summary:  Canary to check perl compatibility for schmorp's modules
BuildArch: noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/%{cpanname}-%{version}.tar.gz
Source90: PERL-Artistic
Source91: PERL-Copying

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(ExtUtils::MakeMaker)
Provides: perl(Canary::Stability) = %{version}

%description
This module is used by Schmorp's modules during configuration
stage to test the installed perl for compatibility with his modules.

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
%defattr(0444,root,root)
%dir %{perl5_vendorlib}/Canary
%{perl5_vendorlib}/Canary/Stability.pm
%attr(0644,root,root) %{_mandir}/man3/Canary::Stability.3*
%license COPYING PERL-Artistic PERL-Copying
%doc %{name}-make.test.log
%doc COPYING PERL-Artistic PERL-Copying
%doc Changes README


%changelog
* Thu Nov 14 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2013-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
