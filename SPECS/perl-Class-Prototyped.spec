%global cpanname Class-Prototyped

Name:     perl-%{cpanname}
Version:  1.16
Release:  %{?repo}0.rc2%{?dist}
Summary:  Fast prototype-based OO programming in Perl
BuildArch: noarch

Group:    Perl/Libraries
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/T/TE/TEVERETT/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt

BuildRequires: perl-devel
BuildRequires: perl(Module::Build) >= 0.4200
#
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(overload)
BuildRequires: perl(strict)
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Data::Dumper)
Requires: perl(overload)
Requires: perl(strict)
#
Provides: perl(Class::Prototyped) = %{version}
# FIXME below ?? for Graph.pm
Suggests: perl(GraphViz)
Suggests: perl(IO::File)

%description
This package provides for efficient and simple prototype-based
programming in Perl. You can provide different subroutines for
each object, and also have objects inherit their behavior and
state from another object.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from README
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README


EOF

START=`grep -n "^LICENSE" README |cut -d":" -f1`
END=`grep -n "^SEE ALSO" README |cut -d":" -f1`
DIFF="$((${END}-${START}))"
REND="$((${END}-1))"

head -${REND} README |tail -${DIFF} >> Perl-License-Extracted.txt


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
%dir %{perl5_vendorlib}/Class
%dir %{perl5_vendorlib}/Class/Prototyped
%{perl5_vendorlib}/Class/Prototyped.pm
%{perl5_vendorlib}/Class/Prototyped/Graph.pm
%{perl5_vendorlib}/Class/Prototyped/why.pod
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license Artistic-1.0-Perl.txt GPL-1.0.txt Perl-License-Extracted.txt
%doc %{name}-make.test.log
%doc README Changes Perl-License-Extracted.txt



%changelog
* Mon Dec 30 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16-0.rc2
- Spec file cleanup, license cleanup

* Thu Nov 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
