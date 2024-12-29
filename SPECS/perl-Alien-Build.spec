%global cpanname Alien-Build

### Comment out bootstrap globals for final build
### Uncomment (or put in ~/.rpmmacros etc.) for bootstrap build
#
# Avoid circular test dependencies until bootstrapped
#
#%%global alienbuild_bootstrap 1
#%%global ffiplatypus_bootstrap 1

Name:     perl-%{cpanname}
Version:  2.84
Release:  %{?repo}0.rc3%{?dist}
Summary:  Build external dependencies for use in CPAN
BuildArch: noarch

Group:    Perl/Installer-Tools
License:  Artistic-1.0-Perl or GPL-1.0-or-later
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.8.4
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.64
#
BuildRequires: perl(Capture::Tiny) >= 0.17
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(Env)
BuildRequires: perl(Env::ShellWords)
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(ExtUtils::ParseXS) >= 3.30
BuildRequires: perl(FFI::CheckLib) >= 0.11
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::Temp)
BuildRequires: perl(File::Which) >= 1.10
BuildRequires: perl(File::chdir)
BuildRequires: perl(IO::Socket::SSL)
BuildRequires: perl(JSON::PP)
BuildRequires: perl(List::Util) >= 1.33
BuildRequires: perl(Mojo::DOM58) >= 1.00
BuildRequires: perl(Net::SSLeay)
BuildRequires: perl(Path::Tiny) >= 0.077
BuildRequires: perl(PkgConfig) >= 0.14026
BuildRequires: perl(Readonly) >= 1.60
BuildRequires: perl(Storable)
BuildRequires: perl(Term::ANSIColor)
BuildRequires: perl(Test2::API) >= 1.302096
BuildRequires: perl(Test2::V0) >= 0.000121
BuildRequires: perl(Text::ParseWords) >= 3.26
BuildRequires: perl(YAML)
BuildRequires: perl(constant)
BuildRequires: perl(overload)
BuildRequires: perl(parent)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
# Bootstrap Conditional BuildRequires
%if 0%{?!alienbuild_bootstrap:1} == 1
BuildRequires: perl(Alien::Base::ModuleBuild)
BuildRequires: perl(Alien::cmake3)
# Below is broken w/ YJL libpkgconfig
#BuildRequires: perl(PkgConfig::LibPkgConf)
%endif
# Below *probably* should be integrated into above*
%if 0%{?!ffiplatypus_bootstrap:1} == 1
BuildRequires: perl(FFI::Platypus)
%endif
#
# Requires
#
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.8.4
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Suggests: perl(Alien::cmake3)
Requires: perl(Capture::Tiny) >= 0.17
Requires: perl(Carp)
Requires: perl(Config)
Requires: perl(Data::Dumper)
Requires: perl(Digest::SHA)
Requires: perl(Env)
Requires: perl(Env::ShellWords)
Requires: perl(Exporter)
Requires: perl(ExtUtils::CBuilder)
Requires: perl(ExtUtils::MakeMaker) >= 6.64
Requires: perl(ExtUtils::ParseXS) >= 3.30
Requires: perl(FFI::CheckLib) >= 0.11
Suggests: perl(FFI::Platypus)
Requires: perl(File::Basename)
Requires: perl(File::Copy)
Requires: perl(File::Find)
Requires: perl(File::Spec)
Requires: perl(File::Temp)
Requires: perl(File::Which) >= 1.10
Requires: perl(File::chdir)
Requires: perl(IO::Socket::SSL)
Requires: perl(JSON::PP)
Requires: perl(List::Util) >= 1.33
Requires: perl(Mojo::DOM58) >= 1.00
Requires: perl(Net::SSLeay)
Requires: perl(Path::Tiny) >= 0.077
Requires: perl(PkgConfig) >= 0.14026
# Below broken for YJL libpkgconfig, so suggest only
Suggests: perl(PkgConfig::LibPkgConf) >= 0.04
Requires: perl(Storable)
Requires: perl(Term::ANSIColor)
Requires: perl(Test2::API) >= 1.302096
Requires: perl(Text::ParseWords) >= 3.26
Requires: perl(YAML)
Requires: perl(constant)
Requires: perl(overload)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(warnings)
Suggests: %{_bindir}/pkg-config
%if 0%{?!alienbuild_bootstrap:1} == 1
Requires: perl(Alien::Base::ModuleBuild)
%endif
#
Provides: perl(Alien::Base) = %{version}
Provides: perl(Alien::Base::PkgConfig) = %{version}
Provides: perl(Alien::Base::Wrapper) = %{version}
Provides: perl(Alien::Build) = %{version}
Provides: perl(Alien::Build::CommandSequence) = %{version}
Provides: perl(Alien::Build::Interpolate) = %{version}
Provides: perl(Alien::Build::Interpolate::Default) = %{version}
Provides: perl(Alien::Build::Log) = %{version}
Provides: perl(Alien::Build::Log::Abbreviate) = %{version}
Provides: perl(Alien::Build::Log::Default) = %{version}
Provides: perl(Alien::Build::MM) = %{version}
Provides: perl(Alien::Build::Plugin) = %{version}
Provides: perl(Alien::Build::Plugin::Build::Autoconf) = %{version}
Provides: perl(Alien::Build::Plugin::Build::CMake) = %{version}
Provides: perl(Alien::Build::Plugin::Build::Copy) = %{version}
Provides: perl(Alien::Build::Plugin::Build::MSYS) = %{version}
Provides: perl(Alien::Build::Plugin::Build::Make) = %{version}
Provides: perl(Alien::Build::Plugin::Build::SearchDep) = %{version}
Provides: perl(Alien::Build::Plugin::Core::CleanInstall) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Download) = %{version}
Provides: perl(Alien::Build::Plugin::Core::FFI) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Gather) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Legacy) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Override) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Setup) = %{version}
Provides: perl(Alien::Build::Plugin::Core::Tail) = %{version}
Provides: perl(Alien::Build::Plugin::Decode::DirListing) = %{version}
Provides: perl(Alien::Build::Plugin::Decode::DirListingFtpcopy) = %{version}
Provides: perl(Alien::Build::Plugin::Decode::HTML) = %{version}
Provides: perl(Alien::Build::Plugin::Decode::Mojo) = %{version}
Provides: perl(Alien::Build::Plugin::Digest::Negotiate) = %{version}
Provides: perl(Alien::Build::Plugin::Digest::SHA) = %{version}
Provides: perl(Alien::Build::Plugin::Digest::SHAPP) = %{version}
Provides: perl(Alien::Build::Plugin::Download::Negotiate) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::CurlCommand) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::HTTPTiny) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::Local) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::LocalDir) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::LWP) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::NetFTP) = %{version}
Provides: perl(Alien::Build::Plugin::Fetch::Wget) = %{version}
Provides: perl(Alien::Build::Plugin::Gather::IsolateDynamic) = %{version}
Provides: perl(Alien::Build::Plugin::PkgConfig::CommandLine) = %{version}
Provides: perl(Alien::Build::Plugin::PkgConfig::LibPkgConf) = %{version}
Provides: perl(Alien::Build::Plugin::PkgConfig::MakeStatic) = %{version}
Provides: perl(Alien::Build::Plugin::PkgConfig::Negotiate) = %{version}
Provides: perl(Alien::Build::Plugin::PkgConfig::PP) = %{version}
Provides: perl(Alien::Build::Plugin::Prefer::BadVersion) = %{version}
Provides: perl(Alien::Build::Plugin::Prefer::GoodVersion) = %{version}
Provides: perl(Alien::Build::Plugin::Prefer::SortVersions) = %{version}
Provides: perl(Alien::Build::Plugin::Probe::CBuilder) = %{version}
Provides: perl(Alien::Build::Plugin::Probe::CommandLine) = %{version}
Provides: perl(Alien::Build::Plugin::Probe::Vcpkg) = %{version}
Provides: perl(Alien::Build::Plugin::Test::Mock) = %{version}
Provides: perl(Alien::Build::Temp) = %{version}
Provides: perl(Alien::Build::Util) = %{version}
Provides: perl(Alien::Build::Version::Basic) = %{version}
Provides: perl(Alien::Build::rc) = %{version}
Provides: perl(Alien::Role) = %{version}
Provides: perl(Alien::Util) = %{version}
Provides: perl(Test::Alien) = %{version}
Provides: perl(Test::Alien::Build) = %{version}
Provides: perl(Test::Alien::CanCompile) = %{version}
Provides: perl(Test::Alien::Diag) = %{version}
Provides: perl(Test::Alien::Run) = %{version}
Provides: perl(Test::Alien::Synthetic) = %{version}
Provides: perl(alienfile) = %{version}


%description
This distribution provides tools for building external (non-CPAN)
dependencies for CPAN distributions. `Alien::Build` is mainly
designed to be used at install time by a CPAN client, and work
closely with `Alien::Base` which is used at runtime.


%prep
%setup -q -n %{cpanname}-%{version}


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
%dir %{perl5_vendorlib}/Alien
%dir %{perl5_vendorlib}/Alien/Base
%dir %{perl5_vendorlib}/Alien/Build
%dir %{perl5_vendorlib}/Alien/Build/Interpolate
%dir %{perl5_vendorlib}/Alien/Build/Log
%dir %{perl5_vendorlib}/Alien/Build/Manual
%dir %{perl5_vendorlib}/Alien/Build/Plugin
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Build
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Core
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Decode
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Digest
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Download
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Extract
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Fetch
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Gather
%dir %{perl5_vendorlib}/Alien/Build/Plugin/PkgConfig
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Prefer
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Probe
%dir %{perl5_vendorlib}/Alien/Build/Plugin/Test
%dir %{perl5_vendorlib}/Alien/Build/Version
%dir %{perl5_vendorlib}/Test
%dir %{perl5_vendorlib}/Test/Alien
%{perl5_vendorlib}/alienfile.pm
%{perl5_vendorlib}/Alien/*.pm
%{perl5_vendorlib}/Alien/Base/*.pm
%{perl5_vendorlib}/Alien/Base/*.pod
%{perl5_vendorlib}/Alien/Build/*.pm
%{perl5_vendorlib}/Alien/Build/*.pod
%{perl5_vendorlib}/Alien/Build/Interpolate/*.pm
%{perl5_vendorlib}/Alien/Build/Log/*.pm
%{perl5_vendorlib}/Alien/Build/Manual/*.pod
%{perl5_vendorlib}/Alien/Build/Plugin/*.pod
%{perl5_vendorlib}/Alien/Build/Plugin/Build/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Core/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Decode/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Digest/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Download/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Extract/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Fetch/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Gather/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/PkgConfig/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Prefer/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Probe/*.pm
%{perl5_vendorlib}/Alien/Build/Plugin/Test/*.pm
%{perl5_vendorlib}/Alien/Build/Version/*.pm
%{perl5_vendorlib}/Test/Alien.pm
%{perl5_vendorlib}/Test/Alien/*.pm
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes* README SUPPORT example



%changelog
* Wed Dec 18 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.84-0.rc3
- Some spec file cleanup for YJL standards

* Fri Dec 06 2024 Michael A. Peters <anymouseprophet@gmail.com> - 2.84-0.rc2
- Initial spec file for YJL 6.6 (LFS 12.2 based)
