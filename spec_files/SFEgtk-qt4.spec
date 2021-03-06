#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEgtk-qt4
License:             GPL
Summary:             A GTK plugin to allow GTK apps to use QT styles.
Version:             1.1
URL:                 http://gtk-qt.ecs.soton.ac.uk/
Source:              http://gtk-qt-engine.googlecode.com/files/gtk-qt-engine-%{version}.tar.bz2
Patch1:              gtk-qt-engine-01-utilities.cpp.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SFEqt4
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SFEqt4-devel
BuildRequires:       SFEcmake
Conflicts:           SFEgtk-qt3

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Conflicts:           SFEgtk-qt3-l10n
%endif

%prep
%setup -q -n gtk-qt-engine
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__ -DUSE_SOLARIS"
export CXXFLAGS=$CFLAGS
export LDFLAGS="%_ldflags %{gnu_lib_path}"
gnu_prefix=`dirname %{gnu_bin}`

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --localedir=%{_localedir} \
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT/usr/local/share/locale $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT/usr/local/share/applications $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT/usr/local
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_localedir}
rm -rf $RPM_BUILD_ROOT/usr/local
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gtk-2.0
%{_libdir}/gtk-2.0/*
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/themes
%{_datadir}/themes/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_localedir}
%endif

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
