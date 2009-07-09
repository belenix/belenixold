#
# spec file for package SUNWgnome-xml-root and SUNWgnome-xml-share
#
# includes module(s): sgml-common docbook-dtds docbook-style-dsssl
#                     docbook-style-xsl
#                     all of the above originally taken from Fedora Core 6
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%use common = sgml-common.spec
%use dtds = docbook-dtds.spec
%use dsssl = docbook-style-dsssl.spec
%use xsl = docbook-style-xsl.spec

Name:                    SUNWgnome-xml
SUNW_Pkg:                %{name}-share
Summary:                 docbook SGML and XML stylesheets
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source1:                 docbook-catalog-install.sh
Source2:                 docbook-catalog-uninstall.sh
%include default-depend.inc
Requires: SUNWlxml
Requires: SUNWbash
Requires: SUNWperl584core
# /usr/bin/unzip in SUNWunzip on Nevada, SUNWswmt on Solaris 10.
%if %is_nevada
BuildRequires: SUNWunzip
%else
BuildRequires: SUNWswmt
%endif

%package -n SUNWgnome-xml-root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWgnome-xml-share
Requires: SUNWpostrun-root

%prep
rm -rf %name-%version
mkdir %name-%version
%common.prep -d %name-%version
%dtds.prep -d %name-%version
%dsssl.prep -d %name-%version
%xsl.prep -d %name-%version

%build
%common.build -d %name-%version
%dtds.build -d %name-%version
%dsssl.build -d %name-%version
%xsl.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%common.install -d %name-%version
%dtds.install -d %name-%version
%dsssl.install -d %name-%version
%xsl.install -d %name-%version

install -m 744 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook
install -m 744 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook
touch $RPM_BUILD_ROOT%{_sysconfdir}/xml/catalog

# move collateindex.pl out of /usr/bin
mv $RPM_BUILD_ROOT%{_bindir}/collateindex.pl \
    $RPM_BUILD_ROOT%{_datadir}/sgml/docbook

# move /usr/share/sgml/docbook/xmlcatalog to /etc/xml because it's edited
# by the postinstall script
mv $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xmlcatalog \
    $RPM_BUILD_ROOT%{_sysconfdir}/xml/docbook-xmlcatalog
( cd $RPM_BUILD_ROOT%{_datadir}/sgml/docbook;
    ln -s ../../../../etc/xml/docbook-xmlcatalog xmlcatalog )

# create an empty catalog so that it's included in the pkgmap
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog

# remove stale symlinks -- the files these point to are created by the
# postinstall script, so create the symlink there
rm $RPM_BUILD_ROOT%{_sysconfdir}/sgml/sgml-docbook.cat
rm $RPM_BUILD_ROOT%{_sysconfdir}/sgml/xml-docbook.cat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/install-catalog
%{_bindir}/sgmlwhich
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sgml
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/xml
%{_datadir}/man

%files -n SUNWgnome-xml-root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%ghost %{_sysconfdir}/*
%defattr (-, root, sys)

%post -n SUNWgnome-xml-root
( echo %{_datadir}/sgml/docbook/docbook-catalog-install.sh
) | $BASEDIR/var/lib/postrun/postrun -c JDS


%preun -n SUNWgnome-xml-root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo %{_datadir}/sgml/docbook/docbook-catalog-uninstall.sh
) | $BASEDIR/var/lib/postrun/postrun -c JDS

%changelog
* Wed Mar 21 2007 - laca@sun.com
- update %files after fixing sgml-common
* Wed Feb 28 2007 - halton.huo@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Tue Mar 21 2006 - damien.carbery@sun.com
- Modify BuildRequires to work on s10 and snv, where /usr/bin/unzip in
  different packages.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Add BuildRequires for SUNWunzip.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Add BuildRequires SUNWswmt for /usr/bin/unzip.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Bump to 2.12.
* Thu Sep 08 2005 - brian.cameron@sun.com
- Verified builds fine on Solaris, bump to 2.11.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Tue Feb 24 2004 - laca@sun.com
- Initial version
