#
# spec file for package SFEtaglib
#
# includes module(s): taglib
#
#
%include Solaris.inc

Name:                    SFEtaglib
Summary:                 TagLib  - a library for reading and editing the meta-data of several popular audio formats
Version:                 1.5rel
%define tarball_version  1.5
Source:                  http://developer.kde.org/~wheeler/files/src/taglib-%{tarball_version}.tar.gz
Patch1:                  taglib-01-map.diff
Patch2:                  taglib-02-kde#161721.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
%if %cc_is_gcc
Requires: SFEgccruntime
%else
Requires: SUNWlibC
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n taglib-%tarball_version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

if [ "x`basename $CC`" = xgcc ]
then
	export LDFLAGS="%_ldflags -lc -lstdc++"
else
	export LDFLAGS="%_ldflags -lc -lCrun -lCstd"
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Bump version to 1.5 release.
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Bump version to 1.5b1.
- Add dependency on SFEgccruntime for Gcc builds.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Allow build using g++
* Sun Nov 04 2007 - trisk@acm.jhu.edu
- Initial spec
