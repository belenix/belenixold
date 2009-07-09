#
# spec file for package SUNWopenjade
#
# includes module(s): openjade
#
# Copyright (c) 2003 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

Name:                    SUNWopenjade
Summary:                 DSSSL-Engine for SGML documents
Version:                 1.3.2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source:                  http://umn.dl.sourceforge.net/openjade/openjade-1.3.2.tar.gz
Source1:		 jade_style-sheet.dtd
# date:2004-01-09 owner:laca type:bug state:upstream
# autoconf macros takes from upstream sources
Patch1:			 openjade-01-macros.diff
# date:2004-01-09 owner:laca type:feature
# marked as a feature patch because upstream development stopped years ago
# but it's really a bug fix
Patch2:			 openjade-02-forte.diff
# date:2009-02-20 owner:mattman type:branding
Patch3:			 openjade-03-manpages.diff

%include default-depend.inc
Requires: SUNWopensp
Requires: SUNWlibC
Requires: SUNWlibms

%package devel
Summary:                 %{summary}  - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n openjade-%{version}
cp %SOURCE1 dsssl
%patch1 -p1 -b .macros
%patch2 -p1 -b .forte
%patch3 -p1

%define INSTALL install -m755 -s
%define INSTALL_DIR install -d -m755
%define INSTALL_DATA install -m644
%define orig_name openjade
%define sgml_dir %{_datadir}/sgml
%define sgml_dir_pkg %{sgml_dir}/%{orig_name}
%define sgml_var_dir %{_localstatedir}/lib/sgml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CXXFLAGS="%cxx_optflags"
export LD=/usr/ccs/bin/ld
rm -f aclocal.m4 missing
[ -r config/configure.in ] && mv config/configure.in .
aclocal -I config
autoconf --force
./configure --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --localstatedir=%{_localstatedir} \
  --datadir=%{sgml_dir}/openjade \
  --enable-spincludedir=%_includedir/OpenSP \
  --enable-splibdir=%_libdir \
  --disable-http \
  --enable-mif \
  --enable-default-catalog="CATALOG:/etc/sgml/catalog:%{sgml_dir}/CATALOG"
make -j$CPUS

%install
[ "$RPM_BUILD_ROOT" != "" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
%{INSTALL_DIR} $RPM_BUILD_ROOT%{_libdir} \
  $RPM_BUILD_ROOT%{sgml_dir}/%{orig_name} \
  $RPM_BUILD_ROOT%{_includedir}/%{orig_name}
make install DESTDIR=$RPM_BUILD_ROOT
( cd $RPM_BUILD_ROOT/%_bindir; ln -sf openjade jade )
[ -r jade/openjade-valid-fo ] && install -s jade/openjade-valid-fo $RPM_BUILD_ROOT%{_bindir}
make install-man DESTDIR=$RPM_BUILD_ROOT mandir=%_mandir
%{INSTALL_DATA} generic/*.h $RPM_BUILD_ROOT%{_includedir}/%{orig_name}
%{INSTALL_DATA} grove/Node.h $RPM_BUILD_ROOT%{_includedir}/%{orig_name}
%{INSTALL_DATA} spgrove/GroveApp.h \
                spgrove/GroveBuilder.h $RPM_BUILD_ROOT%{_includedir}/%{orig_name}
%{INSTALL_DATA} style/FOTBuilder.h style/GroveManager.h \
                style/DssslApp.h style/dsssl_ns.h \
                $RPM_BUILD_ROOT%{_includedir}/%{orig_name}
pushd dsssl
%{INSTALL_DATA} catalog dsssl.dtd extensions.dsl fot.dtd style-sheet.dtd \
  builtins.dsl jade_style-sheet.dtd $RPM_BUILD_ROOT%{sgml_dir_pkg}
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_var_dir}
sed 's:"\([^"]*\(dtd\|dsl\)\)"$:"%{sgml_dir_pkg}/\1":' catalog \
  > $RPM_BUILD_ROOT%{sgml_var_dir}/CATALOG.%{orig_name}
ln -sf CATALOG.%{orig_name} $RPM_BUILD_ROOT%{sgml_var_dir}/CATALOG.jade_dsl
cd $RPM_BUILD_ROOT%{sgml_dir} \
  && ln -sf ../../../..%{sgml_var_dir}/CATALOG.%{orig_name} CATALOG.%{orig_name} \
  && ln -sf ../../../..%{sgml_var_dir}/CATALOG.%{orig_name} CATALOG.jade_dsl
popd
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_dir}/James_Clark/dtd
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_dir}/OpenJade/dtd
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_dir}/ISO_IEC_10179:1996/dtd
(cd $RPM_BUILD_ROOT%{sgml_dir}/James_Clark/dtd \
   && ln -sf ../../%{orig_name}/jade_style-sheet.dtd DSSSL_Style_Sheet \
   && ln -sf ../../%{orig_name}/fot.dtd DSSSL_Flow_Object_Tree)
(cd $RPM_BUILD_ROOT%{sgml_dir}/OpenJade/dtd \
   && ln -sf ../../%{orig_name}/style-sheet.dtd DSSSL_Style_Sheet)
(cd $RPM_BUILD_ROOT%{sgml_dir}/ISO_IEC_10179:1996/dtd \
   && ln -sf ../../%{orig_name}/dsssl.dtd DSSSL_Architecture)
# for compatibility with SL <= 8.1
pushd $RPM_BUILD_ROOT%{sgml_dir}
  pushd %{orig_name}
  ln -s ../opensp/japan.dcl .
  ln -s ../opensp/opensp-implied.dcl sp_implied.dcl
  ln -s ../opensp/xml.dcl .
  ln -s ../opensp/xml.soc .
  for d in *.dcl; do
    ln -sf $d ${d/.dcl/.decl}
  done
  popd
popd

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libogrove
%{_libdir}/libogrove.0*
%{_libdir}/libospgrove
%{_libdir}/libospgrove.0*
%{_libdir}/libostyle
%{_libdir}/libostyle.0*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/sgml
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%{_localstatedir}/lib/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Feb 20 2009 - matt.keenan@sun.com
- Add manpages patch, Add ATTRIBUTES and ARC comments, create jade shadow page
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Fri Sep  8 2006 - laca@sun.com
- delete -zignore, fixes CR 6466538
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
- move to /usr
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Sat Oct 02 2004 - laca@sun.com
- moved to /usr/sfw
- added %pkgbuild_postprocess
* Sat Oct 02 2004 - laca@sun.com
- move to /usr/sfw
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files should be in a separate devel package
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Tue Jun 1 2004 - danek.duvall@sun.com
- fix broken symlinks
* Tue Apr 20 2004 - laca@sun.com
- fix %_includedir permissions
- fix %_localstatedir permissions
* Sat Feb 28 2004 - laca@sun.com
- use cxx_optflags
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
