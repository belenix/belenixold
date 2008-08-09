#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.9
%define _sessionsdir %{_datadir}/xsessions

Name:                SFEkdebase3
Summary:             Base KDE3 applications, infrastructure files and libraries
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdebase-%{version}.tar.bz2
Source1:             kde.desktop
Source2:             kdm.xml
Source3:             kdmrc
Source4:             backgroundrc
Patch1:              kdebase-01-mwm.diff
Patch2:              kdebase-02-Xsession.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including qt, aRts and others.
Requires: SFEkdelibs3
BuildRequires: SFEkdelibs3-devel
Requires: SFEcyrus-sasl
Requires: %{name}-root

# For md5sum
Requires: SUNWgnu-coreutils

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SFEkdelibs3-root

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEkdelibs3-devel

%package doc
Summary:        %{summary} - documentation
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n kdebase-%version
%patch1 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="-I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="-Wl,-zignore -Wl,-zcombreloc -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"

# Decide whether we can enable the Compositing features. Unfortunately
# the legacy libX11 on Solaris Express does not provide Xutf8SetWMProperties
# function so kompmgr cannot be built. However the FOX bits on Indiana
# does provide a current libX11 from Xorg so composite can be enabled if
# building with FOX bits.

COMPOSITE_ARG=`nm /usr/lib/libX11* 2>/dev/null | grep Xutf8SetWMProperties > /dev/null
if [ $? -eq 0 ]
then
	echo ""
else
	nm /usr/X11/lib/libX11* 2>/dev/null | grep Xutf8SetWMProperties > /dev/null
	if [ $? -eq 0 ]
	then
		echo ""
	else
		nm /usr/openwin/lib/libX11* 2>/dev/null | grep Xutf8SetWMProperties > /dev/null
		if [ $? -eq 0 ]
		then
			echo ""
		else
			echo "--without-composite"
		fi
	fi
fi`

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-ssl-dir=/usr/sfw \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:/usr/include/pcre" \
           --with-pam=yes \
           --without-ldap $COMPOSITE_ARG


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sessionsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sessionsdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kapplications-merged
(cd $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kapplications-merged; ln -s ../applications-merged/kde-essential.menu)

#(cd $RPM_BUILD_ROOT
#    cat %{PATCH2} | gpatch -p0 --fuzz=0)

#
# Copy BeleniX specific branding and customizations to override the default ones
#
cp %{SOURCE3} ${RPM_BUILD_ROOT}/usr/share/config/kdm/
cp %{SOURCE4} ${RPM_BUILD_ROOT}/usr/share/config/kdm/

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/application/graphical-login
cp %{SOURCE2} $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/application/graphical-login

# KDE requires the .la files
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

# Generate binfiles list since we have to specify
# setuid/gid perms for two files.
#
(cd ${RPM_BUILD_ROOT}; find ./%{_bindir}/* | \
    egrep -v "kcheckpass|kdesud" | sed 's/^\.\///' \
    > %{_builddir}/kdebase-%version/kbase_binfiles)

%clean
rm -rf $RPM_BUILD_ROOT

%files -f kbase_binfiles
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (4755, root, bin) %{_bindir}/kcheckpass
%attr (2755, root, bin) %{_bindir}/kdesud
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la*
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*
%dir %attr (0755, root, other) %{_libdir}/kconf_update_bin
%{_libdir}/kconf_update_bin/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*
%dir %attr (0755, root, other) %{_datadir}/applnk
%{_datadir}/applnk/*
%dir %attr (0755, root, other) %{_datadir}/applnk/.hidden
%{_datadir}/applnk/.hidden/*
%dir %attr (0755, root, other) %{_datadir}/applnk/.hidden/.directory
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/wallpapers
%{_datadir}/wallpapers/*
%dir %attr (0755, root, other) %{_datadir}/fonts
%{_datadir}/fonts/*
%dir %attr (0755, root, other) %{_datadir}/templates
%{_datadir}/templates/*
%dir %attr (0755, root, other) %{_datadir}/templates/.source
%{_datadir}/templates/.source/*

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*
%dir %attr (0755, root, bin) %{_datadir}/desktop-directories
%{_datadir}/desktop-directories/*
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/graphical-login
%class(manifest) %{_localstatedir}/svc/manifest/application/graphical-login/kdm.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sat Aug 09 2008 - moinakg@belenix.org
- Moved custom kdmrc and backgroundrc from belenix_constructor.
* Sat Aug 09 2008 - moinakg@belenix.org
- Introduce a documentation package
* Sat Jun 21 2008 - moinakg@gmail.com
- Add patch to fix mwm path.
* Sat Jun 14 2008 - moinakg@gmail.com
- Bump to KDE 3.5.9
- Remove upstream patch.
* Tue Mar 18 2008 - moinakg@gmail.com
- Add missing dependency on root package.
* Sun Feb 24 2008 - moinakg@gmail.com
- Add SMF Manifest for KDM.
- Add Xsession patch to use ctrun on OpenSolaris.
* Tue Jan 22 2008 - moinakg@gmail.com
- Fixed typo in configure options.
* Sun Jan 20 2008 - moinakg@gmail.com
- Updated devel package dependency.
* Sat Jan 19 2008 - moinakg@gmail.com
- Handle a few startkde nits
* Wed Jan 16 2008 - moinakg@gmail.com
- Initial spec.
- Handle setting setuid attributes for non-root builds.
- Add kapplications-merged to properly get kde-essential menu.
