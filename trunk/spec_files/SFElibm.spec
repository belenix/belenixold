#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFElibm
Summary:             SUN Math library and microtasking library
Version:             1.0
Source0:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-libm-src-20060131.tar.bz2
Source1:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-libmtsk-bins-20060228.i386.tar.gz
Source2:             http://www.belenix.org/binfiles/libm-sun-freebsd-schily-0.3.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %{name}-root

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%package -n SUNWlibm
Summary:       SUN Math library and microtasking library dummy package.
SUNW_BaseDir:  %{_basedir}
Requires:      %{name}

%package -n SUNWlibmr
Summary:       SUN Math library and microtasking library dummy package.
SUNW_BaseDir:  /
Requires:      %{name}-root

%package -n SUNWlibms
Summary:       SUN Math library and microtasking library dummy package.
SUNW_BaseDir:  %{_basedir}
Requires:      %{name}

%package -n SUNWlibmsr
Summary:       SUN Math library and microtasking library dummy package.
SUNW_BaseDir:  /
Requires:      %{name}-root

%prep
%setup -c -n %{name}-%{version}
%setup -T -D -a 1

%build

if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

export PATH=/usr/ccs/bin:${PATH}

gunzip -c %{SOURCE1} | /usr/bin/tar xpf - 
cd usr/src/harness
make -f Makefile-os

%install

rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
(cd root_i386; tar cpf - lib usr) | (cd ${RPM_BUILD_ROOT}; tar xpf -)
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/libmtsk
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/SUNWlibm
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/SUNWlibmr
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/SUNWlibms
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/SUNWlibmsr

cp root_i386/README.DEVPROLIBMTSKBINARIES.i386 ${RPM_BUILD_ROOT}/usr/share/doc/libmtsk
(cd destdir/i386/DEV; tar cpf - usr lib) | (cd ${RPM_BUILD_ROOT}; tar xpf -)
(cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -s ../../lib/llib-lm.ln
    ln -s ../../lib/llib-lm
    ln -s ../../lib/libm.so.2 libm.so
    ln -s ../../lib/libm.so.2
    ln -s ../../lib/libm.so.1
    mkdir libmvec
    cd libmvec
    ln -s ../../../lib/libmvec/libmvec_hwcap1.so.1
    cd ..
    ln -s ../../lib/libmvec.so.1 libmvec.so
    ln -s ../../lib/libmvec.so.1
    cd %{_arch64}
    ln -s ../../../lib/%{_arch64}/llib-lm.ln
    ln -s ../../../lib/%{_arch64}/libm.so.2 libm.so
    ln -s ../../../lib/%{_arch64}/libm.so.2
    ln -s ../../../lib/%{_arch64}/libm.so.1
    ln -s ../../../lib/%{_arch64}/libmvec.so.1 libmvec.so
    ln -s ../../../lib/%{_arch64}/libmvec.so.1)

cat << __EOF__ > ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibm/README.txt
This is a dummy package retained for backward compatibility.
We do not have the SUNW pkgdefs for the SUN Math libraries
so we cannot provide fully populated SUNWlibm* packages.
__EOF__
cp ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibm/README.txt ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibmr/README.txt
cp ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibm/README.txt ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibms/README.txt
cp ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibm/README.txt ${RPM_BUILD_ROOT}%{_docdir}/SUNWlibmsr/README.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/llib*
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/llib*
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/libmvec
%{_libdir}/libmvec/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/libmtsk
%{_docdir}/libmtsk/*

%files root
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /lib
/lib/llib*
/lib/*.so*
%dir %attr (0755, root, bin) /lib/%{_arch64}
/lib/%{_arch64}/llib*
/lib/%{_arch64}/*.so*
%dir %attr (0755, root, bin) /lib/libmvec
/lib/libmvec/*.so*

%files -n SUNWlibm
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/SUNWlibm
%{_docdir}/SUNWlibm/*

%files -n SUNWlibmr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/SUNWlibmr
%{_docdir}/SUNWlibmr/*

%files -n SUNWlibms
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/SUNWlibms
%{_docdir}/SUNWlibms/*

%files -n SUNWlibmsr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/SUNWlibmsr
%{_docdir}/SUNWlibmsr/*

%changelog
* Sun Feb 24 2008 - moinakg@gmail.com
- Fix a couple of typos.
* Wed Feb 20 2008 - moinakg@gmail.com
- Add some missing links under /usr/lib.
* Sun Feb 10 2008 - moinakg@gmail.com
- Initial spec.
