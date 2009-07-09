#
# spec file for package SUNWgnome-component
#
# includes module(s): libIDL, ORBit2, libbonobo
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _sysconfdir /etc/%{_arch64}
%define _sbindir %{_prefix}/sbin/%{_arch64}
%use idl_64 = libIDL.spec
%use orbit_64 = ORBit2.spec
%use bonobo_64 = libbonobo.spec
%endif

%define _sbindir %{_prefix}/sbin
%include base.inc
%use idl = libIDL.spec
%use orbit = ORBit2.spec
%use bonobo = libbonobo.spec

Name:                    SUNWgnome-component
Summary:                 GNOME CORBA ORB and component framework
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-glib-devel
Requires: SUNWlibpopt
Requires: SUNWgnome-component-root
Requires: SUNWgnome-base-libs
Requires: SUNWdbus
Requires: SUNWperl584usr
Requires: SUNWperl584core
Requires: SUNWlxml
Requires: SUNWdbus-glib
%if %option_with_gnu_iconv
# for /usr/gnu/bin/printf needed in po/Makefile
BuildRequires: SUNWgnu-coreutils
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-common-devel
Requires: SUNWgnome-base-libs-devel
Requires: SUNWlxml
Requires: SUNWgnome-component
Requires: SUNWgnome-base-libs
Requires: SUNWlibpopt
Requires: SUNWlibms

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%idl_64.prep -d %name-%version/%_arch64
%orbit_64.prep -d %name-%version/%_arch64
%bonobo_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%idl.prep -d %name-%version/%{base_arch}
%orbit.prep -d %name-%version/%{base_arch}
%bonobo.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PERL=/usr/perl5/bin/perl
export PERL_PATH=/usr/perl5/bin/perl
export CPP=/usr/lib/cpp

%ifarch amd64 sparcv9
%if %option_with_gnu_iconv
export EXTRA_LDFLAGS="-L/usr/gnu/lib/%_arch64 -R/usr/gnu/lib/%_arch64"
%endif
export PKG_CONFIG_PATH=../ORBit2-%{orbit.version}:../libIDL-%{idl.version}:../libbonobo-%{bonobo.version}:/usr/lib/%{_arch64}/pkgconfig

%idl_64.build -d %name-%version/%_arch64
%orbit_64.build -d %name-%version/%_arch64

export EXTRA_LDFLAGS="-L%{_builddir}/%name-%version/%_arch64/ORBit2-%{orbit.version}/src/services/name -R/usr/lib/%{_arch64}"

%bonobo_64.build -d %name-%version/%_arch64
%endif

export EXTRA_LDFLAGS=

export PKG_CONFIG_PATH=../ORBit2-%{orbit.version}:../libIDL-%{idl.version}:../libbonobo-%{bonobo.version}:/usr/lib/pkgconfig
%if %option_with_gnu_iconv
export EXTRA_LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
%endif
%idl.build -d %name-%version/%{base_arch}
%orbit.build -d %name-%version/%{base_arch}

export EXTRA_LDFLAGS="-L%{_builddir}/%name-%version/%{base_arch}/ORBit2-%{orbit.version}/src/services/name"
 
%bonobo.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%idl_64.install -d %name-%version/%_arch64
%orbit_64.install -d %name-%version/%_arch64
%bonobo_64.install -d %name-%version/%_arch64
%endif

%idl.install -d %name-%version/%{base_arch}
%orbit.install -d %name-%version/%{base_arch}
%bonobo.install -d %name-%version/%{base_arch}

rm -f $RPM_BUILD_ROOT%{_mandir}/*/*.gz
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/info

%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/libIDL-config-2
rm $RPM_BUILD_ROOT%{_libexecdir}/%{_arch64}/bonobo-activation-server
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/orbit2-config
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/bonobo-slay
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch} libIDL-%{idl.version}/AUTHORS
%doc -d %{base_arch} libIDL-%{idl.version}/README
%doc(bzip2) -d %{base_arch} libIDL-%{idl.version}/NEWS
%doc(bzip2) -d %{base_arch} libIDL-%{idl.version}/COPYING
%doc(bzip2) -d %{base_arch} libIDL-%{idl.version}/ChangeLog
%doc -d %{base_arch} ORBit2-%{orbit.version}/AUTHORS
%doc -d %{base_arch} ORBit2-%{orbit.version}/README
%doc(bzip2) -d %{base_arch} ORBit2-%{orbit.version}/NEWS
%doc(bzip2) -d %{base_arch} ORBit2-%{orbit.version}/COPYING
%doc(bzip2) -d %{base_arch} ORBit2-%{orbit.version}/COPYING.LIB
%doc(bzip2) -d %{base_arch} ORBit2-%{orbit.version}/ChangeLog
%doc -d %{base_arch} libbonobo-%{bonobo.version}/AUTHORS
%doc -d %{base_arch} libbonobo-%{bonobo.version}/README
%doc(bzip2) -d %{base_arch} libbonobo-%{bonobo.version}/NEWS
%doc(bzip2) -d %{base_arch} libbonobo-%{bonobo.version}/COPYING
%doc(bzip2) -d %{base_arch} libbonobo-%{bonobo.version}/COPYING.LIB
%doc(bzip2) -d %{base_arch} libbonobo-%{bonobo.version}/ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/activation-client
%{_bindir}/bonobo-activation-run-query
%{_bindir}/bonobo-slay
%{_bindir}/ior-decode-2
%{_bindir}/linc-cleanup-sockets
%{_bindir}/typelib-dump
%{_bindir}/echo-client-2
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/bonobo-activation-sysconf
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/bonobo/monikers/*.so
%{_libdir}/bonobo/servers
%{_libdir}/bonobo-2.0
%{_libdir}/orbit*/*.so
%{_libexecdir}/bonobo-activation-server
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/activation-client
%{_bindir}/%{_arch64}/bonobo-activation-run-query
%{_bindir}/%{_arch64}/ior-decode-2
%{_bindir}/%{_arch64}/linc-cleanup-sockets
%{_bindir}/%{_arch64}/typelib-dump
%{_bindir}/%{_arch64}/echo-client-2
%dir %attr (0755, root, bin) %{_sbindir}/%{_arch64}
%{_sbindir}/%{_arch64}/bonobo-activation-sysconf
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/bonobo/monikers/*.so
%{_libdir}/%{_arch64}/bonobo/servers
%{_libdir}/%{_arch64}/bonobo-2.0
%{_libdir}/%{_arch64}/orbit*/*.so
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libIDL*
%{_bindir}/orbit*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/orbit-idl-2
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/idl
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/[bo]*
%ifarch sparcv9 amd64
%{_sysconfdir}/%{_arch64}/*
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Fri Sep 12 2008 - christian.kelly@sun.com
- Take out %{_datadir}/doc as it's no longer there.
* Wed Sep 10 2008 - ghee.teo@sun.com
- Made changes to use new copyright format.
* Thu Aug 21 2008 - laca@sun.com
- reset EXTRA_LDFLAGS before starting the 32-bit build to avoid adding
  the 64-bit runpath to the 32-bit binaries, fixes 6738781
* Wed Jun 18 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus/-devel as required by libbonobo. Add
  SUNWdbus-bindings/-devel too as /usr/lib/bonobo-activation-server requires 
  /usr/lib/libdbus-glib-1.so.2
* Fri Oct 26 2007 - damien.carbery@sun.com
- Only add /usr/gnu/lib to EXTRA_LDFLAGS when using GNU iconv.
* Tue Oct  2 2007 - laca@sun.com
- add SUNWgnu-coreutils dep for /usr/bin/printf
* Sun Sep 30 2007 - laca@sun.com
- convert to new style multi-ISA build
* Thu Apr 26 2007 - laca@sun.com
- set PERL_PATH for bonobo-slay, part of 6454456
* Fri Sep 08 2006 - Matt.Keenan@sun.com
- Remove "rm" of _mandir during %install
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sat Aug 12 2006 - laca@sun.com
- set PERL to /usr/perl5/bin/perl as per CR6454456
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Sun Feb 19 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Feb  2 2006 - damien.carbery@sun.com
- Add hack to use /usr/xpg4/bin/sed for libbonobo so last line of file not 
  dropped.
* Sun Sep 18 2005 - laca@sun.com
- remove unpackaged 64-bit files
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Wed May 11 2005 - brian.cameron@sun.com
- Create symlink when building ORBit2 to allow uninstalled.pc
  files to find header files properly.
* Thu Oct 21 2004 - laca@sun.com
- set PERL and PERL_PATH, fixes 5100958
* Wed Oct 13 2004 - laca@sun.com
- use _pkg_config_path64 in $PKG_CONFIG_PATH64
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added bonobo-slay.1 manpage
* Tue Aug 31 2004 - shirley.woo@sun.com
- Bug 5091588 : Added BuildRequires SUNWgnome-base-libs-devel since 
  SUNWgnome-base-libs was split
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004 - damien.carbery@sun.com
- Changed manpage mode to 0755 for Solaris integration.
* Tue Aug 17 2004 - damien.carbery@sun.com
- Changed manpage mode to 0755 for Solaris integration.
* Mon Aug 16 2004 - damien.carbery@sun.com
- Changed multiple manpage modes to 0755 for Solaris integration.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Thu May 27 2004 - laca@sun.com
- added l10n subpkg, remove share, since it only contained the l10n files
* Wed May 19 2004 - brian.cameron@sun.com
- Added missing man pages
* Thu May 06 2004 - brian.cameron@sun.com
- Removed libraries from devel package since they are already
  in the SUNWgnome-component package.
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Fri Mar 12 2004 - Niall.Power@sun.com
- more missing files: sbindir, bonobo monikiers and servers
* Mon Mar 01 2003 - Niall.Power@sun.com
- added missing bonobo/activation binaries to
  files map. 
* Fri Feb 13 2004 - Laszlo.Peter@sun.com
- added %dir flags
* Mon Jan 19 2004 - Laszlo.Peter@sun.com
- initial Sun release.
