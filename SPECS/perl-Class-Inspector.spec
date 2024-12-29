%global cpanname Class-Inspector

Name:     perl-%{cpanname}
Version:  1.36
Release:  %{?repo}0.rc1%{?dist}
Summary:  Get information about a class and its structure
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec) >= 0.80
BuildRequires: perl(Test::More) >= 0.98
BuildRequires: perl(base)
BuildRequires: perl(utf8)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Exporter)
Requires: perl(File::Spec) >= 0.80
Requires: perl(base)
Requires: perl(strict)
Requires: perl(utf8)
Requires: perl(warnings)
Provides: perl(Class::Inspector) = %{version}
Provides: perl(Class::Inspector::Functions) = %{version}

%description
'Class::Inspector' allows you to get information about a loaded
class. Most or all of this information can be found in other
ways, but they aren't always very friendly, and usually involve a
relatively high level of Perl wizardry, or strange and unusual
looking code. 'Class::Inspector' attempts to provide an easier,
more friendly interface to this information.


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
%dir %{perl5_vendorlib}/Class
%dir %{perl5_vendorlib}/Class/Inspector
%{perl5_vendorlib}/Class/Inspector.pm
%{perl5_vendorlib}/Class/Inspector/Functions.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README



%changelog
* Fri Nov 22 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.36-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
