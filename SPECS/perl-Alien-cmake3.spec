%global cpanname Alien-cmake3

Name:     perl-%{cpanname}
Version:  0.08
Release:  %{?repo}0.rc2%{?dist}
Summary:  Alien package for CMake 3 or better
BuildArch: noarch

Group:    Perl/Development
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpanname}-%{version}.tar.gz

BuildRequires: cmake >= 3.0.0
#
BuildRequires: perl(:VERSION) >= 5.8.1
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.52
#
BuildRequires: perl(Alien::Base) >= 0.92
BuildRequires: perl(Alien::Build) >= 1.19
BuildRequires: perl(Alien::Build::MM) >= 0.32
BuildRequires: perl(Capture::Tiny)
BuildRequires: perl(File::Which)
BuildRequires: perl(Path::Tiny)
BuildRequires: perl(Test::Alien) >= 0.92
BuildRequires: perl(Test2::V0) >= 0.000121
BuildRequires: perl(base)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Alien::Base) >= 0.92
Requires: perl(base)
Requires: perl(strict)
Requires: perl(warnings)
# Make sure installed Alien::cmake3 does not need to download CMake
Requires: cmake >= 3.0.0
#
Provides: perl(Alien::cmake3) = %{version}


%description
This Alien distribution ensures that a CPAN external dependency
on the common build tool `cmake` version 3.0.0 or better is met.
`cmake` is a popular alternative to `autoconf`.


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
%dir %{perl5_vendorlib}/auto/Alien
%dir %{perl5_vendorlib}/auto/Alien/cmake3
%dir %{perl5_vendorlib}/auto/share
%dir %{perl5_vendorlib}/auto/share/dist
%dir %{perl5_vendorlib}/auto/share/dist/Alien-cmake3
%dir %{perl5_vendorlib}/auto/share/dist/Alien-cmake3/_alien
%{perl5_vendorlib}/Alien/cmake3.pm
%{perl5_vendorlib}/auto/Alien/cmake3/cmake3.txt
%{perl5_vendorlib}/auto/share/dist/Alien-cmake3/_alien/alien.json
%{perl5_vendorlib}/auto/share/dist/Alien-cmake3/_alien/alienfile
%attr(0644,root,root) %{_mandir}/man3/Alien::cmake3.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.08-0.rc2
- Spec file cleanup

* Thu Dec 05 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.08-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
