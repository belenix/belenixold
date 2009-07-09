#
# spec file for package gtk-doc
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#

%define pythonver 2.6

Name:			gtk-doc
License:		GPL
Group:			Utilities/Text
BuildArchitectures:	noarch
Version:		1.11
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		GTK+ DocBook Documentation Generator
Source:			http://ftp.gnome.org/pub/GNOME/sources/gtk-doc/1.11/gtk-doc-%{version}.tar.bz2
# owner:davelam date:2009-03-18 type:bug
Patch1:  gtk-doc-01-cmp-space-escape.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define libxslt_version 1.0.19
%define libxml2_version 2.5.3

BuildRequires: docbook-xsl-stylesheets
Requires: libxml2 >= %{libxml2_version}
Requires: libxslt >= %{libxslt_version}

%description
gtk-doc is a set of perl scripts that generate API reference documention in
DocBook format.  It can extract documentation from source code comments in a
manner similar to java-doc.  It is used to generate the documentation for
GLib, Gtk+, and GNOME.

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
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"
export PYTHON=/usr/bin/python%{pythonver}
./configure $MYARCH_FLAGS --prefix=%{_prefix}		\
                          --disable-scrollkeeper        \
                	  --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
for f in `find . -name '*.omf' -print`; do
    echo Creating $f.out
    loc=`echo $f | sed -e 's/.*-\([a-zA-Z_]*\).omf/\1/'`
    sed -e 's,url=",url="file://%{_datadir}/gnome/help/gtk-doc-manual/'${loc}'/,' $f > $f.out
done

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/gtk-doc/*
%{_datadir}/aclocal/*
%{_datadir}/sgml/*
%{_libdir}/pkgconfig/*

%changelog
* Wed mar 18 2009 - dave.lin@sun.com
- Add patch 01-cmp-space-escape.diff to handle the file name that contains space.
* Thu Mar 12 2009 - brian.cameron@sun.com
- Change pythonver from 2.5 to 2.6.
* Fri Dec  5 2008 - laca@sun.com
- delete old scrollkeeper hack and disable scrollkeeper install properly
* Thu Dec 04 2008 - dave.lin@sun.com
- Bump to 1.11
* Mon Mar 31 2008 - patrick.ale@gmail.com
- Change download directory to 1.10
* Sun Mar 23 2008 - damien.carbery@sun.com
- Bump to 1.10.
* Tue Oct  2 2007 - damien.carbery@sun.com
- Bump to 1.9.
* Fri Feb 16 2007 - damien.carbery@sun.com
- Bump to 1.8.
* Sat Sep 16 2006 - laca@sun.com
- set scrollkeeper_config so that docs are always installed
- create .omf.out files using sed since scrollkeeper-preinstall is not
  available yet
* Mon Jul 31 2006 - damien.carbery@sun.com
- Bump to 1.7.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Specify ACLOCAL_FLAGS for use on Solaris to find a pkgconfig macro.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 1.6.
* Tue Mar  7 2006 - damien.carbery@sun.com
- Bump to 1.5.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 1.3
* Tue Aug 24 2004 - ghee.teo@sun.com
- Added BuildRequires with docbook-xsl-stylesheets.
  so that this can be detected even at -bp state.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Feb 23 2004 - matt.keenan@sun.com
- Back up to 1.1 as 1.2 DTD XML is causing build failures... DANG
* Mon Dec 15 2003 - glynn.foster@sun.com
- Add the m4 macro to installation
* Sat Oct 04 2003 - laca@sun.com
- upgrade to 1.1
* Thu May 12 2003 - ghee.teo@Sun.COM
- Created new spec file for gtk-doc
