#
# spec file for package SUNWgnome-base-libs-java.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jmr
#
%include Solaris.inc

%use glibjava = glib2-java.spec
%use cairojava = cairo-java.spec
%use gtkjava = gtk2-java.spec
%use gnomejava = gnome-libs-java.spec
%use gladejava = glade-java.spec

%define docbasedir %{_datadir}/lib/java/javadoc/java-gnome
%define macrobasedir %{_datadir}/lib/java/javadoc/java-gnome
%define jardir %{_datadir}/lib/java
%define srcjardir %{_datadir}/lib/java/src/java-gnome

Name:                    SUNWgnome-base-libs-java
Summary:                 Part of Java-Gnome - Java core bindings
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
URL:                     http://java-gnome.sourceforge.net

%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWj5rt
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWj5dev

%package devel
Summary:                 %{summary} - development files
Requires:                %name
Requires:                SUNWbash

%description
base libs package required by Java-Gnome, Java bindings to core Gnome libs.
Java-Gnome is a set of Java bindings for the GNOME and GTK+ libraries that allow GNOME and GTK+ applications to be written in Java. 
This release series, collectively called java-gnome, consists of glib-java, cairo-java, libgtk-java, libglade-java, libgnome-java, and libgconf-java.

%prep
rm -rf %name-%version
mkdir %name-%version
%glibjava.prep -d %name-%version
%cairojava.prep -d %name-%version
%gtkjava.prep -d %name-%version
%gnomejava.prep -d %name-%version
%gladejava.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PKG_CONFIG_PATH=../glib-java-%{glibjava.version}:../cairo-java-%{cairojava.version}:../libgtk-java-%{gtkjava.version}:../libgnome-java-%{gnomejava.version}:../libglade-java-%{gladejava.version}:%{_pkg_config_path}

export JAVA_HOME=/usr/java
export CFLAGS="-I/usr/java/include/solaris" 
export ACLOCAL_FLAGS="-I %{_builddir}/%name-%version/glib-java-%{glibjava.version}/macros -I %{_builddir}/%name-%version/libgtk-java-%{gtkjava.version}/macros"

%glibjava.build -d %name-%version
%cairojava.build -d %name-%version
%gtkjava.build -d %name-%version
%gnomejava.build -d %name-%version
%gladejava.build -d %name-%version

%install
%glibjava.install -d %name-%version
%cairojava.install -d %name-%version
%gtkjava.install -d %name-%version
%gnomejava.install -d %name-%version
%gladejava.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libglibjni-%{glibjava.file_ver}.so
%{_libdir}/libglibjni.so
%{_libdir}/libcairojni-%{cairojava.maj_min_ver}.so
%{_libdir}/libcairojni.so
%{_libdir}/libgtkjni-%{gtkjava.file_ver}.so
%{_libdir}/libgtkjni.so
%{_libdir}/libgnomejni-%{gnomejava.maj_min_ver}.so
%{_libdir}/libgnomejni.so
%{_libdir}/libgladejni-%{gladejava.maj_min_ver}.so
%{_libdir}/libgladejni.so

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr (0755, root, sys) %{jardir}
%{jardir}/glib%{glibjava.file_ver}-%{glibjava.version}.jar
%{jardir}/glib%{glibjava.file_ver}.jar
%{jardir}/cairo%{cairojava.maj_min_ver}-%{cairojava.version}.jar
%{jardir}/cairo%{cairojava.maj_min_ver}.jar
%{jardir}/gtk%{gtkjava.file_ver}-%{gtkjava.version}.jar
%{jardir}/gtk%{gtkjava.file_ver}.jar
%{jardir}/gnome%{gnomejava.maj_min_ver}-%{gnomejava.version}.jar
%{jardir}/gnome%{gnomejava.maj_min_ver}.jar
%{jardir}/glade%{gladejava.maj_min_ver}-%{gladejava.version}.jar
%{jardir}/glade%{gladejava.maj_min_ver}.jar
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/java-gnome.3

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/glib-java.pc
%{_libdir}/pkgconfig/cairo-java.pc
%{_libdir}/pkgconfig/gtk2-java.pc
%{_libdir}/pkgconfig/gnome2-java.pc
%{_libdir}/pkgconfig/glade-java.pc

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/lib
%dir %attr(0755, root, sys) %{_datadir}/lib/java
%dir %attr(0755, root, bin) %{_datadir}/lib/java/src
%dir %attr (0755, root, sys) %{srcjardir}
%{srcjardir}/glib%{glibjava.file_ver}-src.jar
%{srcjardir}/cairo%{cairojava.maj_min_ver}-src.jar
%{srcjardir}/gtk%{gtkjava.file_ver}-src.jar
%{srcjardir}/gnome%{gnomejava.maj_min_ver}-src.jar
%{srcjardir}/glade%{gladejava.maj_min_ver}-src.jar

%dir %attr (0755, root, other) %{_datadir}/lib/java/javadoc
%dir %attr (0755, root, other) %{docbasedir}
%{docbasedir}/glib-java-%{glibjava.version}/AUTHORS
%{docbasedir}/glib-java-%{glibjava.version}/COPYING
%{docbasedir}/glib-java-%{glibjava.version}/NEWS
%{docbasedir}/glib-java-%{glibjava.version}/README
%{docbasedir}/glib-java-%{glibjava.version}/INSTALL
%{docbasedir}/glib-java-%{glibjava.version}/api/*
%{docbasedir}/cairo-java-%{cairojava.version}/AUTHORS
%{docbasedir}/cairo-java-%{cairojava.version}/COPYING
%{docbasedir}/cairo-java-%{cairojava.version}/NEWS
%{docbasedir}/cairo-java-%{cairojava.version}/README
%{docbasedir}/cairo-java-%{cairojava.version}/INSTALL
%{docbasedir}/cairo-java-%{cairojava.version}/api/*
%{docbasedir}/libgtk-java-%{gtkjava.version}/AUTHORS
%{docbasedir}/libgtk-java-%{gtkjava.version}/COPYING
%{docbasedir}/libgtk-java-%{gtkjava.version}/NEWS
%{docbasedir}/libgtk-java-%{gtkjava.version}/README
%{docbasedir}/libgtk-java-%{gtkjava.version}/INSTALL
%{docbasedir}/libgtk-java-%{gtkjava.version}/THANKS
%{docbasedir}/libgtk-java-%{gtkjava.version}/examples/*
%{docbasedir}/libgtk-java-%{gtkjava.version}/api/*
%{docbasedir}/libgnome-java-%{gnomejava.version}/AUTHORS
%{docbasedir}/libgnome-java-%{gnomejava.version}/COPYING
%{docbasedir}/libgnome-java-%{gnomejava.version}/NEWS
%{docbasedir}/libgnome-java-%{gnomejava.version}/README
%{docbasedir}/libgnome-java-%{gnomejava.version}/examples/*
%{docbasedir}/libgnome-java-%{gnomejava.version}/tutorial/*
%{docbasedir}/libgnome-java-%{gnomejava.version}/api/*

%{docbasedir}/libglade-java-%{gladejava.version}/AUTHORS
%{docbasedir}/libglade-java-%{gladejava.version}/COPYING
%{docbasedir}/libglade-java-%{gladejava.version}/NEWS
%{docbasedir}/libglade-java-%{gladejava.version}/README
%{docbasedir}/libglade-java-%{gladejava.version}/examples/*
%{docbasedir}/libglade-java-%{gladejava.version}/api/*

# Note: macrobasedir and docbasedir are the same so no need to specify them twice
# %dir %attr (0755, root, sys) %{macrobasedir}
%dir %attr (0755, root, sys) %{macrobasedir}/glib-java
%dir %attr (0755, root, sys) %{macrobasedir}/glib-java/macros
%{macrobasedir}/glib-java/macros/ac_prog_jar.m4
%{macrobasedir}/glib-java/macros/am_path_gcj.m4
%{macrobasedir}/glib-java/macros/ac_prog_javac_works.m4
%{macrobasedir}/glib-java/macros/jg_check_nativecompile.m4
%{macrobasedir}/glib-java/macros/ac_prog_javac.m4
%{macrobasedir}/glib-java/macros/jg_common.m4
%{macrobasedir}/glib-java/macros/ac_prog_javadoc.m4
%{macrobasedir}/glib-java/macros/jg_lib.m4
%{macrobasedir}/glib-java/macros/am_path_docbook.m4

%dir %attr (0755, root, sys) %{macrobasedir}/libgtk-java
%dir %attr (0755, root, sys) %{macrobasedir}/libgtk-java/macros
%{macrobasedir}/libgtk-java/macros/jg_gnome_java.m4
%{macrobasedir}/libgtk-java/macros/jg_gtk_java.m4

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/glib-java
%{_includedir}/glib-java/jg_jnu.h
%{_includedir}/glib-java/glib_java.h
%dir %attr (0755, root, bin) %{_includedir}/libgtk-java
%{_includedir}/libgtk-java/gtk_java.h

%changelog
* Thur Apr 15 2008 - john.rice@sun.com
- Added Copyright file.

* Wed Feb 28 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-vfs/-devel, an indirect requirement.

* Tue Feb 27 2006 - damien.carbery@sun.com
- Incorporate java-gnome.3 manpage.

* Tue Oct 31 2006 - damien.carbery@sun.com
- Correct dir perms for javadoc dir, to match SUNWdtrc.

* Fri Oct 20 2006 - damien.carbery@sun.com
- Add SUNWgnome-base-libs-java/-devel to Build/Requires list.

* Fri Oct 13 2006 - damien.carbery@sun.com
- Correct and sync dir perms with other Java Gnome packages. Change root:other 
  to root:sys.

* Thu Oct 12 2006 - john.rice@sun.com
- Added support for srcjar creation and doc api creation for 
  gnome, glade
- Modified srcjardir to conform to PSARC/2006/053
- Added support for srcjar creation and doc api creation for 
  cairo, gtk
- Add srcjar and api doc to dev files
- Use docbasedir and macrobasedir

* Mon Oct 02 2006 - john.rice@sun.com
- Remove INSTALLED_CLASSPATH and INSTALLED_MACRODIR, not required 

* Mon Oct 02 2006 - damien.carbery@sun.com
- Correct group for %{_datadir}/lib (root:sys). 
- Use global version for package version number.
- Add Build/Requires for Java packages (SUNWj5dev/SUNWj5rt).

* Mon Oct 02 2006 - john.rice@sun.com
- Added gnome-libs, required build dependency of libglade.

* Thur Sep 28 2006 - john.rice@sun.com
- Initial spec

