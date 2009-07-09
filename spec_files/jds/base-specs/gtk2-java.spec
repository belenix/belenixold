#
# spec file for package gtk2-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%define maj_min_ver 2.10
%define rev 2
# Some filenames have a version number different from maj_min_ver.
%define file_ver 2.10

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

Name:                    gtk2-java
License:		 LGPL	
Group:			 System/Library
Version:                 %{maj_min_ver}.%{rev}
Release:		 1
Distribution:		 Java Desktop System
Vendor:			 Sun Microsystems, Inc.
Summary:                 Part of Java-Gnome - Java to Gtk core bindings
Source:                  http://ftp.gnome.org/pub/gnome/sources/libgtk-java/%{maj_min_ver}/libgtk-java-%{version}.tar.bz2
URL:                     http://java-gnome.sourceforge.net
BuildRoot:		 %{_tmppath}/%{name}-%{version}-build
Docdir:			 %{_defaultdocdir}/doc
Autoreqprov:		 on

Requires: glib2-java >= 0.4.0
Requires: cairo-java >= 1.0.6
Requires: gtk2 >= 2.0
BuildRequires: glib2-java-devel >= 0.3.2
BuildRequires: cairo-java-devel >= 1.0.5

%package devel
Summary:                 %{summary} - development files
Requires:                %name

%description
gtk2-java base package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n libgtk-java-%{version}

%build
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
   	    --with-docbasedir=%{docbasedir}	\
   	    --with-macrobasedir=%{macrobasedir}	\
   	    --with-jardir=%{jardir}	        \
	    --with-srcjar			\
	    --with-srcjardir=%{srcjardir}       \
            --without-gcj-compile              
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgtkjni.la
rm $RPM_BUILD_ROOT%{docbasedir}/libgtk-java-%{version}/examples/runExample.sh.in

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgtkjni-%{file_ver}.so
%{_libdir}/libgtkjni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{jardir}
%{jardir}/gtk%{file_ver}-%{version}.jar
%{jardir}/gtk%{file_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/gtk2-java.pc
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{srcjardir}
%{srcjardir}/gtk%{maj_min_ver}-src.jar

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/libgtk-java-%{version}/AUTHORS
%{docbasedir}/libgtk-java-%{version}/COPYING
%{docbasedir}/libgtk-java-%{version}/NEWS
%{docbasedir}/libgtk-java-%{version}/README
%{docbasedir}/libgtk-java-%{version}/INSTALL
%{docbasedir}/libgtk-java-%{version}/THANKS
%{docbasedir}/libgtk-java-%{version}/examples/*
%{docbasedir}/libgtk-java-%{version}/api/*

%dir %attr (0755, root, other) %{_datadir}/libgtk-java
%{macrobasedir}/libgtk-java/macros/jg_gnome_java.m4
%{macrobasedir}/libgtk-java/macros/jg_gtk_java.m4
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libgtk-java/gtk_java.h

%changelog
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.10.2.

* Tue Nov 28 2006 - damien.carbery@sun.com
- Remove upstream patch, 01-runExample.

* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.10.1.

* Fri Oct 27 2006 - john.rice@sun.com
- Added local patch for runExample.sh.in also submitted upstream
  Bugzilla #365847 java-gnome: Problem with generated runExample.sh for libgtk-java 
- gtk2-java-01-runExample.diff: Fix for runExample.sh.in so jar paths and libdir
  are correctly set

* Wed Oct 25 2006 - john.rice@sun.com
- Bumped libgtk-java tarball to 2.10.0 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/gtk2-java-01-example.diff
- patches/gtk2-java-02-uninstalled.diff
- Solaris/patches/gtk2-java-03-installpaths.diff
- patches/gtk2-java-04-doc.diff
- patches/gtk2-java-05-srcjar.diff
- patches/gtk2-java-06-docbasedir.diff
- patches/gtk2-java-07-macrobasedir.diff

* Thur Oct 12 2006 - john.rice@sun.com
- Modify installpaths patch to allow jardir to be specified in configure
- Add patch to allow api doc to be created
- gtk2-java-04-doc.diff: work around unsupported "find -mindep" in generating
  api doc list
- Enabled creation of srcjar with configure switch
- gtk2-java-05-srcjar.diff: added BUILD_SRCJAR target to Makefile.am
- Modified srcjardir to conform to PSARC/2006/053
- Add patches to allow doc base dir to be specified in configure
- gtk2-java-06-docbasedir.diff: patch to use docbasedir in Makefile.am
- Added macrobasedir option to configure 
- Add patch to allow macrobasedir to be used
- gtk2-java-07-macrobasedir.diff: used macrobasedir in gtk-java.pc creation
  and Makefile.am

* Mon Oct 2 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS

* Thur Sep 28 2006 - john.rice@sun.com
- Initial spec

