#
# spec file for package SUNWlibunique
#
# includes module(s): libunique
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libunique_64 = libunique.spec
%endif

%include base.inc
%use libunique = libunique.spec

Name:           SUNWlibunique
Summary:        libunique - library for writing single instance applications
Version:        %{libunique.version}
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:       SUNWdbus-glib
Requires:       SUNWgnome-base-libs
Requires:       SUNWxwplt
BuildRequires:  SUNWdbus-glib-devel
BuildRequires:  SUNWgnome-base-libs-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %name

%prep
rm -rf %name-%version
mkdir -p %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%libunique_64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%libunique.prep -d %name-%version/%{base_arch}

%build

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
export CFLAGS="%optflags64"
export RPM_OPT_FLAGS="$CFLAGS"
%libunique_64.build -d %name-%version/%{_arch64}
%endif

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%libunique.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libunique_64.install -d %name-%version/%{_arch64}
%endif

%libunique.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/libunique-%{libunique.version} README AUTHORS NEWS
%doc(bzip2) -d %{base_arch}/libunique-%{libunique.version} COPYING ChangeLog po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libunique*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libunique*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Mon Feb 16 2009 - halton.huo@sun.com
- Add 64-bit support
* Sat Jan 24 2009 - halton.huo@sun.com
- Spilit unique.spec for possible 64-bit build
- Move .h and pkgconfig and gtk-doc into -devel package
 Thu Jan 08 2009 - christian.kelly@sun.com
- Initial spec
