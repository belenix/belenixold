#
# spec file for package glade-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%define maj_min_ver 2.12
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

Name:                    glade-java
License:		 LGPL	
Group:			 System/Library
Version:                 %{maj_min_ver}.%{rev}
Release:		 1
Distribution:		 Java Desktop System
Vendor:			 Sun Microsystems, Inc.
Summary:                 Part of Java-Gnome - Java to Glade core bindings
Source:                  http://ftp.gnome.org/pub/gnome/sources/libglade-java/%{maj_min_ver}/libglade-java-%{version}.tar.bz2
URL:                     http://java-gnome.sourceforge.net
BuildRoot:		 %{_tmppath}/%{name}-%{version}-build
Docdir:			 %{_defaultdocdir}/doc
Autoreqprov:		 on
# date:2006-11-03 owner:migi type:bug bugzilla:370042
Patch1:       glade-java-01-runExample.diff

Requires: glib2 >= 2.0
BuildRequires: glib2 >= 2.0

Requires: glib2-java >= 0.4.0
Requires: cairo-java >= 1.0.6
Requires: gkt2-java >= 2.10.0
Requires: glade >= 2.12
BuildRequires: glib2-java-devel >= 0.4.0
BuildRequires: cairo-java-devel >= 1.0.6
BuildRequires: gkt2-java-devel >= 2.10.0

%package devel
Summary:                 %{summary} - development files
Requires:                %name

%description
libglade-java base package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n libglade-java-%{version}
%patch1 -p1

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
rm $RPM_BUILD_ROOT%{_libdir}/libgladejni.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgladejni-%{maj_min_ver}.so
%{_libdir}/libgladejni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{jardir}
%{jardir}/glade%{maj_min_ver}-%{version}.jar
%{jardir}/glade%{maj_min_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/glade-java.pc
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{srcjardir}
%{srcjardir}/glade%{maj_min_ver}-src.jar

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/libglade-java-%{version}/AUTHORS
%{docbasedir}/libglade-java-%{version}/COPYING
%{docbasedir}/libglade-java-%{version}/NEWS
%{docbasedir}/libglade-java-%{version}/README
%{docbasedir}/libglade-java-%{version}/examples/*
%{docbasedir}/libglade-java-%{version}/api/*

%changelog
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.12.8.

* Fri Nov  3 2006 - michal.pryc@sun.com
- Added local patch for runExample.sh.in also submitted upstream
  Bugzilla #370042 java-gnome: Problem with generated runExample.sh for
  libglade-java
- glade-java-01-runExample.diff: Fix for runExample.sh.in so jar paths and
  libdir are correctly set
     
* Wed Oct 25 2006 - john.rice@sun.com
- Bumped libglade-java tarball to 2.12.7 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/glade-java-01-config.diff
- Solaris/patches/glade-java-02-installpaths.diff
- Solaris/patches/glade-java-03-doc.diff
- patches/glade-java-04-srcjar.diff
- patches/glade-java-05-docbasedir.diff

* Thur Oct 12 2006 - john.rice@sun.com
- Modify installpaths patch to allow jardir to be specified in configure
- Add patch to allow api doc to be created
- glade-java-03-doc.diff: work around unsupported "find -mindep" in generating
  api doc list
- Enabled creation of srcjar with configure switch
- glade-java-04-srcjar.diff: added BUILD_SRCJAR target to Makefile.am
- Add patches to allow doc base dir to be specified in configure
- glade-java-05-docbasedir.diff: patch to use docbasedir in Makefile.am

* Mon Oct 2 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS
* Thur Sep 28 2006 - john.rice@sun.com
- Initial spec

