#
# spec file for package SFExulrunner
#
# includes module(s): XULRunner
#
# 64Bit build fails with the following errors:
#  Error: suffix or operands invalid for `push'
#  Error: suffix or operands invalid for `call'
# and so on at file:
# mozilla/xpcom/reflect/xptcall/src/md/unix/xptcstubs_x86_solaris.cpp
# 

%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

#%include base.inc

Name:                    SFExulrunner
Summary:                 XUL Runtime for Gecko Applications
Version:                 1.9.0.10
URL:                     http://developer.mozilla.org/En/XULRunner
Source:                  http://releases.mozilla.org/pub/mozilla.org/xulrunner/releases/%{version}/source/xulrunner-%{version}-source.tar.bz2
Source1:                 xulrunner-mozconfig
Source2:                 xulrunner-find
%define tarball_dir mozilla
%define version_internal  1.9.1
%define mozappdir         %{_libdir}/%{name}-%{version_internal}

Patch1:                  xulrunner-01-path.diff
Patch3:                  xulrunner-03-build.diff
Patch4:                  xulrunner-04-ps-pdf-simplify-operators.diff
Patch5:                  xulrunner-05-configure-rpath-link.diff
Patch6:                  xulrunner-06-nsAppRunner.cpp.diff
Patch7:                  xulrunner-07-SunOS5.mk.diff
Patch8:                  xulrunner-08-toolkit-Makefile.in.diff
Patch9:                  xulrunner-09-configure.diff

License:                 MPLv1.1 or GPLv2+ or LGPLv2+
SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWcairo
Requires:                SUNWpng
Requires:                SUNWjpg
Requires:                SUNWgnome-component
Requires:                SUNWgtk2
Requires:                SUNWgnome-libs
Requires:                SUNWzlib
Requires:                SUNWpango
Requires:                SUNWfreetype2
Requires:                SUNWxorg-clientlibs
Requires:                SUNWsqlite3
Requires:                SFElcms
BuildRequires:           SUNWcairo-devel
BuildRequires:           SUNWpng-devel
BuildRequires:           SUNWjpg-devel
BuildRequires:           SUNWgnome-libs
BuildRequires:           SUNWzip
BuildRequires:           SUNWzlib
BuildRequires:           SUNWgnome-component-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWpango-devel
BuildRequires:           FSWxorg-headers
BuildRequires:           SUNWsqlite3-devel
BuildRequires:           SFElcms-devel

%description
XULRunner provides the XUL Runtime environment for Gecko applications.

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
#Requires:           SUNWprd
#Requires:           SUNWtlsd
Requires:           SUNWcairo-devel
Requires:           SUNWpng-devel
Requires:           SUNWjpg-devel
Requires:           SUNWgnome-libs
Requires:           SUNWzip
Requires:           SUNWbzip
Requires:           SUNWzlib
Requires:           SUNWgnome-component-devel
Requires:           SUNWgtk2-devel
Requires:           SUNWpango-devel
Requires:           FSWxorg-headers
Requires:           SUNWsqlite3-devel
Requires:           SFElcms-devel

%prep
%if %cc_is_gcc
%else
%error "This SPEC should be built with Gcc. Please set CC and CXX env variables"
%endif

%setup -q -c -n %name-%version
mkdir 32
mv %{tarball_dir} 32
cd 32/%{tarball_dir}
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
rm -f .mozconfig
cp %{SOURCE1} .mozconfig
cd ../..

#%ifarch amd64 sparcv9
#mkdir 64
#cp -rp 32/%{tarball_dir} 64/%{tarball_dir}
#%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{_libdir}/%{name}-${INTERNAL_GECKO}
export PREFIX='%{_prefix}'
MOZ_SMP_FLAGS=-j1
[ "$CPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j2
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++

#%ifarch amd64 sparcv9
#cd 64/%{tarball_dir}
#
#export CFLAGS="%optflags64 -I/usr/include/mps"
#export CXXFLAGS="%cxx_optflags64 -I/usr/include/mps"
#export LDFLAGS="%_ldflags64 -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} -L/usr/lib/mps/%{_arch64} -R/usr/lib/mps/%{_arch64} %{gnu_lib_path64} %{sfw_lib_path64}"
#export LIBDIR='%{_libdir}/%{_arch64}'
#
#gmake -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"
#
#cd ../..
#%endif

cd 32/%{tarball_dir}
accel=x86
#export CFLAGS="%optflags -I/usr/include/mps"
#export CXXFLAGS="%cxx_optflags -I/usr/include/mps"
#export LDFLAGS="%_ldflags -L/usr/lib -R/usr/lib -L/usr/lib/mps -R/usr/lib/mps %{gnu_lib_path} %{sfw_lib_path}"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/lib -R/usr/lib %{gnu_lib_path} %{sfw_lib_path}"
export LIBDIR='%{_libdir}'

gmake -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

cd ../..

%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd %{tarball_dir}-64
#make install DESTDIR=${RPM_BUILD_ROOT}
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
#cd ..
#%endif

cd 32
cp %{SOURCE2} ./find
chmod +x ./find
export PATH=`pwd`:${PATH}

cd %{tarball_dir}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

(cd ${RPM_BUILD_ROOT}%{_datadir}/idl; ln -s xulrunner-%{version} xulrunner)
(cd ${RPM_BUILD_ROOT}%{_libdir}; ln -s xulrunner-%{version} xulrunner)

install -m 0555 dist/sdk/bin/regxpcom ${RPM_BUILD_ROOT}%{_libdir}/xulrunner-%{version}
cp -rL dist/include/* $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{version}
cp -rL dist/include/string/* $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{version}/stable
cp $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{version}/js/jsconfig.h \
   $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{version}/js/jsversion.h

find $RPM_BUILD_ROOT%{_includedir} -type f -name "*.h" | xargs chmod 644
find $RPM_BUILD_ROOT%{_datadir}/idl -type f -name "*.idl" | xargs chmod 644

(cd ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
 cat libxul-unstable.pc | \
  sed 's#includetype=unstable#includetype=unstable\nlibdir=\${sdkdir}/lib#' > libxul-unstable.pc.new
 mv libxul-unstable.pc.new libxul-unstable.pc
 cat libxul.pc | \
  sed 's#includetype=stable#includetype=stable\nlibdir=\${sdkdir}/lib#' > libxul.pc.new
 mv libxul.pc.new libxul.pc

 cat mozilla-gtkmozembed-embedding.pc | \
  sed 's#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=\${sdkdir}/lib#' \
  > mozilla-gtkmozembed-embedding.pc.new
 mv mozilla-gtkmozembed-embedding.pc.new mozilla-gtkmozembed-embedding.pc
 cat mozilla-gtkmozembed.pc | \
  sed 's#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=\${sdkdir}/lib#' \
  > mozilla-gtkmozembed.pc.new
 mv mozilla-gtkmozembed.pc.new mozilla-gtkmozembed.pc

 cat mozilla-js.pc | \
  sed 's#-I\${includedir}/stable#-I\${includedir}/stable -I\${includedir}/js#' > mozilla-js.pc.new
 mv mozilla-js.pc.new mozilla-js.pc
 cat mozilla-plugin.pc | \
  sed 's#-I\${includedir}/stable#-I\${includedir}/stable -I\${includedir}/java -I\${includedir}/plugin#' \
  > mozilla-plugin.pc.new
 mv mozilla-plugin.pc.new mozilla-plugin.pc
)

cd ../..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xulrunner
%dir %attr (0755, root, bin) %{_libdir}/xulrunner-%{version}
%{_libdir}/xulrunner-%{version}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/gre.d
%{_sysconfdir}/gre.d/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%_arch64
#%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/xulrunner-devel-%{version}
%{_libdir}/xulrunner-devel-%{version}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/idl
%{_datadir}/idl/*



%changelog
* Mon Jun 29 2009 - moinakg@belenix.org
- Initial spec file
