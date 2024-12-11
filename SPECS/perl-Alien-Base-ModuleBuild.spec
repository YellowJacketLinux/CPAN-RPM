%global cpanname Alien-Base-ModuleBuild

Name:     perl-%{cpanname}
Version:  1.17
Release:  %{?repo}0.rc1%{?dist}
Summary:  A Module::Build subclass for building Alien:: modules and libraries
BuildArch: noarch

Group:    System Environment/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.8.1
BuildRequires: perl-devel
BuildRequires: perl(Module::Build) >= 0.4004
BuildRequires: perl(Alien::Base)
BuildRequires: perl(Alien::Base::PkgConfig) >= 1.20
BuildRequires: perl(Archive::Extract)
BuildRequires: perl(Archive::Tar) >= 1.40
BuildRequires: perl(Capture::Tiny) >= 0.17
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(Env)
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::Installed)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::chdir) >= 0.1005
BuildRequires: perl(HTML::LinkExtor)
BuildRequires: perl(HTTP::Tiny) >= 0.044
BuildRequires: perl(List::Util) >= 1.45
BuildRequires: perl(Net::FTP)
BuildRequires: perl(Path::Tiny) >= 0.077
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(Shell::Config::Generate)
BuildRequires: perl(Shell::Guess)
BuildRequires: perl(Sort::Versions)
BuildRequires: perl(Test2::V0) >= 0.000121
BuildRequires: perl(Text::Balanced)
BuildRequires: perl(Text::ParseWords) >= 3.26
BuildRequires: perl(URI)
BuildRequires: perl(URI::file)
BuildRequires: perl(parent)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Alien::Base)
Requires: perl(Alien::Base::PkgConfig) >= 1.20
Requires: perl(Archive::Extract)
Requires: perl(Archive::Tar) >= 1.40
Requires: perl(Capture::Tiny) >= 0.17
Requires: perl(Carp)
Requires: perl(Config)
Requires: perl(Digest::SHA)
Requires: perl(Env)
Requires: perl(Exporter)
Requires: perl(ExtUtils::Installed)
Requires: perl(File::Basename)
Requires: perl(File::Copy)
Requires: perl(File::Find)
Requires: perl(File::Path)
Requires: perl(File::Spec)
Requires: perl(File::chdir) >= 0.1005
Requires: perl(HTML::LinkExtor)
Requires: perl(HTTP::Tiny) >= 0.044
Requires: perl(List::Util) >= 1.45
Requires: perl(Net::FTP)
Requires: perl(Module::Build) >= 0.4004
Requires: perl(Path::Tiny) >= 0.077
Requires: perl(Scalar::Util)
Requires: perl(Shell::Config::Generate)
Requires: perl(Shell::Guess)
Requires: perl(Sort::Versions)
Requires: perl(Text::Balanced)
Requires: perl(Text::ParseWords) >= 3.26
Requires: perl(URI)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(warnings)
#
Provides: perl(Alien::Base::ModuleBuild) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Cabinet) = %{version}
Provides: perl(Alien::Base::ModuleBuild::File) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Repository) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Repository::FTP) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Repository::HTTP) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Repository::Local) = %{version}
Provides: perl(Alien::Base::ModuleBuild::Utils) = %{version}


%description
This is a subclass of 'Module::Build', that with 'Alien::Base'
allows for easy creation of Alien distributions.

NOTE: Please consider for new development of Aliens that you use
'Alien::Build' and alienfile instead. Like this module they work
with 'Alien::Base'. Unlike this module they are more easily
customized and handle a number of corner cases better.


%prep
%setup -q -n %{cpanname}-%{version}


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
%dir %{perl5_vendorlib}/Alien
%dir %{perl5_vendorlib}/Alien/Base
%dir %{perl5_vendorlib}/Alien/Base/ModuleBuild
%dir %{perl5_vendorlib}/Alien/Base/ModuleBuild/Repository
%{perl5_vendorlib}/Alien/Base/ModuleBuild.pm
%{perl5_vendorlib}/Alien/Base/ModuleBuild/*.pm
%{perl5_vendorlib}/Alien/Base/ModuleBuild/*.pod
%{perl5_vendorlib}/Alien/Base/ModuleBuild/Repository/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes README



%changelog
* Thu Dec 05 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.17-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
