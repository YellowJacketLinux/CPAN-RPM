%global cpanname B-COW

Name:     perl-%{cpanname}
Version:  0.007
Release:  %{?repo}0.rc2%{?dist}
Summary:  Additional B helpers to check COW status

Group:    Perl/Libraries
License:  Artistic-1.0 or Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source99: CPAN-LICENSE-AMBIGUITY.md

BuildRequires: perl(:VERSION) >= 5.8.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Devel::Peek)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More)
BuildRequires: perl(XSLoader)
BuildRequires: perl(base)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
#
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI} >= 5.8.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorarch}
%endif
Requires: perl(Exporter)
Requires: perl(XSLoader)
Requires: perl(base)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(B::COW) = %{version}

%description
`B::COW` provides some naive additional `B` helpers to check the
`COW` status of one SvPV.


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
     NO_PERLLOCAL=1     \
     OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorarch}/B
%dir %{perl5_vendorarch}/auto/B
%dir %{perl5_vendorarch}/auto/B/COW
%{perl5_vendorarch}/B/COW.pm
%attr(0555,root,root) %{perl5_vendorarch}/auto/B/COW/COW.so
%attr(0644,root,root) %{_mandir}/man3/B::COW.3*
%license LICENSE Artistic-1.0-Perl.txt CPAN-LICENSE-AMBIGUITY.md
%doc %{name}-make.test.log
%doc LICENSE Changes README examples



%changelog
* Sat Dec 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.007-0.rc2
- Spec file cleanup

* Fri Nov 22 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.007-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
