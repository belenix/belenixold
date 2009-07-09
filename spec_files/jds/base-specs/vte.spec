#
# spec file for package vte
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         vte
License:      LGPL v2
Group:        System/Libraries
Version:      0.20.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Terminal Emulation Widget Library
Source:       http://download.gnome.org/sources/%{name}/0.20/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
AutoReqProv:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.10.0
%define python_version 2.4

Requires:      gtk2 >= %{gtk2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: python >= %{python_version}

%description
VTE is a terminal emulation widget for GTK+, used in GNOME Terminal.

%package devel
Summary:	Terminal Emulation Widget Development Library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk2-devel >= %{gtk2_version}

%description devel
VTE is a terminal emulation widget for GTK+, used in GNOME Terminal.

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
gtkdocize
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --datadir=%{_datadir} 	\
	    --libexecdir=%{_libexecdir} \
	    %{gtk_doc_option}

make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

# Clean up unpackaged files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%attr(2711,root,utmp) %{_libexecdir}/gnome-pty-helper
%{_datadir}/%{name}
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/*
%{_libdir}/*.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_libdir}/pkgconfig/*
%{_libdir}/python2.4/vendor-packages/gtk-2.0/vtemodule.so

%changelog
* Tue Mar 17 2009 - halton.huo@sun.com
- Bump to 0.20.0
- Remove upstreamed patches: static-func.diff, ncurses-typo.diff and
  alloca.diff
- Add patch gtkdoc-rebase.diff to fix bugzilla #575793
* Tue Mar 03 2009 - brian.cameron@sun.com
- Use find command to remove .a and .la files.
* Tue Feb 02 2009 - christian.kelly@sun.com
- Take out line that rm's gtk-2.0/*.a.
* Fri Dec 26 2008 - halton.huo@sun.com
- Bump to 0.19.4
- Add patch static-func.diff to fix bugzilla #565663
- Add patch ncurses-typo.diff to fix bugzilla #565675
- Add patch alloca.diff to fix bugzilla #565679
* Fri Dec 05 2008 - brian.cameron@sun.com
- Remove upstream patches vte-01-update-utmpx.diff and
  vte-02-g11n-ambigous-wide.diff.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 0.19.1
* Fri Nov 28 2008 - takao.fujiwara@sun.com
- Add vte-02-g11n-ambigous-wide.diff to show some chars on Shift_JIS correctly.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 0.17.4.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 0.17.3.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 0.17.1.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Bump to 0.16.14.
* Tue Apr 15 2008 - brian.cameron@sun.com
- Add patch vte-01-update-utmpx.diff patch.  This patch was written by
  Arvind Samptur (Arvind.Samptur@Sun.COM) to integrate into Solaris 10.
  However, this patch has not able to go upstream in the 2.22 timeframe
  so Arvind asked me to integrate this patch for now.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 0.16.13.
* Tue Jan 08 2007 - damien.carbery@sun.com
- Bump to 0.16.12.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 0.16.11.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 0.16.10.
* Mon Dec 03 2007 - takao.fujiwara@sun.com
- Remove vte-02-inputmethod-spotlocation.diff to replace the gtk patch.
* Tue Nov 06 2007 - brian.cameron@sun.com
- Remove stale vte-03-selection-perf-improve.diff patch.  It does not 
  improve performance and it was rejected by the maintainer.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 0.16.9. Remove upstream patch, 03-cut-copy-paste-handle. Renumber
  rest.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 0.16.8.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 0.16.7.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 0.16.6.
* Tue May 29 2007 - damien.carbery@sun.com
- Bump to 0.16.4. Remove upstream patches, 05-g11n-segv-preedit and 
  06-terminal-access-visibility-notify.
* Fri May 25 2007 - yi.jin@sun.com
- Add vte-06-terminal-access-visibility-notify.diff. Fixes 6556709.
  The signal callback function should return FALSE to let the rest of
  callback functions get called.
* Mon Apr 30 2007 - damien.carbery@sun.com
- Bump to 0.16.3.
* Fri Apr 27 2007 - takao.fujiwara@sun.com
- Add vte-05-g11n-segv-preedit.diff. Fixes 6548846
* Tue Apr 24 2007 - damien.carbery@sun.com
- Bump to 0.16.2. Remove upstream patch 04-utf8-ambiguous. Renumber rest.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Remove upstream patch, 06-nullptr-check.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Bump to 0.16.1.
* Wed Apr  4 2007 - dougs@truemail.co.th
- Added patch vte-06-nullptr-check.diff to fix bugzilla 425767.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 0.16.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 0.15.6.
* Wed Feb 28 2007 - damien.carbery@sun.com
- Bump to 0.15.5. Remove upstream patch 06-environ.
* Wed Feb 14 2007 - damien.carbery@sun.com
- Remove upstream patch, 06-vte-pty-open. Add patch, 06-environ to fix #407839.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 0.15.3.
* Thu Feb 08 2007 - brian.cameron@sun.com
- Remove unneeded patch vte-01-vtefc.diff.  Now FC_WIDTH is defined on
  Solaris, so it's no longer needed to wrap it with #ifdef FC_WIDTH.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Add patch, 07-vte-pty-open, to sync func declaration with definition; #400184.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 0.15.2. Remove upstream patch, 06-get-text. Renumber remainder.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 0.15.1.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 0.15.0.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 0.14.1.
* Thu Sep 14 2006 - matt.keenan@sun.com
- Remove patch vte-08-pre-edit-crash-on-close.diff, as causing
  two bugs, 6453098, and 6465619, and removing does not re-introduce 6193929.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 0.14.0.
* Fri Aug 25 2006 - damien.carbery@sun.com
- Bump to 0.13.7.
* Mon Aug 21 2006 - damien.carbery@sun.com
- Bump to 0.13.6.
* Tue Aug 01 2006 - damien.carbery@sun.com
- Bump to 0.13.5.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Remove upstream patch, 05-update-logout-record. Rename remaining.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 0.13.4.
* Fri Jul 21 2006 - padraig.obriain@sun.com
- Bump to 0.13.3 for gnome 2.15.
- Remove patch vte-07-g11n-word-char.diff as this issue is addressed,
  slightly differently, in vte code. 
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 0.12.2.
* Thu Apr 27 2006 - damien.carbery@sun.com
- Remove upstream patch, vte-12-msgfmt-no-c-param.diff.
* Thu Apr 27 2006 - damien.carbery@sun.com
- Bump to 1.12.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Add patch, 12-msgfmt-no-c-param, to remove '-c' param from msgfmt call. That
  switch breaks Solaris build.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.12.0.
* Thu Mar  9 2006 - damien.carbery@sun.com
- Bump to 0.11.21.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 0.11.20.
- Remove upstream patch, 08-logname. Renumber 12-g11n-word-char to 08.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Enable freetype test in configure. Somehow this makes it build.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 0.11.18.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 0.11.17
* Mon Jan 16 2006 - damien.carbery@sun.com
- Remove upstream patch 08-fix-crash; rename 13-logname to 08-logname.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 0.11.16
* Thu Oct 27 2005 - laca@sun.com
- move the python stuff from site-packages to vendor-packages
* Tue Sep 06 2005 - damien.carbery@sun.com
- Remove upstream patch, vte-04-a11y-selection.diff. Reorder remaining.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.15.
* Thu Aug 25 2005 - damien.carbery@sun.com
- Add python build dependency and add python modules back into %files.
* Wed Aug 24 2005 - damien.carbery@sun.com
- Remove python references as the module doesn't generate any.
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 0.11.14.
* Fri May 13 2005 - balamurali.viswanathan@wipro.com
- Bump to 0.11.13
* Wed Mar 16 2005 - takao.fujiwara@sun.com
- Added vte-14-g11n-word-char.diff fo select localized strings exactly.
  Fix 6241338.
* Wed Nov 24 2004 - narayana.pattipati@wipro.com
- Updated the patch vte-11-scrolling-perf-improve.diff to chnage 
  vte input buffer size to 2K. Fixes bugtraq bug#6198452.
  Patch reviewed by ghee.teo@sun.com
* Fri Nov 12 2004 - suresh.chandrasekharan@sun.com
- Added patch vte-13-preddit-crash-on-close.diff
  Bugster #6193929
* Fri Nov 05 2004 - balamurali.viswanathan@wipro.com
- Added patch vte-12-selection-perf-improve.diff to improve selection
  performance 
* Fri Oct 29 2004 - narayana.pattipati@wipro.com
- Added patch vte-11-scrolling-perf-improve.diff to improve scrolling 
  performance of gnome-terminal based on VTE. The patch improves the 
  performance of the issues mentioned in bugtraq bug#5014824. Most of 
  the patch is taken from the patch given to bugzilla bug#143914.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add vte.1, libvte.3 man pages
* Wed Oct 27 2004 - padraig.obriain@sun.com
- Add patch vte-10-get-text.diff to fix bugzilla 156161.
* Mon Oct 18 2004 - padraig.obriain@sun.com
- Add patch vte-09-fix-crash.diff to fix bug 5107420.
* Sat Oct 09 2004 - federic.zhang@sun.com
- Add patch vte-08-utf8-ambiguous.diff to fix bug 5028816
  gnome-terminal display full-width characters as half-width on UTF-8
* Fri Oct 08 2004 - archana.shah@wipro.com
- Added patch vte-07-update-logout-record.diff
  Fixes bug#5084840
* Mon Oct 04 2004 - narayana.pattipati@wipro.com
- Added patch vte-06-cut-copy-paste-handle.diff to make Sun Cut,
  Copy, Paste keys work in gnome-terminal. Fixes bug#5098217
* Thu Aug 26 2004 - hidetoshi.tajima@sun.com
- Add patch vte-05-inputmethod-spotlocation.diff for bugzilla #150052,
  bugtraq #5080038
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Thu Jul 22 2004 - padraig.obriain@sun.com
- Add patch vte-04-a11y-selection.diff for bugzilla #113590
* Sun Jul 11 2004 - niall.power@sun.com
- build fixup
* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4
- removed auto*-jds stuff, not needed with SuSE 9.1
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to vte-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - ghee.teo@sun.com
- updated vte.spec to remove the ifos from around gnome-pty-helper
  essentially yo revert back to what it was.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Jun 22 2004 <federic.zhang@sun.com>
- Based on the 0.11.11 version, recreate the vte-03-fcconfig.diff patch
* Mon Jun 14 2004 ghee.teo@sun.com
- Fixes stopper bug 5062671, not to use gnome-pty-helper on Solaris.
  Essentially just don't include the binary in Solaris.
* Fri Jun 11 2004 damien.carbery@sun.com
- Added patch to add '-lglib-2.0' to src/Makefile.am to build on Solaris sparc.
* Thu Jun 10 2004 johan.steyn@sun.com
- Changed to use correct autotools, hence no longer need autotools patch
* Wed Jun 09 2004 damien.carbery@sun.com
- Add '--disable-freetypetest' configure switch because S9x86 build fails when
  configure tries to run the test app, because /opt/jds/lib not in
  LD_LIBRARY_PATH or -R link parameter.
* Tue Jun 08 2004 johan.steyn@sun.com
- Update to 0.11.11 tarball
* Mon May 17 2004 - <federic.zhang@sun.com>
- Fixed bug 5042257 by adding patch vte-02-fcconfig.diff
  [Cinnabar Linux] The CJK font rendering in gnome-terminal is not acceptable
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to vte-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to vte-l10n-po-1.0.tar.bz2
* Tue Feb 24 2004 - <matt.keenan@sun.com>
- Update Distro, l10n tarball
* Thu Feb 12 2004 - <niall.power@sun.com>
- Added patch #01 to create an *-uninstalled-pc.file
- Autotoolize the build stage
* Fri Oct 17 2003 - <michael.twomey@sun.com> - 0.11.10-1
- Uprevved to GNOME 2.4.0 version.
- Changed source url.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a
* Tue May 13 2003 - ghee.teo@sun.com
- initial Sun release
