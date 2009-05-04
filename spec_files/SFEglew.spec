#
# spec file for package SFEglew
#
# includes module(s): glew
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEglew
Summary:                 The OpenGL Extension Wrangler Library
Version:                 1.5.1
Source:                  http://nchc.dl.sourceforge.net/sourceforge/glew/glew-%{version}-src.tgz
Source1:                 glew-01-Makefile.solaris
Source2:                 glew-01-Makefile.solaris.64
Patch1:                  glew-02-Makefile.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxorg-mesa
Requires: SFEgccruntime

%prep
%setup -q -c -n %name-%version
%if %cc_is_gcc
%else
%error "This spec file need GCC4 please set the CC and CXX variables."
%endif
cd glew
cp Makefile Makefile.orig
cp config/config.guess config/config.guess.orig
cat Makefile.orig | sed 's///' > Makefile
cat config/config.guess.orig | sed 's///' > config/config.guess
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp glew glew-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd glew-64
cp %{SOURCE2} config/Makefile.solaris
make -j$CPUS ARCH64=%{_arch64} CC="${CC} -m64"
cd ..
%endif

cd glew
cp %{SOURCE1} config/Makefile.solaris
make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{base_isa}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11/include

%ifarch amd64 sparcv9
cd glew-64
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{_arch64}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11/lib/%{_arch64}
make install DESTDIR=$RPM_BUILD_ROOT ARCH64=%{_arch64} CC="${CC} -m64"
rm -f ${RPM_BUILD_ROOT}/*.a
mv ${RPM_BUILD_ROOT}/lib*.so* ${RPM_BUILD_ROOT}%{_prefix}/X11/lib/%{_arch64}
mv ${RPM_BUILD_ROOT}/glewinfo ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{_arch64}
mv ${RPM_BUILD_ROOT}/visualinfo ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{_arch64}
(cd ${RPM_BUILD_ROOT}%{_prefix}/X11/lib/%{_arch64}
    for lib in *.so; do
        ln -s ${lib} ${lib}.1
    done)
cd ..
%endif

cd glew
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}/*.a
mv ${RPM_BUILD_ROOT}/lib*.so* ${RPM_BUILD_ROOT}%{_prefix}/X11/lib
mv ${RPM_BUILD_ROOT}/glewinfo ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{base_isa}
mv ${RPM_BUILD_ROOT}/visualinfo ${RPM_BUILD_ROOT}%{_prefix}/X11/bin/%{base_isa}
mv ${RPM_BUILD_ROOT}/GL ${RPM_BUILD_ROOT}%{_prefix}/X11/include
(cd ${RPM_BUILD_ROOT}%{_prefix}/X11/lib
    for lib in *.so; do
        ln -s ${lib} ${lib}.1
    done)
(cd ${RPM_BUILD_ROOT}%{_prefix}/X11/bin
    ln -sf ../../lib/isaexec glewinfo
    ln -sf ../../lib/isaexec visualinfo)
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/bin
%hard %{_prefix}/X11/bin/visualinfo
%hard %{_prefix}/X11/bin/glewinfo
%dir %attr (0755, root, bin) %{_prefix}/X11/bin/%{base_isa}
%{_prefix}/X11/bin/%{base_isa}/visualinfo
%{_prefix}/X11/bin/%{base_isa}/glewinfo
%dir %attr (0755, root, bin) %{_prefix}/X11/lib
%{_prefix}/X11/lib/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_prefix}/X11/bin/%{_arch64}
%{_prefix}/X11/bin/%{_arch64}/visualinfo
%{_prefix}/X11/bin/%{_arch64}/glewinfo
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/%{_arch64}
%{_prefix}/X11/lib/%{_arch64}/*.so*
%endif

%dir %attr (0755, root, bin) %{_prefix}/X11/include
%dir %attr (0755, root, bin) %{_prefix}/X11/include/GL
%{_prefix}/X11/include/GL/*

%changelog
* Mon May 04 2009 - moinakg@belenix.org
- Initial version.
