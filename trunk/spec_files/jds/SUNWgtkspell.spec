#
# spec file for package SUNWgtkspell
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
#

%include Solaris.inc
Name:                    SUNWgtkspell
Summary:                 Gtkspell provides word-processor-style highlighting and replacement of misspelled words in a GtkTextView widget.
License:                 GPL v2
Version:                 2.0.15
Source:                  http://gtkspell.sourceforge.net/download/gtkspell-%{version}.tar.gz
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
Source2:                 %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWgnome-base-libs
Requires:		 SUNWgnome-spell
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:		 SUNWgnome-spell-devel

%package devel
Summary:                 Gtkspell - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-spell-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gtkspell-%version
cd %{_builddir}/gtkspell-%version
gzcat %SOURCE2 | tar xf -

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CPPFLAGS="%optflags"
export LDFLAGS="%_ldflags"

intltoolize --force --copy

%if %build_l10n
sh %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
libtoolize --force
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
cd %{_builddir}/gtkspell-%version/sun-manpages
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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc README AUTHORS
%doc(bzip2) COPYING ChangeLog
%doc(bzip2) po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Sep 19 2008 - dave.lin@sun.com
- Set the attribute of the dir %{_datadir}/doc in base pkg.
* Wed Sep 17 2008 - jim.li@sun.com
- Revised new format copyright file
* Thu Jul 03 2008 - Jim Li
- Copied from SFEgtkspell and rename to SUNWgtkspell
* Sun Mar 02 2008 - Petr Sobotka
- Source tar file was moved
* Wed July 26 2006 - lin.ma@sun.com
- Initial spec file
