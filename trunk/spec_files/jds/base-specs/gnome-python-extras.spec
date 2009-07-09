#
# base spec file for package gst-python
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%{?!pythonver:%define pythonver 2.4}

Name:                    gnome-python-extras
Summary:                 Supplemental Python bindings for GNOME
URL:                     http://ftp.gnome.org/pub/GNOME/sources/gnome-python-extras
Version:                 2.25.3
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-python-extras/2.25/gnome-python-extras-%{version}.tar.bz2
# date:2008-02-18 owner:dkenny type:feature
Patch1:                  gnome-python-extras-01-libgksu-missing-funcs.diff
# date:2008-05-29 owner:evan type:bug bugzilla:532856
Patch2:                  gnome-python-extras-02-using-firefox3.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                python

%prep
%setup -q -n %name-%version
%patch1 -p1
%patch2 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
autoconf
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 03 2009 - brian.cameron@sun.com
- Use find command to remove .la files.
  files.
* Thu Feb 26 2009 - brian.cameron@sun.com
- Split from SUNWgnome-python-extras.spec file.

