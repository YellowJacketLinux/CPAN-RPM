%global cpanname Class-Tiny

Name:     perl-%{cpanname}
Version:  1.008
Release:  %{?repo}0.rc1%{?dist}
Summary:  Minimalist class construction
BuildArch: noarch

Group:    System Environment/Libraries
License:  Apache-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires: perl(Carp)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::FailWarnings)
BuildRequires: perl(Test::More) >= 0.96
BuildRequires: perl(base)
BuildRequires: perl(lib)
BuildRequires: perl(subs)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(Class::Tiny) = %{version}

%description
This module offers a minimalist class construction kit in around
120 lines of code.


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
%{perl5_vendorlib}/Class/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Class::Tiny.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING.mkdn README



%changelog
* Wed Nov 20 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.008-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
