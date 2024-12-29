%global cpanname Class-XSAccessor

Name:     perl-%{cpanname}
Version:  1.19
Release:  %{?repo}0.rc1%{?dist}
Summary:  Generate fast XS accessors without runtime compilation

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/%{cpanname}-%{version}.tar.gz
Source90: PERL-Artistic
Source91: PERL-Copying

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Test::More)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(XSLoader)
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif
Requires: perl(Carp)
Requires: perl(Time::HiRes)
Requires: perl(XSLoader)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(Class::XSAccessor) = %{version}
Provides: perl(Class::XSAccessor::Array) = %{version}
Provides: perl(Class::XSAccessor::Heavy) = %{version}

%description
Class::XSAccessor implements fast read, write and read/write
accessors in XS.


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
%dir %{perl5_vendorarch}/Class
%dir %{perl5_vendorarch}/Class/XSAccessor
%dir %{perl5_vendorarch}/auto/Class
%dir %{perl5_vendorarch}/auto/Class/XSAccessor
%{perl5_vendorarch}/Class/XSAccessor.pm
%{perl5_vendorarch}/Class/XSAccessor/Array.pm
%{perl5_vendorarch}/Class/XSAccessor/Heavy.pm
%attr(0555,root,root) %{perl5_vendorarch}/auto/Class/XSAccessor/XSAccessor.so
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license README PERL-Artistic PERL-Copying
%doc %{name}-make.test.log
%doc README PERL-Artistic PERL-Copying Changes



%changelog
* Tue Nov 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.19-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
