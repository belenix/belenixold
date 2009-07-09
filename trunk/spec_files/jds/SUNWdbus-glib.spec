#
# spec file for package SUNWdbus-glib
#
# includes module(s): dbus-glib
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use dbus_glib_64   = dbus-glib.spec
%define _libdir %{_basedir}/lib
%endif

%include base.inc
%use dbus_glib   = dbus-glib.spec

Name:                    SUNWdbus-glib
Summary:                 D-Bus GLib bindings
Version:                 %{dbus_glib.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWdbus
Requires:	SUNWgnome-base-libs
Requires:	SUNWlxml
Requires:       SUNWlexpt
BuildRequires:	SUNWdbus-devel
BuildRequires:	SUNWgnome-base-libs-devel
BuildRequires:	SUNWlxml
BuildRequires:  SUNWsfwhea

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:       SUNWgnome-base-libs

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%dbus_glib_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%dbus_glib.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
%if %cc_is_gcc
export EXTRA_CFLAGS="-I/usr/sfw/include"
%else
export EXTRA_CFLAGS="-xc99 -D_REENTRANT -I/usr/sfw/include -D__EXTENSIONS__"
%endif
# Put /usr/ccs/lib first in the PATH so that cpp is picked up from there
# note: I didn't put /usr/lib in the PATH because there's too much other
# stuff in there
#
export PATH=/usr/ccs/lib:$PATH

%ifarch amd64 sparcv9
export EXTRA_LDFLAGS="-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64} -lexpat"
export PKG_CONFIG_PATH=../dbus-glib-%{dbus_glib.version}:/usr/lib/%{_arch64}/pkgconfig
%dbus_glib_64.build -d %name-%version/%_arch64
%endif

export PKG_CONFIG_PATH=../dbus-glib-%{dbus_glib.version}
export EXTRA_LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib -lexpat"
%dbus_glib.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%dbus_glib_64.install -d %name-%version/%_arch64
%endif

%dbus_glib.install -d %name-%version/%{base_arch}

# Remove dbus-bash-completion.sh, a bash autocompletion script in the
# %{_sysconfdir}/profile.d dir. We don't ship such files. It is the only file
# under %{_sysconfdir} so remove the entire structure.
# rm/rmdir used instead of 'rm -r' so that files added under %{_sysconfdir} are
# found, via build failure.
rm $RPM_BUILD_ROOT%{_libexecdir}/dbus-bash-completion-helper
%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_libexecdir}/%{_arch64}/dbus-bash-completion-helper
%endif
rm $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
rmdir $RPM_BUILD_ROOT%{_sysconfdir}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1
%doc %{base_arch}/dbus-glib-%{dbus_glib.version}/AUTHORS
%doc %{base_arch}/dbus-glib-%{dbus_glib.version}/README
%doc(bzip2) %{base_arch}/dbus-glib-%{dbus_glib.version}/COPYING
%doc(bzip2) %{base_arch}/dbus-glib-%{dbus_glib.version}/ChangeLog
%doc(bzip2) %{base_arch}/dbus-glib-%{dbus_glib.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/gtk-doc
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Tue Mar 10 2009 - brian.cameron@sun.com
- Cleanup based on code review.
* Thu Mar 05 2009 - brian.cameron@sun.com
- Split from SUNWdbus-bindings.spec.
* Wed Mar 04 2009 - dave.lin@sun.com
- Add /usr/share/man/man1 in %files
* Sun Sep 14 2008 - brian.cameron@sun.com
- Add new copyright files.
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright
* Tue Nov 20 2007 - brian.cameron@sun.com
- Add libdbus-glib-1.3 manpage.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
- delete SUNWxwrtl dep
* Sat Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
* Fri Jan 26 2007 - damien.carbery@sun.com
- Set PKG_CONFIG vars in %build because dbus-python use autofoo/configure/make
  process rather than setup.py.
* Thu Jan 25 2007 - damien.carbery@sun.com
- Add %{_datadir}/doc to devel pkg, because of new dbus-python tarball.
* Thu Dec 21 2006 - brian.cameron@sun.com
- Remove references to SUNWdbus-bindings-root since we do not
  build this package.
* Thu Sep 21 2006 - brian.cameron@sun.com
- Created.

