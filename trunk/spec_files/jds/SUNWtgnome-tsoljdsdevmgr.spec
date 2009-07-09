#
# spec file for package SUNWtgnomedevmgr
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: johnf

%include Solaris.inc

# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define devmgr_version 0.6.4

Name:                    SUNWtgnome-tsoljdsdevmgr
Summary:                 GNOME Trusted Device Manager
Version:                 %{default_pkg_version}
Source:			 http://dlc.sun.com/osol/jds/downloads/extras/tjds/tsoljdsdevmgr-%{devmgr_version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
# owner:johnf date:2009-03-09 type:bug
Patch1:                  tsoljdsdevmgr-01-dialog-crash.diff
%endif
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWtsu
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-panel
Requires: SUNWtgnome-tsol-libs
BuildRequires: SUNWtsu
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWtgnome-tsol-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n tsoljdsdevmgr-%{devmgr_version}

%patch1 -p1

%build
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

libtoolize -f
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -acf

CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS" \
./configure --with-gnome-prefix=%{_prefix} \
            --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
	    --mandir=%{_mandir}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/tsoljdsdevmgr

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Fri Aug 22 2008 - stephen.browne@sun.com
- Uprev version, remove upstream patches

* Tue Aug  5 2008 - takao.fujiwara@sun.com
- Add tsoljdsdevmgr-02-no-gettext.diff to avoid segv. Fixes 6727185.

* Thu Jul 10 2008 - damien.carbery@sun.com
- Add 01-gtk-disable-deprecated to get module to build with new gtk+ tarball.

* Fri May 16 2008 - stephen.browne@sun.com
- Uprev version, remove upstream patch, remove conditional build

* Thu May 08 2008 - takao.fujiwara@sun.com
- Add SUNWtgnome-tsoljdsdevmgr-01-po.diff for cs.po
  Contributed l10n from Hana Zalska <Hana.Zalska@sun.com>

* Tue Mar 25 2008 - takao.fujiwara@sun.com
- Remove upstreamed scripts.
- Remove upstreamed tsoljdsdevmgr-01-pwd-fns.diff

* Fri Mar 14 2008 - stephen.browne@sun.com
- update version. point source at dlc.sun.com

* Wed Sep 19 2007 - damien.carbery@sun.com
- Remove getpwuid_r patch, tsoljdsdevmgr-01-pwd-fns.diff, as they it is not
  needed from snv_73 on.

* Wed Aug 19 2007 - damien.carbery@sun.com
- Only apply the patch to sparc as x86 builds use the 4 param versions.

* Tue Aug 18 2007 - damien.carbery@sun.com
- Add patch tsoljdsdevmgr-01-pwd-fns.diff to use 5 param versions of some 
  password functions.

* Fri Sep 15 2006 - takao.fujiwara@sun.com
- Add *-10n package.

* Sun Jul 30 2006 - damien.carbery@sun.com
- Always use nightly tarballs as source.

* Thu Jul 13 2006 - damien.carbery@sun.com
- Add %{_datadir}/locale to %files, a byproduct of intltool up-rev.

* Tue Jul 11 2006 - damien.carbery@sun.com
- Add autogen.sh commands to %prep to permit building from 'cvs co' tarballs.

* Wed May 24 2006 - stephen.browne@sun.com
- remove man page from files and shorten summary

* Wed Mar 29 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWtgnome-tsol-libs/-devel.
- Add Build/Requires SUNWtsu.

* Wed Mar  8 2006 - damien.carbery@sun.com
- Add %dir %attr for %{_datadir} as %defattr is wrong for this dir.

* Tue Mar  7 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-panel/-devel, for libwnck.

* Sat Feb 25 2006 - <john.fischer@sun.com>
- created 
