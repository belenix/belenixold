#
# spec file for package SUNWgnome-img-editor-help
#
# includes module(s): gimp-help
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include Solaris.inc

%use gimp_help = gimp-help.spec

Name:                    SUNWgnome-img-editor-help
Summary:                 The Gimp image editor - on-line help documents
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-img-editor
BuildRequires: SUNWgnome-img-editor-devel
BuildRequires: SUNWgnome-common-devel

%if %build_l10n
%package                 de
Summary:                 Gimp on-line help in German
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                de
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 es
Summary:                 Gimp on-line help in Spanish
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                es
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 fr
Summary:                 Gimp on-line help in French
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                fr
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 it
Summary:                 Gimp on-line help in Italian
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                it
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 ko
Summary:                 Gimp on-line help in Korean
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                ko,ko.UTF-8
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 pl
Summary:                 Gimp on-line help in Polish
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                pl_PL
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 ru
Summary:                 Gimp on-line help in Russian
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                ru_RU
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 sv
Summary:                 Gimp on-line help in Swedish
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                sv
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 cs
Summary:                 Gimp on-line help in Czech
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                cs_CZ
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 zhCN
Summary:                 Gimp on-line help in Simplified Chinese
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                zh,zh.GBK,zh_CN.GB18030,zh.UTF-8
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help

%package                 extra
Summary:                 Gimp on-line help in other languages
SUNW_BaseDir:            %{_basedir}
SUNW_PkgList:            SUNWgnome-img-editor
SUNW_Loc:                nl_BE,nl_NL,no_NO,hr_HR
%include default-depend.inc
Requires:                SUNWgnome-img-editor-help
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gimp_help.prep -d %name-%version

%build
%gimp_help.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gimp_help.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
for loc in cs de es fr hr it ko nl no ru sv zh_CN; do
    rm -rf $RPM_BUILD_ROOT%{_datadir}/gimp/*/help/$loc
    for subdir in callouts dialogs dialogs/examples filters filters/examples \
        glossary math menus preferences tool-options toolbox tutorials using; do
        rm -rf $RPM_BUILD_ROOT%{_datadir}/gimp/*/help/images/$subdir/$loc
    done
done
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/en
%{_datadir}/gimp/*/help/images/*.png
%{_datadir}/gimp/*/help/images/callouts/*.png
%{_datadir}/gimp/*/help/images/dialogs/*.png
%{_datadir}/gimp/*/help/images/dialogs/examples/*.{png,gif,jpg,mng}
%{_datadir}/gimp/*/help/images/filters/*.png
%{_datadir}/gimp/*/help/images/filters/examples/*.{png,jpg,mng,xcf}
%{_datadir}/gimp/*/help/images/glossary/*.png
%{_datadir}/gimp/*/help/images/math/*.png
%{_datadir}/gimp/*/help/images/menus/*.png
%{_datadir}/gimp/*/help/images/menus/*.jpg
%{_datadir}/gimp/*/help/images/preferences/*.png
%{_datadir}/gimp/*/help/images/tool-options/*.png
%{_datadir}/gimp/*/help/images/toolbox/*.png
%{_datadir}/gimp/*/help/images/tutorials/*.{png,jpg}
%{_datadir}/gimp/*/help/images/using/*.{png,jpg}
%doc -d gimp-help-%{gimp_help.version} AUTHORS README quickreference/README
%doc(bzip2) -d gimp-help-%{gimp_help.version} COPYING ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files de
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/de
%{_datadir}/gimp/*/help/images/dialogs/de
%{_datadir}/gimp/*/help/images/filters/de
%{_datadir}/gimp/*/help/images/filters/examples/de
%{_datadir}/gimp/*/help/images/math/de
%{_datadir}/gimp/*/help/images/menus/de
%{_datadir}/gimp/*/help/images/preferences/de
%{_datadir}/gimp/*/help/images/toolbox/de
%{_datadir}/gimp/*/help/images/using/de

%files es
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/es
%{_datadir}/gimp/*/help/images/dialogs/es
%{_datadir}/gimp/*/help/images/filters/es
%{_datadir}/gimp/*/help/images/menus/es
%{_datadir}/gimp/*/help/images/preferences/es
%{_datadir}/gimp/*/help/images/tool-options/es
%{_datadir}/gimp/*/help/images/toolbox/es
%{_datadir}/gimp/*/help/images/using/es

%files fr
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/fr
%{_datadir}/gimp/*/help/images/dialogs/fr
%{_datadir}/gimp/*/help/images/filters/fr
%{_datadir}/gimp/*/help/images/filters/examples/fr
%{_datadir}/gimp/*/help/images/menus/fr
%{_datadir}/gimp/*/help/images/preferences/fr
%{_datadir}/gimp/*/help/images/using/fr
%{_datadir}/gimp/*/help/images/toolbox/fr
%{_datadir}/gimp/*/help/images/tutorials/fr

%files it
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/it
%{_datadir}/gimp/*/help/images/dialogs/it
%{_datadir}/gimp/*/help/images/filters/it
%{_datadir}/gimp/*/help/images/filters/examples/it
%{_datadir}/gimp/*/help/images/menus/it
%{_datadir}/gimp/*/help/images/preferences/it
%{_datadir}/gimp/*/help/images/tool-options/it
%{_datadir}/gimp/*/help/images/toolbox/it
%{_datadir}/gimp/*/help/images/tutorials/it
%{_datadir}/gimp/*/help/images/using/it

%files ko
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/ko
%{_datadir}/gimp/*/help/images/dialogs/ko
%{_datadir}/gimp/*/help/images/toolbox/ko
%{_datadir}/gimp/*/help/images/using/ko

%files pl
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/pl

%files ru
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/ru
%{_datadir}/gimp/*/help/images/dialogs/ru
%{_datadir}/gimp/*/help/images/preferences/ru
%{_datadir}/gimp/*/help/images/using/ru

%files sv
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/*/help/sv

%files cs
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}

%files zhCN
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}

%files extra
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
# nl locale
%{_datadir}/gimp/*/help/nl
%{_datadir}/gimp/*/help/images/dialogs/nl
%{_datadir}/gimp/*/help/images/preferences/nl
%{_datadir}/gimp/*/help/images/using/nl
%{_datadir}/gimp/*/help/images/toolbox/nl
# no locale
%{_datadir}/gimp/*/help/no
%{_datadir}/gimp/*/help/images/dialogs/no
%{_datadir}/gimp/*/help/images/filters/no
%{_datadir}/gimp/*/help/images/filters/examples/no
%{_datadir}/gimp/*/help/images/math/no
%{_datadir}/gimp/*/help/images/menus/no
%{_datadir}/gimp/*/help/images/preferences/no
%{_datadir}/gimp/*/help/images/using/no
%{_datadir}/gimp/*/help/images/toolbox/no
%{_datadir}/gimp/*/help/images/tutorials/no
%endif

%changelog
* Wed Nov 05 2008 - takao.fujiwara@sun.com
- Updated pkgmap

* Mon Sep 15 2008 - matt.keenan@sun.com
- Update copyright

* Fri Apr 25 2008 - damien.carbery@sun.com
- Add pl package after bump to 2.4.1. Remove obsoleted images.

* Fri Jan 11 2008 - laca@sun.com
- create - split from SUNWgnome-img-editor.spec
