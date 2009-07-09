#
# spec file for package SUNWhamster
#
# includes module(s): hamster
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
#

%include Solaris.inc

%define pythonver 2.4

Name:                    SUNWhamster
License:                 GPL v3 
Summary:		 Time tracking for masses	
Version:                 2.26.0
Source:                  http://ftp.gnome.org/pub/GNOME/sources/hamster-applet/2.26/hamster-applet-%{version}.tar.gz
#date:2008-11-27 owner:wangke bugster:6776761 type:branding
Patch1:			 hamster-01-hotkey.diff
URL:                     http://live.gnome.org/ProjectHamster
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWpysqlite
BuildRequires:     SUNWPython-devel
BuildRequires:     SUNWgnome-python-desktop
Requires:          SUNWsqlite3
Requires:          SUNWpysqlite
Requires:          SUNWPython
Requires:          SUNWgnome-python-desktop
Requires:          %{name}-root
Requires:          SUNWdesktop-cache

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif
 
%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%prep
%setup -q -n hamster-applet-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"

./configure --prefix=%{_prefix} \
	    --sysconfdir=%{_sysconfdir}    \
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --mandir=%{_mandir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# move to verndor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/hamster/keybinder/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif
 
%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%doc AUTHORS
%doc(bzip2) COPYING NEWS
%doc(bzip2) ChangeLog README
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%attr (-, root, other) %{_datadir}/icons/*/*/apps
%{_datadir}/gnome-control-center
%{_datadir}/hamster-applet 

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/hamster-applet.schemas
 
%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 17 2009 - ke.wang@sun.com
- Bump to 2.26.0
* Thu Mar 05 2009 - ke.wang@sun.com
- Bump to 2.25.92
* Tue Mar 03 2009 - brian.cameron@sun.com
- Remove .la files.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Mon Feb 09 2009 - jijun.yu@sun.com
- Remove the comments.
* Mon Feb 09 2009 - jijun.yu@sun.com
- Correct site-packages to vendor-packages to fix #6802053.
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
- Remove patches/hamster-02-g11n-strftime.diff.
* Jerry Jan 23 2008 - jijun.yu@sun.com
- Bump to 2.25.3.
* Mon Dec 22 2008 - takao.fujiwara@sun.com
- Add hamster-02-g11n-strftime.diff for none UTF-8.
* Thu Dec 4 2008 - jijun.yu@sun.com
- Install the schemas file to right palce using sysconfdir
- Use post/preun scripts to install schemas into the merged gconf files
* Mon Dec 1 2008 - jijun.yu@sun.com
- Change Patch 1 to branding type.
* Thu Nov 27 2008 - jijun.yu@sun.com
- Add Patch 1 to fix bugster #6776761.
* Tue Nov 25 2008 - jijun.yu@sun.com
- Bump to 2.24.2.
* Mon Nov 24 2008 - jijun.yu@sun.com
- Add Requires and Buildrequires.
* Thu Nov 20 2008 - jijun.yu@sun.com
- Add %build_l10n section and correct attributes for some files.
* Thu Nov 13 2008 - jijun.yu@sun.com
- Move from sfe to spec-files.
* Tue Nov 11 2008 - jijun.yu@sun.com
- Add BuildRequires.
* Wed Oct 22 2008 - jijun.yu@sun.com
- Bump to 2.24.1
* Tue Oct 07 2008 - jijun.yu@sun.com
- Initial spec
