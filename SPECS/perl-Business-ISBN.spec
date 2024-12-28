%global cpanname Business-ISBN

Name:     perl-%{cpanname}
Version:  3.009
Release:  %{?repo}0.rc1%{?dist}
Summary:  Work with International Standard Book Numbers
BuildArch: noarch

Group:    System Environment/Libraries
License:  Artistic-2.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/B/BR/BRIANDFOY/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(Test::More)
BuildRequires: perl(Business::ISBN::Data) >= 20230322.001
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
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
Provides: perl(Business::ISBN) = %{version}
Provides: perl(Business::ISBN10) = %{version}
Provides: perl(Business::ISBN13) = %{version}

%description
This modules handles International Standard Book Numbers,
including ISBN-10 and ISBN-13.

The data come from 'Business::ISBN::Data', which means you can
update the data separately from the code. Also, you can use
'Business::ISBN::Data' with whatever RangeMessage.xml you like
if you have updated data. See that module for details.


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
%dir %{perl5_vendorlib}/Business
%{perl5_vendorlib}/Business/ISBN.pm
%{perl5_vendorlib}/Business/ISBN10.pm
%{perl5_vendorlib}/Business/ISBN13.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE *.txt Changes README.pod examples



%changelog
* Sat Nov 16 2024 Michael A. Peters <anymouseprophet@gmail.com> - 3.009-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
