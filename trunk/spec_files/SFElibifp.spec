#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# 64Bit build commented for now since there is no 64Bit libusb yet.
#

%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc

Name:                SFElibifp
Summary:             A general-purpose library-driver for iRiver's iFP portable audio players
Version:             1.0.0.2
License:             GPLv2
Source:              http://dl.sourceforge.net/ifp-driver/libifp-%{version}.tar.gz
URL:                 http://ifp-driver.sourceforge.net/

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlibusb
BuildRequires: SFEdoxygen
BuildRequires: SUNWlibusb

%description
libifp is a general-purpose library-driver for iRiver's iFP (flash-based)
portable audio players. The source code is pure C and is fairly portable.

Also included is a console app that uses the library.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWlibusb

%prep
%setup -q -c -n %name-%version

#%ifarch amd64 sparcv9
#cp -rp libifp-%version libifp-%{version}-64
#%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#%ifarch amd64 sparcv9
#cd libifp-%{version}-64
#
#PDIR=`pwd`
#ln -s %{_libdir}/%{_arch64}/libast.so.1 libast.so
#
#export CFLAGS="%optflags64"
#export CPPFLAGS="-I%{_includedir}/ast -I%{sfw_inc}"
#export LDFLAGS="%_ldflags64 -L${PDIR} -R%{_libdir}/%{_arch64} -last %{sfw_lib_path64}"
#
#./configure --prefix=%{_prefix} \
#            --bindir=%{_bindir}/%{_arch64} \
#            --libdir=%{_libdir}/%{_arch64} \
#            --sysconfdir=%{_sysconfdir} \
#            --datadir=%{_datadir} \
#            --includedir=%{_includedir} \
#            --mandir=%{_mandir} \
#            --with-libusb \
#            --disable-static
#
#gmake -j$CPUS
#
#cd ..
#%endif

cd libifp-%{version}
PDIR=`pwd`
ln -s %{_libdir}/libast.so.1 libast.so

export CFLAGS="%optflags"
export CPPFLAGS="-I%{_includedir}/ast -I%{sfw_inc}"
export LDFLAGS="%_ldflags -L${PDIR} -R%{_libdir} -last %{sfw_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --with-libusb \
            --disable-static

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd libifp-%{version}-64
#
#gmake install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
#cd ..
#%endif

cd libifp-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

# Bloody la files!
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
