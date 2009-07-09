#
# spec file for package system-config-printer
#
# includes module(s): system-onfig-printer
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%{?!pythonver:%define pythonver 2.4}
%include l10n.inc


Name:         system-config-printer
License:      GPL V2
Group:        Development/Languages/Python
Version:      1.0.13
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Print Manager for CUPS
Source:       http://cyberelk.net/tim/data/%{name}/1.0.x/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Patch1:	      system-config-printer-01-temp-for-2.4.diff
Patch2:	      system-config-printer-02-no-manpage.diff
#owner:gheet date:2006-11-03 type:branding
Patch3:	      system-config-printer-03-app-path.diff
#owner:gheet date:2006-11-03 type:branding bugster:6780731
Patch4:	      system-config-printer-04-remove-fedora-specific.diff
URL:          http://cyberelk.net/tim/software/%{name}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  off
Prereq:       /sbin/ldconfig
Requires:     SFEcups
# uncomment this once we sorted samba 3.2.x
#Requires:     SUNWpysmbc
BuildRequires: SFEcups-devel
#BuildRequires: SUNWpysmbc

%description
System Config Printer is a tool is to configure a CUPS server (often the local machine) 
using the CUPS API. The tool is written in Python, using pygtk for the graphical parts 
and with some Python bindings (pycups) for the CUPS API.

It is largely the same as using the CUPS web interface for configuring printers, but 
has the advantage of being a native application rather than a web page.

%prep
%setup -q -n %{name}-%{version}

bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..

%patch01 -p1
%patch02 -p0
%patch03 -p0
%patch04 -p1

%build
intltoolize --force --copy
aclocal -I /usr/gnu/share/aclocal
automake -a -c -f
autoconf
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc
make install DESTDIR=$RPM_BUILD_ROOT

%install
python%{pythonver} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move private directory from /usr/share to /usr/lib
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/*.py \
   $RPM_BUILD_ROOT%{_libdir}/%{name}

if [ ! -d $RPM_BUILD_ROOT%{_libdir}/%{name}/troubleshoot ]
then
   mv $RPM_BUILD_ROOT%{_datadir}/%{name}/troubleshoot \
      $RPM_BUILD_ROOT%{_libdir}/%{name}
else
   rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/troubleshoot
fi

# Move system-config-printer-applet to /usr/lib/%{name}
mv $RPM_BUILD_ROOT%{_bindir}/system-config-printer-applet \
   $RPM_BUILD_ROOT%{_libdir}/%{name}

# do not deliver my-default-printer
rm $RPM_BUILD_ROOT%{_bindir}/my-default-printer
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/my-default-printer.py

# Don't need desktop files as they are shared and managed by sym links
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications
rm -rf $RPM_BUILD_ROOT/etc/xdg

# move to vendor-packages, but don't provide .pyc files
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
rm $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/cupshelpers/*.pyc
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jan 19 2009 - ghee.teo@sun.com
- Bump tarball to 1.0.13. Removed upteram l10n patch.
* Mon Dec 15 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Dec 12 2008 - takao.fujiwara@sun.com
- Add patch 05-g11n-textdomain.diff to set textdomain.
* Thu Dec 11 2008 - ghee.teo@sun.com
  uprev to 1.0.12 tarball and added patch 04-remove-fedora-specific.diff
* Wed Nov 05 2008 - ghee.teo@sun.com
- initial version
