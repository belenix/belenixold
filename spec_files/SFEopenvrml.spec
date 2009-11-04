#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEopenvrml
Summary:             VRML/X3D player and runtime library 
Version:             0.18.3
License:             LGPLv3+
Group:               System Environment/Libraries
Source:              %{sf_download}/openvrml/openvrml-%{version}.tar.gz
URL:                 http://openvrml.org

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEboost-gpp
BuildRequires: SFEboost-gpp-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWlxml
BuildRequires: SUNWlxml-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWglib2
BuildRequires: SUNWglib2-devel
Requires: SUNWdbus-glib
Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
Requires: SFEgtkglext
BuildRequires: SFEgtkglext-devel
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWcurl
BuildRequires: SUNWcurl-devel
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFEsdl
BuildRequires: SFEsdl-devel

%description
OpenVRML is a free cross-platform runtime for VRML and X3D available
under the GNU Lesser General Public License. The OpenVRML distribution
includes libraries you can use to add VRML/X3D support to an application.
On platforms where GTK+ is available, OpenVRML also provides a plug-in
to render VRML/X3D worlds in Web browsers.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SFEboost-gpp-devel
Requires: SUNWpng-devel
Requires: SUNWlxml-devel
Requires: SUNWjpg-devel
Requires: SUNWglib2-devel
Requires: SUNWgtk2-devel
Requires: SFEgtkglext-devel
Requires: SUNWgnome-libs-devel
Requires: SUNWcurl-devel
Requires: SUNWxorg-headers
Requires: SFEsdl-devel

%prep
%setup -q -c -n %name-%version
cd openvrml-%version
cd ..

%ifarch amd64 sparcv9
cp -rp openvrml-%version openvrml-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#
# Minimally need 64Bit libltdl for 64Bit build
#
#%ifarch amd64 sparcv9
#cd openvrml-%{version}-64
#
#export CFLAGS="%optflags64 -pthreads -I%{_includedir}/boost/gcc4"
#export CXXFLAGS="%cxx_optflags64 -pthreads -I%{_includedir}/boost/gcc4"
#export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -L%{_libdir}/%{_arch64}/boost/gcc4 -R%{_libdir}/%{_arch64}/boost/gcc4"
#export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
#
#./configure --prefix=%{_prefix} \
#            --bindir=%{_bindir}/%{_arch64} \
#            --libdir=%{_libdir}/%{_arch64} \
#            --sysconfdir=%{_sysconfdir} \
#            --datadir=%{_datadir} \
#            --includedir=%{_includedir} \
#            --libexecdir=%{_libexecdir} \
#            --disable-script-node-java \
#            --disable-player \
#            --disable-mozilla-plugin
## No 64-bit XULrunner yet and no 64Bit gnome libs yet.
#
#gmake -j$CPUS
#cd ..
#%endif

cd openvrml-%{version}
export CFLAGS="%optflags -pthreads -I%{_includedir}/boost/gcc4"
export CXXFLAGS="%cxx_optflags -pthreads -I%{_includedir}/boost/gcc4"
export LDFLAGS="%_ldflags -L%{_libdir} -R%{_libdir} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4"
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --disable-script-node-java

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd openvrml-%{version}-64
#
#gmake DESTDIR=$RPM_BUILD_ROOT install
#cd ..
#%endif

cd openvrml-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/openvrml/node/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/openvrml/node/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/openvrml/script/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/openvrml/script/*.a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/openvrml
%{_libdir}/openvrml/*
%attr (0555, root, bin) %{_libdir}/openvrml-xembed
%dir %attr (0755, root, bin) %{_libdir}/mozilla
%{_libdir}/mozilla/*

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/openvrml
%{_datadir}/openvrml/*
%dir %attr(0755, root, bin) %{_datadir}/openvrml-xembed
%{_datadir}/openvrml-xembed/*
%dir %attr(0755, root, bin) %{_datadir}/openvrml-player
%{_datadir}/openvrml-player/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/*.a
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/openvrml
%{_includedir}/openvrml/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_datadir}/javadoc
%{_datadir}/javadoc/*

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
