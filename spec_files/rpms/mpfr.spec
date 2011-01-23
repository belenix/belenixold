Name:          mpfr
Summary:       C library for multiple-precision floating-point computations
Version:       3.0.0
Release:       3%{?dist}
Source:        http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.bz2
License:       LGPLv3+ and GPLv3+ and GFDL
Group:         System Environment/Libraries
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
BuildRequires: gmp-devel
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary:        %{summary} - developer files
Group:          Development/Libraries
Requires: %name = %{version}-%{release}
Requires: gmp-devel

%description devel
Header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd mpfr-%{version}
export CFLAGS="%optflags -I%{_includedir}/gmp"
export CXXFLAGS="%cxx_optflags -I%{_includedir}/gmp"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
            --docdir=%{_docdir}         \
	    --infodir=%{_infodir}	\
	    --without-emacs		\
	    --enable-shared		\
	    --disable-static		\
            --disable-assert            \
	    $nlsopt

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd mpfr-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in mpfr.info
do
  install-info --quiet --info-dir=%{_infodir} %{_infodir}/$info
done

%preun devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in mpfr.info
do
  install-info --info-dir=%{_infodir} --delete %{_infodir}/mpfr.info
done

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr(0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Wed May 06 2009 - moinakg@belenix.org
- Bump version to 2.4.1
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2.3.1
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 2.3.0
* Tue Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
