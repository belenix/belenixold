#
# spec file for package vino
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include l10n.inc
Name:			vino
License:		GPL v2
Group:			System/GUI/GNOME
Version:		2.26.1
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		GNOME Remote Desktop
Source:			http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                l10n-configure.sh
Source2:                %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
# date:2008-07-14 type:branding owner:jedy
Patch1:                 %{name}-01-menu-entry.diff
# date:2008-11-28 type:feature owner:fujiwara bugzilla:562523
Patch2:                 %{name}-02-cp-utf8.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define			gnutls_version 0.9.5
%define			gtk2_version 2.2.0
%define			GConf_version 2.2.0
%define			libglade_version 2.0.0
%define                 intltool_version 0.25
%define			libgnomeui_version 2.4.0

Requires:		gnutls         >= %{gnutls_version}
Requires:		gtk2           >= %{gtk2_version}
Requires:		GConf          >= %{GConf_version}
Requires:		libglade       >= %{libglade_version}
Requires:		libgnomeui     >= %{libgnomeui_version}
BuildRequires:		gnutls-devel   >= %{gnutls_version}
BuildRequires:		gtk2-devel     >= %{gtk2_version}
BuildRequires:		GConf-devel    >= %{GConf_version}
BuildRequires:		libglade-devel >= %{libglade_version}
BuildRequires:		intltool       >= %{intltool_version}

%description
Vino is an integrated GNOME VNC server and a VNC client written in Java.


%prep
%setup -q
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal $ACLOCAL_FLAGS
libtoolize --force
intltoolize --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

autoheader
automake -a -f -c --gnu
autoconf 

CFLAGS="$RPM_OPT_FLAGS" \
./configure   --prefix=%{_prefix}               \
              --sysconfdir=%{_sysconfdir}       \
              --libexecdir=%{_libexecdir}       \
              --enable-http-server=yes          \
              --enable-gnome-keyring=yes        \
              --enable-avahi=yes                \
              --enable-libunique=yes            \
%if %debug_build
              --enable-debug=yes                \
%endif
              --enable-ipv6=yes

make -j $CPUS


%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/vino-server.schemas >/dev/null

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc docs/remote-desktop.txt
%doc docs/TODO
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libexecdir}/*
%{_datadir}/applications/
%{_datadir}/vino/*
%{_datadir}/icons/
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%config %{_sysconfdir}/gconf/schemas/*

%changelog
* Tue Apr 14 2009 - halton.huo@sun.com
- Bump to 2.26.1
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Mar 03 2009 - halton.huo@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - halton.huo@sun.com
- Bump to 2.25.91
* Mon Feb 09 2009 - halton.huo@sun.com
- Bump to 2.25.90
- Remove upstreamed patch typo.diff
* Sat Jan 24 2009 - halton.huo@sun.com
- Enable libunique explicitly
* Tue Jan 22 2009 - halton.huo@sun.com
- Bump to 2.25.5
- Remove patch ifaddrs.diff
- Add patch typo.diff to fix bugzilla #568646
* Tue Jan 06 2009 - halton.huo@sun.com
- Bump to 2.25.4
* Tue Dec 23 2008 - halton.huo@sun.com
- Bump to 2.25.3
- Add patch ifaddrs.diff to fix bugzilla #565422
* Fri Nov 28 2008 - takao.fujiwara@sun.com
- Add patch cp-utf8.diff to copy multibyte chars.
* Tue Oct 21 2008 - halton.huo@sun.com
- Bump to 2.24.1.
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - halton.huo@sun.com
- Bump to 2.23.92
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 19 2008 - halton.huo@sun.com
- Bump to 2.23.90
- Remove upstreamed patch keyring-h.diff and autostart.diff
* Thu Aug 07 2008 - halton.huo@sun.com
- Add patch autostart.diff to fix bugster #6727827, bugzilla #544650 

* Wed Jul 23 2008 - halton.huo@sun.com
- Bump to 2.23.5
- Add patch keyring-h.diff to fix bugzilla #544277

* Mon Jul 13 2008 - jedy.wang@sun.com
- Add 01-desktop.diff.

* Tue May 27 2008 - halton.huo@sun.com
- Bump to 2.22.2

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.

* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.

* Tue Jan 29 2008 - halton.huo@sun.com
- Bump to 2.21.90.

* Tue Dec 04 2007 - halton.huo@sun.com
- Bump to 2.21.3.

* Tue Nov 13 2007 - halton.huo@sun.com
- Bump to 2.21.2.

* Wed Oct 31 2007 - halton.huo@sun.com
- Enable avahi.

* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.

* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.92.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.

* Tue Jul 10 2007 - halton.huo@sun.com
- Bump to 2.19.5
- Remove upstreamed patches.

* Mon Jul 09 2007 - halton.huo@sun.com
- Add patch crash-on-null-password.diff.

* Wed Jun 20 2007 - halton.huo@sun.com
- Use --enable-debug when using pkgtool --with-debug.

* Fri Apr 20 2007 - halton.huo@sun.com
- Rework patch xsun-disable-scroll.diff, remove %ifarch thing.
- Add patch http-vnc-command.diff to fix bugzilla 431635.

* Wed Apr 18 2007 - halton.huo@sun.com
- Add patch xsun-disable-scroll.diff to fix bugster 6508483.

* Tue Apr 10 2007 - halton.huo@sun.com
- Bump to 2.18.1.
- Remove patch crash-critical-warning.diff, upstreamed.

* Fri Mar 13 2007 - halton.huo@sun.com
- Add patch crash-critical-warning.diff to fix critical warning,
  for bugzilla #418836, bugster #6535190.

* Tue Mar 13 2007 - halton.huo@sun.com
- Remove patch gtkicontheme-header.diff, upstreamed.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Tue Feb 27 2007 - halton.huo@sun.com
- Bump to 2.17.92.
- Add patch gtkicontheme-header.diff to fix bugzilla #412559.

* Mon Feb 26 2007 - halton.huo@sun.com
- remove option --enable-session-support=yes to 
  do not distribute vino-session.
- remove useless patch vino-01-remove-vino-session.diff

* Tue Feb 13 2007 - halton.huo@sun.com
- Add patch remove-vino-session.diff to fix bugzilla  #407364

* Fri Feb 09 2007 - halton.huo@sun.com
- Remove useless patch vino-01-fix-a11y-hang.diff.

* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.

* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4. Remove upstream patch, vino-02-keyborad-map.diff.

* Mon Nov 27 2006 - halton.huo@sun.com
- Remove patch disable-xsun.diff.
- Add patch keyborad-map.diff.

* Thu Nov 23 2006 - damien.carbery@sun.com
- Remove upstream patches, 02-a11y-theme-icons and 03-a11y-selectable-label. 
  Renumber remainder.

* Thu Nov 23 2006 - damien.carbery@sun.com
- Bump to 2.17.2. Remove 8 upstream patches: 02-gnome-keyring, 03-xgl,
  04-ipv6-remove-dead-code, 05-ipv6-use-getaddrinfo, 06-ipv6-use-inet-ntop,
  07-ipv6-configure-check, 08-ipv6-create-ipv6-socket,
  09-ipv6-create-ipv6-http-socket.

* Fri Nov 17 2006 - halton.huo@sun.com
- Change patch owner to opensolaris id.

* Thu Nov 16 2006 - halton.huo@sun.com
- Add patch disable-xsun.diff.

* Wed Nov 08 2006 - halton.huo@sun.com
- Add patch a11y-theme-icons.diff to fix bug
  bugster:6491224 bugzilla:345394
- Add patch a11y-selectable-label.diff to fix bug
  bugster:6491221 bugzilla:338043

* Tue Nov 07 2006 - halton.huo@sun.com
- Remove glib-gettextize because intltoolize added.
- Enable ipv6-create-ipv6-socket.diff and 
  ipv6-create-ipv6-http-socket.diff to fix ipv6 problem, 
  bugster #6483870, bugzilla #310965.

* Fri Nov 03 2006 - halton.huo@sun.com
- Add autoheader before configure to fix ipv6 and gnome-keyring.

* Fri Oct 27 2006 - halton.huo@sun.com
- Change IPv6 patch according community new patch
- Add configure option --enable-ipv6=yes

* Thu Oct 19 2006 - halton.huo@sun.com
- Rename patch keyring.diff to gnome-keyring.diff
- Add option --enable-gnome-keyring.
- Add patch ipv6-support.diff to support IPv6, #6483870.

* Tue Oct 17 2006 - halton.huo@sun.com
- Add patch xgl.diff to fix sparc crash bug #6409721.

* Tue Oct 17 2006 - halton.huo@sun.com
- Bump to 2.16.0.

* Wed Oct 11 2006 - halton.huo@sun.com
- Remove Patch2 vino-02-libgnomeui-include.diff and reorder,
  since patch1 already fix this problem.

* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.5.

* Fri Sep 30 2005 - damien.carbery@sun.com
- Add patch to move a #include outside '#ifdef HAVE_GNUTLS' code so that it
  builds. Bugzilla: 315459.

* Sun Sep 18 2005 - glynn.foster@sun.com
- Remove the resolution-change patch, and reorder.

* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Tue Aug 23 2005 - damien.carbery@sun.com
- Remove PATH setting as it is not used (info was wrong and build unaffected).

* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.90.

* Thu May 26 2005 - leena.gunda@wipro.com
- Bump to 2.10.1

* Fri May 20 2005 - leena.gunda@wipro.com
- Added vino-08-fix-a11y-hang.diff to fix the gnome-session hang
  with a11y and remote desktop enabled. Fixes bug #6272397.

* Wed Mar 02 2005 - leena.gunda@wipro.com
- Added vino-07-allow-resolution-change.diff to fix the crash when
  trying to change resolution from the client. Fixes bug #4965618.

* Thu Sep 16 2004 - ciaran.mcdermott@sun.com
* Added vino-05-g11n-alllinguas.diff to include cs,hu linguas

* Thu Aug 26 2004 - vinay.mandyakoppal@wipro.com
- Help invocation for vino is implemented.
 
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to vino-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Sun May 30 2004 - dermot.mccluskey@sun.com
- New JDK

* Wed May 14 2004 - hidetoshi.tajima@sun.com
- added vino-03-fix-stdint.diff to fix build error on S9

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to vino-l10n-po-1.1.tar.bz2

* Thu Apr 14 2004 - brian.cameron@sun.com
- Add ACLOCAL_FLAGS to aclocal call for Solaris build.

* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to vino-l10n-po-1.0.tar.bz2

* Wed Feb 11 2004 - <erwann.chenede@sun.com>
- Update to 0.14 + port

* Thu Nov 06 2003 - <markmc@sun.com>
- Initial spec file
