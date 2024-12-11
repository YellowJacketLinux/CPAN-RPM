%global cpanname aliased

Name:     perl-%{cpanname}
Version:  0.34
Release:  %{?repo}0.rc2%{?dist}
Summary:  Use shorter versions of class names
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires: perl-devel
BuildRequires: perl(Module::Build::Tiny)
BuildRequires: perl(B)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Carp)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test::More)
BuildRequires: perl(if)
BuildRequires: perl(lib)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(aliased) = %{version}

%description
'aliased' is simple in concept but is a rather handy module. It
loads the class you specify and exports into your namespace a
subroutine that returns the class name. You can explicitly alias
the class to another name or, if you prefer, you can do so
implicitly.


%prep
%setup -q -n %{cpanname}-%{version}


%build
PERL_MM_USE_DEFAULT=1   \
perl Build.PL --installdirs vendor
./Build


%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete

%check
./Build test > %{name}-make.test.log 2>&1


%files
%defattr(0444,root,root,-)
%{perl5_vendorlib}/aliased.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING README



%changelog
* Fri Nov 29 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.34-0.rc2
- Remove .packlist during %%install

* Mon Nov 25 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.34-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
