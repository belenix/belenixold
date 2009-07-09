#
# spec file for package shared-mime-info
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
# bugdb: bugzilla.freedesktop.org
#
Name:         shared-mime-info
License:      GPL
Group:        Hardware/Other
Version:      0.51
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Core Common Mime Type Database
#Source:       http://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.bz2
Source:       http://freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
Source1:      defaults.list
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
URL:          http://www.freedesktop.org/Software/%{name}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
DocDir:       %{_defaultdocdir}/%{name}

BuildRequires: glib2

%description
shared-mime-info contains the core database of common types and the
update-mime-database command used to extend it.

%prep
%setup -q

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

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make -j $CPUS

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
make DESTDIR=$RPM_BUILD_ROOT install-strip
install --mode=0644 %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/applications/defaults.list
install -d $RPM_BUILD_ROOT%{_datadir}/application-registry

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%post
update-mime-database %{_datadir}/mime

%files
%defattr(-,root,root)
%{_bindir}/update-mime-database
%{_datadir}/locale/*/LC_MESSAGES/shared-mime-info.mo
# No point in making a seperate devel pkg just for one silly pkgconfig file
%{_libdir}/pkgconfig/*.pc
%{_datadir}/mime/*
%{_datadir}/applications/defaults.list
%{_mandir}/man1/*
%{_datadir}/application-registry

%changelog
* Thu Aug 21 2008 - jijun.yu@sun.com
- Bump to 0.51.

* Fri Jun 13 2008 - damien.carbery@sun.com
- Bump to 0.40.

* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize calls to update intltool scripts.

* Wed Aug 22 2007 - damien.carbery@sun.com
- Bump to 0.22. Remove both patches as they are upstream.

* Tue Jun 26 2007 - matt.keenan@sun.com
- Split add-mime-types patch into two patches to facilitate pushing upstream

* Thu Mar 15 2007 - damien.carbery@sun.com
- Bump to 0.20.

* Fri Dec 01 2006 - damien.carbery@sun.com
- Bump to 0.19. Remove upstream patch 02-java-types.

* Mon Jul 03 2006 - damien.carbery@sun.com
- Bump to 0.18

* Thu May 11 2006 - glynn.foster@sun.com
- Add Java types from Joe.

* Tue Apr 11 2006 - glynn.foster@sun.com
- Bump to 0.17

* Tue Apr 11 2006 - glynn.foster@sun.com
- Add shared-mime-info-02-fix-m3u.diff to keep Bart happy.

* Thu Dec 09 2005 - archana.shah@wipro.com
- Modified patch shared-mime-info-01-add-mime-types.diff to include mime type 
  for speex file.

* Thu Dec 08 2005 - damien.carbery@sun.com
- Remove l10n tarball. Not maintained in OpenSolaris releases.

* Fri Dec 02 2005 - archana.shah@wipro.com
- Added javaws in defaults.list as the default application for the .jnlp files. Fixes bug #6351401

* Thu Jul 21 2005 - archana.shah@wipro.com
- Added defaults.list file in the package. It provides the defaults application 
  handler for all mime types. 

* Tue Jun 21 2005 - dermot.mccluskey@sun.com
- 6285970: create /usr/share/application-registry for RealPlayer

* Thu Jun 16 2005 - matt.keenan@wipro.com
- Bump to 0.16, re-align patches

* Fri Apr 08 2005 - vinay.mandyakoppal@wipro.com
- Added shared-mime-info-05-add-magic.diff to provide mime magic for
  staroffice and opendocuments file types. Fixes #6234855.

* Thu Mar 31 2005 - glynn.foster@sun.com
- Add some more media types to get things working.

* Thu Jan 27 2005 - dinoop.thomas@wipro.com
- Added shared-mime-info-04-mime-type-mrproject.diff patch to 
  associate the application planner for .mrproject files. 
  Fixes bug #6217022.
 
* Fri Nov 05 2004 - vinay.mandyakoppal@wipro.com
- Added shared-mime-info-03-mime-type-staroffice-capital.diff to associate  
  correct mime type for staroffice applications extension in capitals.
  Fixes bug #5097261.

* Thu Oct 28 2004 - matt.keenan@sun.com
- Add update-mime-database.1 man page

* Wed Sep 15 2004 - ciaran.mcdermott@sun.com
- Added shared-mime-info-02-g11n-alllinguas.diff, to update support for all linguas

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to shared-mime-info-l10n-po-1.2.tar.bz2

* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to shared-mime-info-l10n-po-1.1.tar.bz2

* Mon Apr 5 2004 - glynn.foster@sun.com
- Bump to 0.14.

* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding shared-mime-info-l10n-po-1.0.tar.bz2 l10n content

* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added shared-mime-info-01-g11n-potfiles.diff

* Tue Mar 02 2004 - niall.power@sun.com
- remove "-n gtkam" from changelog tag
- add ACLOCAL_FLAGS to aclocal args

* Mon Feb 23 2004 - matt.keenan@sun.com
- Update Distro

* Mon Feb 02 2004 - matt.keenan@sun.com
- Initial version
