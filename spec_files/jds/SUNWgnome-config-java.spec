#
# spec file for package SUNWgnome-config-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%include Solaris.inc

%define maj_min_ver 2.12
%define rev 5
%define  tarball_version %{maj_min_ver}.%{rev}
%define docbasedir %{_datadir}/lib/java/javadoc/java-gnome
%define jardir %{_datadir}/lib/java
%define srcjardir %{_datadir}/lib/java/src/java-gnome

Name:                    SUNWgnome-config-java
Summary:                 Part of Java-Gnome - Java to Gconf core bindings
Version:                 %{default_pkg_version}
Source:                  http://ftp.gnome.org/pub/gnome/sources/libgconf-java/%{maj_min_ver}/libgconf-java-%{tarball_version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
URL:                     http://java-gnome.sourceforge.net

%include default-depend.inc

Requires: SUNWgnome-base-libs-java
Requires: SUNWbash
Requires: SUNWgnome-config

BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-base-libs-java-devel
BuildRequires: SUNWgnome-config-devel

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires: %name

%description
libgconf-java base package required by Java-Gnome, Java bindings to core Gconf lib.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
%setup -q -n libgconf-java-%{tarball_version}

%build
export JAVA_HOME=/usr/java
export CFLAGS="-I/usr/java/include/solaris" 
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
rm $RPM_BUILD_ROOT%{_libdir}/libgconfjni.la
rm $RPM_BUILD_ROOT%{docbasedir}/libgconf-java-%{tarball_version}/examples/runExample.sh.in

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgconfjni.so
%{_libdir}/libgconfjni-%{maj_min_ver}.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr (0755, root, sys) %{jardir}
%{jardir}/gconf%{maj_min_ver}-%{tarball_version}.jar
%{jardir}/gconf%{maj_min_ver}.jar

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/gconf-java.pc
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr(0755, root, sys) %{_datadir}/lib/java
%dir %attr(0755, root, bin) %{_datadir}/lib/java/src
%dir %attr (0755, root, sys) %{srcjardir}
%{srcjardir}/gconf%{maj_min_ver}-src.jar

%dir %attr (0755, root, other) %{_datadir}/lib/java/javadoc
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/libgconf-java-%{tarball_version}/AUTHORS
%{docbasedir}/libgconf-java-%{tarball_version}/COPYING
%{docbasedir}/libgconf-java-%{tarball_version}/NEWS
%{docbasedir}/libgconf-java-%{tarball_version}/README
%{docbasedir}/libgconf-java-%{tarball_version}/examples/*
%{docbasedir}/libgconf-java-%{tarball_version}/api/*

%changelog
* Thur Apr 15 2008 - john.rice@sun.com
- Added Copyright file.

* Tue Oct 31 2006 - damien.carbery@sun.com
- Correct dir perms for javadoc dir, to match SUNWdtrc.

* Wed Oct 25 2006 - john.rice@sun.com
- Bumped libgconf-java tarball to 2.12.5 for the Java-Gnome 2.16 release
- All patches merged upstream, so removed following local patches
- Solaris/patches/gnome-config-java-01-config.diff
- Solaris/patches/gnome-config-java-02-jni.diff
- Solaris/patches/gnome-config-java-03-example.diff
- Solaris/patches/gnome-config-java-04-installpaths.diff
- Solaris/patches/gnome-config-java-05-doc.diff
- Solaris/patches/gnome-config-java-06-srcjar.diff
- Solaris/patches/gnome-config-java-07-docbasedir.diff

* Fri Oct 13 2006 - damien.carbery@sun.com
- Correct and sync dir perms with other Java Gnome packages. Change root:other 
  to root:sys.

* Thu Oct 12 2006 - john.rice@sun.com
- Modified srcjardir to conform to PSARC/2006/053
- Add patches to allow doc base dir to be specified in configure
- gnome-config-java-07-docbasedir.diff: change Makefile.am to use docbasedir, 
  instead of hardcoded $(datadir)/doc
- Enabled generation of src jar. Added configure option. 
- gnome-config-java-06-srcjar.diff: added BUILD_SRCJAR target to Makefile.am
- Modify patch to so specifying javadir as configure option works
- gnome-config-java-04-installpaths.diff: replace hard coded java dir with 
  specifiable javadir.

* Fri Oct 6 2006 - damien.carbery@sun.com
- Set dir perms of %{_datadir}/lib/java/javadoc to match
  SUNWgnome-base-libs-java.spec.

* Thur Oct 05 2006 - john.rice@sun.com
- Add tarball_version as this needs to be different from the default_pkg_version

* Wed Oct 04 2006 - damien.carbery@sun.com
- Correct dir perms.

* Tue Oct 03 2006 - john.rice@sun.com
- Added patch to allow api doc to be generated ("find -mindep 1" in 
  Makefile.am is not supported)

* Mon Oct 02 2006 - john.rice@sun.com
- Added patch for install dirs for jar location on Solaris, better to have as 
  a configure option for all OS
- Added aclocal macro flags

* Thu Sep 28 2006 - john.rice@sun.com
- Replaced mkdir with install -d

* Wed Sep 27 2006 - john.rice@sun.com
- Corrected SUNWgnome-libs-java version.
- Changed requires to use new Java-Gnome package names.
- Rename to SUNWgnome-config-java, rename patches and add devel package
- Moved location of docs under %{_datadir}/lib/java/javadoc/java-gnome

* Fri Aug 04 2006 - damien.carbery@sun.com
- Bump to 2.12.4.

* Wed Jun 28 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.

* Fri Jun 23 2006 - john.rice@sun.com
- Updates from review

* Thu Jun 22 2006 - john.rice@sun.com
- Make %files attributes explicit except examples & remove libtool .la archive
  file
- Patch0 fix config file so it's correctly generated
- Patch1 fix jni *.c files, incorrectly included header guards in c files 
  causing all fncs to be compiled out.
- Patch2 fix runExamples.sh.in to find java and javac correctly

* Mon Jun 19 2006 - john.rice@sun.com
- Initial spec
