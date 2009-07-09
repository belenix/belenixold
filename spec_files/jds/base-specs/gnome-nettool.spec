#
# spec file for package gnome-nettool
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include l10n.inc
Name:               gnome-nettool
License:	    GPL/LGPL
Group:		    System/GUI/GNOME
Version:            2.26.0
Release:	    1
Summary:	    GNOME Network Tools
Source:		    http://ftp.gnome.org/pub/GNOME/sources/gnome-nettool/2.26/gnome-nettool-%{version}.tar.bz2
#owner:gheet date:2008-09-10 type:feature bugster:6736233
Patch1:             %{name}-01-sun-patch.diff
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWgnome-base-libs
Requires:           SUNWgnome-libs

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires:	 %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%setup -q 
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -I/usr/include"
export RPM_OPT_FLAGS="$CFLAGS"

libtoolize --force --copy
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
#automake --add-missing
autoconf
CFLAGS="$RPM_OPT_FLAGS"
./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir}
make -j $CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif


%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (0755, root, other) %{_datadir}/omf
%{_datadir}/omf/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.22.1.
* Wed Sep 10 2008 - takao.fujiwara@sun.com
- Update 01-sun-patch.diff to enable ping hostname.
* Mon Aug 04 2008 - ghee.teo@sun.com
- Initial spec
