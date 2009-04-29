#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define        major      1
%define        minor      38
%define        patchlevel 0
%define src_url http://easynews.dl.sourceforge.net/sourceforge/boost

Name:                SFEboost-gpp
Summary:             Boost - free peer-reviewed portable C++ source libraries (g++-built)
Version:             %{major}.%{minor}.%{patchlevel}
License:             Boost Software License
Source:              %{src_url}/boost_%{major}_%{minor}_%{patchlevel}.tar.bz2
Patch1:              boost-01-studio.diff
Patch2:              boost-02-gcc34.diff
URL:                 http://www.boost.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEicu4c
BuildRequires: SUNWPython25
Requires: SFEicu4c

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}

%prep
%setup -q -c -n %name-%version
cd boost_%{major}_%{minor}_%{patchlevel}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp boost_%{major}_%{minor}_%{patchlevel} boost_%{major}_%{minor}_%{patchlevel}-64
%endif

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd boost_%{major}_%{minor}_%{patchlevel}-64

export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags64"
export LDFLAGS="%_ldflags64 -L%{_prefix}/lib/%{_arch64} -R%{_prefix}/lib/%{_arch64}"
export EXPAT_INCLUDE=%{_prefix}/include
export EXPAT_LIBPATH=%{_prefix}/lib/%{_arch64}

BOOST_ROOT=`pwd`
TOOLSET=gcc
PYTHON_VERSION=`%{_prefix}/bin/%{_arch64}/python2.5 -c "import sys; print (\"%%d.%%d\" %% (sys.version_info[0], sys.version_info[1]))"`
PYTHON_ROOT=`%{_prefix}/bin/%{_arch64}/python2.5 -c "import sys; print sys.prefix"`

# Overwrite user-config.jam
cat > user-config.jam <<EOF
# Compiler configuration
import toolset : using ;
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" <linker-type>sun ;

# Python configuration
using python : $PYTHON_VERSION : $PYTHON_ROOT ;
EOF

# Build bjam
cd "tools/jam/src" && ./build.sh "$TOOLSET"
cd $BOOST_ROOT

# Build Boost
BJAM=`find tools/jam/src -name bjam -a -type f`
$BJAM --v2 -j$CPUS -sBUILD="release <threading>single/multi" -sICU_PATH=%{_prefix} \
  --layout=system --user-config=user-config.jam address-model=64 release stage

cd ..
%endif

cd boost_%{major}_%{minor}_%{patchlevel}
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"
export EXPAT_INCLUDE=%{_prefix}/include
export EXPAT_LIBPATH=%{_prefix}/lib

BOOST_ROOT=`pwd`
TOOLSET=gcc
PYTHON_VERSION=`python2.5 -c "import sys; print (\"%%d.%%d\" %% (sys.version_info[0], sys.version_info[1]))"`
PYTHON_ROOT=`python2.5 -c "import sys; print sys.prefix"`

# Overwrite user-config.jam
cat > user-config.jam <<EOF
# Compiler configuration
import toolset : using ;
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" <linker-type>sun ; 

# Python configuration
using python : $PYTHON_VERSION : $PYTHON_ROOT ;
EOF

# Build bjam
cd "tools/jam/src" && ./build.sh "$TOOLSET"
cd $BOOST_ROOT

# Build Boost
BJAM=`find tools/jam/src -name bjam -a -type f`
$BJAM --v2 -j$CPUS -sBUILD="release <threading>single/multi" -sICU_PATH=/usr \
  --layout=system --user-config=user-config.jam release stage

%install
BOOST_ROOT=`pwd`
rm -rf $RPM_BUILD_ROOT

gcc_maj=`gcc --version | head -1 | nawk '{ print $3 }' | cut -f1 -d"."`

%ifarch amd64 sparcv9
cd boost_%{major}_%{minor}_%{patchlevel}-64
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/boost/gcc${gcc_maj}
cd stage/lib
find * | cpio -pdum ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/boost/gcc${gcc_maj}

(cd ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/boost/gcc${gcc_maj}
  rm -f *.a
  for f in *.so
  do
	  mv ${f} ${f}.%{version}
	  ln -s ${f}.%{version} ${f}.%{major}
	  ln -s ${f}.%{version} ${f}
  done)

cd ../../..
%endif

cd boost_%{major}_%{minor}_%{patchlevel}
cd stage/lib
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/boost/gcc${gcc_maj}
find * | cpio -pdum ${RPM_BUILD_ROOT}%{_libdir}/boost/gcc${gcc_maj}

(cd ${RPM_BUILD_ROOT}%{_libdir}/boost/gcc${gcc_maj}
  rm -f *.a
  for f in *.so
  do
          mv ${f} ${f}.%{version}
          ln -s ${f}.%{version} ${f}.%{major}
          ln -s ${f}.%{version} ${f}
  done)

mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/boost/gcc${gcc_maj}
cd ../..
find boost | cpio -pdum ${RPM_BUILD_ROOT}%{_includedir}/boost/gcc${gcc_maj}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/boost
%{_libdir}/boost/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/boost
%{_libdir}/%{_arch64}/boost/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/boost
%{_includedir}/boost/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Pull in from SFE gate, bump version to 1.38.0
- Fix build,install and add 64Bit build.
* Wed Apr 23 2008 - laca@sun.com
- create, based on SFEboost.spec
- force building with g++ and install the libs to /usr/lib/g++/<version>
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
