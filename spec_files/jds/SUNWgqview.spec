#
#
# spec file for package SUNWgqview
#
# includes module(s): gqview
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc
%use gqview = gqview.spec
Name:                    SUNWgqview
Summary:                 GQview - Image browser
URL:                     http://gqview.sourceforge.net/
Version:                 %{gqview.version}
Source:                  http://prdownloads.sourceforge.net/gqview/gqview-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SUNWgqview.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgnome-base-libs-devel

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
%gqview.prep -d %name-%version

%build
export CFLAGS="%optflags -DEDITOR_GIMP"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl -lsocket"
%endif
export LDFLAGS="-lX11 -lsocket"
%gqview.build -d %name-%version

%install
%gqview.install -d %name-%version
if [ -d $RPM_BUILD_ROOT/%{_libdir}/locale ]; then
  mv $RPM_BUILD_ROOT/%{_libdir}/locale $RPM_BUILD_ROOT/%{_datadir}/
  rm -r  $RPM_BUILD_ROOT/%{_libdir}
fi
%if %{build_l10n}
mv $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN.GB2312 $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN 
%else
rm -r  $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d gqview-%{gqview.version} README AUTHORS
%doc(bzip2) -d gqview-%{gqview.version} COPYING ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/doc/gqview-%{gqview.version}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Mon Sep 16 2008 - chris.wang@sun.com
- Revised copyright file
* Wed Aug 21 2008 - chris.wang@sun.com
- Move #6734879's fix to Solaris spec from base spec
* Wed Jul 23 2008 - damien.carbery@sun.com
- Check that installed dirs exist before removing or moving them.

* Wed Jul 23 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-base-libs/-devel because gtk+ is required. Also
  add BuildRequires SUNWgnome-common-devel because pkg-config is used by
  configure.

* Tue Jul  7 2008 - chris.wang@sun.com 
- Initial build.

