%global cpanname Archive-Extract

Name:     perl-%{cpanname}
Version:  0.88
Release:  %{?repo}0.rc2%{?dist}
Summary:  A generic archive extracting mechanism
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/B/BI/BINGOS/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Carp)
BuildRequires: perl(Cwd)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec) >= 0.82
BuildRequires: perl(FileHandle)
BuildRequires: perl(IPC::Cmd) >= 0.64
BuildRequires: perl(Locale::Maketext::Simple)
BuildRequires: perl(Module::Load::Conditional) >= 0.66
BuildRequires: perl(Params::Check) >= 0.07
BuildRequires: perl(Test::More)
BuildRequires: perl(constant)
BuildRequires: perl(deprecate)
BuildRequires: perl(if)
BuildRequires: perl(strict)
BuildRequires: perl(vars)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Cwd)
Requires: perl(IPC::Cmd) >= 0.64
Requires: perl(File::Basename)
Requires: perl(File::Path)
Requires: perl(File::Spec) >= 0.82
Requires: perl(FileHandle)
Requires: perl(Locale::Maketext::Simple)
Requires: perl(Module::Load::Conditional) >= 0.66
Requires: perl(Params::Check) >= 0.07
Requires: perl(constant)
Requires: perl(deprecate)
Requires: perl(if)
Requires: perl(strict)
Requires: perl(vars)
#
Requires: %{__tar}
#
Provides: perl(Archive::Extract) = %{version}

%description
`Archive::Extract` is a generic archive extraction mechanism.

It allows you to extract any archive file of the type `.tar`,
`.tar.gz`, `.gz`, `.Z`, `tar.bz2`, `.tbz`, `.bz2`, `.zip`, `.xz`,
`.txz`, `.tar.xz`, or `.lzma` without having to worry how it does
so, or use different interfaces for each type by using either
perl modules, or commandline tools on your system.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from README
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README


EOF

START=`grep -n "^COPYRIGHT" README |cut -d":" -f1`
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
     NO_PERLLOCAL=1
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%check
make test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%dir %{perl5_vendorlib}/Archive
%{perl5_vendorlib}/Archive/Extract.pm
%attr(0644,root,root) %{_mandir}/man3/Archive::Extract.3*
%license Perl-License-Extracted.txt Artistic-1.0-Perl.txt GPL-1.0.txt
%doc %{name}-make.test.log
%doc CHANGES README Perl-License-Extracted.txt



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.88-0.rc2
- Fix license info, cleanup spec file

* Thu Dec 05 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.88-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
