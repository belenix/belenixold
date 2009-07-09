#
# spec file for package gvfs
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         gvfs
License:      LGPL
Group:        System/Libraries/GNOME
Version:      1.2.0
Release:      4
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Virtual File System Library for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.2/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
#owner:yippi date:2008-04-28 type:branding 
# Note this patch is needed until HAL 0.5.10 is available on Solaris.
Patch1:       gvfs-01-hal-version.diff
#owner:padraig date:2008-04-28 type:feature bugster:6664678 bugzilla:526902
Patch2:       gvfs-02-enable-cdda-without-cdio.diff
#owner:gheet date:2009-03-23 type:branding bugzilla:6598
Patch3:	      gvfs-03-debug-crash.diff

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

#autoreconf --force --install
libtoolize --force 
aclocal $ACLOCAL_FLAGS
autoconf
CFLAGS="$RPM_OPT_FLAGS -DDBUS_API_SUBJECT_TO_CHANGE=1"	\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 23 2009 - ghee.teo@sun.com
- added gvfs-03-debug-crash.diff to stop crashing when default workgroup is nul.
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 1.2.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 1.1.8
* Tue Mar 03 2009 - ghee.teo@sun.com
Removed gvfs-03-trash-only-home.diff as it is not required based on the current
behaviour. Files from different file system are copied to trash directory.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 1.1.6
* Tue Feb 02 2009 - christian.kelly@sun.com
- Bump to 1.1.5.
* Wed Jan 07 2009 - christian.kelly@sun.com
- Bump to 1.1.3.
* Fri Jan 01 2009 - padraig.obriain@sun.com
- Comment out gvfs-03-trash-only-home.diff. Must determine whether the
  patch needs to be reworked.
* Sat Dec 27 2008 - dave.lin@sun.com
- Bump to 1.1.2.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 1.1.1
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 1.0.1.
* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 0.99.8.
- Remove patch gvfs-03-trash-only-home.diff.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 0.99.7.1.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 0.99.6.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 0.99.5
* Thu Aug 14 2008 - padraig.obriain@sun.com
- Add patch -trash-only-home to avoid stat'ing Trash directories on Unix
  mounts.
* Wed Aug 06 2008 - christian.kelly@sun.com
- Bump to 0.99.4.
- Remove patch 03-trash-only-home, fixed upstream bugzilla:525779
- Rename patch 04 to 03
- Rework patch 02
* Thu Jul 24 2008 - damien.carbery@sun.com
- Bump to 0.99.3.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 0.99.2.
* Fri Jul 04 2008 - padraig.obriain@sun.com
- Add patch 04-smb-mount to fix CR 6715607
* Wed Jun 25 2008 - padraig.obriain@sun.com
- Add patch -trash-only-home to avoid stat'ing Trash directory on mounted filesystems
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 0.99.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 0.2.4.
* Mon Apr 28 2008 - padraig.obriain@sun.com
- Add patch -enable-cdda-without-cdio to enable cdda backend without libcdio.
* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 0.2.3.
* Mon Mar 31 2008 - damien.carbery@sun.com
- Bump to 0.2.2.
* Thu Mar 27 2008 - damien.carbery@sun.com
- Bump to 0.2.1.
* Wed Mar 05 2008 - damien.carbery@sun.com
- Bump to 0.1.11.
* Mon Mar 03 2008 - alvaro.lopez@sun.com
- Added gvfs-01-hal-version.diff
* Thu Feb 28 2008 - damien.carbery@sun.com
- Bump to 0.1.8.
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Bump to 0.0.2. Remove upstream patches, 01-solaris and 02-solaris2.
* Fri Nov 09 2007 - daymobrew@users.sourceforge.net
- Add patch 02-solaris2 to include header files to fix 'implicit function
  declaration' warnings.

* Wed Nov 07 2007 - daymobrew@users.sourceforge.net
- Initial version.
