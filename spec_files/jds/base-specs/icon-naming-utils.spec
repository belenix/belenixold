#
# spec file for package icon-naming-utils
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
# bugdb: bugs.freedesktop.org
#
Name:         		icon-naming-utils
License:      		GPL
Group:        		System/GUI/GNOME
BuildArchitectures:	noarch
Version:      		0.8.90
Release:      		1
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		Icon naming utils
Source:       		http://tango.freedesktop.org/releases/%name-%version.tar.bz2
# date:2006-09-19 owner:erwannc type:feature
# FIXME: upstreamable?
Patch1:                 icon-naming-utils-01-extra-file.diff
URL:          		http://tango.freedesktop.org/
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Docdir:	      		%{_defaultdocdir}/doc
Autoreqprov:  		on

BuildRequires:		intltool
BuildRequires:		glib2
BuildRequires:		automake >= 1.9
BuildRequires:		perl-XML-Simple

%description
Icon naming utilities provide a set of scripts for dealing with icon
themes.

%prep
%setup -q
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
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --libexecdir=%{_libexecdir}	\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_datadir}/dtds
%{_datadir}/icon-naming-utils
%{_datadir}/pkgconfig/icon-naming-utils.pc
%{_libexecdir}/*

%changelog
* Thu Mar 26 2009 - brian.cameron@sun.com
- Bump to 0.8.90.
* Tue Aug 05 2007 - damien.carbery@sun.com
- Bump to 0.8.7.
* Tue Jul 03 2007 - damien.carbery@sun.com
- Bump to 0.8.6. Remove upstream patch, 02-uninstalled.
* Wed Mar 07 2007 - damien.carbery@sun.com
- Add patch, 02-uninstalled, to add support for uninstalled.pc file. Will help
  resolve #9837. Changes to SUNWgnome-themes to follow.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 0.8.2. Remove upstream patch, 01-mapping-dir. Renumber rest.
* Wed Aug 23 2006 - damien.carbery@sun.com
- Bump to 0.8.1.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 0.8.0.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 0.7.3.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 0.7.2.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 0.7.0.
* Thu Feb  9 2006 - damien.carbery@sun.com
- Bump to 0.6.8.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.6.5.
* Fri Jan 06 2006 - damien.carbery@sun.com
- Specify libexec dir in configure to put icon-name-mapping in right dir.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 0.6.2.
* Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 0.3.2.
* Sat Oct 15 2005 - laca@sun.com
- created
