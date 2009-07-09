#
# spec file for package libvisual-plugins.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan

Name:                   libvisual-plugins
License:		GPL v2
Summary:                Visualization plugins for the Libvisual library
Version:                0.4.0
URL:                    http://localhost.nl/~synap/libvisual-wiki/index.php/Main_Page
Source:                 http://downloads.sourceforge.net/libvisual/libvisual-plugins-%{version}.tar.bz2
# date:2008-11-25 owner:jerrytan type:branding 
Patch1:			libvisual-plugins-01-compiler.diff

Requires: libvisual

%prep
%setup -q -n libvisual-plugins-%{version}
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# the following ifarch-endif contains plugins
# which depend on OpenGL 
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no		\
%ifarch sparc
	    --disable-nastyfft		\
	    --disable-madspin		\
	    --disable-flower		\
	    --disable-gltest		\
%endif
	    --disable-corona		\
	    --disable-gforce 


make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*

%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Tue Mar 10 2009 - harry.lu@sun.com
- Change owner to Jerry Tan
* Tue Nov 25 2008 - jim.li@sun.com
- add license tag
- rename SFElibvisual-plugins to libvisual-plugins
- use sun compiler 12 instead of gcc
* Tue Jan 29 2008 - moinak.ghosh@sun.com
- Initial spec.
