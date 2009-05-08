#
# spec file for package SUNWpython25-pyopenssl
#
# includes module(s): Pyopenssl
#
%include Solaris.inc

Name:                    SUNWpython25-pyopenssl
Summary:                 pyOpenSSL - Python interface to the OpenSSL library (Python 2.5)
Version:                 0.9
Source:                  http://nchc.dl.sourceforge.net/sourceforge/pyopenssl/pyOpenSSL-%{version}.tar.gz
URL:                     http://pyopenssl.sourceforge.net/

SUNW_BaseDir:            %{_basedir}
License:                 GPL2
SUNW_Copyright:          LICENSE.GPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython25
BuildRequires:           SUNWPython25-devel

%prep
%setup -q -c -n %{name}-%version

%build
cd pyOpenSSL-%{version}

python2.5 setup.py build_ext -I/usr/sfw/include -L/usr/sfw/lib -R/usr/sfw/lib
python2.5 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd pyOpenSSL-%{version}
python2.5 setup.py install --prefix=${RPM_BUILD_ROOT}%{_prefix}

mv ${RPM_BUILD_ROOT}%{_libdir}/python2.5/site-packages ${RPM_BUILD_ROOT}%{_libdir}/python2.5/vendor-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.5
%dir %attr (0755, root, bin) %{_libdir}/python2.5/vendor-packages
%{_libdir}/python2.5/vendor-packages/*

%changelog
* Web May 06 2009 - moinakg@belenix.org
- Initial spec file.

