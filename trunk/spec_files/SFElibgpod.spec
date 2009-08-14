#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFElibgpod
Summary:             Library to access the contents of an iPod
Version:             0.7.0
License:             LGPLv2+
Source:              http://downloads.sourceforge.net/gtkpod/libgpod-%{version}.tar.gz
URL:                 http://www.gtkpod.org/libgpod.html
Patch1:              libgpod-01-hal_callout_mount_dir.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWglib2
Requires: SUNWgtk2
Requires: SUNWPython26
Requires: SUNWhal
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWgnome-python26-libs
Requires: SFEpython26-mutagen
%if %cc_is_gcc
Requires: SFEgccruntime
%endif
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWperl-xml-parser
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SFEswig

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWglib2-devel
Requires: SUNWgtk2-devel
Requires: SUNWPython26-devel
Requires: SUNWlxml-devel
Requires: SUNWlxsl-devel
Requires: SUNWperl-xml-parser
Requires: SUNWgnome-python26-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%description
Libgpod is a library to access the contents of an iPod. It supports playlists,
smart playlists, playcounts, ratings, podcasts, album artwork, photos, etc.

%prep
%setup -q -c -n %name-%version
cd libgpod-%version
%patch1 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd libgpod-%{version}
export CFLAGS=""
export CXXFLAGS=""
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --enable-shared \
            --disable-static \
            --target=..generic

# set GCC.LDFLAGS to avoid stripping and useless -debuginfo
gmake -j $CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd libgpod-%{version}
gmake -i install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rmdir $RPM_BUILD_ROOT%{_bindir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
