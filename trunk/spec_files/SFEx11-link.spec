#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEx11-link
Summary:             Temporary X11 links to accommodate FOX gate changes
Version:             1.0

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf SFEx11-link
mkdir SFEx11-link

%build
cd SFEx11-link

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT
mkdir -p usr/X11/lib
mkdir -p usr/X11/lib/%{_arch64}

cd usr/X11/lib
ln -sf libX11.so.4 libX11.so.6 
ln -sf libXt.so.4 libXt.so.6 

cd %{_arch64}
ln -sf libX11.so.4 libX11.so.6
ln -sf libXt.so.4 libXt.so.6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, bin) /usr/X11
%dir %attr (0755, root, bin) /usr/X11/lib
%dir %attr (0755, root, bin) /usr/X11/lib/%{_arch64}
/usr/X11/lib/libX11.so.6
/usr/X11/lib/%{_arch64}/libX11.so.6
/usr/X11/lib/libXt.so.6
/usr/X11/lib/%{_arch64}/libXt.so.6

%changelog
* Sat Jun 14 2008 - moinakg@gmail.com
- Initial spec
- Temporary compatibility package to adjust to changing FOX gate.
