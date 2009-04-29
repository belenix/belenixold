#
# spec file for package SFEid3lib
#
# includes module(s): id3lib
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEid3lib
Summary:                 id3lib  - a software library for manipulating ID3v1/v1.1 and ID3v2 tags
Version:                 3.8.3
Source:                  %{sf_download}/id3lib/id3lib-%{version}.tar.gz
Patch1:                  id3lib-01-wall.diff
Patch2:                  id3lib-02-uchar.diff
Patch3:                  id3lib-03-gcc4-iomanip.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibC
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd id3lib-%version
%patch1  -p1
%patch2  -p1
%patch3  -p1
cd ..

%ifarch amd64 sparcv9
cp -rp id3lib-%{version} id3lib-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

%if %cc_is_gcc
export B_CFLAGS="-O3"
export B_CXXFLAGS="-O3"
%else
%ifarch sparc
export B_CFLAGS="-xO5 -xlibmil"
export B_CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export B_CFLAGS="-xO3 -xlibmil"
export B_CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif
%endif

%ifarch amd64 sparcv9
cd id3lib-%{version}-64
export CFLAGS="${B_CFLAGS} -m64"
export CXXFLAGS="${B_CXXFLAGS} -m64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd id3lib-%{version}
export CFLAGS="${B_CFLAGS}"
export CXXFLAGS="${B_CXXFLAGS}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd id3lib-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd id3lib-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/id3*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/id3*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Add 64Bit build.
- Add patch to fix iomanip include for Gcc4.
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEid3lib
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
