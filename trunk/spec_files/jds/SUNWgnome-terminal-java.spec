#
# spec file for package SUNWgnome-terminal-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%include Solaris.inc

%define maj_min_ver 0.12
%define rev 2
%define tarball_version %{maj_min_ver}.%{rev}
%define docbasedir %{_datadir}/lib/java/javadoc/java-gnome
%define jardir %{_datadir}/lib/java
%define srcjardir %{_datadir}/lib/java/src/java-gnome

Name:                    SUNWgnome-terminal-java
Summary:                 Part of Java-Gnome - Java to Gnome Terminal bindings
Version:                 %{default_pkg_version}
Source:                  http://ftp.gnome.org/pub/gnome/sources/libvte-java/%{maj_min_ver}/libvte-java-%{tarball_version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
URL:                     http://java-gnome.sourceforge.net

%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWgnome-base-libs-java
Requires: SUNWbash
Requires: SUNWgnome-terminal

BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-base-libs-java-devel
BuildRequires: SUNWgnome-terminal-devel

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires: %name

%description
libvte-java Gnome Terminal bindings required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libvte-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n libvte-java-%{tarball_version}

%build
export JAVA_HOME=/usr/java
export CFLAGS="-I/usr/java/include -I/usr/java/include/solaris" 
export ACLOCAL_FLAGS="-I /usr/share/lib/java/javadoc/java-gnome/glib-java/macros -I /usr/share/lib/java/javadoc/java-gnome/libgtk-java/macros"
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
   	    --with-docbasedir=%{docbasedir}	\
   	    --with-jardir=%{jardir}	\
	    --with-srcjar			\
	    --with-srcjardir=%{srcjardir} \
            --without-gcj-compile               

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libvtejni.la
rm $RPM_BUILD_ROOT%{docbasedir}/libvte-java-%{tarball_version}/examples/runExample.sh.in

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libvtejni-%{maj_min_ver}.so
%{_libdir}/libvtejni.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr (0755, root, sys) %{jardir}
%{jardir}/vte%{maj_min_ver}-%{tarball_version}.jar
%{jardir}/vte%{maj_min_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/vte-java.pc
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr(0755, root, sys) %{_datadir}/lib/java
%dir %attr(0755, root, bin) %{_datadir}/lib/java/src
%dir %attr (0755, root, sys) %{srcjardir}
%{srcjardir}/vte%{maj_min_ver}-src.jar

%dir %attr (0755, root, other) %{_datadir}/lib/java/javadoc
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/libvte-java-%{tarball_version}/AUTHORS
%{docbasedir}/libvte-java-%{tarball_version}/COPYING
%{docbasedir}/libvte-java-%{tarball_version}/NEWS
%{docbasedir}/libvte-java-%{tarball_version}/README
%{docbasedir}/libvte-java-%{tarball_version}/examples/*
%{docbasedir}/libvte-java-%{tarball_version}/api/*

%changelog
* Thur Apr 15 2008 - john.rice@sun.com
- Added Copyright file.

* Tue Oct 31 2006 - damien.carbery@sun.com
- Correct dir perms for javadoc dir, to match SUNWdtrc.

* Wed Oct 25 2006 - john.rice@sun.com
- Bumped libvte-java tarball to 0.12.2 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/gnome-terminal-java-01-installpaths.diff
- Solaris/patches/gnome-terminal-java-02-doc.diff
- Solaris/patches/gnome-terminal-java-03-srcjar.diff
- Solaris/patches/gnome-terminal-java-04-docclasspath.diff
- Solaris/patches/gnome-terminal-java-05-jardir.diff
- Solaris/patches/gnome-terminal-java-06-docbasedir.diff

* Fri Oct 13 2006 - damien.carbery@sun.com
- Correct and sync dir perms with other Java Gnome packages. Change root:other 
  to root:sys.

* Thu Oct 12 2006 - john.rice@sun.com
- Modified srcjardir to conform to PSARC/2006/053
- gnome-terminal-java-03-srcjar.diff: updated patch with all-local target
- rename patch gnome-terminal-java-05-javadir.diff to 
  gnome-terminal-java-05-jardir.diff

* Fri Oct 06 2006 - damien.carbery@sun.com
- Set dir perms of %{_datadir}/lib/java/javadoc to match 
  SUNWgnome-base-libs-java.spec.

* Thu Oct 05 2006 - john.rice@sun.com
- gnome-terminal-java-01-installpaths.diff: modified patch so generated .pc file
  now refers to $(jardir) instead of hard coding classpath
- Add patches to allow doc base dir to be specified in configure
- glib2-java-04-docbasedir.diff: add docbasedir param to jg_common.m4 which is
  used to create the aclocal.m4 macros by autoconf, which are used to create
  Makefile.in using automake.
- gnome-terminal-java-06-docbasedir.diff: change Makefile.am to use docbasedir, 
  instead of hardcoded $(datadir)/doc
- Add patch to so specifying javadir as configure option works.
- gnome-terminal-java-05-jardir.diff: replace hard coded java dir with 
  specifiable jardir.
- Add patch to remove javadoc compiler warnings.
- gnome-terminal-java-04-docclasspath.diff: add classpath to javadoc options 
  in Makefile.am.
- Add tarball_version as this needs to be different from the default_pkg_version

* Wed Oct 04 2006 - john.rice@sun.com
- Enabled generation of src jar. Added configure option. 
- gnome-terminal-java-03-srcjar.diff: added BUILD_SRCJAR target to Makefile.am

* Wed Oct 04 2006 - damien.carbery@sun.com
- Correct dir perms.

* Tue Oct 03 2006 - john.rice@sun.com
- Added patch to allow examples and api doc to be generated ("find -mindep 1" 
  in Makefile.am is not supported)

* Tue Oct 03 2006 - john.rice@sun.com
- Added patch to allow examples and api doc to be generated ("find -mindep 1" 
  in Makefile.am is not supported)

* Mon Oct 02 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS
- Added aclocal macro flags

* Thu Sep 28 2006 - john.rice@sun.com
- Replaced mkdir with install -d

* Wed Sep 27 2006 - john.rice@sun.com
- Changed requires to use new Java-Gnome package names.
- Moved location of docs under %{_datadir}/lib/java/javadoc/java-gnome

* Mon Sep 25 2006 - john.rice@sun.com
- Rename to SUNWgnome-terminal-java and add devel package.

* Wed Aug 16 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWlibgtk-java as required by configure.

* Wed Aug 09 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-terminal/-devel for vte.

* Fri Aug 04 2006 - damien.carbery@sun.com
- Initial spec
