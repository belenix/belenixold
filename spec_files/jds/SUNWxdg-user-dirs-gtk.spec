#
# spec file for package SUNWxdg-user-dirs-gtk
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc

Name:                SUNWxdg-user-dirs-gtk
Summary:             GTK Frontend for handling user directories
Version:             0.8
Source:              http://ftp.gnome.org/pub/gnome/sources/xdg-user-dirs-gtk/%{version}/xdg-user-dirs-gtk-%{version}.tar.bz2
Source1:           	 %{name}-manpages-0.1.tar.gz
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %name-root
Requires: SUNWxdg-user-dirs

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
#unzip the manpage tarball
cd %{_builddir}/%{name}-%{version}
gzcat %SOURCE1 | tar xf -
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd xdg-user-dirs-gtk-%{version}
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

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
cd xdg-user-dirs-gtk-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
#Install manpages
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc -d xdg-user-dirs-gtk-%{version} AUTHORS README NEWS
%doc(bzip2) -d xdg-user-dirs-gtk-%{version} COPYING ChangeLog po/ChangeLog
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
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 0.8, change from gz to bz2.
* Fri Apr 04 2008 - darren.kenny@sun.com
- Add manpages
* Fri Feb 22 2008 - darren.kenny@sun.com
- initial version - 0.7
