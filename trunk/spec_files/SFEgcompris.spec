#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)

Name:                SFEgcompris
License:             GPL
Summary:             gcompris - A Free Educational Suite for Kids
Version:             8.4.7
URL:                 http://gcompris.net/
Source:              http://heanet.dl.sourceforge.net/sourceforge/gcompris/gcompris-8.4.7.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevant deps including kdelibs, qt, aRts and others.
Requires: gnuchess
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnu-libiconv
BuildRequires: SUNWgnu-libiconv-devel
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWxorg-headers
Requires: SUNWtexi
Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3-devel
Requires: SUNWPython
Requires: SUNWgnome-python-libs
BuildRequires: SUNWgnome-python-libs-devel
Requires: pysqlite
%if %SFEfreetype
Requires: SFEfreetype
BuildRequires: SFEfreetype-devel
%else
Requires: SUNWfreetype2
BuildRequires: SUNWfreetype2
%endif

%if %build_l10n
%package l10n
Summary:                 gcompris_l10n - l10n files for GCompris
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gcompris-%version

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%{gnu_lib_path} -liconv -lintl %_ldflags %{xorg_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl -lglib-2.0 -lpangoft2-1.0"

extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"
%if %SFEfreetype
export FREETYPE_CONFIG=%{sfw_bin}/freetype-config
%else
export FREETYPE_CONFIG=%{gnu_bin}/freetype-config
%endif

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="${extra_inc}" \
	   --with-libiconv-prefix="/usr/gnu"


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/gcompris
%{_libdir}/gcompris/*
%dir %attr (0755, root, other) %{_libdir}/menu
%{_libdir}/menu/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/*
%dir %attr (0755, root, bin) %{_datadir}/info
%{_datadir}/info/gcompris.info
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/gcompris
%{_datadir}/gcompris/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Jun 14 2008 - moinakg@gmail.com
- Bump version to 2.2.7
* Sat Feb 02 2008 - moinak.ghosh@sun.com
- Initial spec.
