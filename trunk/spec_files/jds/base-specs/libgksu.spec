#
# spec file for package libgksu
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: lin
#
Name:         libgksu1.2
License:      LGPL v2
Group:        Development/Libraries
Version:      1.3.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Simple API for embedded_su, pfexec and sudo (optional)
Source:       http://people.debian.org/~kov/gksu/old_stuff/libgksu1.2/%{name}-%{version}.tar.gz
# date:2006-10-21 owner:lin type:feature
Patch1:	      libgksu1.2-01-Makefile.diff
# date:2006-10-21 owner:lin type:feature
Patch2:	      libgksu1.2-02-config.diff
# date:2006-10-21 owner:lin type:feature
Patch3:	      libgksu1.2-03-mkdtemp.diff
# date:2006-10-21 owner:lin type:feature
Patch4:	      libgksu1.2-04-rbac-support.diff
# date:2006-10-21 owner:lin type:feature
Patch5:       libgksu1.2-05-gnu_gettext.diff
URL:          http://www.nongnu.org/gksu/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf


BuildRequires: gettext, bison, pkgconfig, glib2-devel, gtk-doc

%description
LibGKSu is a library from the gksu program that provides a simple API for
using su and sudo in programs that need to execute tasks as other users.
It provides X authentication facilities for running programs in a X session.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

glib-gettextize -f
aclocal $ACLOCAL_FLAGS
libtoolize --force
# automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
	--disable-scrollkeeper
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
# rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING INSTALL
%{_libdir}/libgksu*.so.*
%{_libdir}/libgksu*/
%{_datadir}/gtk-doc/html/libgksu*/
%{_datadir}/locale/*/*/libgksu*

%files devel
%defattr(-, root, root)
%{_includedir}/gksu*.h
%{_libdir}/libgksu*.a
%{_libdir}/libgksu*.so
%{_libdir}/pkgconfig/libgksu*pc
# %exclude %{_libdir}/libgksu*.la

%changelog
* Tue Mar 10 2009 - harry.lu@sun.com
- Change owner to Lin Ma
* Thu Sep 18 2008 - li.yuan@sun.com
- Add patch libgksu1.2-06-exit.diff. Quit gksu after launch the child process.
* Sun Jan 28 2007 - laca@sun.com
- fix download url
* Sat Oct 21 2006 Jim Li <jim.li@sun.com>
- reorg all patches
- Put all configure.ac changes into config.diff
- Put all gksu-context.c changes into rbac-support.diff
- remove forkpty.diff since it already exists in rbac-support.diff.
- remove package_name.diff since it already exists in rbac-support.diff.
* Tue Oct 10 2006 damien.carbery@sun.com
- Add patch, 06-package_name, to use PACKAGE_NAME from config.h in as PACKAGE
  is incorrectly expanded by the preprocessor.
* Wed Oct 04 2006 damien.carbery@sun.com
- Add patch, 04-gnu_gettext, to use GNU gettext. Add associated autofoo.
* Thu Sep 28 2006 Darren Kenny <darren.kenny@sun.com>
- Run autoconf since we're patching configure.ac to look for libsecdb
* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.3.7-1.2
- Rebuild for Fedora Core 5.
* Tue Dec 06 2005 Dries Verachtert <dries@ulyssis.org> - 1.3.7-1
- Initial package.
