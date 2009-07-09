#
# spec file for package SUNWtgnome-tsol-libs
#
# includes module(s): libgnometsol
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen

# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define libgnometsol_version 0.6.2

%include Solaris.inc

Name:                    SUNWtgnome-tsol-libs
Summary:                 GNOME Trusted Extensions Libraries - platform dependent
Version:                 %{default_pkg_version}
Source:			 http://dlc.sun.com/osol/jds/downloads/extras/tjds/libgnometsol-%{libgnometsol_version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:	  	 %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%package devel
Summary:                 GNOME Trusted Extensions Libraries - platform independent
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWtgnome-tsol-libs


%prep
%setup -q -n libgnometsol-%{libgnometsol_version}

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

./configure --with-gnome-prefix=%{_prefix} \
            --prefix=%{_prefix}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgnometsol.la
rm $RPM_BUILD_ROOT%{_libdir}/libgnometsol.a
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgnometsol.so*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%files devel
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/pkgconfig

%changelog
* Fri May 16 2008 - stephen.browne@sun.com
- Uprev version, remove upstream patch, remove conditional build

* Thu May 08 2008 - takao.fujiwara@sun.com
- Add SUNWtgnome-tsol-libs-01-po.diff for cs.po
  Contributed l10n from Hana Zalska <Hana.Zalska@sun.com>

* Tue Mar 25 2008 - takao.fujiwara@sun.com
- remove upstreamed scripts.

* Fri Mar 14 2008 - stephen.browne@sun.com
- update version. point source at dlc.sun.com

* Fri Sep 15 2006 - takao.fujiwara@sun.com
- Add *-10n package.

* Sun Jul 30 2006 - damien.carbery@sun.com
- Always use nightly tarballs as source.

* Wed Jul 19 2006 - damien.carbery@sun.com
- Update Build/BuildRequires after check-deps.pl run.

* Tue Jul 11 2006 - damien.carbery@sun.com
- Add autogen.sh commands to %prep to permit building from 'cvs co' tarballs.

* Fri Jun 30 2006 - <stephen.browne@sun.com>
- changed version to default for port to vermillion

* Tue Feb 14 2006 - <ghee.teo@sun.com>
- Added Build/BuildRequires for SUNWgnome-base-libs/-devel.

* Mon Feb 13 2006 - <ghee.teo@sun.com>
- Added Build/BuildRequires for SUNWxwts

* Thu Aug 25 2005 - <stephen.browne@sun.com>
- created 
