#
# includes module(s): accerciser
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
%define pythonver 2.4

Name:           accerciser
Version:        1.6.0
Release:        1%{?dist}
Summary:        An interactive Python accessibility explorer for the GNOME desktop

Group:          Applications/System
License:        BSD
URL:            http://live.gnome.org/Accerciser
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.6/%{name}-%{version}.tar.bz2
#owner:liyuan date:2007-11-09 bugster:6610155 type:branding
Patch1:         accerciser-01-remove-from-menu.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires: gnome-doc-utils, desktop-file-utils, scrollkeeper, gnome-python2-libwnck, gettext
Requires:  at-spi, pygtk2, gnome-python2, gnome-python2-libwnck, pygtk2-libglade, gnome-python2-bonobo

#Requires(pre): GConf2
#Requires(post): scrollkeeper GConf2
#Requires(postun): scrollkeeper
#Requires(preun): GConf2

%description
Accerciser is an interactive Python accessibility explorer for the GNOME 
desktop. It uses AT-SPI to inspect and control widgets, allowing you to 
check if an application is providing correct information to assistive 
technologies and automated test frameworks.

%prep
%setup -q
%patch1 -p1


%build
aclocal $ACLOCAL_FLAGS
automake --add-missing
autoconf

./configure     --prefix=%{_prefix}		\
                --libdir=%{_libdir}             \
                --bindir=%{_bindir}             \
                --datadir=%{_datadir}           \
                --sysconfdir=%{_sysconfdir}	\
		--disable-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#desktop-file-install --vendor="" --delete-original \
#  --dir $RPM_BUILD_ROOT%{_datadir}/applications        \
#  $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

#%find_lang %{name}

# Move to vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages

%clean
rm -rf $RPM_BUILD_ROOT

%prep
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/accerciser.schemas >/dev/null || :
    killall -HUP gconfd-2 || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/accerciser.schemas > /dev/null || :
killall -HUP gconfd-2 || :

scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
scrollkeeper-update -q || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/accerciser.schemas > /dev/null || :
    killall -HUP gconfd-2 || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog COPYING NEWS
%{_bindir}/%{name}
#%{python_sitearch}/%{name}
%{_datadir}/%{name}
%{_datadir}/omf/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/gnome/help/%{name}
%{_sysconfdir}/gconf/schemas/%{name}.schemas

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 1.6.0
* Wed Feb 18 2009 - dave.lin@sun.com
- Bump to 1.5.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 1.5.9.
* Thu Jan 22 2009 - li.yuan@sun.com
- Bump to 1.5.5.
* Thu Jan 08 2009 - li.yuan@sun.com
- Bump to 1.5.4.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 1.5.2
* Wed Nov 05 2008 - li.yuan@sun.com
- Change copyright information.
* Mon Sep 29 2008 - patrick.ale@gmail.com
- Correct download URL
* Tue Sep 23 2008 - christian.kelly@sun.com
- Bump to 1.4.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 1.3.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 1.3.91.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 1.3.6.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 1.3.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 1.3.4. Remove upstream patch, 02-pyatspi-check.
* Tue Jun 10 2008 - damien.carbery@sun.com
- Add patch 02-pyatspi-check to skip the pyatspi check as it requires a display.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 1.3.1.
* Thu Mar 27 2008 - damien.carbery@sun.com
- Bump to 1.2.0. Call aclocal, automake and autoconf to get patched
  intltool.m4.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 1.1.92.
* Mon Feb 11 2008 - brian.cameron@sun.com
- Bump to 1.1.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 1.1.90.
* Mon Jan 14 2008 - brian.cameron@sun.com
- Bump to 1.1.5.
* Mon Dec 03 2007 - brian.cameron@sun.com
- Bump to 1.1.3.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 1.1.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 1.0.1.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Move files from site-packages to vendor-packages. Fixes 6615442.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.0.0.
* Tue Sep 04 2007 - damien.carbery@sun.com
- Bump to 0.1.92.
* Sun Sep 02 2007 - li.yuan@sun.com
- Initial version.
