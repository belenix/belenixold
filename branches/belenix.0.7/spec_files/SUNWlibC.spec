#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWlibC
Summary:             SUN Workshop Compilers Bundled libC
Version:             5.11
Source0:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-SUNWlibC-closed-bins-20060918.i386.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -c -n %{name}-%{version}

%build

if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

export PATH=/usr/ccs/bin:${PATH}
mkdir -p ./%{_docdir}/SUNWlibC
mv usr/BINARYLICENSE.txt ./%{_docdir}/SUNWlibC
mv usr/opensolaris.license.txt ./%{_docdir}/SUNWlibC
mv usr/README.devpro.SUNWlibC-closed-bins-20060918.i386 ./%{_docdir}/SUNWlibC

%install

rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
tar cpf - * | (cd ${RPM_BUILD_ROOT}; tar xpf -)
(cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -s libdemangle.so.1 libdemangle.so)
(cd ${RPM_BUILD_ROOT}%{_libdir}%{_arch64}
    ln -s libdemangle.so.1 libdemangle.so)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
