#
# spec file for package SFElibofa
#
# includes module(s): libofa
#
%include Solaris.inc

Name:		SFElibofa
Summary:	library for accesing MusicBrainz servers
Version:	0.9.3
License:	LGPL
Source:		http://musicip-libofa.googlecode.com/files/libofa-%{version}.tar.gz
Patch1:         libofa-01-Real_abs.diff
Patch2:         libofa-02-abs.diff
Patch3:         libofa-03-example_string.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:       SFEfftw
BuildRequires:  SFEfftw-devel

%prep
%setup -q -n libofa-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export LDFLAGS="%_ldflags -L/lib -R/lib %{gnu_lib_path}"

./configure -prefix %{_prefix} \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CMAKE_INSTALL_PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Sep 12 2009 - moinakg(at)belenix<dot>org
- Rebuild and repatch for KDE 4.3.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Initial Spec.
