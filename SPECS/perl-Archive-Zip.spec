%global cpanname Archive-Zip

Name:     perl-%{cpanname}
Version:  1.68
Release:  %{?repo}0.rc2%{?dist}
Summary:  Provide an interface to ZIP archive files
BuildArch: noarch

Group:    Perl/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/P/PH/PHRED/%{cpanname}-%{version}.tar.gz
Source90: Artistic-1.0-Perl.txt
Source91: GPL-1.0.txt


BuildRequires: perl(:VERSION) >= 5.6.0
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
#
BuildRequires: perl(Carp)
BuildRequires: perl(Config)
BuildRequires: perl(Cwd)
BuildRequires: perl(Compress::Raw::Zlib) >= 2.017
BuildRequires: perl(Encode)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec) >= 0.80
BuildRequires: perl(File::Temp)
BuildRequires: perl(FileHandle)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(IO::Seekable)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Time::Local)
BuildRequires: perl(constant)
BuildRequires: perl(integer)
BuildRequires: perl(vars)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%else
Requires: perl(:MODULE_COMPAT_%(eval `perl -V:version`; echo $version))
Requires: %{perl5_vendorlib}
%endif
Requires: perl(Carp)
Requires: perl(Cwd)
Requires: perl(Compress::Raw::Zlib) >= 2.017
Requires: perl(Encode)
Requires: perl(Exporter)
Requires: perl(File::Basename)
Requires: perl(File::Copy)
Requires: perl(File::Find)
Requires: perl(File::Path)
Requires: perl(File::Spec) >= 0.80
Requires: perl(File::Temp)
Requires: perl(FileHandle)
Requires: perl(IO::File)
Requires: perl(IO::Handle)
Requires: perl(IO::Seekable)
Requires: perl(Time::Local)
Requires: perl(constant)
Requires: perl(integer)
Requires: perl(strict)
Requires: perl(vars)
#
Suggests: crc32
#
Provides: perl(Archive::Zip) = %{version}
Provides: perl(Archive::Zip::Archive) = %{version}
Provides: perl(Archive::Zip::BufferedFileHandle) = %{version}
Provides: perl(Archive::Zip::DirectoryMember) = %{version}
Provides: perl(Archive::Zip::FileMember) = %{version}
Provides: perl(Archive::Zip::Member) = %{version}
Provides: perl(Archive::Zip::MemberRead) = %{version}
Provides: perl(Archive::Zip::MockFileHandle) = %{version}
Provides: perl(Archive::Zip::NewFileMember) = %{version}
Provides: perl(Archive::Zip::StringMember) = %{version}
Provides: perl(Archive::Zip::Tree) = %{version}
Provides: perl(Archive::Zip::ZipFileMember) = %{version}

%description
The `Archive::Zip` module allows a Perl program to create,
manipulate, read, and write Zip archive files.

%package -n crc32
Group: System Environment/Utilities
Summary: Computes and prints the CRC-32 values of the given files
Requires: perl(:VERSION) >= 5.6.0
Requires: %{name} = %{version}-%{release}
Requires: perl(Archive::Zip) = %{version}
Requires: perl(FileHandle)
Requires: perl(lib)
Requires: perl(strict)
Requires: perl(vars)

%description -n crc32
This perl script uses 'Archive::Zip' to compute and print to
stdout the CRC-32 values of the given files.


%prep
%setup -q -n %{cpanname}-%{version}
cp %{SOURCE90} .
cp %{SOURCE91} .
# Extract license info from README.md
cat << "EOF" > Perl-License-Extracted.txt
The following was extracted from

  %{_datadir}/doc/perl-%{cpanname}-%{version}/README.md


EOF

START=`grep -n "^# COPYRIGHT" README.md |cut -d":" -f1`
END=`wc -l README.md |cut -d " " -f1`
DIFF="$((${END}-${START}))"
TAIL="$((${DIFF}+1))"

tail -${TAIL} README.md >> Perl-License-Extracted.txt


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
%dir %{perl5_vendorlib}/Archive
%dir %{perl5_vendorlib}/Archive/Zip
%{perl5_vendorlib}/Archive/Zip.pm
%{perl5_vendorlib}/Archive/Zip/*.pm
%{perl5_vendorlib}/Archive/Zip/FAQ.pod
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license Perl-License-Extracted.txt Artistic-1.0-Perl.txt GPL-1.0.txt
%doc %{name}-make.test.log
%doc README.md Perl-License-Extracted.txt Changes examples

%files -n crc32
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/crc32
%license Perl-License-Extracted.txt Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Perl-License-Extracted.txt

%changelog
* Wed Dec 11 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.68-0.rc2
- Clear up license files, general spec file cleanup

* Thu Nov 28 2024 Michael A. Peters <anymouseprophet@gmail.com> - 1.68-0.rc1
- Initial spec file for YJL 6.6 (LFS 12.2 based)
