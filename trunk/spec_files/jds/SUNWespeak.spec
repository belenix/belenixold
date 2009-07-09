#
# spec file for package SUNWespeak
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: ww36193
#

%include Solaris.inc

%define src_name espeak
%define src_url http://downloads.sourceforge.net/%{src_name}

Name:		SUNWespeak
Summary:	eSpeak - compact open source software speech synthesizer
Version:	1.37
Source:		%{src_url}/%{src_name}-%{version}-source.zip
Source1:        %{name}-manpages-0.1.tar.gz
# date:2008-08-15 owner:ww36193 type:bug
Patch1:         espeak-01-makefile.diff
# date:2008-08-29 owner:ww36193 type:bug bugster:6741969
Patch2:         espeak-02-endian.diff
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:	SUNWaudh
Requires: SUNWlibC
Requires: SUNWlibmsr

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}-source
%patch1 -p1
%patch2 -p1
gzcat %SOURCE1 | tar xf -

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
%ifarch sparc
%define endian_macro "-DBYTE_ORDER=BIG_ENDIAN"
cd platforms/big_endian
make -j$CPUS CFLAGS="%{endian_macro}"
./espeak-phoneme-data ../../espeak-data ../../espeak-data phondata-manifest
cd ../..
%else
%define endian_macro ""
%endif
cd src
make -j$CPUS EXTRA_LIBS=-lm AUDIO=sada CXXFLAGS="-O2 %{endian_macro}"
make install EXTRA_LIBS=-lm AUDIO=sada DESTDIR=$RPM_BUILD_ROOT CXXFLAGS="-O2 %{endian_macro}"
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.a

%install
#Install manpages
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%src_name-%version-source/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Tue Feb 10 2009 - halton.huo@sun.com
- Add dependency on SUNWlibC and SUNWlibmsr, CR #6755918
* Fri Sep 19 2008 - Willie Walker
- Add BuildRequires: SUNWaudh
* Mon Sep 02 2008 - Harry Lu
- Add bug ID for espeak-02-endian.diff
* Fri Aug 29 2008 - Willie Walker
- Fix SPARC build endian-ness
* Thu Aug 21 2008 - Dermot McCluskey
- added manpages and file header
* Wed Aug 20 2008 - Willie Walker
- Migrate to JDS (SFEespeak.spec to SUNWespeak.spec)
* Tue Aug 12 2008 - Willie Walker
- Port to SunStudio (thanks Brian Cameron!)
* Tue Apr 15 2008 - Willie Walker
- Upgrade to version 1.37 which contains direct SADA support and eliminates
  all PulseAudio and other dependencies.
* Tue Jan 29 2008 - Willie Walker
- Initial spec
