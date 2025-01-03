%global cpanname Business-ISBN

Name:     perl-%{cpanname}
Version:  3.009
Release:  %{?repo}0.rc2%{?dist}
Summary:  Work with International Standard Book Numbers
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/B/BR/BRIANDFOY/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.8.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.64
#
BuildRequires: perl(Business::ISBN::Data) >= 20230322.001
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(Test::More)
BuildRequires: perl(base)
BuildRequires: perl(strict)
BuildRequires: perl(subs)
BuildRequires: perl(vars)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.8.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Business::ISBN::Data) >= 20230322.001
Requires: perl(Carp)
Requires: perl(Data::Dumper)
Requires: perl(Exporter)
Suggests: perl(GD::Barcode::EAN13)
Requires: perl(base)
Requires: perl(strict)
Requires: perl(subs)
Requires: perl(vars)
#
Provides: perl(Business::ISBN) = %{version}
Provides: perl(Business::ISBN10) = %{version}
Provides: perl(Business::ISBN13) = %{version}

%description
This modules handles International Standard Book Numbers,
including ISBN-10 and ISBN-13.

The data come from `Business::ISBN::Data`, which means you can
update the data separately from the code. Also, you can use
`Business::ISBN::Data` with whatever `RangeMessage.xml` you like
if you have updated data. See that module for details.


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
%{perl5_vendorlib}/Business/ISBN.pm
%{perl5_vendorlib}/Business/ISBN10.pm
%{perl5_vendorlib}/Business/ISBN13.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE *.txt Changes README.pod examples



%changelog
* Sat Dec 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 3.009-0.rc2
- Spec file cleanup

* Sat Nov 16 2024 Michael A. Peters <anymouseprophet@gmail.com> - 3.009-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
