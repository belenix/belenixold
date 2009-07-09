#
# spec file for package SUNWsolaris-devel-docs
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%include Solaris.inc

Name:                    SUNWsolaris-devel-docs
Summary:                 Developer documentation
Version:                 %{default_pkg_version}
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define tarball_version 0.11
Source:                  http://dlc.sun.com/osol/jds/downloads/extras/devguide-%{tarball_version}.tar.bz2
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWgnome-common-devel
BuildRequires:           SUNWgnome-base-libs-devel
%include default-depend.inc

%if 0
%if %build_l10n
%package de
Summary:                 %{summary} - German documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%package es
Summary:                 %{summary} - Spanish documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%package fr
Summary:                 %{summary} - French documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%package ja
Summary:                 %{summary} - Japanese documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%package zhCN
Summary:                 %{summary} - Simplified Chinese documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif
%endif

%prep
%setup -q -n devguide-%{tarball_version}

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc README
%doc(bzip2) COPYING ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc/soldevex/html/developer_guide.html
%{_datadir}/doc/soldevex/html/images
%{_datadir}/doc/soldevex/html/content
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png

%if 0
%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/C/developer_guide.html
%{_datadir}/doc/soldevex/html/C/images
%{_datadir}/doc/soldevex/html/C/content
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png

%if %build_l10n
%files de
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/de/developer_guide.html
%{_datadir}/doc/soldevex/html/de/images
%{_datadir}/doc/soldevex/html/de/content

%files es
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/es/developer_guide.html
%{_datadir}/doc/soldevex/html/es/images
%{_datadir}/doc/soldevex/html/es/content

%files fr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/fr/developer_guide.html
%{_datadir}/doc/soldevex/html/fr/images
%{_datadir}/doc/soldevex/html/fr/content

%files ja
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/ja/developer_guide.html
%{_datadir}/doc/soldevex/html/ja/images
%{_datadir}/doc/soldevex/html/ja/content

%files zhCN
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/soldevex/html/zh_CN/developer_guide.html
%{_datadir}/doc/soldevex/html/zh_CN/images
%{_datadir}/doc/soldevex/html/zh_CN/content
%endif
%endif

%changelog
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Fri Sep 19 2008 - halton.huo@sun.com
- Add %doc part to %files
* Thu Apr 03 2008 - damien.carbery@sun.com
- Add SUNW_Copyright.
* Thu Jan 03 2008 - damien.carbery@sun.com
- Bump to 0.11.
* Thu Nov 29 2007 - damien.carbery@sun.com
- Bump to 0.10 for SXDE 1/08.
* Fri Nov 16 2007 - damien.carbery@sun.com
- Bump to 0.9 for SXDE 1/08.
* Wed Apr 25 2007 - laca@sun.com
- bump to 0.5, delete patch
* Mon Mar 05 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-base-libs/-devel for aclocal.
* Wed Feb 28 2007 - damien.carbery@sun.com
- Add BuildRequires SUNWgnome-common-devel for intltoolize.
* Tue Feb 06 2007 - takao.fujiwara@sun.com
- Added SUNWsolaris-devel-docs-01-g11n-desktop.diff for i18n. CR 6517955. Add
  associated l10n packages.
* Fri Dec  8 2006 - laca@sun.com
- bump to 0.2, update %files
* Wed Dec  6 2006 - laca@sun.com
- use a tarball instead of individual Sources.
* Wed Dec 06 2006 - damien.carbery@sun.com
- Initial spec.
