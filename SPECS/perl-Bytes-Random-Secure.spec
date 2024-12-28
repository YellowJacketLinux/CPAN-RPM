%global cpanname Bytes-Random-Secure

Name:     perl-%{cpanname}
Version:  0.29
Release:  %{?repo}0.rc2%{?dist}
Summary:  Perl extension to generate cryptographically-secure random bytes
BuildArch: noarch

Group:    System Environment/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAVIDO/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl(:VERSION) >= 5.6.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.56
#
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
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.6.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
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
#
Provides: perl(Bytes::Random::Secure) = %{version}

%description
`Bytes::Random::Secure` provides two interfaces for obtaining
crypto-quality random bytes. The simple interface is built around
plain functions. For greater control over the Random Number
Generator's seeding, there is an Object Oriented interface that
provides much more flexibility.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from README
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README


EOF

START=`grep -n "^LICENSE AND COPYRIGHT" README |cut -d":" -f1`
END=`wc -l README |cut -d " " -f1`
DIFF="$((${END}-${START}))"
TAIL="$((${DIFF}+1))"

tail -${TAIL} README >> Perl-License-Extracted.txt


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
%dir %{perl5_vendorlib}/Bytes
%dir %{perl5_vendorlib}/Bytes/Random
%{perl5_vendorlib}/Bytes/Random/Secure.pm
%attr(0644,root,root) %{_mandir}/man3/Bytes::Random::Secure.3*
%license Perl-License-Extracted.txt Artistic-1.0-Perl.txt GPL-1.0.txt
%doc %{name}-make.test.log
%doc README Perl-License-Extracted.txt Changes examples



%changelog
* Sat Dec 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.29-0.rc2
- Clean up spec file
- Better handling of specified license terms

* Sat Nov 30 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.29-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
