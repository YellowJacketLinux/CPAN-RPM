%global cpanname Class-Loader

Name:     perl-%{cpanname}
Version:  2.03
Release:  %{?repo}0.rc1%{?dist}
Summary:  Load modules and create objects on demand
BuildArch: noarch

Group:    System Environment/Libraries
License:  Artistic-1.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/V/VI/VIPUL/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(CPAN)
BuildRequires: perl(Data::Dumper)
#BuildRequires: perl(Test)
BuildRequires: perl(lib)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(CPAN)
Requires: perl(Data::Dumper)
Requires: perl(vars)
Provides: perl(Class::Loader) = %{version}
Provides: perl(Class::LoaderTest)

%description
'Class::Loader' is an inheritable class that provides a method,
'_load()', to load a module from disk and construct an object by
calling its constructor. It also provides a way to map modules
names and associated metadata with symbolic names that can be
used in place of module names at '_load()'.


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
%{perl5_vendorlib}/Class/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license ARTISTIC
%doc %{name}-make.test.log
%doc ARTISTIC Changes



%changelog
* Sun Dec 01 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.03-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
