%global cpanname Class-Plain

Name:     perl-%{cpanname}
Version:  0.06
Release:  %{?repo}0.rc3%{?dist}
Summary:  A class syntax for the hash-based Perl OO

Group:    Perl/Libraries
License:  Artistic-1.0 or Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/K/KI/KIMOTO/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source99: CPAN-LICENSE-AMBIGUITY.md

BuildRequires: perl(:VERSION) >= 5.16.0
BuildRequires: perl-devel
BuildRequires: perl(Module::Build) >= 0.4004
#
BuildRequires: perl(Carp)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(File::ShareDir)
BuildRequires: perl(Role::Tiny) >= 2.002004
BuildRequires: perl(Role::Tiny::With)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(XS::Parse::Keyword) >= 0.22
BuildRequires: perl(XS::Parse::Keyword::Builder) >= 0.22
BuildRequires: perl(XS::Parse::Sublike) >= 0.15
BuildRequires: perl(XS::Parse::Sublike::Builder) >= 0.15
BuildRequires: perl(mro)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI} >= 5.16.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorarch}
%endif
Requires: perl(Carp)
Requires: perl(DynaLoader)
Requires: perl(Role::Tiny) >= 2.002004
Requires: perl(Role::Tiny::With)
Requires: perl(XS::Parse::Keyword) >= 0.22
Requires: perl(XS::Parse::Sublike) >= 0.15
Requires: perl(mro)
Requires: perl(strict)
Requires: perl(warnings)
#
Provides: perl(Class::Plain) = %{version}
Provides: perl(Class::Plain::Base)

%description
This module provides a class syntax for the hash-based Perl OO.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE99} .

%build
PERL_MM_USE_DEFAULT=1   \
MODULEBUILDRC=/dev/null \
perl Build.PL --installdirs vendor
./Build


%install
./Build pure_install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete


%check
./Build test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorarch}/Class
%dir %{perl5_vendorarch}/Class/Plain
%dir %{perl5_vendorarch}/Class/Plain/Document
%dir %{perl5_vendorarch}/auto/Class
%dir %{perl5_vendorarch}/auto/Class/Plain
%{perl5_vendorarch}/Class/Plain.pm
%{perl5_vendorarch}/Class/Plain/Base.pm
%{perl5_vendorarch}/Class/Plain/Document/Cookbook.pm
%attr(0555,root,root) %{perl5_vendorarch}/auto/Class/Plain/Plain.so
%exclude %{perl5_vendorarch}/auto/Class/Plain/Plain.bs
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE Artistic-1.0-Perl.txt CPAN-LICENSE-AMBIGUITY.md
%doc %{name}-make.test.log
%doc LICENSE Changes README*



%changelog
* Mon Dec 30 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.06-0.rc3
- Spec file cleanup, license cleanup

* Wed Nov 27 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.06-0.rc2
- remove .packlist during %%install, exclude .bs file

* Fri Nov 22 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.06-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
