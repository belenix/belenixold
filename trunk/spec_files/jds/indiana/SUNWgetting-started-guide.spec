#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

Name:                SUNWgetting-started-guide
Summary:             Indiana Getting Started Guide
Version:             1.0.1
Source:              http://dlc.sun.com/osol/jds/downloads/extras/getting-started-guide/getting-started-guide-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-de
Summary:             %{summary} for German
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            de
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-es
Summary:             %{summary} for Spanish
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            es
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-fr
Summary:             %{summary} for French
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            fr
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-it
Summary:             %{summary} for Italian
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            it
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-ja
Summary:             %{summary} for Japanese
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            ja,ja_JP.PCK,ja_JP.UTF-8
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-ko
Summary:             %{summary} for Korean
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            ko,ko.UTF-8
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-ptBR
Summary:             %{summary} for Portugese Brazilian
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            pt_BR
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-ru
Summary:             %{summary} for Portugese Russian
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            pt_BR
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-sv
Summary:             %{summary} for Swedish
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            sv
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-zhCN
Summary:             %{summary} for Simplified Chinese
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            zh,zh.GBK,zh_CN.GB18030,zh.UTF-8
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-zhHK
Summary:             %{summary} for Hong Kong Chinese
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            zh_HK.BIG5HK,zh_HK.UTF-8
SUNW_PkgList:        %{name}
%include default-depend.inc

%package -n          SUNWgetting-started-l10n-zhTW
Summary:             %{summary} for Traditional Chinese
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
SUNW_Loc:            zh_TW,zh_TW.BIG5,zh_TW.UTF-8
SUNW_PkgList:        %{name}
%include default-depend.inc

%prep
%setup -q -n getting-started-guide-%{version}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/C
%{_datadir}/doc/getting-started/html/index.html

%files -n SUNWgetting-started-l10n-de
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/de

%files -n SUNWgetting-started-l10n-es
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/es

%files -n SUNWgetting-started-l10n-fr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/fr

%files -n SUNWgetting-started-l10n-it
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/it

%files -n SUNWgetting-started-l10n-ja
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/ja

%files -n SUNWgetting-started-l10n-ko
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/ko

%files -n SUNWgetting-started-l10n-ptBR
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/pt_BR

%files -n SUNWgetting-started-l10n-ru
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/ru

%files -n SUNWgetting-started-l10n-sv
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/sv

%files -n SUNWgetting-started-l10n-zhCN
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/zh_CN

%files -n SUNWgetting-started-l10n-zhHK
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/zh_HK

%files -n SUNWgetting-started-l10n-zhTW
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/getting-started/html/zh_TW

%changelog
* Tue Apr  9 2009 - laca@sun.com
- bump to 1.0.1
* Tue Mar 31 2009 - laca@sun.com
- bump to 1.0.0
* Sat Nov 15 2008 - takao.fujiwara@sun.com
- bump to 0.9.2
* Wed Nov 12 2008 - laca@sun.com
- bump to 0.9.1
* Tue Oct 28 2008 - laca@sun.com
- bump to 0.9.0
* Tue Oct 14 2008 - laca@sun.com
- bump to 0.8.0
* Tue Aug 12 2008 - takao.fujiwara@sun.com
- bump to 0.7.1. Updated $lang/index.html with the latest link.
* Tue Aug  5 2008 - laca@sun.com
- bump to 0.7.0; delete patches
* Thu May 15 2008 - takao.fujiwara@sun.com
- Add getting-started-guide-02-po.diff. Fixes #1514.
* Mon Apr 21 2008 - laca@sun.com
- add patch refresh-0.diff
- get the version of opensolaris-welcome from SUNWopensolaris-welcome.spec
* Mon Apr 21 2008 - takao.fujiwara@sun.com
- Add getting-started-guide-01-refresh-0.diff to set interval 0.
- Add opensolaris-welcome translations for a workaround. bug #1358
* Wed Apr 16 2008 - laca@sun.com
- fix default permissions
* Mon Apr 14 2008 - takao.fujiwara@sun.com
- bump to 0.6.5
* Wed Apr  9 2008 - laca@sun.com
- bump to 0.6.4
* Fri Apr 04 2008 - takao.fujiwara@sun.com
- Add SUNW_PkgList
* Fri Apr  4 2008 - laca@sun.com
- bump to 0.6.3
* Thu Apr 03 2008 - takao.fujiwara@sun.com
- Add l10n packages
- bump to 0.6.2
* Tue Apr  1 2008 - laca@sun.com
- bump to 0.6.1
* Wed Mar 26 2008 - laca@sun.com
- bump to 0.6.0
* Mon Mar 24 2008 - laca@sun.com
- add copyright file
* Tue Feb  5 2008 - laca@sun.com
- bump to 0.5
* Mon Oct 29 2007 - laca@sun.com
- bump to 0.3
* Wed Oct 24 2007 - laca@sun.com
- bump to 0.2
* Sat Oct 20 2007 - laca@sun.com
- create
