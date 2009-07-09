#
# spec file for package gqview
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#Owner: bewitche
#bugdb: https://sourceforge.net/tracker/index.php?func=detail&group_id=4050&atid=104050&aid=
#

Summary: Graphics file browser utility.
Name: gqview
Version: 2.0.4
Release: 1
License: GPL
Group: Applications/Multimedia
Source: http://prdownloads.sourceforge.net/gqview/gqview-%{version}.tar.gz
#owner:bewitche date:2008-07-07 bugid:2024250 type:feature
Patch1:       gqview-01-editor.diff
#owner:bewitche date:2008-07-29 type:branding
Patch2:       gqview-02-manpage.diff
#owner:bewitche data:2008-08-21 bugid:2063964 type:bug
Patch3:	      gqview-03-remote.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-root

URL: http://gqview.sourceforge.net

Requires: gtk2 >= 2.4.0

%description
GQview is a browser for graphics files.
Offering single click viewing of your graphics files.
Includes thumbnail view, zoom and filtering features.
And external editor support.

%prep
%setup -q -n gqview-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} 
make -j$CPUS 

#mkdir html
#cp doc/*.html doc/*.txt html/.

%install
rm -rf $RPM_BUILD_ROOT

make mandir=$RPM_BUILD_ROOT%{_mandir} bindir=$RPM_BUILD_ROOT%{_bindir} \
 prefix=$RPM_BUILD_ROOT%{_prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%doc README COPYING TODO html
%{_bindir}/gqview
%{_datadir}/locale/*/*/*
%{_datadir}/applications/gqview.desktop
%{_datadir}/pixmaps/gqview.png
%{_mandir}/man?/*

%changelog
* Wed Sep 03 2008  dermot.mccluskey@sun.com
- Remove gqview-04-desktop.diff - menu entry required for OpenSolaris
* Mon Sep 01 2008  dermot.mccluskey@sun.com
- Add gqview-04-desktop.diff to remove from Launch menu
* Wed Aug 21 2008  chris.wang@sun.com
- Move harry's change to Solaris spec
* Wed Aug 21 2008  chris.wang@sun.com
- Add patch 03-remote to fix bug 6734746, gqview hang will -r option
* Fri Aug 15 2008  harry.fu@sun.com
- Move zh_CN.GB2312 dir to zh_CN dir to fix #6734879
* Wed Jul 30 2008  chris.wang@sun.com
- Add patch gqview-02-manpage.diff to add ARC number and Attributes to manpage
* Tue Jul 22 2008  chris.wang@sun.com
- Add bugdb and bugid
* Thu Jul 17 2008  chris.wang@sun.com
- Add patch gqview-01-editor.diff, the default editor can be selected 
  while configure.
* Tue Jul  7 2008  chris.wang@sun.com 
- Initial build.
