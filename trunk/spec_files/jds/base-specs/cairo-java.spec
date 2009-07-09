#
# spec file for package cairo-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%define maj_min_ver 1.0
%define rev 8

%ifos solaris
%define docbasedir %{_datadir}/lib/java/javadoc/java-gnome
%define macrobasedir %{_datadir}/lib/java/javadoc/java-gnome
%define jardir %{_datadir}/lib/java
%define srcjardir %{_datadir}/lib/java/src/java-gnome
%else
%define docbasedir %{_datadir}/doc
%define macrobasedir %{_datadir}
%define jardir %{_datadir}/java
%define srcjardir %{_datadir}/java
%endif

Name:                    cairo-java
License:		 LGPL	
Group:			 System/Library
Version:                 %{maj_min_ver}.%{rev}
Release:		 1
Distribution:		 Java Desktop System
Vendor:			 Sun Microsystems, Inc.
Summary:                 Part of Java-Gnome - Java to Cairo core bindings
Source:                  http://ftp.gnome.org/pub/gnome/sources/cairo-java/%{maj_min_ver}/cairo-java-%{version}.tar.bz2
URL:                     http://java-gnome.sourceforge.net
BuildRoot:		 %{_tmppath}/%{name}-%{version}-build
Docdir:			 %{_defaultdocdir}/doc
Autoreqprov:		 on


Requires: glib2-java >= 0.4.0
Requires: cairo >= 1.2.4
BuildRequires: glib2-java-devel >= 0.4.0

%package devel
Summary:                 %{summary} - development files
Requires:                %name

%description
cairo-java base package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n cairo-java-%{version}

%build
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
   	    --with-docbasedir=%{docbasedir}	\
   	    --with-jardir=%{jardir}		\
	    --with-srcjar			\
	    --with-srcjardir=%{srcjardir}       \
            --without-gcj-compile               

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libexecdir}/libcairojni.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libcairojni-%{maj_min_ver}.so
%{_libdir}/libcairojni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{jardir}
%{jardir}/cairo%{maj_min_ver}-%{version}.jar
%{jardir}/cairo%{maj_min_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/cairo-java.pc
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{srcjardir}
%{srcjardir}/cairo%{maj_min_ver}-src.jar

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/cairo-java-%{version}/AUTHORS
%{docbasedir}/cairo-java-%{version}/COPYING
%{docbasedir}/cairo-java-%{version}/NEWS
%{docbasedir}/cairo-java-%{version}/README
%{docbasedir}/cairo-java-%{version}/INSTALL
%{docbasedir}/cairo-java-%{version}/api/*

%changelog
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 1.0.8.
* Wed Oct 25 2006 - john.rice@sun.com
- Bumped cairo-java tarball to 1.0.6 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- patches/cairo-java-01-uninstalled.diff
- Solaris/patches/cairo-java-02-installpaths.diff
- Solaris/patches/cairo-java-03-doc.diff
- patches/cairo-java-04-srcjar.diff
- patches/cairo-java-05-docbasedir.diff

* Thur Oct 12 2006 - john.rice@sun.com
- Modify installpaths patch to allow jardir to be specified in configure
- Add patch to allow api doc to be created
- cairo-java-03-doc.diff: work around unsupported "find -mindep" in generating
  api doc list
- Enabled creation of srcjar with configure switch
- cairo-java-04-srcjar.diff: added BUILD_SRCJAR target to Makefile.am
- Modified srcjardir to conform to PSARC/2006/053
- Add patches to allow doc base dir to be specified in configure
- cairo-java-05-docbasedir.diff: patch to use docbasedir in Makefile.am

* Mon Oct 2 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS

* Thur Sep 28 2006 - john.rice@sun.com
- Initial spec

