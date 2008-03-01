#
# spec file for package OSOLlibnotify
#
# includes module(s): libnotify
#

%include Solaris.inc

# The the following is quite a bit hacky.  It is due to historic reasons.
# libnotify was first introduced in SFE as SFElibnotify but it was later
# moved to Xfce as OSOLlibnotify, then even later it became part of JDS
# and included in SUNWgnome-panel.  So %prep below will test if
# /usr/lib/libnotify.so is one of these.
%define libnotify_installed %(test -f /usr/lib/libnotify.so && echo 1 || echo 0)

Name:         OSOLlibnotify
License:      Other
Group:        System/Libraries
Version:      0.4.4
Summary:      libnotify is a notification system for the GNOME desktop environment.
Source:       http://www.galago-project.org/files/releases/source/libnotify/libnotify-%{version}.tar.bz2
URL:          http://www.galago-project.org/news/index.php
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
Requires: SUNWgnome-base-libs
Requires: SUNWdbus

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%if %libnotify_installed
grep /usr/lib/libnotify.so /var/sadm/install/contents | grep ' SFElibnotify' && {
    echo "WARNING: SFElibnotify already installed"
    exit 1
}
grep /usr/lib/libnotify.so /var/sadm/install/contents | grep ' OSOLlibnotify' && {
    echo "WARNING: OSOLlibnotify already installed"
    exit 0
}
grep /usr/lib/libnotify.so /var/sadm/install/contents | grep ' SUNWgnome-panel' && {
    echo "INFO: libnotify is now part of SUNWgnome-panel, no need to build it"
    exit 0
}
echo "ERROR: unknown libnotify in /usr/lib/libnotify.so"
exit 1
%else
%setup -q -n libnotify-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
		--libdir=%{_libdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%if %libnotify_installed
# do nothing
%else

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%dir %attr (0755, root, bin) %dir %{_includedir}/libnotify
%{_includedir}/libnotify/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %dir %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%endif
# %libnotify_installed

%changelog
* Mon Apr 16 2007 - laca@sun.com
- bump to 0.4.4
* Tue Apr  3 2007 - laca@sun.com
- add hack that installs libnotify when it's not installed by another package
* Fri Feb  9 2007 - dougs@truemail.co.th
- copied across from SFE repository
* Sun Jan 21 2007 - laca@sun.com
- add defattr tag to files
* Sun Jan  7 2007 - laca@sun.com
- fix gtk-doc dir attributes
* Thu Nov 23 2006 - jedy.wang@sun.com
- Initial spec
