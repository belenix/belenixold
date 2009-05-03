%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	ctl
Name:                   SFEctl
Summary:                The Color Transformation Language, or CTL, is a programming language for digital color management.
Version:                1.4.1
Source:                 %{sf_download}/ampasctl/%{src_name}-%{version}.tar.gz
Patch1:                 ctl-1-CtlAlign.h.diff
Patch2:                 ctl-2-CtlLContext.cpp.diff
Patch3:                 ctl-3-CtlInterpreter.cpp.diff
Patch4:                 ctl-4-CtlLex.cpp.diff
Patch5:                 ctl-5-CtlSimdReg.h.diff
Patch6:                 ctl-6-CtlSymbolTable.cpp.diff
Patch7:                 ctl-7-CtlType.cpp.diff
Patch8:                 ctl-8-IlmCtlSimd.diff
Patch9:                 ctl-9-testAffineRec.cpp.diff
Patch10:                ctl-10-testGaussRec.cpp.diff
patch11:                ctl-11-configure.diff

URL:                    http://www.oscars.org/council/ctl.html
License:                A.M.P.A.S.
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:         %{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:		SFEopenexr
Requires:               SFEilmbase
BuildRequires:		SFEopenexr-devel
BuildRequires:		SFEilmbase-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
export CXXFLAGS="%cxx_optflags64"

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir}/%{_arch64} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared \
        --disable-static \
        --enable-threading --enable-posix-sem \
        --with-pic

make -j $CPUS
cd ..
%endif

cd %{src_name}-%{version}

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export CXXFLAGS="%cxx_optflags"

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared \
        --disable-static \
        --enable-threading --enable-posix-sem \
        --with-pic

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libIlmCtl*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/CTL-%{version}/

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libIlmCtl*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/CTL/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial version
