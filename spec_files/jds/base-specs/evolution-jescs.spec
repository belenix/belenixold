#
# spec file for package evolution-jescs
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
Name:         evolution-jescs
License:      GPL v2
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Evolution connector for Sun Java Enterprise System Calendar Server
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define evolution_version 2.2
%define libgnomeui_version 2.10.0
%define libglade_version 2.5.0
%define libsoup_version 2.2.3
%define GConf_version 2.10.0
%define openldap2_version 2.2.6
%define gtk_doc_version 1.3

Requires:       evolution >= %{evolution_version}
Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       libglade >= %{libglade_version}
Requires:       libsoup >= %{libsoup_version}
Requires:       GConf >= %{GConf_version}
Requires:       openldap2-client >= %{openldap2_version}

BuildRequires:  evolution-devel >= %{evolution_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libglade-devel >= %{libglade_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  openldap2-devel >= %{openldap2_version}
BuildRequires:  gtk-doc >= %{gtk_doc_version}

%description
This is the Evolution Connector for Sun Java Enterprise System Calendar Server
(SJESCS), which adds support for SJESCS 5.1 and above to Evolution.

%post
ldconfig

# $RPM_COMMAND is an environment variable used by the SUN build
# system to control the build process with finer granularity than RPM
# normally allows.  This specfile will function as expected by RPM if
# $RPM_COMMAND is unset.  If you are not the SUN build system,
# feel free to ignore it.

%prep
%setup -q

%build

aclocal $ACLOCAL_FLAGS
libtoolize --force
glib-gettextize --force --copy
intltoolize --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

autoheader
automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix}                                        \
             --enable-idn=yes

make

%install
make -i install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc COPYING ChangeLog AUTHORS INSTALL NEWS README
%{_libdir}/bonobo/servers/GNOME_Evolution_SunOne_Storage.server
%{_libdir}/evolution
%{_libexecdir}/evolution
%{_libdir}/evolution-data-server-*
%{_datadir}/evolution
%{_datadir}/evolution-jescs
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Mon Mar 16 2009 - jedy.wang@sun.com
- Bump to 2.26.0.

* Mon Feb 26 2009 - jedy.wang@sun.com
- Bump to 2.25.2.

* Wed Jan 21 2009 - jeff.cai@sun.com
- Bump to 2.25.1.

* Tue Nov 11 2008 - jeff.cai@sun.com
- Bump to 2.25.0.

* Wed Nov 05 2008 - jedy.wang@sun.com
- Update license version.

* Tue Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0.

* Fri Aug 22 2008 - jedy.wang@sun.com
- Bump to 2.23.2.

* Tue Aug 19 2008 - jedy.wang@sun.com
- Bump to 2.23.1.

* Tue Jun 03 2008 - jedy.wang@sun.com
- Bump to 2.23.0.

* Tue May 27 2008 - jedy.wang@sun.com
- Bump to 2.22.2.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.

* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.91.

* Thu Jan 31 2008 - jedy.wang@sun.com
- Bump to 2.21.90.

* Wed Nov 07 2007 - jedy.wang@sun.com
- Bump to 2.21.0.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.12.0.

* Thu Jul 03 2007 - jedy.wang@sun.com
- Remove patch, 01-pkg-config-ver-nums.diff as it is upstream.

* Thu Jul 02 2007 - jedy.wang@sun.com
- Bump to 2.11.2.

* Thu Jun 28 2007 - jedy.wang@sun.com
- Bump to 2.11.1.

* Thu Jun 07 2007 - damien.carbery@sun.com
- Add patch, 01-pkg-config-ver-nums, to remove version numbers from modules in
  pkg-config calls. Fixes #445048.

* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 2.11.0. Remove both patches as they are upstream.

* Tue May 15 2007 - damien.carbery@sun.com
- Add patch, 02-e-gtk-utils, to build with Evo 2.11.x. Fixes 438627.

* Tue May 15 2007 - damien.carbery@sun.com
- Add patch, 01-evo-shell-ver, to build with Evolution 2.11.x. Fixes 438618.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.9.1.

* Wed Dec 27 2006 - jedy.wang@sun.com
- Update source link.

* Mon Dec 11 2006 - jedy.wang@sun.com
- Bump to 2.9.0.
- Remove the patch 01-evo-api-ver-hack.

* Mon Nov 29 2006 - damien.carbery@sun.com
- Add patch 01-evo-api-ver-hack so that the evolution 2.9 module can be found.
  It will be removed when evolution-jescs is bumped to 2.9.

* Wed Sep 27 2006 - jedy.wang@sun.com
- Bump to 2.8.2.

* Mon Sep 21 2006 - jedy.wang@sun.com
- Bump to 2.8.1.

* Mon Sep 14 2006 - jedy.wang@sun.com
- Bump to 2.8.0.

* Mon Sep 14 2006 - jedy.wang@sun.com
- Bump to 2.7.1.

* Mon Jul 24 2006 - jedy.wang@sun.com
- Bump to 2.7.0.

* Mon Jul 14 2006 - jedy.wang@sun.com
- Bump to 2.6.4.

* Mon Jun 12 2006 - jedy.wang@sun.com
- Bump to 2.6.3.

* Mon May 29 2006 - halton.huo@sun.com
- Bump to 2.6.2.

* Fri May 12 2006 - halton.huo@sun.com
- Bump to 2.6.1.

* Thu May 11 2006 - halton.huo@sun.com
- Bump to 2.5.4.

* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.5.3.

* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Remove patch, 01-bonobo, as crashes have been fixed upstream.

* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 2.5.2.
- Remove upstream patch, 01-close-tag.

* Fri Mar  3 2006 - harry.lu@sun.com
- Add patch, 01-bonobo.diff to fix a starup crash.

* Fri Feb 24 2006 - damien.carbery@sun.com
- Bump to 2.5.1.
- Remove upstream patch, 01-close-tag.

* Thu Feb  2 2006 - damien.carbery@sun.com
- Add patch, 01-close-tag, to close a tag in 
  GNOME_Evolution_SunOne_Storage.server.in.in file. 

* Tue Jan 24 2006 - halton.huo@sun.com
- s/%{eds_api_version}/\*/g

* Tue Jan 24 2006 - halton.huo@sun.com
- Remove hard code evo_major_version and eds_api_version.

* Tue Jan 24 2006 - halton.huo@sun.com
- Bump to 2.5.0.
- Add define evo_major_version and eds_api_version.
- Remove define evolution_imagesdir.

* Fri Nov 25 2005 - halton.huo@sun.com
- Bump to 2.4.3.

* Wed Nov 16 2005 - halton.huo@sun.com
- Bump to 2.4.2.

* Thu Sep 8 2005 - halton.huo@sun.com
- Bump to 2.4.1.

* Thu Sep 8 2005 - halton.huo@sun.com
- Remove upstream patch evolution-jescs-01-autogen.diff.
- Enable idn.
- Use aclocal, ..., ./configure steps, not ./autogen, 
  because download tarball does not have autogen.sh.

* Tue Sep 6 2005 - halton.huo@sun.com
- Add patch evolution-jescs-01-autogen.diff.
- Temporarily disable idn.
- Change %install, %clean and %files section.

* Wed Aug 31 2005 - halton.huo@sun.com
- Initial spec file
