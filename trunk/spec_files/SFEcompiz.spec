#
# spec file for package SFEcompiz
#
# Owner: erwannc

# NOTE: You must set up the OpenGL symlinks before building SUNWcompiz:
#   #  /lib/svc/method/ogl-select start

%include Solaris.inc
Name:           SFEcompiz
Summary:        compiz
Version:        0.8.0
Source:		http://releases.compiz.org/core/compiz-%{version}.tar.gz
Source1:	http://dlc.sun.com/osol/jds/downloads/extras/compiz/compiz-desktop-integration-6.5.tar.bz2
Patch1:		compiz-01-solaris-port.diff
Patch3:		compiz-03-indiana-branding.diff
Patch4:		compiz-04-compvector.diff
Patch5:		compiz-05-corexml.diff
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: %{name}.copyright

%ifnarch sparc
# these packages are only available on x86
# =========================================

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires:	SUNWgtk2
Requires:	%name-root
Requires:       SUNWdesktop-cache
Requires: 	SUNWpng
Requires: 	SUNWdbus
Requires: 	SUNWgnome-desktop-prefs
Requires: 	SUNWgnome-panel
Requires: 	SUNWgnome-wm
Requires:       SUNWxwplr
Requires:       SUNWperl584core
Requires:       SUNWgnome-python-libs
Requires:       SUNWxorg-mesa
Requires:       SUNWPython
Requires:       SUNWlibwnck
#Requires:       SFEdbus-qt3
#Requires:       SFEkdelibs3
BuildRequires: 	SUNWgtk2-devel
BuildRequires: 	SUNWpng-devel
BuildRequires: 	SUNWdbus-devel
BuildRequires: 	SUNWgnome-desktop-prefs-devel
BuildRequires: 	SUNWgnome-panel-devel
BuildRequires: 	SUNWgnome-wm-devel
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWxorg-mesa
BuildRequires:  SUNWxwplr
buildRequires:  SUNWlibwnck-devel
#BuildRequires:  SFEdbus-qt3-devel
#BuildRequires:  SFEkdelibs3-devel

%package root
Summary:         %summary - platform dependent files, / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %summary - developer files
sUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
# testing is the OpenGL headers and libs are installed
# if this fails this mean the build machine is not
# properly configured
test -f /usr/X11/include/GL/glx.h || {
  echo "Missing OpenGL headers. Stopping."
  false
  }
test -f /usr/X11/lib/modules/extensions/libglx.so  || {
  echo "Missing OpenGL libraries. Stopping."
  false
  }
%setup -q -c -n %{name}
gtar fxvj %{SOURCE1}
cd compiz-%{version}
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib
PROTO_INC=$RPM_BUILD_DIR/%{name}/usr/X11/include
PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig

export PKG_CONFIG_PATH="$PROTO_PKG"
#export QTINC="/usr/include/qt3"

export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0 -I/usr/X11/include"
%if %option_with_gnu_iconv
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib"
export LIBS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -lgnuintl -lgnuiconv"
%else
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib"
%endif

cd compiz-%{version}

intltoolize --copy --force --automake

aclocal
autoheader
automake -a -c -f
autoconf
 
export CFLAGS="%optflags -I$PROTO_INC -I/usr/include/startup-notification-1.0 -I/usr/X11/include" 
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
	    --datadir=%{_datadir}	\
	    --enable-gnome 		\
	    --without-xcb		\
            --disable-kde               \
	    --with-default-plugins=core,dbus,move,place,png,regex,resize,svg,switcher,imgjpeg,resizeinfo,session,text,workarounds,decoration,animation,wall,fade

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd compiz-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT/usr/X11/lib/*.la
rm -rf $RPM_BUILD_ROOT%{_basedir}/etc

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp compiz.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp compiz.desktop $RPM_BUILD_ROOT%{_datadir}/applications

cp compiz-configure.in compiz-configure
cat compiz-configure.in | sed "s:@prefix_lib@:%{_libdir}:" | sed "s:@prefix_data@:%{_datadir}:" > compiz-configure

cp compiz-configure modify-xorg-conf xglxtest $RPM_BUILD_ROOT%{_libdir}/compiz
cp compiz-config.glade $RPM_BUILD_ROOT%{_datadir}/compiz

mv $RPM_BUILD_ROOT%{_bindir}/compiz $RPM_BUILD_ROOT%{_bindir}/compiz-bin
cp compiz $RPM_BUILD_ROOT%{_bindir}

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%post
%restart_fmri gconf-cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/compiz
%dir %attr (0755, root, bin) %{_libdir}/window-manager-settings
%{_libdir}/lib*so*
%{_libdir}/compiz/*
%{_libdir}/window-manager-settings/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/compiz
%dir %attr(0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/wm-properties
%dir %attr(0755, root, bin) %{_datadir}/gnome-control-center
%dir %attr(0755, root, bin) %{_datadir}/gnome-control-center/keybindings
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/compiz/*
%{_datadir}/gnome/wm-properties/*
%{_datadir}/gnome-control-center/keybindings/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%doc -d compiz-%{version} AUTHORS COPYING README
%doc(bzip2) -d compiz-%{version} COPYING.GPL COPYING.LGPL COPYING.MIT NEWS
%doc(bzip2) -d compiz-%{version} ChangeLog po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

# endif for "ifnarch sparc"
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Copy over updated spec from JDS repo.
- TODO: Enable Kde window decorator after building KDE4
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Apr 01 2009 - dave.lin@sun.com
- mandatorily apply patch 03-indiana-branding.diff for both Nv & OS
  in order to lessen the difference between Nv & OS(doo4284).
* Mon Mar 23 2009 - jeff.cai@sun.com
- Because /usr/lib/compiz/compiz-configure (SUNWcompiz) requires
  /usr/bin/i86/isapython2.4 which is found in SUNWPython, add the
  dependency on SUNWPython
* Wed Mar 11 2009 - matt.keenan@sun.com
- Bump compiz-desktop-integration tarball to 6.3 fix #7287
* Fri Feb 27 2009 - matt.keenan@sun.com
- Bump integration tarball to 6.2 fix #6967
* Wed Feb 11 2009 - matt.keenan@sun.com
- Remove compiz-by-default and compiz-by-default.desktop references, now
  delivered by gnome-session as they need to be compiz package independent
* Fri Feb 06 2009 - matt.keenan@sun.com
- Bump integration tarball to 6, for compiz-by-default bugs
* Tue Feb 03 2009 - matt.keenan@sun.com
- Bump integration tarball to 4, for compiz-by-default
- Add compiz-by-default to %files
* Mon Sep 22 2008 - erwann@sun.com
- Bumped integration tarball to add desktop file
* Wed Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Wed May 21 2008 - damien.carbery@sun.com
- Add 'Requires: SUNWxorg-mesa' after check-deps.pl run.
* Mon Apr 07 2008 - damien.carbery@sun.com
- Break the build if the openGL headers and libraries are not present on the
  machine.
* Thu Mar 27 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-desktop-prefs/-devel and SUNWgnome-panel/-devel
  to ensure GNOME support built. Add --enable-gnome to configure to be doubly
  sure.
* Wed Mar 26 2008 - dave.lin@sun.com
- change to not build this component on SPARC
* Tue Mar 11 2008 - erwann@sun.com
- removed missing X server pc and header file as they are available in
  nevada build 85
* Sun Mar 09 2008 - erwann@sun.com
- add standard gconf script and Perl and Pyhton deps for the config scripts
* Thu Feb 21 2008 - laca@sun.com
- do not install Xregion.h if it already exists (on Indiana)
* Wed Feb 20 2008 - damien.carbery@sun.com
- Remove NVDAgraphics dependency as it is not needed - ogl-select service sets
  up the required links. Add SUNWwxplr as it delivers ogl-select.
* Wed Feb 13 2008 - erwann@sun.com
- cleanup for spec-file-other integration
* Sun Nov 04 2007 - erwann@sun.com
- remove unneeded X bits
- lighter version of missing-stuff
- ship missing X header
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.2
- Don't create icons in gnome-integration (use fusion-icon)
* Tue Oct 16 2007 - laca@sun.com
- add FOX build support
* Fri Sep 21 2007 - Albert Lee <trisk@acm.jhu.edu>
- Add optional patch for "black windows" workaround
- Fix install in GNOME 2.19/2.20
* Thu Sep 06 2007 - Albert Lee <trisk@acm.jhu.edu>
- Updated to coexist with newer X consolidation packages
* Wed Mar 08 2007 - Doug Scott <dougs at truemail.co.th>
- Changed to build on un-modified system
* Tue Mar 06 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

