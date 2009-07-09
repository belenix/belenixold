#
# spec file for package SUNWavahi-bridge-dsd
#
# includes module(s): avahi
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#

%include Solaris.inc

%use avahi = avahi.spec 

Name:                    SUNWavahi-bridge-dsd
Summary:                 Avahi client and bridge to SUNWdsd.
Version:                 %{avahi.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_copyright:          %{name}.copyright
Source1:        avahi-bridge-dsd.xml
Source2:        svc-avahi-bridge-dsd

%include default-depend.inc
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWgnome-python-libs-devel
BuildRequires:  SUNWdbus-python24
BuildRequires:  SUNWpython-setuptools
Requires:       SUNWgnome-base-libs
Requires:       SUNWgnome-python-libs
Requires:       SUNWPython
Requires:       SUNWdbus-python24
Requires:       SUNWavahi-bridge-dsd-root
Requires:       SUNWlibdaemon
Requires:       SUNWlexpt
Requires:       SUNWdsdr

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
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
%avahi.prep -d %name-%version

%build
PKG_CONFIG_DISABLE_UNISTALLED=
unset PKG_CONFIG_DISABLE_UNISTALLED
export PKG_CONFIG_PATH=../avahi-%{avahi.version}:%{_pkg_config_path}
export CFLAGS="%optflags -I/usr/sfw/include"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -ldns_sd -lsocket -lnsl -L/usr/sfw/lib -R/usr/sfw/lib -lexpat"

%avahi.build -d %name-%version

%install
%avahi.install -d %name-%version
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/system
chmod -R 755 $RPM_BUILD_ROOT/var/svc
cp %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/system/
mkdir -p $RPM_BUILD_ROOT/lib/svc/method
chmod -R 755 $RPM_BUILD_ROOT/lib
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

mv $RPM_BUILD_ROOT%{_sbindir}/avahi-daemon $RPM_BUILD_ROOT%{_sbindir}/avahi-daemon-bridge-dsd
%if %option_with_indiana_branding
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif

%pre root
#!/bin/sh
#
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Presence of this temp file will tell postinstall script
# that the avahi-bridge-dsd service is already installed, in which case
# the current service state will be preserved, be it enabled
# or disabled.
rm -f $PKG_INSTALL_ROOT/var/avahi-bridge-dsd_installed.tmp > /dev/null 2>&1

if [ -f $PKG_INSTALL_ROOT/var/svc/manifest/system/avahi-bridge-dsd.xml ]; then 
	touch $PKG_INSTALL_ROOT/var/avahi-bridge-dsd_installed.tmp
fi

exit 0

%post root
#!/bin/sh
#
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Preinstall script will create this file if avahi-bridge-dsd service was 
# already installed, in which case we preserve current service state,
# be it enabled or disabled.
if [ -f $PKG_INSTALL_ROOT/var/avahi-bridge-dsd_installed.tmp ]; then
	rm -f $PKG_INSTALL_ROOT/var/avahi-bridge-dsd_installed.tmp
else
	# enable avahi-bridge-dsd:
	# - PKG_INSTALL_ROOT is / or empty when installing onto a live system
	#   and we can invoke svcadm directly;
	# - otherwise it's upgrade, so we append to the upgrade script
	if [ "${PKG_INSTALL_ROOT:-/}" = "/" ]; then
		if [ `/sbin/zonename` = global ]; then
			/usr/sbin/svcadm enable -r svc:/system/avahi-bridge-dsd:default
		fi
	else
		cat >> ${PKG_INSTALL_ROOT}/var/svc/profile/upgrade <<-EOF
		if [ \`/sbin/zonename\` = global ]; then
			/usr/sbin/svcadm enable -r svc:/system/avahi-bridge-dsd:default
		fi
EOF
	fi
fi

exit 0
%files
%doc -d avahi-%{avahi.version} README LICENSE
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/avahi-daemon-bridge-dsd
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libavahi*.so*
%{_libdir}/avahi/service-types.db.pag
%{_libdir}/avahi/service-types.db.dir
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/avahi/service-types
%if %option_with_sun_branding
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/avahi-discover.desktop
%{_datadir}/applications/bssh.desktop
%{_datadir}/applications/bvnc.desktop
%endif
%{_datadir}/avahi/interfaces/avahi-discover.glade
%{_datadir}/avahi/introspection/Server.introspect
%{_datadir}/avahi/introspection/EntryGroup.introspect
%{_datadir}/avahi/introspection/DomainBrowser.introspect
%{_datadir}/avahi/introspection/ServiceBrowser.introspect
%{_datadir}/avahi/introspection/ServiceTypeBrowser.introspect
%{_datadir}/avahi/introspection/ServiceResolver.introspect
%{_datadir}/avahi/introspection/AddressResolver.introspect
%{_datadir}/avahi/introspection/HostNameResolver.introspect
%{_datadir}/avahi/introspection/RecordBrowser.introspect
%{_datadir}/avahi/avahi-service.dtd
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1/*
%attr (-, root, bin) %{_libdir}/python*

%files root
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config %{_sysconfdir}/*
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/system
%class(manifest) %attr (0444, root, sys) /var/svc/manifest/system/avahi-bridge-dsd.xml
%attr (0555, root, bin) /lib/svc/method/svc-avahi-bridge-dsd


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Mar 23 2009 - jeff.cai@sun.com
- Because /usr/bin/avahi-discover (SUNWavahi-bridge-dsd) requires
  /usr/bin/i86/isapython2.4 which is found in SUNWPython, add the dependency.
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-python.
* Wed Sep 10 2008 - padraig.obriain@sun.com
- Add %doc in %files for copyright
* Wed Aug 06 2008- padraig.obriain@sun.com
- add pre and post scripts for enabling the avahi-bridge-dsd svc upon 
  installation but leaving it as is upon upgrade (based on dbus spec file)
* Fri Jun 06 2008 - damien.carbery@sun.com
- Add l10n package.
* Wed Oct 31 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus-bindings/-devel as the dbus python module is used.
* Wed Oct 31 2007 - damien.carbery@sun.com
- Remove references to /usr/lib/mdns from LDFLAGS as the dir doesn't exist.
* Fri Sep 07 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-base-libs/-devel for glib.
- Add Build/Requires SUNWgnome-python-libs/-devel for gtk Python module.
* Wed Jun 28 2007 - padraig.obriain@sun.com
- Initial spec file created.

