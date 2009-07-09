#
# spec file for package libcroco
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
#####################################
##   Package Information Section   ##
#####################################

Name:			libcroco
License:		LGPL v2
Group:			System/Libraries
Version:		0.6.2
Release:	 	1	
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Cascading Style Sheet (CSS) parsing and manipulation toolkit
Source:			http://ftp.gnome.org/pub/GNOME/sources/libcroco/0.6/%{name}-%{version}.tar.bz2
URL:			http://www.freespiders.org/projects/libcroco/index.html
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
libcroco project aims to build a generic Cascading Style Sheet (CSS) 
parsing and manipulation toolkit.

#####################################
##   Package Development Section   ##
#####################################

%package devel
Summary:		libcroco development headers
Group:			Development/Libraries
Requires:		%{name} = %{version}
Requires:		glib2-devel >= %{glib2_version}
Requires:		libxml2-devel	>=	%{libxml2_version}
Requires:		zlib-devel	>=	%{zlib_version}
Requires:		bzip2	>=	%{bzip2_version}
Requires:		libbonobo-devel	>=	%{libbonobo_version}
Requires:		gnome-vfs-devel	>=	%{gnome_vfs_version}

%description devel
libcroco development headers

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

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --libdir=%{_libdir}			\
	    --includedir=%{_includedir}		\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

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
%{_bindir}
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 0.6.2
- Removed upstreamed patch 01-fixheader.diff.
* Thu Aug 21 2008 - laca@sun.com
- set env variable needed for 64-bit build
* Tue Feb 19 2008 - brian.cameron@sun.com
- Add patch libcroco-01-fixheader.diff to fix bug 6549227.
* Mon Mar  6 2006 - damien.carbery@sun.com
- Bump to 0.6.1.
* Fri Feb 24 2006 - damien.carbery@sun.com
- Update URL and Summary.
* Wed Jul 27 2005 - brian.cameron@sun.com
 - Created.
