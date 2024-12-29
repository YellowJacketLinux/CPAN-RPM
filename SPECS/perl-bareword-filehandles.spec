%global cpanname bareword-filehandles

Name:     perl-%{cpanname}
Version:  0.007
Release:  %{?repo}0.rc1%{?dist}
Summary:  Disables bareword filehandles

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/I/IL/ILMARI/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(B::Hooks::OP::Check)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(XSLoader)
BuildRequires: perl(if)
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif
Requires: perl(B::Hooks::OP::Check)
Requires: perl(XSLoader)
Requires: perl(if)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(bareword::filehandles) = %{version}

%description
This module lexically disables the use of bareword filehandles
with builtin functions, except for the special builtin filehandles
'STDIN', 'STDOUT', 'STDERR', 'ARGV', 'ARGVOUT' and 'DATA'.


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
%dir %{perl5_vendorlib}/bareword
%dir %{perl5_vendorlib}/auto/bareword
%dir %{perl5_vendorlib}/auto/bareword/filehandles
%{perl5_vendorlib}/bareword/filehandles.pm
%attr(0555,root,root) %{perl5_vendorlib}/auto/bareword/filehandles/filehandles.so
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README



%changelog
* Mon Nov 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.007-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
