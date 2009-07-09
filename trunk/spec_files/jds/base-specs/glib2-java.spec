#
# spec file for package glib2-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%define maj_min_ver 0.4
%define rev 2
# Some filenames have a version number different from maj_min_ver.
%define file_ver 0.4

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

Name:                    glib2-java
License:		 LGPL	
Group:			 System/Library
Version:                 %{maj_min_ver}.%{rev}
Release:		 1
Distribution:		 Java Desktop System
Vendor:			 Sun Microsystems, Inc.
Summary:                 Part of Java-Gnome - Java to Glib core bindings
Source:                  http://ftp.gnome.org/pub/gnome/sources/glib-java/%{maj_min_ver}/glib-java-%{version}.tar.bz2
URL:                     http://java-gnome.sourceforge.net
BuildRoot:		 %{_tmppath}/%{name}-%{version}-build
Docdir:			 %{_defaultdocdir}/doc
Autoreqprov:		 on
# date:2008-09-04 owner:jmr type:bug bugzilla:6728675
Patch1:       glib-java-01-registerLogHandler.diff



Requires: glib2 >= 2.12.0
BuildRequires: glib2 >= 2.12.0

%package devel
Summary:                 %{summary} - development files
Requires:                %name

%description
glib-java base package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n glib-java-%{version}
%patch1 -p1

%build
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
%ifos solaris
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
   	    --with-docbasedir=%{docbasedir}	\
   	    --with-macrobasedir=%{macrobasedir}	\
   	    --with-jardir=%{jardir}	\
	    --with-srcjar			\
	    --with-srcjardir=%{srcjardir} \
            --without-gcj-compile               
%else
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
            --without-gcj-compile               
%endif
	    
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libexecdir}/libglibjni.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libglibjni-%{file_ver}.so
%{_libdir}/libglibjni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{jardir}
%{jardir}/glib%{file_ver}-%{version}.jar
%{jardir}/glib%{file_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/glib-java.pc
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{srcjardir}
%{srcjardir}/glib%{file_ver}-%{version}-src.jar

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/glib-java-%{version}/AUTHORS
%{docbasedir}/glib-java-%{version}/COPYING
%{docbasedir}/glib-java-%{version}/NEWS
%{docbasedir}/glib-java-%{version}/README
%{docbasedir}/glib-java-%{version}/INSTALL
%{docbasedir}/glib-java-%{version}/api/*

%dir %attr (0755, root, other) %{macrobasedir}/glib-java
%{macrobasedir}/glib-java/macros/ac_prog_jar.m4
%{macrobasedir}/glib-java/macros/am_path_gcj.m4
%{macrobasedir}/glib-java/macros/ac_prog_javac_works.m4
%{macrobasedir}/glib-java/macros/jg_check_nativecompile.m4
%{macrobasedir}/glib-java/macros/ac_prog_javac.m4
%{macrobasedir}/glib-java/macros/jg_common.m4
%{macrobasedir}/glib-java/macros/ac_prog_javadoc.m4
%{macrobasedir}/glib-java/macros/jg_lib.m4
%{macrobasedir}/glib-java/macros/am_path_docbook.m4
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/glib-java/jg_jnu.h
%{_includedir}/glib-java/glib_java.h

%changelog
* Tue Sep 10 2008 - john.rice@sun.com
- Added local patch for org_gnu_glib_GObject.c, this is a workaround and 
  will not be submitted upstream.
  Bugzilla #6728675 glib-java's JNI abuse causes jvm crashes when glib logs
- glib-java-01-registerLogHandler.diff: comment out logging in registerLogHandler()
  to workaround jvm crash

* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 0.4.2.

* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 0.4.1.

* Tue Oct 24 2006 - john.rice@sun.com
- Bumped glib-java tarball to 0.4.0 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/glib2-java-01-pointer.diff
- patches/glib2-java-02-uninstalled.diff  
- Solaris/patches/glib2-java-03-installpaths.diff
- patches/glib2-java-04-docbasedir.diff
- Solaris/patches/glib2-java-05-doc.diff
- patches/glib2-java-06-macrobasedir.diff

* Thur Oct 12 2006 - john.rice@sun.com
- Modified srcjardir to conform to PSARC/2006/053
- Modify installpaths patch to allow jardir to be specified in configure
- Add patch to allow api doc to be created
- glib2-java-05-doc.diff: work around unsupported "find -mindep" in generating
  api doc list
- Enabled creation of srcjar with configure switch
- Add patches to allow doc base dir to be specified in configure
- glib2-java-04-docbasedir.diff: modified patch to use docbasedir in Makefile.am
- Added macrobasedir option to configure
- glib2-java-06-macrobasedir.diff: added option to jg_common.m4 to allow
  macrobasedir to be specified

* Thur Oct 5 2006 - john.rice@sun.com
- Add patch to allow doc base dir to be specified in configure
- glib2-java-04-docbasedir.diff: add docbasedir param to jg_common.m4 which is
  used to create the aclocal.m4 macros by autoconf, which are used to create
  Makefile.in using automake.

* Mon Oct 2 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS

* Thur Sep 28 2006 - john.rice@sun.com
- Initial spec

