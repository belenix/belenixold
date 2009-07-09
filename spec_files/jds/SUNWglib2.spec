#
# spec file for package SUNWglib2
#
# includes module(s): glib2
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
%use glib_64 = glib2.spec
%endif

%include base.inc

%use glib = glib2.spec

Name:                    SUNWglib2
Summary:                 GNOME core libraries
Version:                 %{glib.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWPython
Requires: SUNWperl584core
BuildRequires: SUNWlibm
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgtk-doc

%if %(/bin/test -e /usr/sfw/include/glib.h && echo 1 || echo 0)
BuildConflicts: SUNWGlib
%endif

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWglib2

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

%glib_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%glib.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PERL_PATH=/usr/perl5/bin/perl
export PERL=/usr/perl5/bin/perl

%ifarch amd64 sparcv9
%glib_64.build -d %name-%version/%_arch64
%endif

%glib.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%glib_64.install -d %name-%version/%_arch64
%endif

%glib.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/glib-{genmarshal,gettextize,mkenums}
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gobject-query
#FIXME: remove the empty dir
rmdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gio/modules
rmdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/gio
%endif

#FIXME: remove the empty dir
rmdir $RPM_BUILD_ROOT%{_libdir}/gio/modules
rmdir $RPM_BUILD_ROOT%{_libdir}/gio

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc -d %{base_arch} glib-%{glib.version}/README
%doc -d %{base_arch} glib-%{glib.version}/AUTHORS
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-1-2
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-0
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-2
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-4
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-6
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-8
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-10
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-12
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/ChangeLog.pre-2-14
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gio/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gmodule/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gobject/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/gthread/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/po/ChangeLog
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/COPYING
%doc(bzip2) -d %{base_arch} glib-%{glib.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gtester
%{_bindir}/gtester-report
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/charset.alias
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gtester
%{_bindir}/%{_arch64}/gtester-report
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/charset.alias
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/entities
%{_mandir}/entities/*
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glib*/include
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%{_libdir}/%{_arch64}/glib*/include
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/glib-2.0
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/glib-genmarshal.1
%{_mandir}/man1/glib-gettextize.1
%{_mandir}/man1/glib-mkenums.1
%{_mandir}/man1/gobject-query.1

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
