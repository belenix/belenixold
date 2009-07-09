#
# spec file for package SUNWgtk2
#
# includes module(s): gtk2
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _sysconfdir /etc/%{_arch64}
%use gtk_64 = gtk2.spec
%endif

%include base.inc

%use gtk = gtk2.spec

Name:                    SUNWgtk2
Summary:                 GTK+ - GIMP toolkit libraries
Version:                 %{gtk.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgtk2-root
Requires: SUNWglib2
Requires: SUNWcairo
Requires: SUNWpango
Requires: SUNWlibatk
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWTiff
Requires: SUNWlibmsr
Requires: SUNWmlib
Requires: SUNWxwplt
Requires: SUNWxwrtl
#Requires: SUNWgnutls
#Requires: SUNWlibgcrypt
#Requires: SUNWlibgpg-error
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWcairo-devel
BuildRequires: SUNWpango-devel
BuildRequires: SUNWlibatk-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWlibm
BuildRequires: SUNWmlibh
#BuildRequires: SUNWgnutls-devel
#BuildRequires: SUNWlibgcrypt-devel
#buildRequires: SUNWlibgpg-error-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWdesktop-cache

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgtk2
Requires: SFEcups-devel
Requires: SUNWlibmsr
Requires: SUNWpapi
Requires: SUNWpng-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n content
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%gtk_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gtk.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%gtk_64.build -d %name-%version/%_arch64
%endif

%gtk.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%gtk_64.install -d %name-%version/%_arch64
%endif

%gtk.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Move demo to demo directory.
#
install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
mv $RPM_BUILD_ROOT%{_bindir}/gtk-demo $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/immodules/im-[a-wyz]*.so

# on linux, these config files are created in %post
# that would be more complicated on Solaris, especially
# during jumpstart or live upgrade, so it's better to do
# it during the build
$RPM_BUILD_ROOT%{_bindir}/gtk-query-immodules-2.0 \
    $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/immodules/im-xim.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gtk.immodules

$RPM_BUILD_ROOT%{_bindir}/gdk-pixbuf-query-loaders \
    $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders

%ifarch amd64 sparcv9
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gtk-2.0/*/immodules/im-[a-wyz]*.so

export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}

mkdir  -p $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/gtk-2.0

$RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk-query-immodules-2.0 \
    $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gtk-2.0/*/immodules/im-xim.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/gtk-2.0/gtk.immodules

$RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gdk-pixbuf-query-loaders \
    $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gtk-2.0/*/loaders/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/gtk-2.0/gdk-pixbuf.loaders

rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gdk-pixbuf-csource
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk-update-icon-cache

mkdir -p $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtk-demo \
    $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/%{_arch64}
%endif

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x  %restart_fmri ]; then
    %restart_fmri pixbuf-loaders-installer
    %restart_fmri input-method-cache
fi

%post root
if [ -x $BASEDIR/usr/share/desktop-cache/restart_fmri ]; then
    $BASEDIR/usr/share/desktop-cache/restart_fmri pixbuf-loaders-installer
fi

%files
%doc -d %{base_arch} gtk+-%{gtk.version}/README
%doc -d %{base_arch} gtk+-%{gtk.version}/AUTHORS
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.gtk-async-file-chooser
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.gtk-printing
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-1-0
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-1-2
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-0
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-2
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-4
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-6
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-8
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/ChangeLog.pre-2-10
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/gdk-pixbuf/ChangeLog
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/po-properties/ChangeLog
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/po/ChangeLog
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/COPYING
%doc(bzip2) -d %{base_arch} gtk+-%{gtk.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gtk-builder-convert
%{_bindir}/gtk-query-immodules-2.0
%{_bindir}/gtk-update-icon-cache
%{_bindir}/gdk-pixbuf-query-loaders
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gtk*/*/engines/*.so
%{_libdir}/gtk*/*/loaders/*.so
%{_libdir}/gtk*/*/immodules/im-xim.so
%{_libdir}/gtk-2.0/modules/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gtk-builder-convert
%{_bindir}/%{_arch64}/gtk-query-immodules-2.0
%{_bindir}/%{_arch64}/gdk-pixbuf-query-loaders
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/gtk*/*/loaders/*.so
%{_libdir}/%{_arch64}/gtk*/*/engines/*.so
%{_libdir}/%{_arch64}/gtk*/*/immodules/im-xim.so
%{_libdir}/%{_arch64}/gtk*/modules/*.so
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/themes
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gtk-builder-convert.1
%{_mandir}/man1/gtk-query-immodules-2.0.1
%{_mandir}/man1/gdk-pixbuf-query-loaders.1
%{_mandir}/man1/gtk-update-icon-cache.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gtk*/include
%{_libdir}/gtk*/*/printbackends
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/gdk-pixbuf-csource
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_prefix}/demo
%dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds
%dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds/bin
%{_prefix}/demo/jds/bin/gtk-demo
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%{_libdir}/%{_arch64}/gtk*/include
%{_libdir}/%{_arch64}/gtk*/*/printbackends
%{_prefix}/demo/jds/bin/%{_arch64}/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/gtk-2.0/demo
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gdk-pixbuf-csource.1

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%ghost %{_sysconfdir}/gtk-2.0/gtk.immodules
%ghost %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
%{_sysconfdir}/gtk-2.0/im-multipress.conf
%ifarch amd64 sparcv9
%ghost %{_sysconfdir}/%{_arch64}/gtk-2.0/gtk.immodules
%ghost %{_sysconfdir}/%{_arch64}/gtk-2.0/gdk-pixbuf.loaders
%{_sysconfdir}/%{_arch64}/gtk-2.0/im-multipress.conf
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Apr 06 2009 - dave.lin@sun.com
- Fix BASEDIR issue in %post root.
- Check %restart_fmri existence to make postscript more robust.
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
