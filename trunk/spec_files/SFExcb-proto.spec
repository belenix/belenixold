#
# spec file for package SFExcb-proto
#
# includes module(s): xcb-proto
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define _python_ver      2.5
%define _orig_ver        1.2
Name:                    SFExcb-proto
Summary:                 XML-XCB protocol descriptions that libxcb uses to generate the majority of its code and API.
Version:                 1.5-%{_orig_ver}
Source:                  http://xcb.freedesktop.org/dist/xcb-proto-1.2.tar.gz
URL:                     http://xcb.freedesktop.org/
License:                 MIT_X11

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWxorg-clientlibs
Requires:               SUNWxwplt
BuildRequires:          SUNWxorg-clientlibs
BuildRequires:          SUNWxorg-headers
BuildRequires:          FSWxorg-headers

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring
a small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp xcb-proto-%{_orig_ver} xcb-proto-%{_orig_ver}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PYTHON=%{_prefix}/bin/python%{_python_ver}

%ifarch amd64 sparcv9
cd xcb-proto-%{_orig_ver}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd xcb-proto-%{_orig_ver}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd xcb-proto-%{_orig_ver}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd xcb-proto-%{_orig_ver}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

mv ${RPM_BUILD_ROOT}%{_libdir}/python%{_python_ver}/site-packages \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{_python_ver}/vendor-packages


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/xcb
%{_datadir}/xcb/randr.xml
%{_datadir}/xcb/bigreq.xml
%{_datadir}/xcb/composite.xml
%{_datadir}/xcb/xinput.xml
%{_datadir}/xcb/glx.xml
%{_datadir}/xcb/xf86dri.xml
%{_datadir}/xcb/shm.xml
%{_datadir}/xcb/xinerama.xml
%{_datadir}/xcb/xselinux.xml
%{_datadir}/xcb/record.xml
%{_datadir}/xcb/sync.xml
%{_datadir}/xcb/xv.xml
%{_datadir}/xcb/screensaver.xml
%{_datadir}/xcb/xc_misc.xml
%{_datadir}/xcb/xevie.xml
%{_datadir}/xcb/damage.xml
%{_datadir}/xcb/xcb.xsd
%{_datadir}/xcb/shape.xml
%{_datadir}/xcb/render.xml
%{_datadir}/xcb/xproto.xml
%{_datadir}/xcb/xtest.xml
%{_datadir}/xcb/xprint.xml
%{_datadir}/xcb/res.xml
%{_datadir}/xcb/dpms.xml
%{_datadir}/xcb/xfixes.xml
%{_datadir}/xcb/xvmc.xml

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.5
%dir %attr (0755, root, bin) %{_libdir}/python2.5/vendor-packages
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/__init__.pyo
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/matcher.pyo
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/expr.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/xtypes.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/error.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/__init__.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/state.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/error.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/state.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/__init__.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/matcher.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/matcher.pyc
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/expr.pyo
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/xtypes.pyo
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/xtypes.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/error.pyo
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/expr.py
%{_libdir}/python%{_python_ver}/vendor-packages/xcbgen/state.pyo

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Downgrade version to support older Xorg in OpenSolaris.
* Sun Apr 17 2009 - moinakg@belenix.org
- Initial version
