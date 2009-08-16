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
Version:                 1.9.1.1release
%define tarball_version  1.9.1.1
URL:                     http://developer.mozilla.org/En/XULRunner
Source:                  http://releases.mozilla.org/pub/mozilla.org/xulrunner/releases/%{tarball_version}/source/xulrunner-%{tarball_version}-source.tar.bz2
Source1:                 xulrunner-mozconfig
Source2:                 xulrunner-find
%define version_internal  1.9.1
%define tarball_dir mozilla-%{version_internal}
%define mozappdir         %{_libdir}/%{name}-%{version_internal}

Patch1:                  xulrunner-01-path.diff
Patch3:                  xulrunner-03-build.diff
Patch4:                  xulrunner-04-ps-pdf-simplify-operators.diff
Patch7:                  xulrunner-07-SunOS5.mk.diff
Patch8:                  xulrunner-08-toolkit-Makefile.in.diff
Patch9:                  xulrunner-09-configure.diff
Patch10:                 xulrunner-10-nanojit_regnames.diff
Patch11:                 xulrunner-11-bool_weirdo.diff

Patch12:                 firefox3-01-locale.diff
#Patch13:                 firefox3-02-preload.diff
Patch14:                 firefox3-03-disable-online-update.diff
Patch15:                 firefox3-04-oggplay.diff
Patch16:                 firefox3-05-g11n-nav-lang.diff
Patch17:                 firefox3-06-donot-delay-stopping-realplayer.diff
Patch18:                 firefox3-07-spellchecker-default.diff
Patch19:                 firefox3-08-ksh.diff
Patch20:                 firefox3-09-jemalloc-shared-library.diff
Patch21:                 firefox3-10-fix-mimetype-for-helper-app.diff
Patch22:                 firefox3-12-bug492720.diff
Patch25:                 firefox3-20-gen-devel-files.diff
Patch26:                 firefox3-28-ss-privacy-level.diff
Patch27:                 firefox3-29-getting-started.diff
Patch29:                 firefox3-34-gtk-includes.diff

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
BuildRequires:           SFEautoconf213

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
Requires:           SFEautoconf213

%prep
%if %cc_is_gcc
%else
%error "This SPEC should be built with Gcc. Please set CC and CXX env variables"
%endif

%setup -q -c -n %name-%version
mkdir 32
mv %{tarball_dir} 32
cd 32/%{tarball_dir}
rm -f configure
rm -f js/src/configure

%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%patch12 -p1
#%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch29 -p1

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
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++

PATH=/usr/bin:/usr/X11/bin:/usr/sbin:/sbin:/usr/gnu/bin:/usr/sfw/bin
export PATH

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
export CFLAGS="-finline-small-functions -march=pentium4 -fno-omit-frame-pointer %{gnu_lib_path}"
export CXXFLAGS="-finline-small-functions -march=pentium4 -fno-omit-frame-pointer %{gnu_lib_path}"
export LDFLAGS="-B direct -z ignore -z muldefs -L/usr/lib -R/usr/lib %{gnu_lib_path}"
export LIBDIR='%{_libdir}'
export PYTHON=%{_bindir}/python2.6

gmake -f client.mk build STRIP="/bin/true"

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

(cd ${RPM_BUILD_ROOT}%{_datadir}/idl; ln -s xulrunner-%{tarball_version} xulrunner)
(cd ${RPM_BUILD_ROOT}%{_libdir}; ln -s xulrunner-%{tarball_version} xulrunner)

install -m 0555 dist/sdk/bin/regxpcom ${RPM_BUILD_ROOT}%{_libdir}/xulrunner-%{tarball_version}
cp -rL dist/include/* $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{tarball_version}
cp -rL dist/include/string/* $RPM_BUILD_ROOT%{_includedir}/xulrunner-%{tarball_version}/stable

find $RPM_BUILD_ROOT%{_includedir} -type f -name "*.h" | xargs chmod 644
find $RPM_BUILD_ROOT%{_datadir}/idl -type f -name "*.idl" | xargs chmod 644

NSS_VERS=`cat ./dist/include/nss/nss.h | sed 's/"//g' | grep "^#define NSS_VERSION" | nawk '{ print $3 }'`
export NSS_VERS

(cd ${RPM_BUILD_ROOT}%{_includedir}/xulrunner-%{tarball_version}/stable
 (cd ../; ls | egrep -v "stable|unstable|*\.h$") | while read d
 do
   ln -s ../${d}
 done)

(cd ${RPM_BUILD_ROOT}%{_includedir}/xulrunner-%{tarball_version}/unstable
 (cd ../; ls | egrep -v "stable|unstable|*\.h$") | while read d
 do
   ln -s ../${d}
 done)

(cd ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
 cat libxul-unstable.pc | \
  sed '
    s#includetype=unstable#includetype=unstable\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#
    s#-L#-R${libdir} -L#
  ' > libxul-unstable.pc.new
 mv libxul-unstable.pc.new libxul-unstable.pc
 cat libxul.pc | \
  sed '
    s#includetype=stable#includetype=stable\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#
    s#-L#-R${libdir} -L#
  ' > libxul.pc.new
 mv libxul.pc.new libxul.pc

 cat mozilla-gtkmozembed-embedding.pc | \
  sed 's#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#' \
  > mozilla-gtkmozembed-embedding.pc.new
 mv mozilla-gtkmozembed-embedding.pc.new mozilla-gtkmozembed-embedding.pc
 cat mozilla-gtkmozembed.pc | \
  sed 's#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#' \
  > mozilla-gtkmozembed.pc.new
 mv mozilla-gtkmozembed.pc.new mozilla-gtkmozembed.pc

 cat mozilla-js.pc | \
  sed 's#-I\${includedir}/stable#-I\${includedir}/stable -I\${includedir}/js#' > mozilla-js.pc.new
 mv mozilla-js.pc.new mozilla-js.pc
 cat mozilla-plugin.pc | \
  sed 's#-I\${includedir}/stable#-I\${includedir}/stable -I\${includedir}/java -I\${includedir}/plugin#' \
  > mozilla-plugin.pc.new
 mv mozilla-plugin.pc.new mozilla-plugin.pc

 cat mozilla-nss.pc | sed "s#^Version:.*#Version: ${NSS_VERS}#" > mozilla-nss.pc.new
 cat mozilla-nss.pc.new | \
   sed '
     s#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#
     s#-L\${sdkdir}/lib#-L\${sdkdir}/sdk/lib -R\${libdir} -L\${libdir}#
   ' > mozilla-nss.pc
 cat mozilla-nspr.pc | \
   sed '
     s#prefix=%{_prefix}#prefix=%{_prefix}\nlibdir=%{_libdir}/xulrunner-%{tarball_version}#
     s#-L\${sdkdir}/lib#-R\${libdir} -L\${libdir}#
   ' > mozilla-nspr.pc.new
 mv mozilla-nspr.pc.new mozilla-nspr.pc
)

cd ../..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/xulrunner
%dir %attr (0755, root, bin) %{_libdir}/xulrunner-%{tarball_version}
%{_libdir}/xulrunner-%{tarball_version}/*
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
%dir %attr (0755, root, bin) %{_libdir}/xulrunner-devel-%{tarball_version}
%{_libdir}/xulrunner-devel-%{tarball_version}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/idl
%{_datadir}/idl/*



%changelog
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Many changes to build.
- Add in patches from JDS Firefox3 build.
* Sun Jul 26 2009 - moinakg<at>belenix(dot)org
- Bump to recent SVN version to get TraceMonkey JIT engine.
* Tue Jul 07 2009 - moinakg(at)belenix<dot>org
- Upgrade to 1.9.1 from current mozilla svn.
* Mon Jun 29 2009 - moinakg@belenix.org
- Initial spec file
