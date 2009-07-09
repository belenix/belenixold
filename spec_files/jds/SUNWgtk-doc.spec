
%include default-depend.inc
%include Solaris.inc

%use gtkdoc = gtk-doc.spec

Name:                    SUNWgtk-doc
Summary:                 GNOME
Version:                 %{default_pkg_version}
#Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Requires: SUNWgnome-xml-root
Requires: SUNWgnome-common-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWgnome-doc-utils

%prep
rm -rf %name-%version
mkdir %name-%version

%gtkdoc.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
cd %{_builddir}
export PYTHON="/usr/bin/python2.6"
export CXXFLAGS="%{cxx_optflags}"
export ACLOCAL_FLAGS="-I /usr/share/gnome-doc-utils -I./m4"
%gtkdoc.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gtkdoc.install -d %name-%version

# Normally we build this package before we build scrollkeeper, but
# remove any scrollkeeper files if user happens to rebuild this
# package after scrollkeeper is already on the system.
#
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

# Remove /usr/share/info/dir, it's a generated file and shared by multiple
# packages
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/gtk-doc.m4
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/gtk-doc-manual/gtk-doc-manual-C.omf
%{_datadir}/sgml/gtk-doc/gtk-doc.cat
%{_datadir}/gtk-doc/data/*
%{_datadir}/pkgconfig/gtk-doc.pc
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gtk-doc-manual/C/gtk-doc-manual.xml
%{_datadir}/gnome/help/gtk-doc-manual/C/fdl-appendix.xml
%{_bindir}/gtkdoc*

%changelog
* Mon Mar 23 2009 - dave.lin@sun.com
* Add 'BuildRequires: SUNWgnome-doc-utils'.
* Mon Mar 23 2009 - dave.lin@sun.com
- Change BuildRequires to SUNWPython26-devel.
* Thu Mar 19 2009 - dave.lin@sun.com
- Add BuildRequires: SUNWPython-devel
