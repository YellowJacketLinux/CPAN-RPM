%global cpanname Class-XSAccessor

Name:     perl-%{cpanname}
Version:  1.19
Release:  %{?repo}0.rc2%{?dist}
Summary:  Generate fast XS accessors without runtime compilation

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SM/SMUELLER/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl(:VERSION) >= 5.8.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Test::More)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(XSLoader)
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI} >= 5.8.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorarch}
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
# Extract license info from README
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README


EOF

START=`grep -n "^COPYRIGHT AND LICENSE" README |cut -d":" -f1`
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
%license Perl-License-Extracted.txt Artistic-1.0-Perl.txt GPL-1.0.txt
%doc %{name}-make.test.log
%doc README Changes Perl-License-Extracted.txt



%changelog
* Mon Dec 30 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.19-0.rc2
- Spec file cleanup, license cleanup

* Tue Nov 19 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.19-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
