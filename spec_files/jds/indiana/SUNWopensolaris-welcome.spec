#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

Name:                SUNWopensolaris-welcome
Summary:             OpenSolaris Welcome document
Version:             0.0.27
Source:              http://dlc.sun.com/osol/jds/downloads/extras/opensolaris-welcome/opensolaris-welcome-%{version}.tar.bz2
SUNW_BaseDir:        /
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
Requires: SUNWPython

%prep
%setup -q -n opensolaris-welcome-%{version}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Most .mo files include the translations of .desktop only.
# We do not want additional packages at the moment.
( \
  cd $RPM_BUILD_ROOT/%_datadir/locale; \
  /bin/ls | grep -v '^de$' | grep -v '^es$' | grep -v '^fr$' | grep -v '^it$' |\
  grep -v '^ja$' | grep -v '^ko$' | grep -v '^pt_BR$' | grep -v '^ru$' |\
  grep -v '^sv$' | grep -v '^zh_CN$' | grep -v '^zh_HK$' | grep -v '^zh_TW$' |\
  xargs /bin/rm -r; \
)


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/opensolaris-about
%{_bindir}/opensolaris-register
%{_bindir}/opensolaris-next-steps
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/opensolaris-welcome
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/opensolaris-welcome/html/C
%{_datadir}/doc/opensolaris-welcome/html/index.html
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/opensolaris-next-steps
%{_datadir}/opensolaris-next-steps/*.png

%dir %attr (0755, root, other) %{_datadir}/locale

%{_datadir}/doc/opensolaris-welcome/html/de
%dir %attr (0755, root, other) %{_datadir}/locale/de
%dir %attr (0755, root, other) %{_datadir}/locale/de/LC_MESSAGES
%{_datadir}/locale/de/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/es
%dir %attr (0755, root, other) %{_datadir}/locale/es
%dir %attr (0755, root, other) %{_datadir}/locale/es/LC_MESSAGES
%{_datadir}/locale/es/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/fr
%dir %attr (0755, root, other) %{_datadir}/locale/fr
%dir %attr (0755, root, other) %{_datadir}/locale/fr/LC_MESSAGES
%{_datadir}/locale/fr/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/it
%dir %attr (0755, root, other) %{_datadir}/locale/it
%dir %attr (0755, root, other) %{_datadir}/locale/it/LC_MESSAGES
%{_datadir}/locale/it/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/ja
%dir %attr (0755, root, other) %{_datadir}/locale/ja
%dir %attr (0755, root, other) %{_datadir}/locale/ja/LC_MESSAGES
%{_datadir}/locale/ja/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/ko
%dir %attr (0755, root, other) %{_datadir}/locale/ko
%dir %attr (0755, root, other) %{_datadir}/locale/ko/LC_MESSAGES
%{_datadir}/locale/ko/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/pt_BR
%dir %attr (0755, root, other) %{_datadir}/locale/pt_BR
%dir %attr (0755, root, other) %{_datadir}/locale/pt_BR/LC_MESSAGES
%{_datadir}/locale/pt_BR/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/ru
%dir %attr (0755, root, other) %{_datadir}/locale/ru
%dir %attr (0755, root, other) %{_datadir}/locale/ru/LC_MESSAGES
%{_datadir}/locale/ru/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/sv
%dir %attr (0755, root, other) %{_datadir}/locale/sv
%dir %attr (0755, root, other) %{_datadir}/locale/sv/LC_MESSAGES
%{_datadir}/locale/sv/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/zh_CN
%dir %attr (0755, root, other) %{_datadir}/locale/zh_CN
%dir %attr (0755, root, other) %{_datadir}/locale/zh_CN/LC_MESSAGES
%{_datadir}/locale/zh_CN/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/zh_HK
%dir %attr (0755, root, other) %{_datadir}/locale/zh_HK
%dir %attr (0755, root, other) %{_datadir}/locale/zh_HK/LC_MESSAGES
%{_datadir}/locale/zh_HK/LC_MESSAGES/*.mo

%{_datadir}/doc/opensolaris-welcome/html/zh_TW
%dir %attr (0755, root, other) %{_datadir}/locale/zh_TW
%dir %attr (0755, root, other) %{_datadir}/locale/zh_TW/LC_MESSAGES
%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo

%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, sys) %dir %{_sysconfdir}/xdg
%attr (0755, root, sys) %dir %{_sysconfdir}/xdg/autostart
%attr (-, root, sys) %{_sysconfdir}/xdg/autostart/*

%changelog
* Tue Apr 07 2009 - matt.keenan@sun.com
- Bump to 0.0.27, fix d.o.o. 7956
* Tue Apr 07 2009 - dave.lin@sun.com
- Removed upstreamed patch 01-po.diff.
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/bin/opensolaris-about (SUNWopensolaris-welcome) requires
  /usr/bin/i86/isapython2.4 which is found in SUNWPython, add the
  dependency.
* Mon Nov 17 2008 - takao.fujiwara@sun.com
- Add opensolaris-welcome-01-po.diff to fix a he.po bug.
* Sat Nov 15 2008 - takao.fujiwara@sun.com
- bump to 0.0.22
* Wed Nov 12 2008 - laca@sun.com
- bump to 0.0.21
* Mon Nov  3 2008 - laca@sun.com
- bump to 0.0.20
* Wed Oct 29 2008 - laca@sun.com
- Bump to 0.0.19
* Fri Oct 24 2008 - glynn.foster@sun.com
- Bump to 0.0.18
* Mon Oct 20 2008 - takao.fujiwara@sun.com
- Bump to 0.0.16. Update opensolaris-desktop.desktop with UI spec.
* Wed Oct 15 2008 - laca@sun.com
- bump to 0.0.15
* Tue Oct 14 2008 - glynn.foster@sun.com
- Once more for luck, 0.0.14
* Tue Oct 14 2008 - glynn.foster@sun.com
- I suck, bumping to 0.0.13
* Tue Oct 14 2008 - glynn.foster@sun.com
- Bump to 0.0.12
* Fri Oct 10 2008 - glynn.foster@sun.com
- Bump to 0.0.11
* Tue Oct 07 2008 - takao.fujiwara@sun.com
- Add opensolaris-welcome-01-g11n-icon-copy.diff to work with xdg.
* Thu Sep 11 2008 - jedy.wang@sun.com
- bump to 0.0.9
* Tue Sep 09 2008 - dave.lin@sun.com
- Remove the upstreamed patch opensolaris-welcome-01-Desktop-dir.diff
- Move opensolaris-icons-copy.sh from /usr/bin to /usr/lib/opensolaris-welcome
* Thu Sep 04 2008 - jedy.wang@sun.com
- bump to 0.0.7
* Wed Sep 03 2008 - dave.lin@sun.com
- Add BuildRequires of SUNWgnome-common-devel
* Sun Aug 17 2008 - laca@sun.com
- add patch Desktop-dir.diff that makes sure $HOME/Desktop is created
  before copying files there
* Thu Aug 14 2008 - laca@sun.com
- also merge the -root pkg in to the base pkg
* Thu Aug 14 2008 - laca@sun.com
- merge l10n content back into SUNWopensolaris-welcome for BTS release
* Tue Aug 12 2008 - takao.fujiwara@sun.com
- Remove opensolaris-welcome-01-comment-out.diff
* Thu Jul 31 2008 - erwann@sun.com
- bump to 0.0.6 
- added root package
* Sat Apr 26 2008 - laca@sun.com
- bump to 0.0.5
- delete "upstream" patch
* Thu Apr 24 2008 - laca@sun.com
- add patch ddu.diff
* Mon Apr 21 2008 - takao.fujiwara@sun.com
- bump to 0.0.4
- Add translations.
* Wed Apr 16 2008 - laca@sun.com
- bump to 0.0.2
- add the new opensolaris-about script
- fix default permissions
* Mon Apr 14 2008 - takao.fujiwara@sun.com
- Add opensolaris-welcome-01-comment-out.diff until translations are delivered.
* Sun Apr 13 2008 - laca@sun.com
- create
