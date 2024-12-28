%global cpanname Bytes-Random-Secure

Name:     perl-%{cpanname}
Version:  0.29
Release:  %{?repo}0.rc1%{?dist}
Summary:  Perl extension to generate cryptographically-secure random bytes
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAVIDO/%{cpanname}-%{version}.tar.gz
Source90: PERL-Artistic
Source91: PERL-Copying

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.56
BuildRequires: perl(Carp)
BuildRequires: perl(Crypt::Random::Seed)
BuildRequires: perl(Exporter)
BuildRequires: perl(Math::Random::ISAAC)
BuildRequires: perl(Math::Random::ISAAC::XS)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(MIME::QuotedPrint) >= 3.03
BuildRequires: perl(Scalar::Util) >= 1.21
BuildRequires: perl(Statistics::Basic)
BuildRequires: perl(Test::More) >= 0.98
BuildRequires: perl(constant)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Crypt::Random::Seed)
Requires: perl(Exporter)
Requires: perl(Math::Random::ISAAC)
Requires: perl(Math::Random::ISAAC::XS)
Requires: perl(MIME::Base64)
Requires: perl(MIME::QuotedPrint) >= 3.03
Requires: perl(Scalar::Util) >= 1.21
Requires: perl(constant)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(Bytes::Random::Secure) >= 0.29

%description
'Bytes::Random::Secure' provides two interfaces for obtaining
crypto-quality random bytes. The simple interface is built around
plain functions. For greater control over the Random Number
Generator's seeding, there is an Object Oriented interface that
provides much more flexibility.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .


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
%dir %{perl5_vendorlib}/Bytes
%dir %{perl5_vendorlib}/Bytes/Random
%{perl5_vendorlib}/Bytes/Random/Secure.pm
%attr(0644,root,root) %{_mandir}/man3/Bytes::Random::Secure.3*
%license README PERL-Artistic PERL-Copying
%doc %{name}-make.test.log
%doc README PERL-Artistic PERL-Copying Changes examples



%changelog
* Sat Nov 30 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.29-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
