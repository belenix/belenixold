#
# spec file for package SUNWgnome-python-libs
#
# includes module(s): pyorbit gnome-python pygtk2
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
%define pythonver 2.4

%use pyorbit = pyorbit.spec
%use pycairo = pycairo.spec
%use gnome_python = gnome-python.spec
%use pygobject = pygobject.spec
%use pygtk2 = pygtk2.spec
%use pygtksourceview = pygtksourceview.spec

Name:              SUNWgnome-python-libs
Summary:           Python support libraries for GNOME
Version:           %{default_pkg_version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-component
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-print
Requires: SUNWgnome-libs
Requires: SUNWPython-extra
Requires: SUNWjdsrm
Requires: SUNWgnome-config
Requires: SUNWPython
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWmlib
Requires: SUNWgnome-gtksourceview
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-file-mgr-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWPython-extra
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-gtksourceview-devel
BuildRequires: SUNWpython-setuptools

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWPython
# the 2.6 devel package is required because it contains the headers
# (they are not duplicated in this package, since they would be identical)
Requires: SUNWgnome-python26-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%pygobject.prep -d %name-%version
%pycairo.prep -d %name-%version
%pygtk2.prep -d %name-%version
%pyorbit.prep -d %name-%version
%gnome_python.prep -d %name-%version
%pygtksourceview.prep -d %name-%version

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PKG_CONFIG_PATH=../pyorbit-%{pyorbit.version}:../pygtk-%{pygtk2.version}:%{_pkg_config_path}:../pygobject-%{pygobject.version}:../pycairo-%{pycairo.version}
export PYTHON="/usr/bin/python2.4"
export CPPFLAGS="-I/usr/xpg4/include -I/usr/include/python%{pythonver}"
export CFLAGS="%optflags -I/usr/xpg4/include -I%{_includedir} -I/usr/include/python%{pythonver} -I%{_builddir}/%name-%version/pyorbit-%pyorbit.version/src -I%{_builddir}/%name-%version/pycairo-%pycairo.version/cairo"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-L/usr/lib/python2.4/pygobject -R/usr/lib/python2.4/pygobject %_ldflags"
export PYCC_CC="$CC"
export PYCC_CXX="$CXX"
export EXTRA_CFLAGS="-R%{_libdir}/python%{pythonver}/pygobject"

%pygobject.build -d %name-%version
%pycairo.build -d %name-%version
%pygtk2.build -d %name-%version
cd %name-%version/pygtk-%{pygtk2.version}
ln -s gtk/*.defs .
ln -s gtk pygtk
cd ../..
%pyorbit.build -d %name-%version
echo 'PYTHONPATH=%{_builddir}/%name-%version/pygobject-%{pygobject.version}/codegen:$PYTHONPATH /usr/bin/python %{_builddir}/%name-%version/pygobject-%{pygobject.version}/codegen/codegen.py "$@"' > %{_builddir}/%name-%version/pygtk-codegen-2.0
chmod a+x %{_builddir}/%name-%version/pygtk-codegen-2.0
export PATH=%{_builddir}/%name-%version:$PATH
%gnome_python.build -d %name-%version
export CFLAGS="`echo %optflags | sed -e 's/-xregs=no.frameptr//'`"
%pygtksourceview.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%pygobject.install -d %name-%version
%pycairo.install -d %name-%version
%pygtk2.install -d %name-%version
%pyorbit.install -d %name-%version
%gnome_python.install -d %name-%version
%pygtksourceview.install -d %name-%version

# move to vendor-packages
if [ -x $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages ]; then
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages
fi

# Move demo to demo directory.
#
install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
mv $RPM_BUILD_ROOT%{_bindir}/pygtk-demo $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/pygtk-demo

# avoid conflicts with 2.5 and 2.6:
cd $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules
mv libpythonmethod.so libpythonmethod-%{pythonver}.so
ln -s libpythonmethod-%{pythonver}.so libpythonmethod.so

# these are included in SUNWgnome-python26-libs
rm -r $RPM_BUILD_ROOT%{_bindir}

# move to subdir to avoid conflict with Python 2.5 and Python 2.6
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/pygobject
mv $RPM_BUILD_ROOT%{_libdir}/libpyglib-2.0.so* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/pygobject
mv $RPM_BUILD_ROOT%{_libdir}/pygtk \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/pygobject

# these are included in SUNWgnome-python26-libs-devel:
rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/pkgconfig

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/vendor-packages
%{_libdir}/python?.?/pygobject
%{_libdir}/gnome-vfs-2.0/modules/libpythonmethod*.so

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/python2.4/pkgconfig
%{_libdir}/python2.4/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_prefix}/demo
%dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds
%dir %attr (0755, root, bin) %dir %{_prefix}/demo/jds/bin
%{_prefix}/demo/jds/bin/pygtk-demo

%changelog
* Wed Mar 25 2009 - li.yuan@sun.com
- Move pyspi from SUNWgnome-python-libs to SUNWgnome-a11y-libs.
* Tue Nov 25 2008 - laca@sun.com
- re-add libpyglib.so* but move in a subdir because it is dependent on
  the python version so we need to include it in both the 2.4 and the 2.5
  package.
- remove references to SUNWgnome-python-libs-common
* Mon Nov 24 2008 - laca@sun.com
- remove bits included in SUNWgnome-python-libs-common, which is defined in
  SUNWgnome-python25-libs.spec
* Wed Sep 17 2008 - laca@sun.com
- set PYTHON to python2.4 (instead of just python) to make sure the
  right version is used for the build
* Tue Aug 12 2008 - damien.carbery@sun.com
- Add %{_libdir}/libpyglib-2.0.so* to %files.
* Mon Aug 11 2008 - damien.carbery@sun.com
- Move site-packages to vendor-packages here because pygobject 2.15.2 borked
  when vendor-packages was specified by pyexecdir and pythondir in make
  install.
* Tue Oct 16 2007 - damien.carbery@sun.com
- Remove unnecessary environment variable settings.
* Mon Oct  8 2007 - damien.carbery@sun.com
- Add SUNWgnome-gtksourceview dependency as it is required to by
  pygtksourceview.
* Sun Oct  7 2007 - damien.carbery@sun.com
- Add pygtksourceview as it is required to build python bindings in gedit.
* Fri Sep 28 2007 - laca@sun.com
- delete some unnecessary env vars
* Fri Aug 31 2007 - damien.carbery@sun.com
- Remove pygtksourceview.spec. It is still not building and isn't required.
* Thu Jul 05 2007 - damien.carbery@sun.com
- Add pygtksourceview.spec, but disable it because it is not building yet.
* Tue Jan  9 2007 - laca@sun.com
- define PYCC_CC and PYCC_CXX to override what the configure script sets
  in CC/CXX
* Mon Aug 28 2006 - damien.carbery@sun.com
- Fix typo in PKG_CONFIG_PATH data (s/=/-/).
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri May 12 2006 - damien.carbery@sun.com
- Small update to dependency list after check-deps.pl run.
* Thu May 11 2006 - brian.cameron@sun.com
- Move pygtk-demo to demo directory.
* Wed Apr  5 2006 - damien.carbery@sun.com
- Add pygobject. It has been moved from pygtk2.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Jan 09 2006 - damien.carbery@sun.com
- Add gnome-vfs module.
* Thu Oct 27 2005 - laca@sun.com
- add pygtk2
* Tue Sep 20 2005 - laca@sun.com
- move to /usr as Python was also moved there
* Thu Sep 01 2005 - damien.carbery@sun.com
- Remove unused pygtk2 references.
* Wed Aug 30 2005 - damien.carbery@sun.com
- Add Build/Requires for SUNWgnome-file-mgr (nautilus) and SUNWgnome-print
  (libgnomeprint/libgnomeprintui) so that those submodules will be built.
* Mon Aug 29 2005 - rich.burridge@sun.com
- Adjusted to put files under /usr/sfw
* Thu Aug 25 2005 - rich.burridge@sun.com
- Removed the 'export CC="/opt/SUNWspro/bin/cc"' line. No longer needed.
* Mon Aug 22 2005 - rich.burridge@sun.com
- Adjustments needed to make the package proto maps equivalent to what gets
  installed via "make install"
* Thu Aug 11 2005 - rich.burridge@sun.com
- initial version
