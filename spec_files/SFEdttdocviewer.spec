#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEdttdocviewer
License:             LGPL
Summary:             A little GUI for viewing DTraceToolkit documentation
Version:             1.0
URL:                 http://www.belenix.org/
Source:              http://www.belenix.org/binfiles/dttdocviewer-%{version}.tar.gz
Source1:             dttdocs.desktop
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
BuildRequires:       SUNWgnome-base-libs-devel

%prep
%setup -q -n dttdocviewer-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

make all -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Wed Apr 02 2008 - moinakg@gmail.com
- Add desktop entry.
* Mon Feb 04 2008 - moinak.ghosh@sun.com
- Initial spec.
