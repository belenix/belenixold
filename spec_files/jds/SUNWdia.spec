#
# spec file for package SUNWdia
#
# includes module(s): dia
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc
%use dia = dia.spec

Name:             SUNWdia
Summary:          Dia Diagram Editor
Source:           %{name}-manpages-0.1.tar.gz
Version:          %{dia.version}
SUNW_BaseDir:     %{_basedir}
SUNW_Copyright:   %{name}.copyright
BuildRoot:        %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgccruntime
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgccruntime

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%dia.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%dia.build -d %name-%version

%install
%dia.install -d %name-%version

rm -r $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
#FIXME: really need to fix this stuff up
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/dia/eu
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/dia/[a-d]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/dia/[f-z]*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/dia/C
%{_datadir}/gnome/help/dia/en
%{_datadir}/man/*
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%{_datadir}/omf/*
%dir %attr (0755, root, other) %{_datadir}/dia
%{_datadir}/dia/*
%doc -d dia-%{dia.version} AUTHORS README
%doc(bzip2) -d dia-%{dia.version} COPYING ChangeLog NEWS po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/dia/eu
# Comment this line out since no [a-d]* locale at this point
#%{_datadir}/gnome/help/dia/[a-d]*
%{_datadir}/gnome/help/dia/[f-z]*
%endif

%changelog
* Wed Oct 22 2008 - matt.keenan@sun.com
- Created
