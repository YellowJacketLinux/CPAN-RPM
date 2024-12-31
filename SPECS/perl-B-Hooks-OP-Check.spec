%global cpanname B-Hooks-OP-Check

Name:     perl-%{cpanname}
Version:  0.22
Release:  %{?repo}0.rc2%{?dist}
Summary:  Wrap OP check callbacks

Group:    Perl/Libraries
License:  Artistic-1.0 or Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source99: CPAN-LICENSE-AMBIGUITY.md

BuildRequires: perl(:VERSION) >= 5.8.1
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(ExtUtils::Depends) >= 0.302
BuildRequires: perl(DynaLoader)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More)
BuildRequires: perl(parent)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI} >= 5.8.1
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorarch}
%endif
Requires: perl(ExtUtils::Depends) >= 0.302
Requires: perl(DynaLoader)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(B::Hooks::OP::Check) = %{version}
Provides: perl(B::Hooks::OP::Check::Install::Files)

%description
This module provides a C API for XS modules to hook into the
callbacks of `PL_check`.

`ExtUtils::Depends` is used to export all functions for other
XS modules to use.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE99} .


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
%dir %{perl5_vendorlib}/B
%dir %{perl5_vendorlib}/B/Hooks
%dir %{perl5_vendorlib}/B/Hooks/OP
%dir %{perl5_vendorlib}/B/Hooks/OP/Check
%dir %{perl5_vendorlib}/B/Hooks/OP/Check/Install
%dir %{perl5_vendorlib}/auto/B
%dir %{perl5_vendorlib}/auto/B/Hooks
%dir %{perl5_vendorlib}/auto/B/Hooks/OP
%dir %{perl5_vendorlib}/auto/B/Hooks/OP/Check
%{perl5_vendorlib}/B/Hooks/OP/Check.pm
%{perl5_vendorlib}/B/Hooks/OP/Check/Install/Files.pm
%{perl5_vendorlib}/B/Hooks/OP/Check/Install/hook_op_check.h
%attr(0555,root,root) %{perl5_vendorlib}/auto/B/Hooks/OP/Check/Check.so
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENCE Artistic-1.0-Perl.txt CPAN-LICENSE-AMBIGUITY.md
%doc %{name}-make.test.log
%doc LICENCE Changes CONTRIBUTING README



%changelog
* Sat Dec 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.22-0.rc2
- spec file cleanup

* Tue Nov 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.22-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
