%global cpanname Alt-Crypt-RSA-BigInt

Name:     perl-%{cpanname}
Version:  0.06
Release:  %{?repo}0.rc2%{?dist}
Summary:  RSA public-key cryptosystem, using Math::BigInt
BuildArch: noarch
Conflicts: perl-Crypt-RSA

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DANAJ/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source99: CPAN-LICENSE-AMBIGUITY.md

BuildRequires: pkgconfig(gmp)
#
BuildRequires: perl(:VERSION) >= 5.8.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Benchmark)
BuildRequires: perl(Carp)
BuildRequires: perl(Class::Loader)
BuildRequires: perl(Convert::ASCII::Armour)
BuildRequires: perl(Crypt::Blowfish)
BuildRequires: perl(Crypt::CBC) >= 2.17
BuildRequires: perl(Crypt::RIPEMD160) >= 0.05
BuildRequires: perl(Data::Buffer)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Digest::MD2)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(Exporter)
BuildRequires: perl(Math::BigInt) >= 1.78
BuildRequires: perl(Math::BigInt::GMP)
BuildRequires: perl(Math::Prime::Util) >= 0.64
BuildRequires: perl(Math::Prime::Util::GMP)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Sort::Versions)
BuildRequires: perl(Test::More) >= 0.45
BuildRequires: perl(Tie::EncryptedHash)
BuildRequires: perl(base)
BuildRequires: perl(constant)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.8.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Class::Loader)
Requires: perl(Convert::ASCII::Armour)
Requires: perl(Crypt::Blowfish)
Requires: perl(Crypt::CBC) >= 2.17
Requires: perl(Crypt::RIPEMD160) >= 0.05
Requires: perl(Data::Buffer)
Requires: perl(Data::Dumper)
Requires: perl(Digest::MD2)
Requires: perl(Digest::MD5)
Requires: perl(Digest::SHA)
Requires: perl(Exporter)
Requires: perl(Math::BigInt) >= 1.78
Requires: perl(Math::BigInt::GMP)
Requires: perl(Math::Prime::Util) >= 0.64
Requires: perl(Math::Prime::Util::GMP)
Requires: perl(Sort::Versions)
Requires: perl(Tie::EncryptedHash)
Requires: perl(base)
Requires: perl(constant)
Requires: perl(strict)
Requires: perl(vars)
Requires: perl(warnings)
#
Provides: perl(Alt::Crypt::RSA::BigInt) = %{version}
#
Provides: perl(Crypt::RSA) = 1.99
Provides: perl(Crypt::RSA::DataFormat)
Provides: perl(Crypt::RSA::Debug)
Provides: perl(Crypt::RSA::Errorhandler)
Provides: perl(Crypt::RSA::ES::OAEP) = 1.99
Provides: perl(Crypt::RSA::ES::PKCS1v15) = 1.99
Provides: perl(Crypt::RSA::Key) = 1.99
Provides: perl(Crypt::RSA::Key::Private) = 1.99
Provides: perl(Crypt::RSA::Key::Private::SSH)
Provides: perl(Crypt::RSA::Key::Public) = 1.99
Provides: perl(Crypt::RSA::Key::Public::SSH)
Provides: perl(Crypt::RSA::Primitives)
Provides: perl(Crypt::RSA::SS::PKCS1v15) = 1.99
Provides: perl(Crypt::RSA::SS::PSS) = 1.99


%description
This is a modification of the `Crypt::RSA` module to remove all
use and dependencies on `Pari` and `Math::Pari`.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE99} .



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
%dir %{perl5_vendorlib}/Alt
%dir %{perl5_vendorlib}/Alt/Crypt
%dir %{perl5_vendorlib}/Alt/Crypt/RSA
%dir %{perl5_vendorlib}/Crypt
%dir %{perl5_vendorlib}/Crypt/RSA
%dir %{perl5_vendorlib}/Crypt/RSA/ES
%dir %{perl5_vendorlib}/Crypt/RSA/Key
%dir %{perl5_vendorlib}/Crypt/RSA/Key/Private
%dir %{perl5_vendorlib}/Crypt/RSA/Key/Public
%dir %{perl5_vendorlib}/Crypt/RSA/SS
%{perl5_vendorlib}/Alt/Crypt/RSA/BigInt.pm
%{perl5_vendorlib}/Crypt/RSA.pm
%{perl5_vendorlib}/Crypt/RSA/*.pm
%{perl5_vendorlib}/Crypt/RSA/ES/*.pm
%{perl5_vendorlib}/Crypt/RSA/Key/*.pm
%{perl5_vendorlib}/Crypt/RSA/Key/Private/*.pm
%{perl5_vendorlib}/Crypt/RSA/Key/Public/*.pm
%{perl5_vendorlib}/Crypt/RSA/SS/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE Artistic-1.0-Perl.txt CPAN-LICENSE-AMBIGUITY.md
%doc %{name}-make.test.log
%doc LICENSE Changes* README TODO



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.06-0.rc2
- Spec file cleanup

* Fri Dec 06 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.06-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
