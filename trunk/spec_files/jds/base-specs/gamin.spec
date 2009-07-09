#
# spec file for package SUNWgamin, SUNWgamin-devel
#
# includes module(s): gamin
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: lin
#

Name:		gamin
Summary:	Library providing the FAM File Alteration Monitor API
URL:		http://www.gnome.org/~veillard/gamin/
Version:	0.1.10
Source0:	http://www.gnome.org/~veillard/gamin/sources/%{name}-%{version}.tar.bz2
# owner:lin date:2007-12-05 type:feature bugzilla:491319
Patch1:		gamin-01-all.diff
License:	LGPL

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal
autoconf --force
automake -a -c -f

config=./configure

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
$config	--prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
#
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Nov 25 2008 - dave.lin@sun.com
- Bump to 0.1.10
* Wed Dec 05 2007 - lin.ma@sun.com
- Changed the type of gamin patch 01 to feature.
* Sat Oct 13 2007 - lin.ma@sun.com
- Initial FEN backend
* Sun Apr 14 2007 - dougs@truemail.co.th
- Initial version
