#
# spec file for package ekiga
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine 
#
%include l10n.inc
Name:		ekiga
License:	GPL
Group:		X11/GNOME/Applications
Version:        3.0.1
Release:	1
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
Summary:	A GNOME based H.323/SIP video conferencing application
Source:         http://ftp.gnome.org/pub/GNOME/sources/ekiga/3.0/%{name}-%{version}.tar.gz
Source2:        %{name}-po-sun-%{po_sun_version}.tar.bz2

# owner:gman date:2006-06-02 type:branding
# change the menu entry according to the UI spec
Patch1:         ekiga-01-menu-entry.diff 

# owner:elaine date:2008-11-11 type:branding
# Once OpenLdap integrated please remove this patch
Patch2:         ekiga-02-use-sunldap.diff 

# owner:elaine date:2008-11-11 type:branding
# remove the test_age check to keep configuration compatibility
Patch3:         ekiga-03-test_age.diff

# owner:elaine date:2008-11-11 type:branding
Patch4:         ekiga-04-template-argument.diff

Patch5:         ekiga-05-makefile-fix.diff

URL:		http://www.ekiga.org
BuildRoot:	%{_tmppath}/%{name}-root
Docdir:       	%{_docdir}/%{name}
Autoreqprov:  	on

# The following version definitions probably are out of date, need update
%define GConf_version 2.4.0.1
%define gtk2_version 2.3.1
%define openldap2_devel_version 2.1.4
%define intltool_version 0.27
%define libgnomeui_version 2.4.0.1
%define des_version 4.04
%define heimdal_version 0.4
%define cyrus_sasl_version 1.5.27
%define openssl_version 0.9.6
%define flex_version 2.5.4
%define slang_version 1.4.5
%define pam_version 0.76
%define db_version 4.0.14
%define gdbm_version 1.8.0
%define howl_version 1.0.0

Requires: ptlib >= %{ptlib_version}
Requires: opal >= %{opal_version}
Requires: GConf >= %{GConf_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: howl >= %{howl_version}
Requires: evolution-data-server
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: GConf-devel >= %{GConf_version}
BuildRequires: openh323-devel >= %{openh323_version}
BuildRequires: ptlib-devel >= %{ptlib_version}
BuildRequires: intltool >= %{intltool_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: des >= %{des_version}
BuildRequires: heimdal-devel >= %{heimdal_version}
BuildRequires: cyrus-sasl-devel >= %{cyrus_sasl_version}
BuildRequires: openssl-devel >= %{openssl_version}
BuildRequires: openldap2-devel >= %{openldap2_devel_version}
BuildRequires: flex >= %{flex_version}
BuildRequires: slang-devel >= %{slang_version}
BuildRequires: pam-devel >= %{pam_version}
BuildRequires: db-devel >= %{db_version}
BuildRequires: gdbm-devel >= %{gdbm_version}
BuildRequires: howl-devel >= %{howl_version}
BuildRequires: evolution-data-server-devel
Prereq:        GConf

%description
Ekiga is a free Voice over IP phone allowing you to do free calls over   
the Internet. Ekiga is the first Open Source application to support 
both H.323 and SIP, as well as audio and video. Ekiga was formerly known 
as GnomeMeeting. 

%prep
%setup -q -n %{name}-%{version}
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

export CFLAGS="%optflags -DSOLARIS -D__inline=inline"
export CXXFLAGS="%cxx_optflags -DSOLARIS -D__inline=inline -I%{ptlib_dir}/include"
export LDFLAGS="%_ldflags"
#export XGETTEXT=`which xgettext`

%{?ekiga_libdir:export LDFLAGS="$LDFLAGS -R%{ekiga_libdir}"}
aclocal
autoconf
./configure --prefix=%{_prefix} \
             --libdir=%{?ekiga_libdir}%{?!ekiga_libdir:%{_libdir}} \
             --bindir=%{_bindir} \
             --datadir=%{_datadir} \
             --includedir=%{_includedir} \
             --mandir=%{_mandir} \
	     --sysconfdir=%{_sysconfdir} \
             %{?ptlib_opt} %{?opal_opt} \
	     --enable-xv
gmake -j $CPUS

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
gmake install DESTDIR=$RPM_BUILD_ROOT

rm -f  $RPM_BUILD_ROOT%{_bindir}/*config*
rm -f  $RPM_BUILD_ROOT%{_bindir}/ekiga-helper
rm -rf $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="ekiga.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-,root,root)
%dir %{_datadir}/ekiga/xdap
%dir %{_datadir}/sounds/ekiga
%{_bindir}/ekiga*
%{_datadir}/locale/*/LC_MESSAGES/ekiga.mo
%{_datadir}/applications/ekiga.desktop
%{_datadir}/sounds/ekiga/*
%{_datadir}/pixmaps/ekiga*
%{_libdir}/bonobo/servers/ekiga.server
%{_datadir}/ekiga/xdap/*
%{_sysconfdir}/gconf/schemas/ekiga.schemas
%{_datadir}/gnome/*
%{_datadir}/omf/*
%{_mandir}/man1/*


%changelog
* Mon Mar 23 2009 - elaine.xiong@sun.com
- Remove ekiga-helper to fix man page problem.
* Thu Nov 20 2008 - elaine.xiong@sun.com
- Bump to 3.0.1.
* Fri Nov 14 2008 - elaine.xiong@sun.com
- Bump to 3.0.0. Add new patches and remove obsolete patches.
- Update build options for new version.
* Wed Sep 03 2008 - elaine.xiong@sun.com
- Add note to not bump to 2.9.90 as it's actually 3.0 beta1 and not ready for
  Solaris.
* Mon Jul 21 2008 - elaine.xiong@sun.com
- Add bugID.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.0.12.
* Wed Mar 05 2008 - elaine.xiong@sun.com
- Add ekiga-06-rm-evcard.diff to fix bugster#6665230. 
  But this patch will not be compatible with Ekiga 3.0.
* Sun Dec 23 2007 - patrick.ale@gmail.com
- Set the XGETTEXT variable based on `which xgettext`
  Since we use JDS-CBE this should be /opt/jdsbld/bin/xgettext
  Ekiga will FAIL when /usr/bin/xgettext (NON-GNU version) is used.
* Fri Nov 02 2007 - elaine.xiong@sun.com
- Enable Avahi support.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.0.11. Remove upstream patch, 06-loopback.
* Thu Aug 30 2007 - elaine.xiong@sun.com
- Disable DBUS component due to weak support.
* Thu Jun 28 2007 - elaine.xiong@sun.com
- Explicitly enable the DBUS component.
* Sun Jun 03 2007 - elaine.xiong@sun.com
- Add patch ekiga-06-loopback.diff to fix bugzilla439873
* Wed Apr 25 2007 - elaine.xiong@sun.com
- Update owner name for ekiga-04-performance-tuning.diff
* Thu Apr 19 2007 - elaine.xiong@sun.com
- Bump to 2.0.9.
* Tue Apr 17 2007 - elaine.xiong@sun.com
- move the -Lpath that could specify the /usr/lib/ as the search directory
  when link time.
* Thu Apr  5 2007 - laca@sun.com
- move libsdl, pwlib and opal to their own separate spec files
* Fri Mar 23 2007 - elaine.xiong@sun.com
- Add patch ekiga-23-opal-illege-payloadtype.diff to fix bugster6537448
  already upstream. Refer to
  http://openh323.cvs.sourceforge.net/openh323/opal/src/h323/h323.cxx?r1=2.143&r2=2.144
* Mon Mar 20 2007 - damien.carbery@sun.com
- Point at ftp.gnome.org for ekiga bz2 tarball. ekiga.org only has gz tarball.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.0.7; bump pwlib to 1.10.5 & bump opal to 2.2.6. Remove upstream
  patch, 21-pwlib-v4l2-enable, renumber remainder.
* Sun Mar 11 2007 - elaine.xiong@sun.com
- Add patch ekiga-22-ekiga-performance-tuning.diff
            ekiga-23-pwlib-performance-tuning.diff
  Both of them for ekiga performance tuning with video support.
  Will upstream them or part of them to community if tuning is done. 
* Wed Feb 14 2007 - elaine.xiong@sun.com
- Add patch ekiga-21-pwlib-enable-v4l2.diff to fix bugzilla407820
  Meantime enable V4L2 plugin in ekiga.spec 
* Wed Feb 14 2007 - damien.carbery@sun.com
- Bump to 2.0.5; bump pwlib to 1.10.4 & bump opal to 2.2.5.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Mon Jan 29 2007 - elaine.xiong@sun.com
- Cancel parallel job option for ekiga(including sdl, pwlib, opal) build.
  To temporily solve the potential problems caused by parallel.
  Will be fixed ASAP.
* Sat Jan 27 2007 - elaine.xiong@sun.com
- Bump ekiga to 2.0.4  shrink patches and spec file for build failure
* Wed Jan 24 2007 - damien.carbery@sun.com
- Bump pwlib to 1.10.3, opal to 2.2.4. Remove upstream patches, 
  08-pwlib-disconnect, 09-pwlib-unset-port, 13-opal-bz356696,
  15-opal-invalidarrayindex, 16-pwlib-video. Add patch 20-opal-break to fix
  build error (sourceforge: 1643652).
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.0.4.
* Thu Jan 04 2007 - elaine.xiong@sun.com
- Add patch ekiga-19-freeze-accessibility.diff. Workes around bugzilla 329454.
* Thu Dec 28 2006 - dave.lin@sun.com
- change the patch type to branding for some patches in patch comments
* Wed Nov 29 2006 - damien.carbery@sun.com
- Fix typo in name of patch 18: s/18-opal-sunray/18-sunray/
* Mon Nov 27 2006 - brian.lu@sun.com
- Add patch ekiga-18-sunray-port-conflict.diff. Fixes bugzilla 367516.
* Mon Nov 20 2006 - davelin@sun.com
- Add patch comment
* Thu Nov 02 2006 - davelin@sun.com
- Bump version to 2.0.3 
- Sync patches those have been upstreamed in ekiga community trunk
- ekiga-10-pwlib-bz356696.diff, ekiga-13-opal-bz356696.diff(better fix 
  for bugzilla356696)
- ekiga-15-opal-invalidarrayindex.diff(bugzilla367482)
- ekiga-16-pwlib-video.diff(bugzilla367516)
- ekiga-17-opal-rtp.diff(CR#6483823, CR#6483831, which caused revert to 
  2.0.2 in b52b)
* Wed Oct 25 2006 - davelin@sun.com
- Roll back to the previous version 2.0.2 since following critical bug
  was found in 2.0.3 CR#6483823(and another P2 bug CR#6483831)
* Tue Oct 17 2006 - dave.lin@sun.com
- Bump version to 2.0.3
- Add patch ekiga-pwlib-09-unset-port.diff to fix bug CR#6476679
- Add patch ekiga-10-pwlib-bz356696.diff to fix bug gnome bugzilla #356696
* Mon Oct 09 2006 - dave.lin@sun.com
- Add patch ekiga-08-pwlib-disconnect-crash.diff to fix bug CR#6470530
* Fri Sep 15 2006 - dermot.mccluskey@sun.com
- Fixed erroneous comments in %defines
* Wed Sep 06 2006 - damien.carbery@sun.com
- Bump pwlib to 1.10.2, opal to 2.2.3.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.0.3.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump libsdl to 1.2.11.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Change 'cd dir*' to use '%{version}'.
* Mon Jul 10 2006 - dave.lin@sun.com
- change to use Ekiga 2.0.2 release
* Fri Jun 16 2006 - dave.lin@sun.com
- add GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 to make sure not
  install the directory based %gconf.xml files based on the 
  instruction in gconf.txt
* Wed Jun 07 2006 - damien.carbery@sun.com
- chdir into ekiga dir before applying ekiga patches.
* Fri Jun 02 2006 - glynn.foster@sun.com
- Add patch for change the menu entry according to the UI spec.
* Mon May 15 2006 - dave.lin@sun.com
- Add patch ekiga-08-multi-decla.diff to fix multiple declaration
  error.
* Fri Apr 14 2006 - <dave.lin@sun.com>
- Initial release for ekiga
