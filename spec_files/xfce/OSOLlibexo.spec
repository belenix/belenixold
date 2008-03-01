#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use libexo = libexo.spec

# The the following is quite a bit hacky.  It is due to historic reasons.
# libnotify was first introduced in SFE as SFElibnotify but it was later
# moved to Xfce as OSOLlibnotify, then even later it became part of JDS
# and included in SUNWgnome-panel.
# If /usr/lib/libnotify.so is found on the system, it is assumed that it
# comes from JDS.  If not, this package will require OSOLlibnotify
%define libnotify_installed %(test -f /usr/lib/libnotify.so && echo 1 || echo 0)

Name:			OSOLlibexo
Summary:		Application library for the Xfce desktop environment
Version:		%{libexo.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:		SUNWgnome-base-libs-devel
Requires:		SUNWgnome-base-libs
Requires:		OSOLxfce4-dev-tools
BuildRequires:		OSOLlibxfce4util-devel
Requires:		OSOLlibxfce4util
Requires:		OSOLxfce-mcs-manager
Requires:		OSOLperl-uri
%if %libnotify_installed
Requires:               SUNWgnome-panel
BuildRequires:          SUNWgnome-panel-devel
%else
Requires:		OSOLlibnotify
BuildRequires:          OSOLlibnotify-devel
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%libexo.prep -d %name-%version/%base_arch

%build
%libexo.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%libexo.install -d %name-%version/%base_arch

# move python stuff to vendor-packages
(
  cd $RPM_BUILD_ROOT%{_libdir}/python*
  mv site-packages vendor-packages
  rm vendor-packages/*/*.la
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/xfce4
%dir %attr (0755, root, bin) %{_datadir}/pygtk
%dir %attr (0755, root, bin) %{_libdir}/xfce4
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%{_bindir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.so.*
%{_libdir}/exo-compose-mail-0.3
%{_libdir}/exo-helper-0.3
%{_libdir}/exo-mount-notify-0.3
%{_libdir}/xfce4/*
%{_datadir}/xfce4/*
%{_datadir}/pygtk/*
%{_libdir}/python2.4/*
%{_mandir}/man1/exo-open.*
%defattr(-,root,other)
%{_datadir}/locale*
%{_datadir}/applications*
%{_datadir}/icons*
%{_datadir}/pixmaps*

%files root
%defattr(-,root,sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/xdg

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_bindir}/exo-csource
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man1/exo-csource.*
%{_datadir}/gtk-doc/*

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
- add hack that decides whether to depend on SUNWgnome-panel or OSOLlibnotify
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added another fixgccism patch
* Fri Feb  9 2007 - dougs@truemail.co.th
- Added libnotify and change perl-ui requirement - Copied from SFE repository
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
