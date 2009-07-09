#
# spec file for package SUNWgtk-vnc
#
# includes module(s): gtk-vnc
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
%define with_64 1
%define with_brower_plugin 0
%define pythonver 2.4
%use gvnc_64 = gtk-vnc.spec
%define pythonver 2.6
%use gvnc_64_py26 = gtk-vnc.spec
%endif

%include base.inc
%define with_64 0
%define with_brower_plugin 1
%define pythonver 2.4
%use gvnc = gtk-vnc.spec
%define pythonver 2.6
%use gvnc_py26 = gtk-vnc.spec

Name:               SUNWgtk-vnc
Summary:            gtk-vnc - A GTK widget for VNC clients
Version:            %{gvnc.version}
SUNW_Copyright:     %{name}.copyright
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
Source1:            %{name}-manpages-0.1.tar.gz

%include default-depend.inc
Requires:      SUNWgnome-base-libs
Requires:      SUNWgnutls
Requires:      SUNWxwplt
Requires:      SUNWzlibr
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnutls-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}
Requires:      SUNWgnome-base-libs-devel
Requires:      SUNWgnutls-devel

%package python24
Summary:       %{summary} - Python 2.4 binding files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}
Requires:      SUNWPython
Requires:      SUNWgnome-python-libs
BuildRequires: SUNWPython-devel
BuildRequires: SUNWpython-setuptools
BuildRequires: SUNWgnome-python-libs-devel

%package python26
Summary:       %{summary} - Python 2.6 binding files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}
Requires:      SUNWPython26
Requires:      SUNWgnome-python26-libs
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWpython26-setuptools
BuildRequires: SUNWgnome-python26-libs-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%gvnc_64.prep -d %name-%version/%{_arch64}
mkdir %name-%version/%{_arch64}-py26
%gvnc_64_py26.prep -d %name-%version/%{_arch64}-py26
%endif

mkdir %name-%version/%{base_arch}
%gvnc.prep -d %name-%version/%{base_arch}
mkdir %name-%version/%{base_arch}-py26
%gvnc_py26.prep -d %name-%version/%{base_arch}-py26

cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
export CFLAGS="%optflags64"
export RPM_OPT_FLAGS="$CFLAGS"

export NSPR_CFLAGS="-I/usr/include/mps"
export NSPR_LIBS="-L/usr/lib/mps/%{_arch64} -R/usr/lib/mps/%{_arch64}"

%gvnc_64.build -d %name-%version/%{_arch64}
%gvnc_64_py26.build -d %name-%version/%{_arch64}-py26
%endif

export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"

export NSPR_CFLAGS="-I/usr/include/mps"
export NSPR_LIBS="-L/usr/lib/mps -R/usr/lib/mps"

%gvnc.build -d %name-%version/%{base_arch}
%gvnc_py26.build -d %name-%version/%{base_arch}-py26

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%gvnc_64.install -d %name-%version/%{_arch64}
%gvnc_64_py26.install -d %name-%version/%{_arch64}-py26
%endif

%gvnc.install -d %name-%version/%{base_arch}
%gvnc_py26.install -d %name-%version/%{base_arch}-py26

# rename plugin dir to firefox
cd $RPM_BUILD_ROOT%{_libdir}
mv mozilla firefox

# remove empty bindir, refer to bugzilla #560112
rmdir $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
rmdir $RPM_BUILD_ROOT%{_bindir}

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/gtk-vnc-%{gvnc.version} README AUTHORS
%doc(bzip2) -d %{base_arch}/gtk-vnc-%{gvnc.version} COPYING.LIB ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_libdir}/firefox/plugins
%{_libdir}/firefox/plugins/gtk-vnc-plugin.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

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

%files python24
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/vendor-packages
%{_libdir}/python2.4/vendor-packages/gtkvnc.so
%dir %attr (0755, root, bin) %{_libdir}/python2.4/vendor-packages/64
%{_libdir}/python2.4/vendor-packages/64/gtkvnc.so

%files python26
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.6
%dir %attr (0755, root, bin) %{_libdir}/python2.6/vendor-packages
%{_libdir}/python2.6/vendor-packages/gtkvnc.so
%dir %attr (0755, root, bin) %{_libdir}/python2.6/vendor-packages/64
%{_libdir}/python2.6/vendor-packages/64/gtkvnc.so

%changelog
* Tue Mar 24 2009 - jeff.cai@sun.com
- Since /usr/lib/amd64/pkgconfig/gtk-vnc-1.0.pc (SUNWgtk-vnc-devel) requires
  /usr/lib/amd64/pkgconfig/gtk+-2.0.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
- Since /usr/lib/amd64/pkgconfig/gtk-vnc-1.0.pc (SUNWgtk-vnc-devel) requires
  /usr/lib/amd64/pkgconfig/gnutls.pc which is found in SUNWgnutls-devel,
  add the dependency.
* Wed Mar 18 2009 - halton.huo@sun.com
- Remove -python25 pkg
* Thu Feb 19 2009 - halton.huo@sun.com
- Add -python26 pkg
* Mon Dec 22 2008 - halton.huo@sun.com
- update deps after run check-deps.pl
* Wed Nov 26 2008 - halton.huo@sun.com
- Add -python25 pkg
- Add 64-bit gtkvnc python moudle
* Thu Nov 20 2008 - halton.huo@sun.com
- Remove -l10n pkg
* Thu Nov 13 2008 - halton.huo@sun.com
- Moved from SFE
- Enable 64-bit build
- Add package -python24
* Tue May 06 2008 - nonsea@users.sourceforge.net
- Remove ast stuff.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Initial spec
