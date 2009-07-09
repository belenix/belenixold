#
# spec file for package SUNWxdg-user-dirs
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc
%include l10n.inc

Name:                SUNWxdg-user-dirs
Summary:             Tool to help manage user directories
Version:             0.10
Source:              http://user-dirs.freedesktop.org/releases/xdg-user-dirs-%{version}.tar.gz
Source1:           	 %{name}-manpages-0.1.tar.gz
Source2:             xdg-user-dirs-update.desktop
Source3:             l10n-configure.sh
Source4:             xdg-user-dirs-po-sun-%{po_sun_version}.tar.bz2
# date:2008-02-15 owner:dkenny type:bug
Patch0:              xdg-user-dirs-01-bugs.diff
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %name-root
Requires: SUNWgnome-base-libs
Requires: SUNWbash
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnu-gettext

%if %build_l10n
%package l10n
Summary:             %{summary} - l10n files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires:            %{name}
%endif

%package root
Summary:             %{summary} - / filesystem
SUNW_BaseDir:        /
%include default-depend.inc


%prep
%setup -c -q -n %{name}-%{version}
cd xdg-user-dirs-%{version}
%patch0 -p1

bzcat %SOURCE4 | tar xf -
cd po-sun; make; cd ..

sed -e "s/TEMPLATES=Templates/TEMPLATES=Documents\/Templates/" \
	-e "s/MUSIC=Music/MUSIC=Documents\/Music/" \
	-e "s/PICTURES=Pictures/PICTURES=Documents\/Pictures/" \
	-e "s/VIDEOS=Videos/VIDEOS=Documents\/Videos/" \
	-e "s/DOWNLOAD=Download/DOWNLOAD=Downloads/" user-dirs.defaults > user-dirs.defaults.$$ 
mv user-dirs.defaults.$$ user-dirs.defaults

sed -e "/\"Download\"/a\\
  \/* SUN_BRANDING *\/\\
  _(\"Downloads\"), \
  \/* SUN_BRANDING *\/\
  _(\"downloads\")," translate.c > translate.c.$$
mv translate.c.$$ translate.c

sed -e "s/^filename_encoding=UTF-8/filename_encoding=locale/" \
  user-dirs.conf > user-dirs.conf.$$
mv user-dirs.conf.$$ user-dirs.conf
cd ..

#unzip the manpage tarball
cd %{_builddir}/%{name}-%{version}
gzcat %SOURCE1 | tar xf -

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd xdg-user-dirs-%{version}
export LDFLAGS="%_ldflags -lglib-2.0"
export CFLAGS="%optflags"

bash -x %SOURCE3 --enable-copyright

aclocal
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir} \
            --sysconfdir=/etc

make -j$CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd xdg-user-dirs-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

#Install manpages
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/xdg/autostart
cp %SOURCE2 $RPM_BUILD_ROOT/etc/xdg/autostart

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*
%doc -d xdg-user-dirs-%{version} AUTHORS README NEWS
%doc(bzip2) -d xdg-user-dirs-%{version} COPYING ChangeLog po/ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*


%changelog
* Fri Jan 23 2009 - takao.fujiwara@sun.com
- Remove patch enable-nls.diff. Use SUNWgnu-gettext instead.
- Add l10n tarball.
* Tue Sep 23 2008 - dave.lin@sun.com
- Change the file attribute to root,bin in l10n pkg to keep consistency with SUNWgnome-l10n*
* Thu Sep 18 2008 - christian.kelly@sun.com
- Remove /usr/share/, /usr/share/doc from -root, which I had added previously in 
  error.
* Fri Sep 15 2008 - christian.kelly@sun.com
- Remove /usr/share/doc from %files.
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Thu Sep 11 2008 - jedy.wang@sun.com
- Fix typo.
* Fri Aug 22 2008 - jedy.wang@sun.com
- Remove option_with_indiana_branding.
* Tue Aug 12 2008 - jedy.wang@sun.com
- Update user-dirs.defaults according to UI spec of OpenSolaris 2008.11.
* Wed May 21 2008 - damien.carbery@sun.com
- Add Requires: SUNWbash to fix 6697951.
* Fri Apr 11 2008 - darren.kenny@sun.com
- Restore desktop file, needs to be run on login after all to fix bug#6682501
* Fri Apr 04 2008 - darren.kenny@sun.com
- Add manpages
* Fri Feb 29 2008 - takao.fujiwara@sun.com
- set filename_encoding=locale
* Mon Feb 25 2008 - darren.kenny@sun.com
- Remove autostart file since the autoastart functionality is now provied by
  xdg-user-dirs-gtk
* Fri Feb 22 2008 - darren.kenny@sun.com
- Moved from spec-files-other/core
* Wed Feb 20 2008 - takao.fujiwara@sun.com
- Add l10n package
* Tue Feb 19 2008 - darren.kenny@sun.com
- Bump to 0.10
* Fri Feb 15 2008 - dermot.mccluskey@sun.com
- added patch comment
- prepend %_ldflags to $LDFLAGS
- set CFLAGS
* Tue Feb 12 2008 - darren.kenny@sun.com
- Updated to create a root pkg and fix a bug in creating of directories.
  Renamed patch to reflect this change.
- Created an autostart desktop file to ensure it's run on startup of desktop.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
