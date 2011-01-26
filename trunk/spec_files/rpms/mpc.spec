Name:    libmpc
Version: 0.8.2
Release: 0.2%{?dist}
Summary: C library for multiple precision complex arithmetic
URL:     http://www.multiprecision.org/
Source:  http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
Group:   Development/Libraries
License: GPLv3+

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: gmp
BuildRequires: gmp-devel
#Requires: gcc-runtime
BuildRequires: mpfr-devel
Requires: mpfr

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary:                 %{summary} - development files
Requires: %name
Requires: gmp-devel
Requires: mpfr-devel

%description devel
Header files and shared object symlinks for MPC library.

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd mpc-%{version}
%if %gcc_compiler
export CPPFLAGS="%optflags -std=gnu99 -I/usr/include/gmp -I/usr/include/mpfr"
export CFLAGS="%optflags -std=gnu99 -I/usr/include/gmp -I/usr/include/mpfr"
%else
export CPPFLAGS="%optflags -xc99=%%all -I/usr/include/gmp -I/usr/include/mpfr"
export CFLAGS="%optflags -xc99=%%all -I/usr/include/gmp -I/usr/include/mpfr"
%endif
export LDFLAGS="%_ldflags"
export EGREP=egrep

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd mpc-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
%find_info

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
%install_info

%preun devel
%uninstall_info

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%changelog
* Wed May 06 2009 - moinakg@belenix.org
- Initial spec file.
