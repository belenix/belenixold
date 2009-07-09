#
# spec file for package SUNWlibcanberra
#
# includes module(s): libcanberra
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
%include Solaris.inc

Name:                    SUNWlibcanberra
Summary:                 Event Sound API Using XDG Sound Theming Specification
Version:                 0.12
License:                 LGPL v2.1
URL:                     http://0pointer.de/blog/projects/sixfold-announcement.html
Source:                  http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.gz
Source1:                 %{name}-manpages-0.1.tar.gz
SUNW_Copyright:          %{name}.copyright
# This patch is needed until autoconf is updated to 2.63 and libtool to 2.2.
#owner:yippi date:2008-09-02 type:branding 
Patch1:                  libcanberra-01-solaris.diff
#owner:jerrytan date:2009-04-16 type:bug bugid:21344 doo:8252
Patch2:                  libcanberra-02-close-file.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWlibcanberra-root
Requires: SUNWxdg-sound-theme
Requires: SUNWgnome-media
Requires: SUNWogg-vorbis
Requires: SUNWltdl
Requires: SUNWdesktop-cache
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWogg-vorbis-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libcanberra-%version
%patch1 -p1 
%patch2 -p1 

cd %{_builddir}/libcanberra-%version
gzcat %SOURCE1 | tar xf -

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libcanberra-%{version}/*.la

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/libcanberra-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-2.0
%{_libdir}/libcanberra-%{version}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc README doc/README
%doc(bzip2) LGPL
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%{_datadir}/gtk-doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/libcanberra.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/libcanberra
%{_datadir}/doc/libcanberra/*
%dir %attr (0755, root, other) %{_datadir}/gnome

%changelog
* Mon Apr 13 2009 - brian.cameron@sun.com
- Bump to 0.12.
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Feb 10 2009 - halton.huo@sun.com
- Add Requires: SUNWltdl to fix issue #5 for CR6753371
* Wed Jan 21 2009 - brian.cameron@sun.com
- Bump to 0.11.  Remove upstream patches.
* Thu Jan 15 2008 - brian.cameron@sun.com
- Add a patch to fix the OSS backend so it works.
* Thu Oct 30 2008 - brian.cameron@sun.com
- Add patch libcanberra-02-gstreamer.diff to fix bug where libcanberra core
  dumps when it tries to play a second sound.  Fixes bugster bug #6761078.
* Mon Oct 13 2008 - brian.cameron@sun.com
- Bump to 0.10.  Add root package and %post and %preun sections for the
  new GConf schemas.
* Tue Sep 09 2008 - brian.cameron@sun.com
- Bump to 0.9.  Remove upstream patches libcanberra-02-gstreamer.diff and
  libcanberra-03-fix-gst-play.diff.
* Fri Aug 29 2008 - brian.cameron@sun.com
- Add patch libcanberra-03-fix-gst-play so it actually plays the sound.
* Fri Aug 29 2008 - brian.cameron@sun.com
- Add patch libcanberra-02-gstreamer.diff to add audioconvert and audioresample
  plugins to the output pipeline, so it works on Solaris.
* Thu Aug 28 2008 - brian.cameron@sun.com
- Bump to 0.8.  Now has its own GStreamer support, so removed our patch.
* Wed Aug 20 2008 - brian.cameron@sun.com
- Add Requires/BuildRequires and patch libcanberra-02-gstreamer.diff to support
  a GStreamer backend.
* Thu Aug 14 2008 - brian.cameron@sun.com
- Created with version 0.6.

