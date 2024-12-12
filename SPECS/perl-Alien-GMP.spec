%global cpanname Alien-GMP

Name:     perl-%{cpanname}
Version:  1.16
Release:  %{?repo}0.rc2%{?dist}
Summary:  Alien package for the GNU Multiple Precision (GMP) library
BuildArch: noarch

Group:    Perl/Development
License:  LGPL-3.0-only
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpanname}-%{version}.tar.gz

BuildRequires: pkgconfig(gmp)
#
BuildRequires: perl(:VERSION) >= 5.6.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.52
#
BuildRequires: perl(Alien::Base) >= 1.46
BuildRequires: perl(Alien::Build) >= 1.46
BuildRequires: perl(Alien::Build::MM) >= 0.32
BuildRequires: perl(Devel::CheckLib)
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(Test::Alien)
BuildRequires: perl(Test2::V0) >= 0.000060
BuildRequires: perl(base)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Alien::Base) >= 1.46
Requires: perl(base)
Requires: perl(strict)
Requires: perl(warnings)
# Make sure installed Alien::GMP does not need to download GMP
Requires: pkgconfig(gmp)
#
Provides: perl(Alien::GMP) = %{version}


%description
The `Alien::GMP` package ensures that the GNU Multiple Precision
(GMP) library header files needed to compile software that links
against the GMP library are available to the Perl `Alien::` build
system.


%prep
%setup -q -n %{cpanname}-%{version}


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
%dir %{perl5_vendorlib}/Alien
%dir %{perl5_vendorlib}/Alien/GMP
%dir %{perl5_vendorlib}/Alien/GMP/Install
%dir %{perl5_vendorlib}/auto/Alien
%dir %{perl5_vendorlib}/auto/Alien/GMP
%dir %{perl5_vendorlib}/auto/share/dist/Alien-GMP
%dir %{perl5_vendorlib}/auto/share/dist/Alien-GMP/_alien
%{perl5_vendorlib}/Alien/GMP.pm
%{perl5_vendorlib}/Alien/GMP/Install/Files.pm
%{perl5_vendorlib}/auto/Alien/GMP/GMP.txt
%{perl5_vendorlib}/auto/share/dist/Alien-GMP/_alien/alien.json
%{perl5_vendorlib}/auto/share/dist/Alien-GMP/_alien/alienfile
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README



%changelog
* Wed Dec 11 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16-0.rc2
- Change License: field to valid SPDX identifier, spec file cleanup.

* Fri Dec 06 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
