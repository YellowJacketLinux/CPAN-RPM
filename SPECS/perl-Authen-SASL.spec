%global cpanname Authen-SASL

Name:     perl-%{cpanname}
Version:  2.1700
Release:  %{?repo}0.rc2%{?dist}
Summary:  SASL Authentication framework
BuildArch: noarch

Group:    Perl/Network
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/EH/EHUELS/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.6.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Carp)
BuildRequires: perl(Digest::HMAC_MD5)
BuildRequires: perl(Digest::MD5)
#BuildRequires: perl(GSSAPI)
BuildRequires: perl(Pod::Coverage::TrustPod)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)
BuildRequires: perl(bytes)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.6.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Digest::HMAC_MD5)
Requires: perl(Digest::MD5)
Suggests: perl(GSSAPI)
Requires: perl(bytes)
Requires: perl(strict)
Requires: perl(vars)
Requires: perl(warnings)
#
Provides: perl(Authen::SASL) = %{version}
Provides: perl(Authen::SASL::CRAM_MD5) = %{version}
Provides: perl(Authen::SASL::EXTERNAL) = %{version}
Provides: perl(Authen::SASL::Perl) = %{version}
Provides: perl(Authen::SASL::Perl::ANONYMOUS) = %{version}
Provides: perl(Authen::SASL::Perl::CRAM_MD5) = %{version}
Provides: perl(Authen::SASL::Perl::DIGEST_MD5) = %{version}
Provides: perl(Authen::SASL::Perl::EXTERNAL) = %{version}
Provides: perl(Authen::SASL::Perl::GSSAPI) = %{version}
Provides: perl(Authen::SASL::Perl::LOGIN) = %{version}
Provides: perl(Authen::SASL::Perl::PLAIN) = %{version}

%description
SASL is a generic mechanism for authentication used by several
network protocols. `Authen::SASL` provides an implementation
framework that all protocols should be able to share.


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
%dir %{perl5_vendorlib}/Authen
%dir %{perl5_vendorlib}/Authen/SASL
%dir %{perl5_vendorlib}/Authen/SASL/Perl
%{perl5_vendorlib}/Authen/SASL.pm
%{perl5_vendorlib}/Authen/SASL.pod
%{perl5_vendorlib}/Authen/SASL/*.pm
%{perl5_vendorlib}/Authen/SASL/Perl.pod
%{perl5_vendorlib}/Authen/SASL/Perl/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE api.txt Changes README compat_pl example_pl



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.1700-0.rc2
- Some spec file cleanup

* Sun Nov 17 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.1700-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
- FIXME TODO - BUILD GSSAPI module for Perl
