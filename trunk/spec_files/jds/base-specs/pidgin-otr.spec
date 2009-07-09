#
# spec file for package pidgin-otr
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
# bugdb :
#
Name:		pidgin-otr
Version:	3.2.0
Release:        1
License:	GPL
Group:		Applications/Internet
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Off-the-Record (OTR) Messaging plugin for GAIM
Source0:        http://www.cypherpunks.ca/otr/%{name}-%{version}.tar.gz
# owner:rickju date:2007-03-07 type:bug bugster:6524858 state:upstream
Patch1:         pidgin-otr-01-gtk-ui.diff
URL:		http://www.cypherpunks.ca/otr/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/pidgin
Autoreqprov:	on

BuildRequires:	pidgin-devel

%description
Off-the-Record (OTR) Messaging allows you to have private
conversations over instant messaging.
This is a plugin for pdgin which implements Off-the-Record
Messaging over any IM network pidgin supports. 

%package devel
Summary:      Off-the-Record (OTR) Messaging Plugin For GAIM
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version

%description devel
Off-the-Record (OTR) Messaging allows you to have private
conversations over instant messaging.
This is a plugin for pidgin which implements Off-the-Record
Messaging over any IM network pidgin supports. 

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
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

export CFLAGS="$RPM_OPT_FLAGS -DG_IMPLEMENT_INLINES -DG_HAVE_ISO_VARARGS"
export LD_LIBRARY_PATH="%{_libdir}:$LD_LIBRARY_PATH:$LIBOTR_BLD_DIR/src/.libs"
./configure 				\
	--prefix=%{_prefix} 		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}     \
	--with-libotr-inc-prefix=$LIBOTR_BLD_DIR/my_build_tmp \
	--with-libotr-prefix=$LIBOTR_BLD_DIR/src/.libs
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    SITEPREFIX=/dummy VENDORPREFIX=/dummy PERLPREFIX=/dummy


%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Wed Mar 11 2009 - elaine.xiong@sun.com
- Change ownership to elaine.

* Thu Dec 25 2008 - dave.lin@sun.com
- Remove glib-gettextize line to avoid build issue with intltool 0.40.5.
* Tue Aug 04 2008 - damien.carbery@sun.com
- 'export' CFLAGS AND LD_LIBRARY_PATH to fix build.

* Tue Jul 29 2008 - damien.carbery@sun.com
- Fix syntax in LD_LIBRARY_PATH (remove -L).

* Thu Jul 23 2008 - damien.carbery@sun.com
- Move libotr from pidgin-otr.spec to libotr.spec. This makes is easier to
  track for ARC and Legal reviews.

* Mon Jul 21 2008 - rick.ju@sun.com
- Bump to 3.2.0.

* Tue Nov 06 2007 - rick.ju@sun.com
- bump to libotr 3.1.0 and pidgin-otr 3.1.0

* Tue Jun 01 2007 - rick.ju@sun.com
- fix the source0 url

* Tue May 30 2007 - rick.ju@sun.com
- bump to pidgin-otr 3.0.1

* Tue Apr 03 2007 - rick.ju@sun.com
- Add a gaim-otr-03-gtk-dialog.diff for bug#632728

* Thu Jan 18 2007 - damien.carbery@sun.com
- Remove the code from %install that deletes $RPM_BUILD_ROOT as it trashes the
  'make install' of gaim when part of SUNWgnome-im-client build.

* Thu Dec 21 2006 - damien.carbery@sun.com
- Remove *.a and *.la files in %install.

* Mon Dec 18 2006 - rick.ju@sun.com
- Add this new spec for libotr and gaim-otr
