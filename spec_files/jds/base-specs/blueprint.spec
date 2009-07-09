#
# spec file for package blueprint
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         blueprint
Summary:      Engine for GTK2 Blue Print Theme
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%ifos solaris
Version:      0.9.20
%define tarball_version %{version}
%else
Version:      0.9.16
%define tarball_version %{version}-os
%endif
Release:      41 
License:      LGPL
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Group:        System/GUI/GNOME
Source:       http://dlc.sun.com/osol/jds/downloads/extras/%{name}-%{tarball_version}.tar.bz2
Source1:      l10n-configure.sh
#owner:fujiwara date:2009-04-10 type:bug bugster:6675046
Patch1:       blueprint-01-rtl-icons.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://www.sun.com/software/javadesktopsystem/

%define gtk2_version 2.4.0
%define intltool_version 0.30
BuildRequires: gtk2 >= %{gtk2_version}
BuildRequires: intltool >= %{intltool_version}

%description
This package contains the Blueprint theme engine for GTK2

%prep
%setup -q -n %name-%tarball_version
%patch1 -p1

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

libtoolize --force
intltoolize --force --copy --automake

bash -x %SOURCE1 --enable-copyright

aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}   \
	    --libdir=%{_libdir}  \
	    --sysconfdir=%{_sysconfdir} 
make -j $CPUS
cd -

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/blueprint-engine
cp -p AUTHORS COPYING ChangeLog NEWS README $RPM_BUILD_ROOT%{_defaultdocdir}/blueprint-engine

# Hack to install images into %{_datadir}/pixmaps with blueprint prefix
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p /tmp/blueprint-pixmaps
installfiles=`find icons/48x48 -name "*.png"`				
for i in $installfiles; do						
  echo -- Installing $i to %{_datadir}/pixmaps with blueprint- prefix ;
  i_base=`basename $i`
  cp $i $RPM_BUILD_ROOT%{_datadir}/pixmaps/blueprint-${i_base}
done;                                           			

rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_defaultdocdir}/blueprint-engine/ChangeLog
%{_defaultdocdir}/blueprint-engine/AUTHORS
%{_defaultdocdir}/blueprint-engine/COPYING
%{_defaultdocdir}/blueprint-engine/README
%{_defaultdocdir}/blueprint-engine/NEWS
%{_libdir}/gtk-2.0/*/engines/*.so
%{_datadir}/themes/*
%{_datadir}/icons/*
%{_datadir}/locale/*
%{_datadir}/pixmaps/*

%changelog
* Fri Apr 10 2009 - takao.fujiwara@sun.com
- Add patch rtl-icons.diff CR 6675046
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize calls to update intltool scripts.
* Fri May 18 2007 - laca@sun.com
- set CFLAGS/LDFLAGS and configure options such that we can use this spec
  file for the 64-bit build too
- write a nicer loop for copying icons with blueprint- prefix
* Fri Jun 23 2006 - brian.cameron@sun.com
- Change "cp -a" to "cp -p" so it works with Solaris cp command.
* Thu Feb 10 2005 - muktha.narayan@wipro.com
- Bumped the tarball to include icons required to fix
  #5088581.
* Mon Jan 31 2005 - takao.fujiwara@sun.com
- Updated %build to stop build error
* Fri Jan 28 2005 - muktha.narayan@wipro.com
- Bumped the tarball which includes the fix for #5088581 and
  merged blueprint-01-g11n-icon.diff in the tarball. 
* Fri Jan 28 2005 - takao.fujiwara@sun.com
- Updated %build to add automake
* Wed Jan 12 2005 - takao.fujiwara@sun.com
- Removed blueprint-01-g11n-alllinguas.diff. Use l10n-configure.sh
- Added blueprint-01-g11n-icon.diff to fix 5083114
* Thu Sep 16 2004 - ciaran.mcdermott@sun.com
- Added blueprint-01-g11n-alllinguas.diff to include cs,hu linguas
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to blueprint-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 2 2004 - glynn.foster@sun.com
- Bump to 0.9.5
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to blueprint-l10n-po-1.1.tar.bz2
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding blueprint-l10n-po-1.0.tar.bz2 l10n content
* Fri Mar 12 2004 Niall Power <niall.power@sun.com>
- remove "rm -rf" evil from the install stage
* Mon Feb 16 2004 Niall Power <niall.power@sun.com>
- add ACLOCAL_FLAGS to aclocal invocation
- do not use the -printf argument with find - it
  doesn't work on Solaris (pipe through sed instead)
* Fri Jan 19 2004 Takao Fujiwara <takao.fujiwara@sun.com>
- Modified blueprint.spec for i18n
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Wed Jul 02 2003 Erwann Chenede - <erwann.chenede@sun.com>
- cleanup + icons theme addition
* Mon May 12 2003 Erwann Chenede - <erwann.chenede@sun.com>
- initial implementation of the spec file

