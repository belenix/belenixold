#
# spec file for package SFEsubversion
#
# includes module(s): subversion
#
%include Solaris.inc
%include usr-gnu.inc

%define package_svn_apache %(/usr/bin/pkginfo -q SUNWsvn && echo 0 || echo 1)

Name:			SFEsubversion
License:		Apache,LGPL,BSD
Group:			system/dscm
Version:		1.4.6
Release:		1
Summary:		Subversion SCM
Source:			http://subversion.tigris.org/downloads/subversion-%{version}.tar.bz2

# Home-grown svn-config needed by kdesdk
Source1:                svn-config
Patch1:                 subversion-01-libneon.la.diff
URL:			http://subversion.tigris.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
Requires: SFEgdbm
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWpostrun
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
#Requires: SFEneon
Requires: SUNWneon
Requires: SFElibapr
Requires: SFEaprutil
BuildRequires: SUNWPython
BuildRequires: SUNWopenssl-include
BuildRequires: SFEgdbm-devel
BuildRequires: SUNWapch22u
BuildRequires: SFElibapr-devel
BuildRequires: SFEaprutil-devel
#BuildConflicts: CBEsvn

%description
Subversion source code management system.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWbash
Requires: SUNWopenssl-include
Requires: SFEgdbm-devel
Requires: SUNWPython
Requires: SFElibapr-devel
Requires: SFEaprutil-devel
%if %package_svn_apache
Requires: SUNWapch22u
%endif

%if %package_svn_apache
%package usr
Summary:                 %{summary} - Apache2 modules
SUNW_BaseDir:            /usr
%include default-depend.inc
Requires:                %{name}
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n subversion-%{version}
%patch1 -p1 -b .patch01

%build
export PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir}"
export PATH=$PATH:/usr/apache2/2.2/bin
aclocal -I build/ac-macros
autoconf
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --disable-static \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --disable-mod-activation \
    --mandir=%{_mandir} \
    --with-ssl \
    --infodir=%{_infodir} \
    --without-berkeley-db \
    --with-apr=/usr/gnu/bin/apr-1-config \
    --with-apr-util=/usr/gnu/bin/apu-1-config \
%if %package_svn_apache
    --with-neon=/usr \
    --with-apxs=/usr/apache2/2.2/bin/apxs
%else
    --with-neon=/usr 
%endif

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Patch svn-config with the correct version
cat $RPM_BUILD_ROOT%{_bindir}/svn-config | sed s/SVN_VERSION/%{version}/ > $RPM_BUILD_ROOT%{_bindir}/svn-config.new
mv $RPM_BUILD_ROOT%{_bindir}/svn-config.new $RPM_BUILD_ROOT%{_bindir}/svn-config
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/svn-config

%if %package_svn_apache
%else
rm -rf ${RPM_BUILD_ROOT}/usr/apache2
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/svn*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %package_svn_apache
%files usr
%defattr (-, root, bin)
/usr/apache2
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Feb 24 2008 - moinakg@gmail.com
- Change to fix install weirdness.
* Tue Jan 22 2008 - moinakg@gmail.com
- Major rework to install in /usr/gnu and avoid conflict with SUNWsvn
- Depends on two new package SFElibapr and SFEaprutil. Having svn to depend on whole
- of Apache seems a bit of an overkill. These are also needed by kdesdk.
- Bumped version to 1.4.6
- Package a home-grown svn-config to satisfy a few software like kdesdk.
* Thu Jan  3 2008 - laca@sun.com
- update apache2 location for newer nevada builds
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.4.3.
- Remove "-I/usr/sfw/include" from CFLAGS and 
  "-L/usr/sfw/lib -R/usr/sfw/lib" from LDFLAGS to build pass
- Nevada bundle neon, Change require from SFEneon to SUNWneon
* Sat Oct 14 2006 - laca@sun.com
- disable parallel build as it breaks on multicpu systems
- bump to 1.4.0
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEsubversion
- add info stuff
- add some configure options to enable ssl, apache, https support
- add devel and l10n pkgs
* Sat Jan  7 2006  <glynn.foster@sun.com>
- initial version
