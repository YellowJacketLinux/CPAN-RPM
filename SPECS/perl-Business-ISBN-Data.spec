%global cpanname Business-ISBN-Data

Name:     perl-%{cpanname}
Version:  20241224.001
Release:  %{?repo}0.rc1%{?dist}
Summary:  Data pack for Business::ISBN
BuildArch: noarch

Group:    Perl/Data
License:  Artistic-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/B/BR/BRIANDFOY/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.8.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.64
#
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(File::Basename)
BuildRequires: perl(Carp)
BuildRequires: perl(Test::More) >= 1
BuildRequires: perl(strict)
BuildRequires: perl(utf8)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.8.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Suggests: perl(Business::ISBN) >= 3.005
Requires: perl(Carp)
Requires: perl(File::Basename)
Requires: perl(File::Spec::Functions)
Requires: perl(strict)
Requires: perl(utf8)
Provides: perl(Business::ISBN::Data) = %{version}


%description
You don't need to load this module yourself in most cases.
`Business::ISBN` will load it when it loads. You must use
`Business::ISBN` 3.005 or later because the data structure
changed slightly to fix a bug with ISBN13 prefixes.

These data are generated from the `RangeMessage.xml` file
provided by the ISBN Agency. The distributed version matches
the date in the version for this module.


%prep
%setup -q -n %{cpanname}-%{version}


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
%dir %{perl5_vendorlib}/Business
%dir %{perl5_vendorlib}/Business/ISBN
%{perl5_vendorlib}/Business/ISBN/Data.pm
%{perl5_vendorlib}/Business/ISBN/RangeMessage.url
%{perl5_vendorlib}/Business/ISBN/RangeMessage.xml
%attr(0644,root,root) %{_mandir}/man3/Business::ISBN::Data.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README.pod examples



%changelog
* Sat Dec 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 20241224.001-0.rc1
- Update data, spec file cleanup

* Sat Dec 07 2024 Michael A. Peters <anymouseprophet@gmail.com> - 20241206.001-0.rc1
- Update data, add spec file compatibility for non YJL distros

* Sat Nov 16 2024 Michael A. Peters <anymouseprophet@gmail.com> - 20241112.001-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
