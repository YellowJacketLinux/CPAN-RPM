%global cpanname Capture-Tiny

Name:     perl-%{cpanname}
Version:  0.50
Release:  %{?repo}0.rc1%{?dist}
Summary:  Capture STDOUT and STDERR from Perl, XS or external programs
BuildArch: noarch

Group:    Perl/Libraries
License:  Apache-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz

BuildRequires: perl(:VERSION) >= 5.6.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.17
#
BuildRequires: perl(Carp)
BuildRequires: perl(CPAN::Meta) >= 2.120900
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::Temp)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(Test::More) >= 0.62
BuildRequires: perl(lib)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API} >= 5.6.0
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(Fcntl)
Requires: perl(File::Spec)
Requires: perl(File::Temp)
Requires: perl(IO::Handle)
Requires: perl(PerlIO)
Requires: perl(Scalar::Util)
Requires: perl(Time::HiRes)
Requires: perl(strict)
Requires: perl(warnings)
Provides: perl(Capture::Tiny) = %{version}

%description
`Capture::Tiny` provides a simple, portable way to capture almost
anything sent to `STDOUT` or `STDERR`, regardless of whether it
comes from Perl, from XS code or from an external program.
Optionally, output can be teed so that it is captured while being
passed through to the original filehandles. Yes, it even works on
Windows (usually). Stop guessing which of a dozen capturing
modules to use in any particular situation and just use this one.


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
%dir %{perl5_vendorlib}/Capture
%{perl5_vendorlib}/Capture/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Capture::Tiny.3*
%license LICENSE
%doc %{name}-make.test.log
%doc LICENSE Changes CONTRIBUTING.mkdn README Todo examples



%changelog
* Sun Dec 29 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.50-0.rc1
- Update to 0.50, spec file cleanup

* Sun Nov 17 2024 Michael A. Peters <anymouseprophet@gmail.com> - 0.48-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
