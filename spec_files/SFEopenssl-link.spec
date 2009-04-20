#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEopenssl-link
Summary:             Temporary /usr/sfw openssl links to accommodate openssl package change
Version:             1.0

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf SFEopenssl-link
mkdir SFEopenssl-link

%build
cd SFEopenssl-link

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT
mkdir -p usr/sfw/lib
mkdir -p usr/sfw/lib/%{_arch64}

cd usr/sfw/lib
ln -sf ../../lib/libcrypto.so.0.9.8
ln -sf ../../lib/libssl.so.0.9.8

cd %{_arch64}
ln -sf ../../../lib/%{_arch64}/libcrypto.so.0.9.8
ln -sf ../../../lib/%{_arch64}/libssl.so.0.9.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, bin) /usr/sfw
%dir %attr (0755, root, bin) /usr/sfw/lib
%dir %attr (0755, root, bin) /usr/sfw/lib/%{_arch64}
/usr/sfw/lib/libcrypto.so.0.9.8
/usr/sfw/lib/%{_arch64}/libcrypto.so.0.9.8
/usr/sfw/lib/libssl.so.0.9.8
/usr/sfw/lib/%{_arch64}/libssl.so.0.9.8

%changelog
* Sun Apr 19 2009 - moinakg@gmail.com
- Initial spec
- Temporary compatibility package to adjust to OpenSSL moving to /usr prefix.
