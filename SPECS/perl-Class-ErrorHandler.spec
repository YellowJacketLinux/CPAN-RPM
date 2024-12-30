%global cpanname Class-ErrorHandler

Name:     perl-%{cpanname}
Version:  0.04
Release:  %{?repo}0.rc2%{?dist}
Summary:  Base class for error handling
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0 or Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/T/TO/TOKUHIROM/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source99: CPAN-LICENSE-AMBIGUITY.md

BuildRequires: perl(:VERSION) >= 5.8.1
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.8.1
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(strict)
Requires: perl(vars)
#
Provides: perl(Class::ErrorHandler) = %{version}

%description
`Class::ErrorHandler` provides an error-handling mechanism that
is generic enough to be used as the base class for a variety of
Object Oriented classes.


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
     NO_PERLLOCAL=1
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorlib}/Class
%{perl5_vendorlib}/Class/ErrorHandler.pm
%attr(0644,root,root) %{_mandir}/man3/Class::ErrorHandler.3*
%license LICENSE Artistic-1.0-Perl.txt CPAN-LICENSE-AMBIGUITY.md
%doc %{name}-make.test.log
%doc LICENSE Changes README.md



%changelog
* Sun Dec 29 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.04-0.rc2
- Spec file cleanup

* Sun Dec 01 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.04-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
