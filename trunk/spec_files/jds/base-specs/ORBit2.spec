
# spec file for package ORBit2
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         ORBit2
License:      LGPL
Group:        System/Libraries
Provides:     ORBit2 
Summary:      High-performance CORBA Object Request Broker
Version:      2.14.17
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:       http://ftp.gnome.org/pub/GNOME/sources/ORBit2/2.14/ORBit2-%{version}.tar.bz2
Source1:      orbitrc
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://www.gnome.org/projects/ORBit2
DocDir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:	      /sbin/ldconfig

%define libIDL_version 0.8.2
%define popt_version 1.6.4
%define gtk_doc_version 1.1
%define linc_version 1.1.1

Requires:      libIDL >= %{libIDL_version}
Requires:      popt >= %{popt_version}
BuildRequires: libIDL-devel >= %{libIDL_version}
BuildRequires: popt-devel >= %{popt_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}

Obsoletes:	linc < %{linc_version}
Provides:	linc = %{linc_version}
Obsoletes:	linc-devel < %{linc_version}
Provides:	linc-devel = %{linc_version}

%description
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

%package devel
Summary:      High-performance CORBA Object Request Broker
Group:        Development/Libraries
Provides:     ORBit2-devel
Autoreqprov:  on
Requires:     %name = %version 
Requires:     libIDL-devel >= %{libIDL_version}

%description devel
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

%prep
%setup -q
ln -s `pwd`/src/services/name `pwd`/include/ORBitservices

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
gtkdocize
aclocal $ACLOCAL_FLAGS -I %{_datadir}/aclocal
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    --sysconfdir=%{_sysconfdir}	\
            %{gtk_doc_option}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install --mode=0644 %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/orbitrc
AFILES=" libORBit-2 libORBit-imodule-2 libORBitCosNaming-2 orbit-2.0/Everything_module"
pushd $RPM_BUILD_ROOT%{_libdir}
for i in $AFILES; do
       rm $i.a
       rm $i.la
done
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libORBit*.so.*
%{_libdir}/orbit-2.0/Every*so*
%{_bindir}/ior-decode-2
%{_bindir}/typelib-dump
%{_bindir}/linc-cleanup-sockets
%{_sysconfdir}/orbitrc

%files devel
%defattr(-, root, root)
%{_includedir}/orbit-2.0
%{_bindir}/orbit-idl-2
%{_bindir}/orbit2-config
%{_libdir}/libname-server-2.a
%{_libdir}/libORBit*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/idl/orbit-2.0/*.idl
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/ORBit2
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.14.17
* Mon Sep 29 2008 - brian.cameron@sun.com
- Bump to 2.14.16.
* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 2.14.15.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.14.14
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.14.13. Remove upstream patch, 01-linc-localhost.
* Tue Apr 15 2008 - jeff.cai@sun.com
- Add patch -01-linc-localhost.diff
  Fix bug #527128
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.14.12.
* Fri Jan 25 2008 - damien.carbery@sun.com
- Bump to 2.14.11.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.14.10.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.14.9.
* Fri Jul 27 2007 - damien.carbery@sun.com
- Bump to 2.14.8. Remove upstream patch, 01-secureports.
* Wed Apr 04 2007 - brian.cameron@sun.com
- Add patch ORBit2-01-secureports.diff so that ports are opened more 
  securely.  This makes sure to bind the socket when using IPv4 and
  IPv6 since this is needed for Secure-By-Default requirements to be
  met.  Without this when you run "netstat -a" you see that all the
  GNOME sockets are listening wide open on the internet even when
  ORBLocalOnly=1 in /etc/orbitrc.  After this change, you see that
  the ports are listed properly with "localhost.####" in the "Local
  Address" column. This indicates Secure By Default is working.
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Tue Mar 06 2005 - damien.carbery@sun.com
- Bump to 2.14.7.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.14.6. Remove upstream patch, 01-uninstalled_pc.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.14.5.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.14.4. Remove upstream patch, ORBit-02-fixhypen.diff.
* Fri Dec 08 2006 - damien.carbery@sun.com
- Bump to 2.14.3. Remove upstream patches, 03-gcc-Werror and 04-localonly.
  Renumber remainder.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Sep 20 2006 - brian.cameron@sun.omc
- Add patch ORBit-06-fixhyphen.diff to resolve escalation #1-19359745
  and bug 6466464.  GNOME Bugzilla bug #152659.
* Fri Sep 15 2006 - brian.cameron@sun.com
- Remove patch ORBit-03-dhcp-hostname.diff after reviewing with the
  maintainer, Michael Meeks, andt he patch writer Arvind
  Samptur we all agreed that this is the wrong approach to fix any 
  issues with ORBit haveing problems with the hostname changing due to
  DHCP reallocation.
* Tue Aug  1 2006 - brian.cameron@sun.com
- Add patch 5 so LocalOnly mode works on Solaris.  This patch causes
  the linc library to not use getaddrinfo() and getaddrname(), which
  do not seem to work on Solaris.  The fallback code that uses
  gethostbyname() and gethostbyaddr() seem to work better.  Might be
  good to fix the getaddrinfo(), getaddrname() code to work on
  Solaris, though not sure if this is really necessary.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Tue Jun  2 2006 - simon.zheng@sun.com
- Add patch, ORBIT-05-signal-broadcast.diff.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Thu Feb  9 2006 - damien.carbery@sun.com
- Remove upstream patch, ORBit-05-illegal_cast.diff.
* Wed Feb  8 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Add patch, 05-illegal_cast.diff, to remove unnecessary cast that breaks the 
  build. Bugzilla #324686.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 2.13.2. Remove upstream patch, 04-ipv4-port-hosed.
- Add ORBit-04-gcc-Werror.diff so gcc option is only set when using gcc.
* Thu Oct 06 2005 - damien.carbery@sun.com
- Add gtkdocize call to 64 bit section.
* Wed Sep 29 2005 - damien.carbery@sun.com
- Add gtkdocize call for automake.
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 2.12.4.
* Sun Sep 18 2005 - glynn.foster@sun.com
- Remove some patches.
* Wed Aug 17 2005 - damien.carbery@sun.com
- Bump to 2.12.3.
* Wed Jun 15 2005 - laca@sun.com
- Add patch new-pkgconfig.diff taken from GNOME CVS to make ORBit2 build
  with pkg-config > 0.15.0
* Fri May 06 2005 - glynn.foster@wipro.com
- Bump to 2.12.2
* Tue Apr 19 2005 - arvind.samptru@wipro.com
- fix login failure when ipv4 port in the IOR
  is taken to be valid on login after reboot
  Fixes #6238754
* Fri Mar 11 2005 - arvind.samptur@wipro.com
- fix a bogus linc_protocol_destroy assertion 
  coming up at install time
* Wed Mar 02 2005 - arvind.samptur@wipro.com
- another attempt to fix dhcp bug safely. 
* Tue Feb 15 2005 - arvind.samptur@wipro.com
- Add patch to fix dhcp hostname change blocking 
  the login
* Tue Dec 21 2004 - ghee.teo@sun.com
- Obsoletes linc for upgrade purposes. Fix bug 6211773.
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - <ghee.teo@sun.com>
- Put back /etc/orbitrc which is required by A11y login. Bug 5059822.
* Tue Jun 08 2004 - <ghee.teo@sun.com>
- removed /etc/orbitrc at the moment as this is a feature for Cinnabar not
  metro.
* Mon Feb 23 2004 - <stephen.browne@sun.com>
- Bump to 2.9.8
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Bump to 2.9.7, gtk-doc.make hack patch 03
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Bump to 2.9.2
* Mon Oct 02 2003 - <markmc@sun.com> 2.8.1-2
- Require gtk-doc.
* Mon Oct 02 2003 - <markmc@sun.com> 2.8.1-1
- Update to 2.8.1.
* Thu Aug 14 2003 - <laca@sun.com>
- add patch to disable static linking of test programs
- remove lib*.a and .la, except libname-server-2.a which is
  apparently needed by bonobo-activation
- move *.so to -devel
* Fri Aug 01 2003 - <markmc@sun.com> 2.6.3-1
- Upgrade to 2.6.3.
* Wed Apr 30 2003 - <niall.power@sun.com>
- Create new spec file for ORBit2
