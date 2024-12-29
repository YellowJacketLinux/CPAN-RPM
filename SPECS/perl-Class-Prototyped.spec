%global cpanname Class-Prototyped

Name:     perl-%{cpanname}
Version:  1.16
Release:  %{?repo}0.rc1%{?dist}
Summary:  Fast prototype-based OO programming in Perl
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/T/TE/TEVERETT/%{cpanname}-%{version}.tar.gz
Source90: PERL-Artistic
Source91: PERL-Copying

BuildRequires: perl-devel
BuildRequires: perl(Module::Build)
BuildRequires: perl(Carp)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(overload)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Data::Dumper)
Requires: perl(overload)
Requires: perl(strict)
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


%build
PERL_MM_USE_DEFAULT=1   \
MODULEBUILDRC=/dev/null \
perl Build.PL --installdirs vendor
./Build


%install
./Build pure_install --destdir %{buildroot}


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
%exclude %{perl5_vendorlib}/auto/Class/Prototyped/.packlist
%license README PERL-Artistic PERL-Copying
%doc %{name}-make.test.log
%doc README PERL-Artistic PERL-Copying Changes



%changelog
* Thu Nov 21 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.16-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
