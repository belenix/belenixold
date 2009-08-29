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

Name:                SFElibmtp
Summary:             A software library for MTP media players
Version:             1.0.0
License:             LGPLv2+
Group:               System Environment/Libraries
Source:              http://download.sourceforge.net/libmtp/libmtp-%{version}.tar.gz
URL:                 http://libmtp.sourceforge.net/

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlibusb
Requires: SUNWhal
Requires: SUNWhalr
BuildRequires: SFEdoxygen
BuildRequires: SUNWlibusb
BuildRequires: SUNWhal

%description
This package provides a software library for communicating with MTP
(Media Transfer Protocol) media players, typically audio players, video
players etc.

%package examples
Summary:        Example programs for libmtp
Group:          Applications/Multimedia
%include default-depend.inc
Requires: %name

%description examples
This package provides example programs for communicating with MTP
devices.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWlibusb
Requires: SUNWhal

%prep
%setup -q -c -n %name-%version

#%ifarch amd64 sparcv9
#cp -rp libmtp-%version libmtp-%{version}-64
#%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#%ifarch amd64 sparcv9
#cd libmtp-%{version}-64
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

cd libmtp-%{version}
export CFLAGS="%optflags"
export CPPFLAGS="-I%{sfw_inc} -Du_int64_t=uint64_t -Du_int32_t=uint32_t"
export LDFLAGS="%_ldflags %{sfw_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --disable-static \
            --program-prefix=mtp-

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd libmtp-%{version}-64
#
#gmake install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
#cd ..
#%endif

cd libmtp-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

# Bloody la files!
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/hal/fdi/information/10freedesktop
install -p -m 644 libmtp.fdi $RPM_BUILD_ROOT%{_sysconfdir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi

mkdir -p $RPM_BUILD_ROOT%{_docdir}/libmtp-%{version}
install -p -m 644 AUTHORS ChangeLog COPYING INSTALL README TODO $RPM_BUILD_ROOT%{_docdir}/libmtp-%{version}

#
# Fix absolute symlinks
#
(cd $RPM_BUILD_ROOT%{_bindir}
 rm -f mtp-delfile mtp-getfile mtp-newfolder mtp-sendfile mtp-sendtr
 for l in mtp-delfile mtp-getfile mtp-newfolder mtp-sendfile mtp-sendtr
 do
   ln -s mtp-connect ${l}
 done
)

# Touch generated files to make them always have the same time stamp.
touch -r configure.ac \
      $RPM_BUILD_ROOT%{_docdir}/libmtp-%{version}/html/* \
      $RPM_BUILD_ROOT%{_includedir}/*.h \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc \
      $RPM_BUILD_ROOT%{_sysconfdir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi

#
# Fix libmtp.pc to not refer to libusb. OpenSolaris libusb does not deliver a pc file.
#
cat libmtp.pc | sed 's/libusb//' > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libmtp.pc
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
