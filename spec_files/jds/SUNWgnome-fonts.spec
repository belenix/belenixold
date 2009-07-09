#
# spec file for package SUNWgnome-fonts
#
# includes module(s): ttf-baekmuk ttf-freefont
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
%include Solaris.inc
%define _prefix /usr

%use ttf_baekmuk = ttf-baekmuk.spec
%use ttf_freefont = ttf-freefont.spec

Name:                    SUNWgnome-fonts
Summary:                 GNOME Unicode and Korean TrueType fonts
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%define font_dir /usr/openwin/lib/X11/fonts/TrueType

%include default-depend.inc
Requires: SUNWgnome-base-libs

%prep
rm -rf %name-%version
mkdir %name-%version
%ttf_baekmuk.prep -d %name-%version
%ttf_freefont.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%ttf_baekmuk.build -d %name-%version
%ttf_freefont.build -d %name-%version

%install
%ttf_baekmuk.install -d %name-%version
%ttf_freefont.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{font_dir}

%changelog
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon May 03 2004 - laca@sun.com
- move to /usr/openwin
