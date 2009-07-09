#
# spec file for package SUNWgnome-system-tools
#
# includes module(s): gnome-system-tools, system-tools-backends
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include Solaris.inc
%use gnomesystemtools = gnome-system-tools.spec
%use systemtoolsbackends = system-tools-backends.spec
%define network_admin_sh %gnomesystemtools.SOURCE3

Name:                    SUNWgnome-system-tools
Summary:                 GNOME system tools
Version:                 %{default_pkg_version}

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source:                  %{name}-manpages-0.1.tar.gz
Source1:                 %{name}-exec_attr
Requires:                SUNWgnome-config
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-file-mgr
Requires:                SUNWgnome-libs
Requires:                SUNWgnome-vfs
Requires:                SUNWlibms
Requires:                SUNWlxml
Requires:                SUNWperl584core
Requires:                SUNWperl-authen-pam
Requires:                SUNWgksu
Requires:                SUNWdesktop-cache
Requires:                %{name}-root
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-file-mgr-devel
BuildRequires:           SUNWgnome-libs-devel
BuildRequires:           SUNWgnome-vfs-devel
BuildRequires:           SUNWgnome-doc-utils
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SUNWgksu-devel
                                                                                
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir} 
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%systemtoolsbackends.prep -d %name-%version
%gnomesystemtools.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I %{_builddir}/%{name}-%{version}/%{systemtoolsbackends.name}-%{systemtoolsbackends.version}/m4macros"
export LDFLAGS="%_ldflags -L%{_libdir} -lgnomevfs-2"
export CFLAGS="%optflags -I%{_includedir}/gnome-vfs-2.0 -I%{_libdir}/gnome-vfs-2.0/include"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_builddir}/%{name}-%{version}/%{systemtoolsbackends.name}-%{systemtoolsbackends.version}:%{_pkg_config_path}
%systemtoolsbackends.build -d %name-%version
%gnomesystemtools.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%systemtoolsbackends.install -d %name-%version
%gnomesystemtools.install -d %name-%version
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security
install --mode=0644 %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/security/exec_attr
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/inet/gnome-system-tools
# Change to allow for addition of a network wrapper script to allow
# for a check whether NWAM is enabled or not.
# Move binary to /usr/lib
mv $RPM_BUILD_ROOT/%{_bindir}/network-admin $RPM_BUILD_ROOT/%{_libdir}/network-admin
# Now place script in to bin dir.
install --mode=0755 %network_admin_sh $RPM_BUILD_ROOT/%{_bindir}/network-admin
#Manpages
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

#FIXME: Remove scrollkeeper files
#rm -rf $RPM_BUILD_ROOT%{_prefix}/var/scrollkeeper
#rm -rf $RPM_BUILD_ROOT/var/lib/scrollkeeper
#rmdir $RPM_BUILD_ROOT/var
#Delete all files we don't need at the moment from /usr/share/setup-tool-backends/scripts/
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/boot*
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/dhcpd*
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/print*
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/font*
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/display-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/media.pl
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/memory-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/mouse-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/type1inst
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/package-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/x.pl
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/internetsharing-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/partition.pl
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/disks-conf
rm $RPM_BUILD_ROOT%{_datadir}/setup-tool-backends/scripts/ishare.pl


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
# Remove empty dirs i.e. those with no C locale omf file.
rmdir $RPM_BUILD_ROOT%{_datadir}/omf/gnome-system-tools
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/nautilus
%{_libdir}/network-admin
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/omf/*/*-C.omf
%{_datadir}/gnome-system-tools
%{_datadir}/setup-tool-backends
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*
%doc gnome-system-tools-%{gnomesystemtools.version}/AUTHORS
%doc gnome-system-tools-%{gnomesystemtools.version}/README
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/COPYING
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/NEWS
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/doc/network/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/doc/services/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/doc/time/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/doc/users/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/interfaces/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/pixmaps/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/po/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/common/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/network/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/services/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/shares/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/time/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/time/e-map/ChangeLog
%doc(bzip2) gnome-system-tools-%{gnomesystemtools.version}/src/users/ChangeLog

%doc system-tools-backends-%{systemtoolsbackends.version}/AUTHORS
%doc system-tools-backends-%{systemtoolsbackends.version}/README
%doc(bzip2) system-tools-backends-%{systemtoolsbackends.version}/COPYING
%doc(bzip2) system-tools-backends-%{systemtoolsbackends.version}/NEWS
%doc(bzip2) system-tools-backends-%{systemtoolsbackends.version}/ChangeLog
%doc(bzip2) system-tools-backends-%{systemtoolsbackends.version}/po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z][a-z]
%{_datadir}/omf/*/*-[a-z][a-z].omf
#%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%files root
%defattr (-, root, sys)
%dir %{_sysconfdir}
%attr (0644, root, sys) %{_sysconfdir}/gconf/schemas/gnome-system-tools.schemas
%{_sysconfdir}/inet
%config %class(rbac) %attr (0644, root, sys) %{_sysconfdir}/security/exec_attr

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Fri Sep 12 2008 - matt.keenan@sun.com
- Update copyright
* Wed Jul  9 2008 - takao.fujiwara@sun.com
- Renamed %{name}-network-admin.ksh to %gnomesystemtools.SOURCE3
  to get the SUN_BRANDING translation.
* Thu Jan 10 2008 - damien.carbery@sun.com
- Add gnome-vfs info to CFLAGS and LDFLAGS as configure no longer retrieves
  them with pkg-config (libnautilus-extension depends on gio instead of
  gnome-vfs).
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu Oct 11 2007 - damien.carbery@sun.com
- Remove install dependency on SUNWgnome-doc-utils and change the build
  dependency from SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils.
* Wed Aug 29 2007 - brian.cameron@sun.com
- Remove comment that this package is not to reviewed by JDS ARC team, since
  now we want it reviewed.
* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of /var dirs as they are no longer installed.
* Wed Jun 27 2007 - darren.kenny@sun.com
- Fix for bug#6555581 - wrapper script for network-admin to first check
  whether NWAM is running.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Mon Nov 20 2006 - darren.kenny@sun.com
- Removed the need for [ir].rbac since they already exist in
  /usr/sadm/install/scripts
* Fri Nov 17 2006 - darren.kenny@sun.com
- Add RBAC profiles
* Fri Nov 17 2006 - darren.kenny@sun.com
- Add manpages for build
* Thu Nov 16 2006 - hua.zhang@sun.com
- Delete all files we don't need now from /usr/share/setup-tool-backends/scripts/
* Mon Oct 23 2006 - darren.kenny@sun.com
- Add dependency on SUNWgksu and SUNWgksu-devel for builds.
* Wed Sep 27 2006 - damien.carbery@sun.com
- Delete empty omf dir when not doing l10n build.
* Wed Sep 20 2006 - laca@sun.com
- Fix l10n package - nl locale omf file was in base and l10n package.
* Mon Aug 21 2006 - damien.carbery@sun.com
- Fix l10n package - nl locale omf file was in base and l10n package.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Mon Jun 12 2006 - damien.carbery@sun.com
- Specify %dir %attr for %{_datadir} in the devel package.
- Change devel package to have a basedir of %{_basedir} instead of /.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Sat Jun 10 2006 - laca@sun.com
- split pkgconfig and aclocal files into a -devel subpkg
* Fri Jun  2 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed Mar 15 2006 - damien.carbery@sun.com
- Add to Build/Requires after running check-deps.pl.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Set perms for %{_libdir} in %files.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-doc-utils/-devel.
- Add to %files for l10n package.
* Fri Mar 03 2006 - darren.kenny@sun.com
- Initial spec-file created
