#
# spec file for package SFElibqalculate
#
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc
%define  gnu_share /usr/gnu/share
Name:			SFElibqalculate
License:		GPLv2+
Group:			System Environment/Libraries
Version:		0.9.6
Summary:		Multi-purpose calculator library
Source:			%{sf_download}/qalculate/libqalculate-%{version}.tar.gz
Patch1:                 libqalculate-01-gcc4.diff
Patch2:                 libqalculate-02-cln.diff

URL:			http://qalculate.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires:               SUNWglib2
BuildRequires:          SUNWglib2-devel
Requires:               SUNWlxml
BuildRequires:          SUNWlxml-devel
Requires:               SFEreadline
BuildRequires:          SFEreadline-devel
Requires:               SFEcln
BuildRequires:          SFEcln-devel
%if %cc_is_gcc
Requires:               SFEgccruntime
%endif

%description
Qalculate! is a multi-purpose desktop calculator for GNU/Linux/Unix. It is
small and simple to use but with much power and versatility underneath.
Features include customizable functions, units, arbitrary precision, plotting.
This package provides the library that underpins Qalculate! and also provides
the text-mode interface for Qalculate!

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:          SUNWglib2-devel
Requires:          SUNWlxml-devel
Requires:          SFEreadline-devel
Requires:          SFEcln-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - localization files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd libqalculate-%{version}
%patch1 -p0
%patch2 -p0
cd ..

%ifarch amd64 sparcv9
cp -pr libqalculate-%{version} libqalculate-%{version}-64
%endif

%build

%ifarch amd64 sparcv9
cd libqalculate-%{version}-64
export CFLAGS="-m64 -march=opteron -g -O2 -fno-omit-frame-pointer -D_LCONV_C99 -I%{_includedir}/%{_arch64}"
export CXXFLAGS="-m64 -march=opteron -g -O2 -fno-omit-frame-pointer -D_LCONV_C99 -I%{_includedir}/%{_arch64}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"
export PKG_CONFIG_PATH="%{_libdir}/%{_arch64}/pkgconfig:%{gnu_lib64}/pkgconfig"

intltoolize --copy --force --automake
libtoolize --force --copy
aclocal -I%{gnu_share}/aclocal
autoheader -I%{gnu_share}/aclocal
automake
autoconf -I%{gnu_share}/aclocal

./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir}/%{_arch64} \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make
cd ..
%endif

cd libqalculate-%{version}
export CFLAGS="-march=pentium4 -g -O2 -fno-omit-frame-pointer -D_LCONV_C99"
export CXXFLAGS="-march=pentium4 -g -O2 -fno-omit-frame-pointer -D_LCONV_C99"
export LDFLAGS="%_ldflags"

intltoolize --copy --force --automake
libtoolize --force --copy
aclocal -I%{gnu_share}/aclocal
autoheader -I%{gnu_share}/aclocal
automake
autoconf -I%{gnu_share}/aclocal

./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir} \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd libqalculate-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd libqalculate-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/qalculate
%{_datadir}/qalculate/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%endif

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
