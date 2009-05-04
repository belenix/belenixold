#
# spec file for package SFEdvgrab
#
# includes module(s): dvgrab
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEdvgrab
Summary:                 Utility to capture video from a DV camera
Version:                 3.4
Source:                  %{sf_download}/kino/dvgrab-%{version}.tar.gz
Source1:                 endian-compat.h
Patch1:                  dvgrab-1-Makefile.in.diff
Patch2:                  dvgrab-2-affine.h.diff
Patch3:                  dvgrab-3-avi.cc.diff
Patch4:                  dvgrab-4-avi.h.diff
Patch5:                  dvgrab-5-config.h.in.diff
Patch6:                  dvgrab-6-dvframe.cc.diff
Patch7:                  dvgrab-7-dvgrab.cc.diff
Patch8:                  dvgrab-8-endian_types.h.diff
Patch9:                  dvgrab-9-error.cc.diff	
Patch10:                 dvgrab-10-error.h.diff
Patch11:                 dvgrab-11-filehandler.cc.diff
Patch12:                 dvgrab-12-hdvframe.cc.diff
Patch13:                 dvgrab-13-iec13818-1.cc.diff
Patch14:                 dvgrab-14-iec13818-2.cc.diff
Patch15:                 dvgrab-15-iec13818-2.h.diff
Patch16:                 dvgrab-16-ieee1394io.cc.diff
Patch17:                 dvgrab-17-inttypes_gnucompat.h.diff
Patch18:                 dvgrab-18-riff.cc.diff
Patch19:                 dvgrab-19-smiltime.h.diff
Patch20:                 dvgrab-20-stringutils.cc.diff
Patch21:                 dvgrab-21-strsep.c.diff
Patch22:                 dvgrab-22-strsep.h.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd dvgrab-%version
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
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

cp %{SOURCE1} ./endian.h
cd ..

%ifarch amd64 sparcv9
cp -rp dvgrab-%{version} dvgrab-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-D__ASSERT_FUNCTION=__FUNCTION__"

%ifarch amd64 sparcv9
cd dvgrab-%{version}-64
%if %cc_is_gcc
export CFLAGS="-O4 -fPIC -DPIC -m64"
export CXXFLAGS="-O4 -fPIC -DPIC -m64"
%else
export CFLAGS="-xO4 -KPIC -DPIC -m64"
export CXXFLAGS="-xO4 -KPIC -DPIC -m64"
%endif

export LDFLAGS="-L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -m64"

libtoolize -f -c
aclocal
autoheader
autoconf -f
automake -a -f

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

cd dvgrab-%{version}
%if %cc_is_gcc
export CFLAGS="-O4 -fPIC -DPIC"
export CXXFLAGS="-O4 -fPIC -DPIC"
%else
export CFLAGS="-xO4 -KPIC -DPIC"
export CXXFLAGS="-xO4 -KPIC -DPIC"
%endif
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"

libtoolize -f -c
aclocal
autoheader
autoconf -f
automake -a -f

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
cd dvgrab-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd dvgrab-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dvgrab

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dvgrab
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Mon May 04 2009 - moinakg@belenix.org
- Initial version off KDE-Solaris repo.
