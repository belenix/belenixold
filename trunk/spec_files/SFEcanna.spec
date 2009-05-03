#
# spec file for package SFEcanna
#
# includes module(s): Canna
#

%include Solaris.inc
Name:                    SFEcanna
Summary:                 Canna - a Japanese input system
Version:                 3.7p3
%define tarball_version 37p3
URL:                     http://canna.sourceforge.jp/
Source:                  http://keihanna.dl.sourceforge.jp/canna/9565/Canna%{tarball_version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWxwplt
BuildRequires:           SUNWxwopt

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n Canna%{tarball_version}

%build

export CFLAGS="%optflags -I/usr/X11/include -I/usr/openwin/include -D__EXTENSIONS__"
export CPPFLAGS=$CFLAGS
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lX11"
export PATH="${PATH}:/usr/X/bin:/usr/openwin/bin"
unset CPP CXXCPP LD

sed 's#/usr/local/canna#/usr#' Canna.conf > Canna.new.conf && mv Canna.new.conf Canna.conf

/usr/X11/bin/xmkmf

make canna

%install
rm -rf $RPM_BUILD_ROOT

echo << EOF > chown
#!/bin/sh
exit 0
EOF

echo << EOF > chgrp
#!/bin/sh
exit 0
EOF

chmod a+x chown
chmod a+x chgrp

PDIR=`pwd`
export PATH="$PDIR:$PATH"

make install DESTDIR=$RPM_BUILD_ROOT
make install.man DESTDIR=$RPM_BUILD_ROOT

rm -f chown chgrp
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -rf ${RPM_BUILD_ROOT}%{_localstatedir}

mv ${RPM_BUILD_ROOT}/usr/man ${RPM_BUILD_ROOT}/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/canna
%{_datadir}/canna/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial spec file
