%global cpanname Class-InsideOut

Name:     perl-%{cpanname}
Version:  1.14
Release:  %{?repo}0.rc1%{?dist}
Summary:  A safe, simple inside-out object construction kit
BuildArch: noarch

Group:    System Environment/Libraries
License:  Apache-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Carp)
BuildRequires: perl(Class::ISA)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::File)
BuildRequires: perl(Scalar::Util) >= 1.09
BuildRequires: perl(Storable)
BuildRequires: perl(Test::More) >= 0.45
BuildRequires: perl(Type::Tiny)
BuildRequires: perl(XSLoader)
BuildRequires: perl(lib)
BuildRequires: perl(threads)
BuildRequires: perl(overload)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Class::ISA)
Requires: perl(Exporter)
Requires: perl(Scalar::Util) >= 1.09
Requires: perl(Storable)
Requires: perl(overload)
Requires: perl(strict)
Requires: perl(vars)
Provides: perl(Class::InsideOut) = %{version}

%description
This is a simple, safe and streamlined toolkit for building
inside-out objects.


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
%dir %{perl5_vendorarch}/Class
%dir %{perl5_vendorarch}/Class/InsideOut
%dir %{perl5_vendorarch}/Class/InsideOut/Manual
%{perl5_vendorarch}/Class/InsideOut.pm
%{perl5_vendorarch}/Class/InsideOut/Manual/*.pod
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING.mkdn README Todo examples



%changelog
* Tue Nov 26 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.14-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
