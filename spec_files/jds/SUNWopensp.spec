#
# spec file for package SUNWopensp
#
# includes module(s): OpenSP
#
# Copyright (c) 2003 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
Name:                    SUNWopensp
Summary:                 The OpenJade group's SGML and XML parsing tools
Version:                 1.5.1
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source:                  http://easynews.dl.sourceforge.net/sourceforge/openjade/OpenSP-%{version}.tar.gz
Source1:                  l10n-configure.sh
# date:2004-01-09 type:feature owner:laca
# marking as a feature patch because upstream development stopped years ago
Patch1:			 opensp-01-forte.diff
# date:2009-02-20 type:branding owner:mattman
Patch2:			 opensp-02-manpages.diff
Requires: SUNWlibC
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /usr
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n OpenSP-%{version}
%patch1 -p1 -b .forte
%patch2 -p1

%define INSTALL install -m 755 -s
%define INSTALL_DIR install -d -m 755
%define INSTALL_DATA install -m 644
%define orig_name opensp
%define sgml_dir %{_datadir}/sgml
%define sgml_dir_pkg %{sgml_dir}/%{orig_name}
%define sgml_var_dir /var/lib/sgml

bash -x %SOURCE1 --enable-sun-linguas

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="-z ignore"
export CFLAGS="%optflags"
aclocal
automake -f -c

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

libtoolize --copy --force
autoconf --force
./configure --prefix=%{_prefix} \
	    --datadir=%{_datadir}       \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --localstatedir=%{_localstatedir} \
            --with-gnu-ld \
            --disable-http \
	    --disable-nls \
            --enable-default-catalog="CATALOG:/etc/sgml/catalog:%{sgml_dir}/CATALOG"
make -j$CPUS
perl -pi -e 's/sx/sgml2xml/g; s/SX/SGML2XML/g;' doc/sx.htm
perl -pi -e 's/>sx/>sgml2xml/g; s/>SX/>SGML2XML/g;' doc/{new,index}.htm

%install
[ "$RPM_BUILD_ROOT" != "" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
%{INSTALL_DIR} $RPM_BUILD_ROOT%{_libdir}
# %{INSTALL_DIR} $RPM_BUILD_ROOT%{_includedir}/opensp
make install DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT%{_bindir}
for b in os* onsgmls; do
  ln -sf ${b} ${b#o}
done
# avoid conflict with rzsz package
rm -f sx
ln -sf osx s2x
ln -sf osx sgml2xml
ln -sf osx osgml2xml
popd
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_dir_pkg}
{
  for c in opensp-implied.dcl japan.dcl xml.dcl; do
    %{INSTALL_DATA} pubtext/$c $RPM_BUILD_ROOT%{sgml_dir_pkg}/$c
    echo "-- SGMLDECL \"%{sgml_dir_pkg}/$c\" --"
  done
} > CATALOG.opensp
sed 's|decl|dcl|' pubtext/xml.soc > $RPM_BUILD_ROOT%{sgml_dir_pkg}/xml.soc
%{INSTALL_DIR} $RPM_BUILD_ROOT%{sgml_var_dir}
%{INSTALL_DATA} CATALOG.opensp $RPM_BUILD_ROOT%{sgml_var_dir}
ln -sf ../../../../%{sgml_var_dir}/CATALOG.opensp \
  $RPM_BUILD_ROOT%{sgml_dir}/CATALOG.opensp
rm -fr html
mkdir html
cp doc/catalog doc/*htm html
%define DOCFILES COPYING README NEWS AUTHORS ABOUT-NLS
{
  echo "<html><head><title>OpenSP documentation directory</title></head>"
  echo "<body>"
  for f in %{DOCFILES}; do
    [ -f $f ] || continue
    echo "<a href=\"$f\">$f</a>"
  done
  echo "<a href=\"html/index.htm\">OpenSP</a>, official documentation (html)"
} >index.html

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/OpenSP
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*nsgmls
%{_bindir}/*sgmlnorm
%{_bindir}/*spcat
%{_bindir}/*spam
%{_bindir}/*spent
%{_bindir}/osx
%{_bindir}/*s2x
%{_bindir}/*sgml2xml
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{sgml_dir_pkg}
%{sgml_dir}/CATALOG.opensp

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/OpenSP

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, other) /var/lib
%{sgml_var_dir}/CATALOG.opensp

%changelog
* Fri Feb 20 2009 - matt.keenan@sun.com
- Add manpage page patch, adds ATTRIBUTES and ARC comments to existing pages
- Remove sym-linking of manpages and create shadow pages instead.
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
* Sun Apr 18 2004 - laca@sun.com
- Set correct permissions on %_includedir
* Sat Feb 28 2004 - laca@sun.com
- use cxx_optflags
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
