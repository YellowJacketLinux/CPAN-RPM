%global cpanname Class-Loader

Name:     perl-%{cpanname}
Version:  2.03
Release:  %{?repo}0.rc2%{?dist}
Summary:  Load modules and create objects on demand
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0; Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/V/VI/VIPUL/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(CPAN)
BuildRequires: perl(Data::Dumper)
#BuildRequires: perl(Test)
BuildRequires: perl(lib)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(CPAN)
Requires: perl(Data::Dumper)
Requires: perl(vars)
#
Provides: perl(Class::Loader) = %{version}
Provides: perl(Class::LoaderTest)

%description
'Class::Loader' is an inheritable class that provides a method,
'_load()', to load a module from disk and construct an object by
calling its constructor. It also provides a way to map modules
names and associated metadata with symbolic names that can be
used in place of module names at '_load()'.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from embedded pod
cat << "EOF" > Perl-License-Extracted.txt
The included perl module claims the same license as Perl itself but the CPAN
distributions includes the Artistic-1.0 license text in the file `ARTISTIC`
which is *different* from the license used by perl itself. Please contact the
CPAN module maintainer if you have a license question.

The following was extracted from:

  %{perl5_vendorlib}/Class/Loader.pm


EOF

START=`grep -n "^=head1 LICENSE" lib/Class/Loader.pm |cut -d":" -f1`
END=`grep -n "^=cut" lib/Class/Loader.pm |cut -d":" -f1`
DIFF="$((${END}-${START}))"
REND="$((${END}-1))"

head -${REND} lib/Class/Loader.pm |tail -${DIFF} >> Perl-License-Extracted.txt


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
%dir %{perl5_vendorlib}/Class
%{perl5_vendorlib}/Class/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license ARTISTIC Artistic-1.0-Perl.txt GPL-1.0.txt Perl-License-Extracted.txt
%doc %{name}-make.test.log
%doc ARTISTIC Changes Perl-License-Extracted.txt



%changelog
* Sun Dec 29 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.03-0.rc2
- Spec file cleanup, license cleanup as much as possible.

* Sun Dec 01 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.03-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
