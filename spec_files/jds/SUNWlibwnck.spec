#
# spec file for package SUNWlibwnck
#
# includes module(s): libwnck
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc
%use lwnck = libwnck.spec

Name:                    SUNWlibwnck
Summary:                 GNOME window navigation utility library.
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWsolnm
BuildRequires: SUNWarc
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWgamin-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SUNWlibpopt
Requires: SUNWlibms
Requires: SUNWdbus
Requires: SUNWgamin

BuildRequires: SUNWtgnome-tsol-libs-devel
%if %option_without_fox
%ifarch i386
Requires: SUNWxorg-xkb
BuildRequires: SUNWxorg-xkb
%endif
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-libs-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%lwnck.prep -d %name-%version
chmod -R u+w %{_builddir}/%name-%version

%build
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/openwin/share/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/openwin/sfw/lib -R/usr/openwin/sfw/lib -L/usr/openwin/lib -R/usr/openwin/lib"

%lwnck.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%lwnck.install -d %name-%version

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT/usr/var
rm -rf $RPM_BUILD_ROOT/var

%if %build_l10n
%else
# REMOVE l10n FILES
#FIXME: really need to fix this stuff up
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/[a-c]*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/[e-z]*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wnckprop
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
