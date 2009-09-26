#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFElibEMF
Summary:             A library for generating Enhanced Metafiles
Version:             1.0.3
License:             LGPLv2+ and GPLv2+
Group:               System Environment/Libraries
Source:              http://dl.sourceforge.net/pstoedit/libEMF-%{version}.tar.gz
URL:                 http://libemf.sourceforge.net/
Patch1:              libEMF-01-amd64.diff
Patch2:              libEMF-02-gcc4.diff

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
BuildRequires: SFEgcc
BuildRequires: SUNWlibtool

%description
libEMF is a library for generating Enhanced Metafiles on systems which
don't natively support the ECMA-234 Graphics Device Interface
(GDI). The library is intended to be used as a driver for other
graphics programs such as Grace or gnuplot. Therefore, it implements a
very limited subset of the GDI.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWglib2-devel
Requires: SUNWpng-devel
Requires: SUNWPython26-devel

%prep
%setup -q -c -n %name-%version
cd libEMF-%version
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libEMF-%version libEMF-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd libEMF-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --disable-static \
            --enable-editing

gmake -j$CPUS
cd ..
%endif

cd libEMF-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --disable-static \
            --enable-editing

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd libEMF-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libEMF-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_docdir}/libEMF-%{version}
cp -r doc/html $RPM_BUILD_ROOT%{_docdir}/libEMF-%{version}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/libEMF
%{_includedir}/libEMF/*.h
%dir %attr (0755, root, bin) %{_includedir}/libEMF/wine
%{_includedir}/libEMF/wine/*
%dir %attr(0755, root, sys) %{_datadir}

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/libEMF-%{version}
%{_docdir}/libEMF-%{version}/*

%changelog
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
