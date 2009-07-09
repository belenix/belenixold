#
# spec file for package SUNWIPython
#
# includes module(s): ipython
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
%define pythonver 2.4

Name:                   ipython
Summary:                Enhanced interactive Python shell
Version:                0.8.4
Release:                1
License:                BSD
Group:                  Development/Libraries
URL:                    http://ipython.scipy.org/
Source:                 http://ipython.scipy.org/dist/ipython-%{version}.tar.gz
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:              noarch

%description
IPython provides a replacement for the interactive Python interpreter with
extra functionality.

%prep
%setup

%build
%{__python} setup.py build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root="$RPM_BUILD_ROOT"

# Move to vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
#%defattr(-, root, root, 0755)
%doc doc/ChangeLog doc/COPYING doc/NEWS doc/README.txt doc/*.txt doc/examples/ doc/manual/
%doc %{_mandir}/man1/ipython.1*
%doc %{_mandir}/man1/pycolor.1*
%{_bindir}/ipython
%{_bindir}/pycolor

%changelog
* Tue Mar 17 2009 - li.yuan@sun.com
- Downgrade to 0.8.4 because of dependency problem.
* Fri Dec 05 2008 - li.yuan@sun.com
- Bump to 0.9.1.

* Fri Jun 06 2008 - brian.cameron@sun.com
- Bump to 0.8.4.

* Fri Dec 07 2007 - brian.cameron@sun.com
- Bump to 0.8.2.

* Wed Oct 10 2007 - damien.carbery@sun.com
- Move files from site-packages to vendor-packages. Fixes 6615442.

* Mon Sep  2 2007 - li.yuan@sun.com
- Initial version.
