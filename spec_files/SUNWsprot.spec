#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWsprot
Summary:             Solaris sccs and make tools
Version:             1.0
Source0:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-sccs-src-20061219.tar.bz2
Source1:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-make-src-20061219.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibm

%package -n SUNWxcu4t
Summary:       XCU4 make and sccs utilities
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SUNWsprot

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build
mkdir %{name}-%{version}-build/sccs
mkdir %{name}-%{version}-build/make

cd %{name}-%{version}-build/sccs
bunzip2 -c %{SOURCE0} | tar xpf -
cd ../make
bunzip2 -c %{SOURCE1} | tar xpf -

%build
cd %{name}-%{version}-build

if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

(cd sccs/usr/src
  ./build)
(cd make/usr/src
  ./build)

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
(cd sccs/destdir/root_i386; tar cpf - *) | (cd ${RPM_BUILD_ROOT}; tar xpf -)
(cd make/destdir/root_i386; tar cpf - *) | (cd ${RPM_BUILD_ROOT}; tar xpf -)

(cd ${RPM_BUILD_ROOT}
  mkdir -p usr/bin
  cd usr/ccs/bin
  for f in *
  do
    mv $f ../../bin
    ln -s ../../bin/$f
  done)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/bin
/usr/bin/*
%dir %attr (0755, root, bin) /usr/ccs
%dir %attr (0755, root, bin) /usr/ccs/bin
/usr/ccs/bin/*
%dir %attr (0755, root, bin) /usr/lib
/usr/lib/*
%dir %attr (0755, root, bin) /usr/ccs/lib
/usr/ccs/lib/*
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, sys) /usr/share/lib
%dir %attr (0755, root, bin) /usr/share/lib/make
/usr/share/lib/make/*

%files -n SUNWxcu4t
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/xpg4
%dir %attr (0755, root, bin) /usr/xpg4/bin
/usr/xpg4/bin/*

%changelog
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
