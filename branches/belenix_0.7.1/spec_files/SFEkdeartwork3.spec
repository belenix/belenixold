#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.9

Name:                SFEkdeartwork3
Summary:             Additional Artwork (themes, wallpapers etc.) for KDE
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdeartwork-%{version}.tar.bz2
Patch1:              kdeartwork-01-libart.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel

%prep
%setup -q -n kdeartwork-%version
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

export CFLAGS="%optflags -fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs` -lartsflow -lartsflow_idl"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:/usr/include/pcre"


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/emoticons
%{_datadir}/emoticons/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applnk
%{_datadir}/applnk/*
%dir %attr (0755, root, other) %{_datadir}/wallpapers
%{_datadir}/wallpapers/*

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*

%changelog
* Sat Jun 14 2008 - moinakg@gmail.com
- Bump to KDE 3.5.9.
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Fixed typo in configure options.
* Wed Jan 16 2008 - moinak.ghosh@sun.com
- Initial spec.