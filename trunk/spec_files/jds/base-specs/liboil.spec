#
# spec file for package liboil
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
#####################################
##   Package Information Section   ##
#####################################

Name:			liboil
License:		BSD, MIT, Motorola
Group:			System/Libraries
Version:		0.3.16
Release:	 	1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		The GNOME Structured File Library
Source:			http://liboil.freedesktop.org/download/%{name}-%version.tar.gz
URL:			http://liboil.freedesktop.org/wiki/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

#####################################
##     Package Defines Section     ##
#####################################

%define			glib2_version	2.6.0
%define			zlib_version	1.2.1
%define			libxml2_version	2.6.7
%define			bzip2_version	1.0.2
%define			libbonobo_version	2.6.0
%define			gnome_vfs_version	2.6.0

#####################################
##  Package Requirements Section   ##
#####################################

Requires:		glib2	>=	%{glib2_version}
Requires:		libxml2	>=	%{libxml2_version}
BuildRequires:		glib2-devel >= %{glib2_version}
BuildRequires:		libxml2-devel	>=	%{libxml2_version}

#####################################
##   Package Description Section   ##
#####################################

%description
liboil is a library of simple functions, generally loops, that are optimized
for various CPU's.  These functions are typically used by media applications
to improve performance.

#####################################
##   Package Development Section   ##
#####################################

%package devel
Summary:		liboil development headers
Group:			Development/Libraries
Requires:		%{name} = %{version}
Requires:		glib2-devel >= %{glib2_version}
Requires:		libxml2-devel	>=	%{libxml2_version}
Requires:		zlib-devel	>=	%{zlib_version}
Requires:		bzip2	>=	%{bzip2_version}
Requires:		libbonobo-devel	>=	%{libbonobo_version}
Requires:		gnome-vfs-devel	>=	%{gnome_vfs_version}

%description devel
liboil development headers

#####################################
##   Package Preparation Section   ##
#####################################

%prep
%setup -q

#####################################
##      Package Build Section      ##
#####################################


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

aclocal $ACLOCAL_FLAGS -I ./m4
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --libdir=%{_libdir}			\
            --includedir=%{_includedir}         \
	    --sysconfdir=%{_sysconfdir}		\
	    %{gtk_doc_option}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

#########################################
##  Package Post[Un] Install Section   ##
#########################################

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

#####################################
##      Package Files Section      ##
#####################################

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/*

%changelog
* Thu Mar 26 2009 - brian.cameron@sun.com
- Bump to 0.3.16.
* Fri Sep 12 2008 - brian.cameron@sun.com
- Bump to 0.3.15.
* Wed Mar 26 2008 - brian.cameron@sun.com
- Bump to 0.3.14.
* Wed Feb 27 2008 - brian.cameron@sun.com
- Add patch liboil-02-fixcopy.diff to fix bug 14643.
* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump to 0.3.13 and remove upstream patch.
* Fri Jun 08 2007 - brian.cameron@sun.com
- Bump to 0.3.12 and remove upstream patch.
* Fri Feb 09 2007 - brian.cameron@sun.com
- Add patch to support hardware acelleration detection on x86 when
  building with GCC.  Also add bugdb info.
* Thu Nov 30 2006 - damien.carbery@sun.com
- Bump to 0.3.10.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Jun 14 2006 - brian.cameron@sun.com
- Bump to 0.3.9.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.3.6.
* Wed Jul 27 2005 - brian.cameron@sun.com
- Created.
