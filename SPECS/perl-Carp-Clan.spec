%global cpanname Carp-Clan

Name:     perl-%{cpanname}
Version:  6.08
Release:  %{?repo}0.rc1%{?dist}
Summary:  Report errors from perspective of caller of a "clan" of modules
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More)
BuildRequires: perl(overload)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(overload)
Requires: perl(strict)
Provides: perl(Carp::Clan) = %{version}

%description
This module is based on "Carp.pm" from Perl 5.005_03. It has been
modified to skip all package names matching the pattern given in
the "use" statement inside the "qw()" term (or argument list).


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
%dir %{perl5_vendorlib}/Carp
%{perl5_vendorlib}/Carp/Clan.pm
%attr(0644,root,root) %{_mandir}/man3/Carp::Clan.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING README



%changelog
* Mon Nov 25 2024 Michael A. Peters <anymouseprophet@gmail.com> - 6.08-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
