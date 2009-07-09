#
# spec file for package gnome-libs-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%define maj_min_ver 2.12
%define rev 7

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

Name:                    gnome-libs-java
License:		 LGPL	
Group:			 System/Library
Version:                 %{maj_min_ver}.%{rev}
Release:		 1
Distribution:		 Java Desktop System
Vendor:			 Sun Microsystems, Inc.
Summary:                 Part of Java-Gnome - Java to Gnome core bindings
Source:                  http://www.gtlib.gatech.edu/pub/gnome/sources/libgnome-java/%{maj_min_ver}/libgnome-java-%{version}.tar.bz2
URL:                     http://java-gnome.sourceforge.net
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Docdir:			 %{_defaultdocdir}/doc
Autoreqprov:		 on

#owner:jmr date:2006-10-27 type:bug bugzilla:365850
Patch1:       gnome-java-01-runExample.diff

Requires: gtk2-java >= 2.10.0
Requires: glib2-java >= 0.4.0
Requires: cairo-java >= 1.0.6
Requires: gnome >= 2.0
BuildRequires: gtk2-java-devel >= 2.10.0
BuildRequires: glib2-java-devel >= 0.4.0
BuildRequires: cairo-java-devel >= 1.0.6

%package devel
Summary:                 %{summary} - development files
Requires:                %name

%description
gnome-java base package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n libgnome-java-%{version}
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
rm $RPM_BUILD_ROOT%{_libdir}/libgnomejni.la
rm $RPM_BUILD_ROOT%{docbasedir}/libgnome-java-%{version}/examples/runExample.sh.in

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgnomejni-%{maj_min_ver}.so
%{_libdir}/libgnomejni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{jardir}
%{jardir}/libgnome%{maj_min_ver}-%{version}.jar
%{jardir}/libgnome%{maj_min_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/gnome2-java.pc
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{srcjardir}
%{srcjardir}/gnome%{maj_min_ver}-src.jar

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/libgnome-java-%{version}/AUTHORS
%{docbasedir}/libgnome-java-%{version}/COPYING
%{docbasedir}/libgnome-java-%{version}/NEWS
%{docbasedir}/libgnome-java-%{version}/README
%{docbasedir}/libgnome-java-%{version}/examples/*
%{docbasedir}/libgnome-java-%{version}/tutorial/*
%{docbasedir}/libgnome-java-%{version}/api/*

%changelog
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.12.7.

* Fri Oct 27 2006 - john.rice@sun.com
- Added local patch for runExample.sh.in also submitted upstream
  Bugzilla #365850 java-gnome: Problem with generated runExample.sh for
  libgnome-java
- gnome-java-01-runExample.diff: Fix for runExample.sh.in so jar paths and
  libdir are correctly set

* Wed Oct 25 2006 - john.rice@sun.com
- Bumped libgnome-java tarball to 2.12.6 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/gnome-libs-java-01-example.diff
- patches/gnome-libs-java-02-uninstalled.diff
- Solaris/patches/gnome-libs-java-03-installpaths.diff
- Solaris/patches/gnome-libs-java-04-doc.diff
- patches/gnome-libs-java-05-srcjar.diff
- patches/gnome-libs-java-06-docbasedir.diff

* Thur Oct 12 2006 - john.rice@sun.com
- Modify installpaths patch to allow jardir to be specified in configure
- Add patch to allow api doc to be created
- gnome-java-04-doc.diff: work around unsupported "find -mindep" in generating
  api doc list
- Enabled creation of srcjar with configure switch
- gnome-java-05-srcjar.diff: added BUILD_SRCJAR target to Makefile.am
- Add patches to allow doc base dir to be specified in configure
- gnome-java-06-docbasedir.diff: patch to use docbasedir in Makefile.am

* Tues Oct 3 2006 - john.rice@sun.com
- Corrected patch name from gnome-java-03-installpaths.diff to
  gnome-libs-java-03-installpaths.diff

* Mon Oct 2 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS
- Initial spec

