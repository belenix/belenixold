#
# spec file for package java-access-bridge
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         java-access-bridge
License:      GPL
Group:        System/Libraries/GNOME
Version:      1.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The Java Access Bridge for GNOME for Java Swing apps.
Source:       http://ftp.gnome.org/Public/gnome/sources/java-access-bridge/1.26/%{name}-%{version}.tar.bz2
#owner:padraig date:2005-06-05 type:bug bugster:6238185 bugzilla:136444
Patch1:       java-access-bridge-01-window-activate.diff
URL:          http://developer.gnome.org/projects/gap
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig
PreReq:       j2re-integration

%define libgnomeui_version 2.4.0.1
%define gtk2_version 2.2.4
%define atk_version 1.4.0
%define at_spi_version 1.1.8
%define at_spi_release 1

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: at-spi-devel >= %{at_spi_version}-%{at_spi_release}
Requires:      atk >= %{atk_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      at-spi >= %{at_spi_version}

# configure also lists:
# libbonobo-2.0 >= 1.1.0 libbonoboui-2.0 >= 1.1.0 libgnomeui-2.0 >= 1.1.0 libspi-1.0 >= 0.10.0

%description
The Java Access Bridge for GNOME connects the built-in accessibility support in
Java Swing apps to the GNOME Accessibility framework, specifically the Assistive
Technology Service Provider Interface (AT-SPI).

%prep
%setup -q 
%patch1 -p1

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

export JAVA_HOME=/usr/jdk/instances/jdk1.6.0
export PATH="$JAVA_HOME/bin:/usr/openwin/bin:$PATH"
CFLAGS="$RPM_OPT_FLAGS"                 \
%ifos linux
./configure --prefix=%{_prefix} \
            --with-java-home=/usr/java
%else
./configure --prefix=%{_prefix}
%endif

make

%install
make DESTDIR=$RPM_BUILD_ROOT install gnome_java_bridgedir=%{_datadir}/jar

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
if [ -L /usr/java/j2redefault/lib/accessibility.properties ]; then
	rm /usr/java/j2redefault/lib/accessibility.properties
fi
ln -s /usr/share/jar/accessibility.properties /usr/java/j2redefault/lib/accessibility.properties
cp /usr/share/jar/gnome-java-bridge.jar /usr/java/j2redefault/lib/ext/gnome-java-bridge.jar

%postun 
if [ -h /usr/java/j2redefault/lib/accessibility.properties ]; then
	rm /usr/java/j2redefault/lib/accessibility.properties
fi
if [ -e /usr/java/j2redefault/lib/ext/gnome-java-bridge.jar ]; then
	rm /usr/java/j2redefault/lib/ext/gnome-java-bridge.jar
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/jar
# %{_prefix}/j2se


%changelog
* Mon Mar 16 2009 - jeff.cai@sun.com
- Bump to 1.26.0
* Tue Jan 20 2009 - jeff.cai@sun.com
- Bump to 1.25.1
* Fri Jan 09 2009 - jeff.cai@sun.com
- Bump to 1.25.0
* Fri Dec 12 2008 - jeff.cai@sun.com
- Use jdk1.6.x by default since jdk 1.6 is default on
  Solaris.
* Tue Sep 09 2008 - jeff.cai@sun.com
- Bump to 1.24.0.
* Tue Jun 24 2008 - damien.carbery@sun.com
- Bump to 1.23.0.
* Tue Jan 03 2008 - damien.carbery@sun.com
- Bump to 1.22.1.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 1.22.0.
* Thu Dec 06 2007 - damien.carbery@sun.com
- Bump to 1.21.1.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 1.20.2.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.20.0.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 1.19.2.
* Tue Jul 03 2007 - jeff.cai@sun.com
- Bump to 1.19.1.
* Wed Mar 07 2007 - damien.carbery@sun.com
- Add /usr/openwin/bin to PATH so that xprop can be found.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 1.18.0.
* Thu Dec 14 2006 - damien.carbery@sun.com
- Set JAVA_HOME to use jdk1.5.0 to fix 6498805.
* Thu Oct 26 2006 - damien.carbery@sun.com
- Set JAVA_HOME so that javac is found.
* Fri Oct 21 2006 - damien.carbery@sun.com
- Remove references to jdk1.5.0_03 because the /usr/java symlink is used.
* Thu Jul 27 2006 - damien.carbery@sun.com
- Bump to 1.6.0. Remove upstream patch, 02-build-fix.
* Mon Jul 24 2006 - padraig.obriain@sun.com
- Add patch 02 to fix build issue with 1.5.0_07.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 1.5.0.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 1.4.7
* Mon Nov 14 2005 - william.walker@sun.com
- Bump version to 1.4.6
* Wed Jun 01 2005 - damien.carbery@sun.com
- Remove accessibility.properties symlink before (re)creating it. Bug 6278672.
* Thu May 19 2005 - dermot.mccluskey@sun.com
- /usr/java/j2redefault/lib/ext/gnome-java-bridge.jar needs to be a
  regular file, not a sym link (bug 6246567)
* Mon May 09 2005 - dermot.mccluskey@sun.com
- New jdk (1.5.0_03)
* Fri May 06 2005 - <bill.haneman@sun.com>
- Added patch to provide window:activate events for newly-created Swing windows
  Part of the fix for bug #6238185.
* Wed May 04 2005 - <bill.haneman@sun.com>
- Revved to 1.4.5, fixes problem with MANAGES_DESCENDANTS state when using
  JVMs >= 1.5.0.
* Mon Apr 18 2005 - <bill.haneman@sun.com>
- Revved to 1.4.4., fixes for bugzilla #172807, #192925, #171951, #300699.
- Removed redundant patch java-access-bridge-03-get-text.diff.
* Mon Feb 28 2005 - <dermot.mccluskey@sun.com>
- use -h to test for links in postun
* Mon Feb 28 2005 - <dermot.mccluskey@sun.com>
- remove '-j CPUS' from make command
* Fri Feb 25 2005 - <dermot.mccluskey@sun.com>
- create and delete links for accessibility.properties and gnome-java-bridge.jar (4768049)
* Wed Sep 29 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Add patch 04-get-deleted-chars for bugzilla #151579.
* Mon Sep 20 2004 - damien.carbery@sun.com
- Disable the Java 1.5.0 patch because it breaks build.
* Wed Sep 15 2004 - dermot.mccluskey@sun.com
- new install dir for JDK 1.5.0
* Wed Aug 20 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.
* Fri Aug 20 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Add patch 03-get-text for bugzilla #149602.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - dermot.mccluskey@sun.com
- removed patch 03
* Thu Jun 10 2004 - damien.carbery@sun.com
- Change 'javac' to 'javac -source 1.4' in configure.in as 1.5 breaks build.
* Mon May 31 2004 - Dermot McCluskey <dermot.mccluskey@sun.com>
- Padraig's patch for JDK1.5.0 compile error
* Sun May 30 2004 - Dermot McCluskey <dermot.mccluskey@sun.com>
- New JDK
* Fri May 15 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Bump version to 1.4.2
* Fri Apr 30 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Update Java version to 1.5.0
* Fri Apr 30 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Bump version to 1.4.1
* Thu Apr 15 2004 - Damien Carbery <damien.carbery@sun.com>
- Temporarily remove the %files line that is breaking the build until I figure
  out a correct solution. Add a missing '%patch1 -p1' line.
* Wed Apr 14 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- * Add patch for installation of accessibility.properties and 
  gnome-java-bridge.jar
* Tue Apr 13 2004 - Padraig O'Briain <padraigo.obriain@sun.com>
- Bump version to 1.4.0
* Tue Mar 16 2004 - Damien Carbery <damien.carbery@sun.com>
- Specify %{_datadir}/jar instead of %{_datadir}/lib in %install.
* Tue Mar 02 2004 - Damien Carbery <damien.carbery@sun.com>
- Correct files list.
* Mon Mar 01 2004 - Damien Carbery <damien.carbery@sun.com>
- Add JDK bin dir to PATH so 'jar' can be found.
- Correct '--with-java-home' path after installing 1.4.2_03 JDK.
* Fri Feb 27 2004 - Damien Carbery <damien.carbery@sun.com>
- Add '--with-java-home' to configure because JDK not being found.
* Thu Feb 26 2004 - Damien Carbery <damien.carbery@sun.com>
- Remove libtoolize stuff because using regular tarball and not CVS.
* Fri Feb 20 2004 - Damien Carbery <damien.carbery@sun.com>
- Initial release version for java-access-bridge.
