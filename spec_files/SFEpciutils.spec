#
# spec file for package SFEpciutils
#
# includes module(s): pciutils
#
#
%include Solaris.inc

%ifarch amd64
%include arch64.inc
%endif

%include base.inc


Name:                    SFEpciutils
Summary:                 The PCI Utilities are a collection of programs for inspecting and manipulating configuration of PCI devices
Version:                 3.1.2
URL:                     http://mj.ucw.cz/pciutils.html
Source:                  ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/pciutils-%{version}.tar.gz
Patch1:                  pciutils-1-types.h.0.diff
Patch2:                  pciutils-2-i386-io-sunos.h.1.diff
Patch3:                  pciutils-3-Makefile.2.diff
Patch4:                  pciutils-4-pci.h.3.diff
Patch7:                  pciutils-7-configure.diff
Patch8:                  pciutils-8-names-net.c.diff
Patch10:                 pciutils-10-internal.h.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 GPLv2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
The PCI Utilities are a collection of programs for inspecting and
manipulating configuration of PCI devices, all based on a common
portable library libpci which offers access to the PCI configuration
space on a variety of operating systems. 

%package devel
Summary:                 Development files for the pciutils package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc

%prep
%setup -q -c -n %name-%version
cd pciutils-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p1
%patch8 -p1
%patch10 -p1
cd ..

%ifarch amd64
cp -rp pciutils-%{version} pciutils-%{version}-64
%endif

%build
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export UNAMEP="`uname -p`"

if [ "$UNAMEP" = "sparc" ] ; then
    echo "SPARC port not ready yet. Stay tuned."
    exit 1
fi

%ifarch amd64
cd pciutils-%{version}-64
PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig

#
# Update Makefile settings
#
cp Makefile Makefile.orig
chmod +w Makefile
cat Makefile.orig | sed '{
    s#OPT=-O2#OPT=-O2 -m64\nLDFLAGS=-m64 %{gnu_lib_path64}#
    s#SHARED=no#SHARED=yes#
    s#PREFIX=/usr/local#PREFIX=%{_prefix}#
    s#/sbin$#/sbin/%{_arch64}#
    s#/lib$#/lib/%{_arch64}#
}' > Makefile

make
cd ..
%endif

cd pciutils-%{version}
PKG_CONFIG_PATH=%{_libdir}/pkgconfig

#
# Update Makefile settings
#
cp Makefile Makefile.orig
chmod +w Makefile
cat Makefile.orig | sed '{
    s#OPT=-O2#OPT=-O2\nLDFLAGS=%{gnu_lib_path}#
    s#SHARED=no#SHARED=yes#
    s#PREFIX=/usr/local#PREFIX=%{_prefix}#
}' > Makefile

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd pciutils-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_sbindir}/%{_arch64}/update-pciids
#(cd ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
# [ ! -h libpci.so ] && ln -s libpci.so.*.* libpci.so )
cd ..
%endif

cd pciutils-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
#(cd ${RPM_BUILD_ROOT}%{_libdir}
# [ ! -h libpci.so ] && ln -s libpci.so.*.* libpci.so )
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/lspci
%{_sbindir}/setpci
%{_sbindir}/update-pciids
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/pci.ids.gz
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_sbindir}/%{_arch64}
%{_sbindir}/%{_arch64}/lspci
%{_sbindir}/%{_arch64}/setpci
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Initial version
