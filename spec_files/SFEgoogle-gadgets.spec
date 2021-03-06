#
# spec file for package SFEgoogle-gadgets
#
# includes module(s): google-gadgets
#
%include Solaris.inc

Name:                    SFEgoogle-gadgets
Summary:                 Google Gadgets - a platform for running desktop gadgets.
Version:                 0.11.0
License:                 ASL 2.0
Source:                  http://google-gadgets-for-linux.googlecode.com/files/google-gadgets-for-linux-%{version}.tar.bz2
URL:                     http://code.google.com/p/google-gadgets-for-linux/

# owner:alfred date:2009-01-12 type:bug
Patch1:                  google-gadgets-01-solaris-build.diff

# Enable Qt4 check on Solaris
Patch2:                  google-gadgets-02-configure.ac.diff

Patch4:                  google-gadgets-04-gecko_version.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SFEgccruntime
Requires: SUNWzlib
Requires: SUNWmlib
Requires: SUNWdbus-libs
Requires: SUNWcurl
Requires: SUNWlibsoup
Requires: SUNWlxml
Requires: SUNWgnome-media
Requires: SFEqt4
Requires: SUNWlibrsvg
Requires: SUNWcairo
Requires: SUNWgtk2
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SFExulrunner
Requires: SUNWltdl

BuildRequires: SUNWcurl-devel
BuildRequires: SUNWlibsoup-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SFEqt4-devel
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWflexlex
BuildRequires: SUNWcairo-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk2-devel
BuildRequires: SFExulrunner-devel
BuildRequires: SUNWlibtool

%package qt
Summary:                 Qt front-end for %{name}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%package gtk
Summary:                 Gtk front-end for %{name}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
Requires: %{name}-qt
Requires: %{name}-gtk
Requires: SUNWcurl-devel
Requires: SUNWlibsoup-devel
Requires: SUNWlxml-devel
Requires: SUNWdbus-devel
Requires: SUNWgnome-media-devel
Requires: SFEqt4-devel
Requires: SUNWlibrsvg-devel
Requires: SUNWgnome-libs-devel
Requires: SUNWgnome-vfs-devel
Requires: SUNWflexlex
Requires: SUNWcairo-devel
Requires: SUNWgnome-libs-devel
Requires: SUNWgnome-common-devel
Requires: SUNWgtk2-devel
Requires: SFExulrunner-devel
Requires: SUNWltdl
Requires: SUNWlibtool

%prep
%setup -q -n google-gadgets-for-linux-%{version}
%patch1 -p0
%patch2 -p1
%patch4 -p1

%build
export CXXFLAGS="-O3 -march=pentium3 -fno-omit-frame-pointer -D_REENTRANT -D__EXTENSIONS__ -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_POSIX_PTHREAD_SEMANTICS"
export LDFLAGS="-lc -lm  -L%{_libdir} -R%{_libdir} %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -lX11 -lXrender"
export CPPFLAGS="-I%{gnu_inc}"
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4

OPATH=${PATH}
export PATH="%{qt4_bin_path}:${OPATH}"
export MOC=%{qt4_bin_path}/moc

#./autotools/bootstrap.sh
#cp /usr/share/automake-1.10/mkinstalldirs libltdl/
#chmod a+x libltdl/mkinstalldirs
./configure --prefix=%{_prefix} \
            --disable-static \
            --with-libcurl=%{_prefix} \
            --with-browser-plugins-dir=%{_libdir}/firefox/plugins

export echo=echo
make

export PATH=$OPATH

%install
rm -rf $RPM_BUILD_ROOT
OPATH=${PATH}
export PATH="%{qt4_bin_path}:${OPATH}"
export echo=echo

make install DESTDIR=$RPM_BUILD_ROOT
# doesn't ship *.a and *.la
cd $RPM_BUILD_ROOT%{_libdir}
rm -f libggadget-*a
cd google-gadgets/modules
rm -f *a
export PATH=$OPATH

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/google-gadgets
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/ggl*.desktop
%dir %attr (0755, root, root)  %{_datadir}/mime
%dir %attr (0755, root, root)  %{_datadir}/mime/packages
%{_datadir}/mime/packages/00-google-gadgets.xml
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libggadget-xdg*.so*
%{_libdir}/libggadget-npapi*.so*
%{_libdir}/libggadget-dbus*.so*
%{_libdir}/libggadget-js*.so*
%{_libdir}/libggadget-1*.so*

%dir %attr (0755, root, bin) %{_libdir}/google-gadgets
%{_libdir}/google-gadgets/gtkmoz-browser-child
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets/modules
%{_libdir}/google-gadgets/modules/analytics*
%{_libdir}/google-gadgets/modules/curl*
%{_libdir}/google-gadgets/modules/dbus*
%{_libdir}/google-gadgets/modules/default*
%{_libdir}/google-gadgets/modules/google*
%{_libdir}/google-gadgets/modules/gst*
%{_libdir}/google-gadgets/modules/libxml2*
%{_libdir}/google-gadgets/modules/linux*
%{_libdir}/google-gadgets/modules/smjs*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%files qt
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ggl-qt
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libggadget-qt*
%{_libdir}/libggadget-web*
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets/modules
%{_libdir}/google-gadgets/modules/qt*.so
%{_libdir}/google-gadgets/modules/html*.so
%{_libdir}/google-gadgets/modules/web*.so
%{_libdir}/google-gadgets/modules/soup*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*qt.desktop

%files gtk
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ggl-gtk
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libggadget-gtk*
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets/modules
%{_libdir}/google-gadgets/modules/gtk*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*gtk.desktop

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets
%dir %attr (0755, root, bin) %{_libdir}/google-gadgets/include
%{_libdir}/google-gadgets/include/*

%changelog
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Remove unnecessary dependency, handle libtool weirdness.
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Add missing dependencies.
- Do not bootstrap to avoid building duplicate libltdl.
- Downgrade platform to pentium3.
* Sun Jul 26 2009 - moinakg<at>belenix(dot)org
- Bump version to get new features. Add patch to use latest XULRunner.
* Sat Jul 04 2009 - moinakg@belenix(dot)org
- Start using XULRunner for the smjs module.
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Pull in and modify from SFE repo.
