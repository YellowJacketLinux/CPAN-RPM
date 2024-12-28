%global cpanname B-Hooks-EndOfScope

Name:     perl-%{cpanname}
Version:  0.28
Release:  %{?repo}0.rc1%{?dist}
Summary:  Execute code after a scope finished compilation
BuildArch: noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Carp)
BuildRequires: perl(File::Glob)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Hash::Util::FieldHash)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(Module::Implementation) >= 0.05
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(Sub::Exporter::Progressive) >= 0.001006
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Tie::Hash)
BuildRequires: perl(Variable::Magic) >= 0.48
BuildRequires: perl(constant)
BuildRequires: perl(lib)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Hash::Util::FieldHash)
Requires: perl(Module::Implementation) >= 0.05
Requires: perl(Scalar::Util)
Requires: perl(Sub::Exporter::Progressive) >= 0.001006
Requires: perl(Tie::Hash)
Requires: perl(Variable::Magic) >= 0.48
Requires: perl(constant)
Requires: perl(strict)
Requires: perl(warnings)
#
Provides: perl(B::Hooks::EndOfScope) = %{version}
Provides: perl(B::Hooks::EndOfScope::PP) = %{version}
Provides: perl(B::Hooks::EndOfScope::XS) = %{version}


%description
This module allows you to execute code when perl finished
compiling the surrounding scope.


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
%dir %{perl5_vendorlib}/B
%dir %{perl5_vendorlib}/B/Hooks
%dir %{perl5_vendorlib}/B/Hooks/EndOfScope
%dir %{perl5_vendorlib}/B/Hooks/EndOfScope/PP
%{perl5_vendorlib}/B/Hooks/EndOfScope.pm
%{perl5_vendorlib}/B/Hooks/EndOfScope/*.pm
%{perl5_vendorlib}/B/Hooks/EndOfScope/PP/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENCE
%doc %{name}-make.test.log
%doc LICENCE Changes CONTRIBUTING README



%changelog
* Thu Nov 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.28-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
