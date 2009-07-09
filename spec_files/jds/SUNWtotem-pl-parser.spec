#
# spec file for package SUNWtotem-pl-parser
#
# includes module(s): totem-pl-parser
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#
%include Solaris.inc


%define makeinstall make install DESTDIR=$RPM_BUILD_ROOT
%use totemparser = totem-pl-parser.spec

Name:                    SUNWtotem-pl-parser
Summary:                 a library to parse playlist
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWhea
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWevolution-data-server-devel
Requires: SUNWevolution-data-server
Requires: SUNWcsl
Requires: SUNWlxml
Requires: SUNWgnome-base-libs


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

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
%totemparser.prep -d %name-%version

%build
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags" 
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_datadir}/pkgconfig
%totemparser.build -d %name-%version


%install
rm -rf $RPM_BUILD_ROOT
%totemparser.install -d %name-%version

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc totem-pl-parser-%{totemparser.version}/AUTHORS
%doc totem-pl-parser-%{totemparser.version}/README
%doc(bzip2) totem-pl-parser-%{totemparser.version}/COPYING.LIB
%doc(bzip2) totem-pl-parser-%{totemparser.version}/NEWS
%doc(bzip2) totem-pl-parser-%{totemparser.version}/ChangeLog
%doc(bzip2) totem-pl-parser-%{totemparser.version}/po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif



%changelog
* Thu Mar 26 2009 -jerry.tan@sun.com
- seperate totem-pl-parser from SUNWgnome-media-player

