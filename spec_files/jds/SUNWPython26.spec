#
# spec file for package SUNWPython26
#
# includes module(s): Python
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
# Bugdb:http://bugs.python.org/issue
#
%include Solaris.inc

Name:                    SUNWPython26
Summary:                 The Python interpreter, libraries and utilities
Version:                 2.6.1
%define majmin           2.6
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source:                  http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
# test script for the ucred module implemented in Python26-xx-ucred.diff
Source1:                 ucredtest.py
# test script for the dlpi module implemented in Python26-xx-dlpi.diff
Source2:                dlpitest.py
# date:2005-10-27 owner:laca type:bug
# upstreamable
Patch1:                  Python26-01-solaris-lib-dirs.diff
# date:2005-10-30 owner:laca type:feature
Patch2:                  Python26-02-pycc.diff
# date:2006-09-18 owner:laca type:feature
Patch3:                  Python26-03-distutils-pycc.diff
# date:2006-09-18 owner:laca type:bug
# upstreamable
Patch4:                  Python26-04-distutils-log.diff
# date:2006-09-18 owner:laca type:feature
# maybe upstreamable
Patch5:                  Python26-05-isalibs.diff
# date:2006-09-18 owner:laca type:bug bugster:6463378
# maybe upstreamable
Patch6:                  Python26-06-write_compiled_module-atomic.diff
# date:2007-03-23 owner:laca type:feature
# written by John.Levon ported to 2.5 by Peter C Norton
Patch7:                  Python26-07-dtrace.diff
# date:2008-05-23 owner:laca type:bug
# upstreamable
Patch8:                  Python26-08-ctypes.diff
# date:2008-04-10 owner:laca type:feature bugster:6686506
# 2008/243 Python interface to ucred_get(3C)/getpeercred(3C)
# written by John.Levon@Sun.Com
# maybe upstreamable
Patch9:                  Python26-09-ucred.diff
# date:2008-06-06 owner:laca type:bug bugster:6614467 bugid:837046
Patch10:                 Python26-10-gethostname.diff
# date:2008-08-28 owner:laca type:feature
# PSARC/2008/514 Python interface to dlpi(7P)
# written by Max.Zhen@Sun.COM
Patch11:                 Python26-11-dlpi.diff
# date:2009-01-06 owner:fujiwara type:feature bugster:6776575
Patch12:                 Python26-12-encoding-alias.diff
# date:2009-01-23 owner:laca type:bug
Patch13:                 Python26-13-cflags.diff
# date:2009-02-18 owner:wangke type:bug bugid:5289
Patch14:                 Python26-14-ctypes-util-find-library.diff

%include default-depend.inc
BuildRequires: SUNWTk
BuildRequires: SUNWTcl
BuildRequires: SUNWlexpt
BuildRequires: SUNWsfwhea
BuildRequires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWaudh
BuildRequires: SUNWlibffi-devel
Requires: SUNWopenssl-libraries
Requires: SUNWTk
Requires: SUNWTcl
Requires: SUNWlexpt
Requires: SUNWxwplt
Requires: SUNWbzip
Requires: SUNWlibmsr
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWsqlite3
Requires: SUNWlibffi

%package devel
Summary:                 %{summary} - development files
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd Python-%{version}
%patch1 -p1 -b .solaris
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .isalibs
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
cd ..

echo fixing python binary name/path in python scripts:
cat > %{_builddir}/%name-%version/is_python_script <<EOF
#!/bin/sh

head -1 \$1 | egrep -s '^#!.*python$'
EOF
chmod +x %{_builddir}/%name-%version/is_python_script

cat > %{_builddir}/%name-%version/set_python_interpreter <<EOF
#!/bin/bash
interp=\$1
fname=\$2
line1=\$(head -1 \$fname)
echo "Changing '\$line1' to '\$interp' (\$fname)";
chmod u+w \$fname
sed -e "1s,^#!.*,#! \$interp," \$fname > \$fname.update-interp && \
    cat \$fname.update-interp > \$fname && \
    rm -f \$fname.update-interp || \
    echo WARNING: set_python_interpreter failed for \$fname
EOF
chmod +x %{_builddir}/%name-%version/set_python_interpreter

find Python-%{version}/Demo \
     Python-%{version}/Tools \
     Python-%{version}/Doc \
     Python-%{version}/Lib \
     -type f -exec %{_builddir}/%name-%version/is_python_script {} \; \
     -exec %{_builddir}/%name-%version/set_python_interpreter %{_bindir}/python%{majmin} {} \;

%ifarch sparcv9 amd64
cp -pr Python-%{version} Python-%{version}-64
%endif

%build
cd Python-%{version}
autoheader
autoconf
export DFLAGS=-32

export LD_LIBRARY_PATH=`pwd`

%if %cc_is_gcc
OPTFLAGS=`echo "%optflags" | sed 's/march=i586/march=pentium4/'`
GCC_EXTRA_OPTS="-findirect-inlining -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fno-gcse -fivopts -ftree-loop-im"

export CFLAGS="$OPTFLAGS -D_LARGEFILE64_SOURCE `pkg-config --cflags libffi` $GCC_EXTRA_OPTS"
export CPPFLAGS="-D_LARGEFILE64_SOURCE `pkg-config --cflags libffi`"
export LDFLAGS="%_ldflags -L. -L/usr/lib -R/usr/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"
export CC="$CC $GCC_EXTRA_OPTS -fPIC -DPIC -march=pentium4"
export CXX="$CXX $GCC_EXTRA_OPTS -fPIC -DPIC -march=pentium4"
%else
export CC="$CC -xregs=no%frameptr"
export CXX="$CXX -xregs=no%frameptr -norunpath -compat=5"
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE `pkg-config --cflags libffi`"
export CPPFLAGS="-D_LARGEFILE64_SOURCE `pkg-config --cflags libffi`"
export LDFLAGS="%_ldflags -L."
%endif

./configure --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --datadir=%{_datadir} \
  --infodir=%{_datadir}/info \
  --enable-shared \
  --with-system-ffi \
  --disable-static %{?_with_pydebug}

# These #define's break the build with gcc and cause problems when
# building c99 compliant python modules
perl -pi -e 's/^(#define _POSIX_C_SOURCE.*)/\/* $1 *\//' pyconfig.h
perl -pi -e 's/^(#define _XOPEN_SOURCE.*)/\/* $1 *\//' pyconfig.h
perl -pi -e 's/^(#define _XOPEN_SOURCE_EXTENDED.*)/\/* $1 *\//' pyconfig.h

make profile-opt
cd ..

%ifarch sparcv9 amd64
cd Python-%{version}-64

export LD_LIBRARY_PATH=`pwd`

OPTFLAGS64="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export CFLAGS="$OPTFLAGS64 -D_LARGEFILE64_SOURCE `PKG_CONFIG_PATH=%{_libdir}/_arch64 pkg-config --cflags libffi`"
export CPPFLAGS="-D_LARGEFILE64_SOURCE `PKG_CONFIG_PATH=%{_libdir}/_arch64 pkg-config --cflags libffi`"
export CFLAGS="$OPTFLAGS64"
export CC="$CC $OPTFLAGS64"
export CXX="$CXX %cxx_optflags64"
export DFLAGS=-64
export LDFLAGS="%_ldflags -L."

%if %cc_is_gcc
export CFLAGS="$CFLAGS $GCC_EXTRA_OPTS"
export LDFLAGS="$LDFLAGS -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
export CC="$CC $GCC_EXTRA_OPTS -fPIC -DPIC"
export CXX="$CXX $GCC_EXTRA_OPTS -fPIC -DPIC"
%endif

autoheader
autoconf
./configure --prefix=%{_prefix} \
  --libdir=%{_libdir}/%{_arch64} \
  --mandir=%{_mandir} \
  --datadir=%{_datadir} \
  --infodir=%{_datadir}/info \
  --enable-shared \
  --with-system-ffi \
  --disable-static %{?_with_pydebug}

# These #define's break the build with gcc and cause problems when
# building c99 compliant python modules
perl -pi -e 's/^(#define _POSIX_C_SOURCE.*)/\/* $1 *\//' pyconfig.h
perl -pi -e 's/^(#define _XOPEN_SOURCE.*)/\/* $1 *\//' pyconfig.h
perl -pi -e 's/^(#define _XOPEN_SOURCE_EXTENDED.*)/\/* $1 *\//' pyconfig.h

make profile-opt
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ifarch sparcv9 amd64
cd Python-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir}/%{_arch64}
rm -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/idle
rm -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/pydoc
rm -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/smtpd.py
cd ..
%endif

cd Python-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: delete while 2.5 is not the default:
rm $RPM_BUILD_ROOT%{_bindir}/smtpd.py
#mkdir -p $RPM_BUILD_ROOT%{_prefix}/demo/python
#mv $RPM_BUILD_ROOT%{_bindir}/smtpd.py $RPM_BUILD_ROOT%{_prefix}/demo/python/

# FIXME: rename temporarily while 2.5 is not the default:
mv $RPM_BUILD_ROOT%{_mandir}/man1/python.1 $RPM_BUILD_ROOT%{_mandir}/man1/python2.6.1

# the pycc script is a C/C++ compiler wrapper to be used in
# the distutils Makefile
install -m 755 -D pycc $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/pycc
(cd $RPM_BUILD_ROOT%{_libdir}/python%{majmin}; ln -s pycc pyCC)
perl -pi -e 's|^(CC=\s*)/.*$|$1%{_libdir}/python%{majmin}/pycc|' \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e 's|^(CXX=\s*)/.*$|$1%{_libdir}/python%{majmin}/pyCC|' \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e 's|^(INSTALL=\s*)/.*$|$1install|' \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e 's|^(OPT=\s*).*$|$1-DNDEBUG|' \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e 's|^(RUNSHARED=\s*).*$|$1|' \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e "s|^(CONFIG_ARGS=\s*.*'CC=)[^']*('.*)\$|\$1%{_libdir}/python%{majmin}/pycc\$2|" \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e "s|^(CONFIG_ARGS=\s*.*'CFLAGS=)[^']*('.*)\$|\$1\$2|" \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile
perl -pi -e "s|^(CONFIG_ARGS=\s*.*'CPP=)[^']*('.*)\$|\$1%{_libdir}/python%{majmin}/pycc -E\$2|" \
    $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/config/Makefile

# search for vendor packages in /usr/lib/python<version>/vendor-packages
echo "import site; site.addsitedir('%{_libdir}/python%{majmin}/vendor-packages')" \
    > $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/site-packages/vendor-packages.pth
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/vendor-packages

# delete stuff that doesn't build/work on Solaris:
rm $RPM_BUILD_ROOT%{_libdir}/python?.?/config/lib*.a
rm -r $RPM_BUILD_ROOT%{_libdir}/python?.?/bsddb

echo deleting pyo files
find $RPM_BUILD_ROOT -name '*.pyo' -exec rm {} \;

install -m 755 %SOURCE1 $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/test/
install -m 755 %SOURCE2 $RPM_BUILD_ROOT%{_libdir}/python%{majmin}/test/

# FIXME: because python 2.5 is not the default
rm $RPM_BUILD_ROOT%{_bindir}/idle
rm $RPM_BUILD_ROOT%{_bindir}/pydoc

cd $RPM_BUILD_ROOT%{_bindir}
rm python

mkdir -p %{base_isa}
mv python%{majmin} %{base_isa}/isapython%{majmin}
ln -s %{base_isa}/isapython%{majmin} python%{majmin}

%ifarch amd64 sparcv9
cd %{_arch64}
rm python
rm python-config
mv python%{majmin} isapython%{majmin}
ln -s isapython%{majmin} python%{majmin}
# don't need a 64-bit version of this tool
rm 2to3
cd ..
%endif

ln -s ../lib/isaexec isapython%{majmin}
# FIXME: because python 2.5 is not the default
# ln -s python%{majmin} python
rm python-config


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/python%{majmin}
# hard link to isaexec
%hard %{_bindir}/isapython%{majmin}
%dir %attr (0755, root, bin) %{_bindir}/%{base_isa}
%{_bindir}/%{base_isa}/isapython%{majmin}
# FIXME: conflicts with python2.4
#%{_prefix}/demo/python/smtpd.py
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/LICENSE.txt
%{_libdir}/python?.?/*.py*
%{_libdir}/python?.?/*.doc
%{_libdir}/python?.?/compiler
%{_libdir}/python?.?/email
%{_libdir}/python?.?/encodings
%{_libdir}/python?.?/hotshot
%{_libdir}/python?.?/idlelib
%{_libdir}/python?.?/json
%{_libdir}/python?.?/lib-dynload
%{_libdir}/python?.?/lib-tk
%{_libdir}/python?.?/lib-old
%{_libdir}/python?.?/logging
%{_libdir}/python?.?/multiprocessing
%{_libdir}/python?.?/plat-*
%{_libdir}/python?.?/site-packages
%{_libdir}/python?.?/vendor-packages
%{_libdir}/python?.?/xml
%{_libdir}/python?.?/curses
%{_libdir}/python?.?/sqlite3
%{_libdir}/python?.?/wsgiref
%{_libdir}/python?.?/wsgiref.egg-info
%{_libdir}/python?.?/ctypes
%{_libdir}/lib*.so*
%ifarch sparcv9 amd64
%dir %attr(0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr(0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/python%{majmin}
%{_bindir}/%{_arch64}/isapython%{majmin}
%endif
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc(bzip2) -d Python-%{version} README
%doc -d Python-%{version} LICENSE
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/python*-config
%{_bindir}/2to3
%ifarch sparcv9 amd64
%dir %attr(0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/python%{majmin}-config
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%{_libdir}/python?.?/config
%{_libdir}/python?.?/distutils
%{_libdir}/python?.?/lib2to3
%{_libdir}/python?.?/test
%{_libdir}/python?.?/py[cC][cC]

%changelog
* Thu Mar 12 2009 - ke.wang@sun.com
- change bugdb to http://bugs.python.org/issue
- correct the comment format of patch14
* Wed Feb 18 2009 - ke.wang@sun.com
- add patch14 to make ctypes.util.find_library use crle instead of ldconfig
* Fri Jan 23 2009 - laca@sun.com
- add patch cflags.diff, fixes 6792612
* Tue Jan 06 2009 - takao.fujiwara@sun.com
- add patch encoding-alias.diff for Solaris encodings.
* Wed Sep 17 2008 - laca@sun.com
- delete the python-config symlink until python 2.5 becomes the default
- move %{_arch64}/python25-config to -devel
* Thu Aug 28 2008 - laca@sun.com
- add patch dlpi.diff
* Mon Aug 18 2008 - laca@sun.com
- port remaining patches from 2.4
* Wed Aug  8 2007 - laca@sun.com
- add patch shared-expat.diff, fixes 6544688
* Tue Mar 27 2007 - laca@sun.com
- set DFLAGS to fix phelper.d build
* Wed Mar 23 2007 - laca@sun.com
- add patches dtrace.diff and pty-leak.diff
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed CC64. Not needed anymore
* Mon Feb  5 2007 - laca@sun.com
- add --with-pydebug configure option if --with-debug option (of pkgbuild)
  is used
* Mon Feb  5 2007 - laca@sun.com
- restore some rm lines in %install that were accidentally deleted when
  I removed Python 2.3
* Mon Feb  5 2007 - damien.carbery@sun.com
- Delete bsddb files if SUNWevolution-bdb-devel is not installed.
* Sun Feb  4 2007 - laca@sun.com
- remove python 2.3 as per PSARC/2006/666
- define bsddb subpkg which gets built if SUNWevolution-bdb-devel is
  installed
* Tue Dec 05 2006 - damien.carbery@sun.com
- Remove "-j$CPUS" from 'make' calls to fix (parallel) build errors.
* Sat Nov  4 2006 - laca@sun.com
- bump to 2.4.4.  (also fixes 6483597)
- add the curses module to %files
* Tue Oct  3 2006 - laca@sun.com
- add patch Python-06-write_compiled_module-atomic.diff, fixes 6463378
- make the patches not create .patch<n> backup files because some of them
  ended up in the packages
- fix the path to the python interpreter in the .py files before they
  are compiled, fixes 6469243;
* Mon Sep 18 2006 - laca@sun.com
- 64-bit python changes
- Python-01-solaris-lib-dirs.diff: (update) merge for 2.4.3 and fix ssl
  libdir part so that it uses a 64-bit libdir when built in 64-bit mode
- Python-02-pycc.diff: (update) reset IFS correctly; use = not ==;
  add some hacks at the bottom to use the right gcc options, so 64-bit
  can build
- Python-03-distutils-pycc.diff: force using pycc/pyCC so that CC/CXX
  CFLAGS/LDFLAGS are picked up from the environment
- Python-04-distutils-log.diff: fix log.info commands so that they work
  when the '%' char appears in a compiler flags
- Python-05-isalibs.diff: (new) make .so's be generated as foo.so,
  64/foo.so; some really nasty fixes to pyconfig.h: we cannot use the
  compile-time version of SIZEOF, so we hack them in using _LP64.
  We use PY_CHECK_SIZEOF to avoid autoconf automatically adding them
  to pyconfig.h; in the Makefile, make python obey libdir for libpython,
  but still put the generic stuff in /usr/lib/python2.4
  (not /usr/lib/amd64/python2.4...)
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.4.3.
* Tue Jun 20 2006 - damien.carbery@sun.com
- Add BuildRequires of the openssl libraries package (already a 'Requires').
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Sun Oct 30 2005 - laca@sun.com
- change interpreter in python scripts to full path to the appropriate
  version (/usr/bin/python2.4 or /usr/sfw/bin/python2.3), fixes 6318475
- set the C/C++ compiler in the distutils Makefile to the pycc/pyCC
  wrapper scripts, fixes 6247860
* Fri Oct 28 2005 - laca@sun.com
- update to 2.4.2
- build shared libpython and remove the static one, fixes 6199942
- remove XOPEN/POSIX defines from pyconfig.h: fixes 6240077
- add missing dependencies, fixes 6318436
* Tue Sep 27 2005 - laca@sun.com
- omit some unnecessary compiler flags
- remove .pyo files
- add a pth file to site-packages that tells python to search for modules
  in the vendor-packages directory too
- change default permissions to root:bin.
* Wed Oct 19 2005 - damien.carbery@sun.com
- Add another missing runtime dependency, SUNWlibmsr, fixes 6208617.
- Move Pyrex to SUNWPython-extra.spec file.
* Tue Sep 20 2005 - laca@sun.com
- move python 2.4.1 to /usr and keep python 2.3 in /usr/sfw for backcompat
- omit -xregs=no%frameptr as it breaks the build
* Fri Aug 26 2005 - laca@sun.com
- update to 2.4.1
* Tue Aug 02 2005 - laca@sun.com
- added SUNWsfwhea build dependency needed for expat headers
* Tue Aug 02 2005 - damien.carbery@sun.com
- Add SUNWlexpt dependency as the Expat library is required for building.
* Fri Jul 29 2005 - damien.carbery@sun.com
- Add missing runtime dependencies, fixes 6208617.
* Sun Nov 14 2004 - laca@sun.com
- add /usr/sfw/lib to RPATH
* Fri Oct 22 2004 - laca@sun.com
- remove bsddb bits (won't work without bsd db itself), fixes 6176600
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Sep 18 2004 - laca@sun.com
- move to /usr/sfw
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Fri Mar 05 2005 - Niall.Power@sun.com
- remove package root def'n
* Thu Mar 04 2004 - Niall.Power@sun.com
- initial version added to CVS
