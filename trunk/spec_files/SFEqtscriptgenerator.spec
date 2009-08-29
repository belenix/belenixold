#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# 64Bit build commented for now since there is no 64Bit libusb yet.
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEqtscriptgenerator
Summary:             A tool to generate Qt bindings for Qt Script
Version:             0.1.0
License:             GPLv2
Group:               System Environment/Libraries
Source:              http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-%{version}.tar.gz
URL:                 http://code.google.com/p/qtscriptgenerator/
Patch1:              qtscriptgenerator-01-gcc44.diff
Patch2:              qtscriptgenerator-02-sun_issue27.diff

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlxsl
Requires: SFEphonon
Requires: SFEqt4
Requires: SFEqtscriptbindings
BuildRequires: SUNWlxsl-devel
BuildRequires: SFEphonon-devel
BuildRequires: SFEqt4-devel

%description
Qt Script Generator is a tool to generate Qt bindings for Qt Script.

%package -n SFEqtscriptbindings
Summary:        Qt bindings for Qt Script
Group:          System Environment/Libraries
SUNW_BaseDir:        /
%include default-depend.inc

%description -n SFEqtscriptbindings
Bindings providing access to substantial portions of the Qt API
from within Qt Script.

%prep
%setup -q -c -n %name-%version
cd qtscriptgenerator-src-%version
%patch1 -p0
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp qtscriptgenerator-src-%version qtscriptgenerator-src-%{version}-64
%endif


%build
OPATH=$PATH
%ifarch amd64 sparcv9
cd qtscriptgenerator-src-%{version}-64

export INCLUDE=%{_includedir}/qt4
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++-64
export PATH="%{_prefix}/qt4/bin/%{_arch64}:${OPATH}"

cd generator
qmake
gmake
./generator
cd ..

cd qtbindings
# Get rid of Phonon - does not work
[ ! -f qtbindings.pro.orig ] && cp qtbindings.pro qtbindings.pro.orig
cat qtbindings.pro.orig | sed '/phonon/d' > qtbindings.pro

qmake
gmake
cd ..

pushd tools/qsexec/src
qmake
gmake
popd

cd ..
%endif

cd qtscriptgenerator-src-%{version}
export INCLUDE=%{_includedir}/qt4
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++
export PATH="%{_prefix}/qt4/bin:${OPATH}"

cd generator
qmake
gmake
./generator
cd ..

cd qtbindings
# Get rid of Phonon - does not work
[ ! -f qtbindings.pro.orig ] && cp qtbindings.pro qtbindings.pro.orig
cat qtbindings.pro.orig | sed '/phonon/d' > qtbindings.pro

qmake
gmake
cd ..

pushd tools/qsexec/src
qmake
gmake
popd

cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd qtscriptgenerator-src-%{version}-64

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/%{_arch64}/qt4/plugins/script
/usr/bin/cp -rP@ plugins/script/libqtscript* $RPM_BUILD_ROOT/%{_prefix}/lib/%{_arch64}/qt4/plugins/script

/usr/bin/cp -rP@ tools/qsexec/README.TXT README.qsexec
ginstall -D -p -m755 tools/qsexec/qsexec $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/qsexec
ginstall -D -p -m755 generator/generator $RPM_BUILD_ROOT%{_prefix}/qt4/bin/%{_arch64}/generator

cd ..
%endif

cd qtscriptgenerator-src-%{version}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/qt4/plugins/script
/usr/bin/cp -rP@ plugins/script/libqtscript* $RPM_BUILD_ROOT/%{_prefix}/lib/qt4/plugins/script

/usr/bin/cp -rP@ tools/qsexec/README.TXT README.qsexec
ginstall -D -p -m755 tools/qsexec/qsexec $RPM_BUILD_ROOT%{_bindir}/qsexec
ginstall -D -p -m755 generator/generator $RPM_BUILD_ROOT%{_prefix}/qt4/bin/generator

mkdir -p $RPM_BUILD_ROOT%{_docdir}/qtscriptbindings
/usr/bin/cp -rP@ doc $RPM_BUILD_ROOT%{_docdir}/qtscriptbindings
/usr/bin/cp -rP@ examples $RPM_BUILD_ROOT%{_docdir}/qtscriptbindings
cp README LICENSE.GPL README.qsexec $RPM_BUILD_ROOT%{_docdir}/qtscriptbindings
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/qt4
%dir %attr (0755, root, bin) %{_basedir}/qt4/bin
%{_basedir}/qt4/bin/generator

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/qt4/bin/%{_arch64}
%{_basedir}/qt4/bin/%{_arch64}/generator
%endif

%files -n SFEqtscriptbindings
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%dir %attr (0755, root, bin) %{_bindir}
%attr (0555, root, bin) %{_bindir}/qsexec

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/qsexec
%endif

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/qt4
%dir %attr (0755, root, bin) %{_libdir}/qt4/plugins
%{_libdir}/qt4/plugins/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%dir %attr (0755, root, bin) %{_libdir}/%_arch64/qt4
%dir %attr (0755, root, bin) %{_libdir}/%_arch64/qt4/plugins
%{_libdir}/%_arch64/qt4/plugins/*
%endif

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
