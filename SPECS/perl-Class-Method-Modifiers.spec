%global cpanname Class-Method-Modifiers

Name:     perl-%{cpanname}
Version:  2.15
Release:  %{?repo}0.rc1%{?dist}
Summary:  Provides Moose-like method modifiers
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(B)
BuildRequires: perl(Carp)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(base)
BuildRequires: perl(if)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(B)
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(base)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(Class::Method::Modifiers) = %{version}

%description
'Class::Method::Modifiers' provides three modifiers: 'before',
'around', and 'after'. The 'before' and 'after' modifiers are run
just before and after the method they modify, but can not really
affect that original method. The 'around' modifer is run in place
of the original method, with a hook to easily call that original
method.


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
%dir %{perl5_vendorlib}/Class/Method
%{perl5_vendorlib}/Class/Method/Modifiers.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING README



%changelog
* Tue Nov 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.15-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
