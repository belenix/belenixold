#
# spec file for package neutral-plus-inverted
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
# bugdb: defect.opensolaris.org
#
Name:         		Neutral_Plus_Inv
License:      		Other
Group:        		System/GUI/GNOME
BuildArchitectures:	noarch
Version:      		70481
Release:      		1
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		Neutral Plus Inverted mouse cursor theme
Source:       		http://www.gnome-look.org/CONTENT/content-files/%{version}-%{name}.tar.gz
URL:          		http://www.gnome-look.org/content/show.php/Neutral+Plus+Inverted?content=94665
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Docdir:	      		%{_defaultdocdir}/doc
Autoreqprov:  		on

%description
The Neutral Plus Inverted mouse cursor theme provides a set of icons for the 
traditional X11 mouse cursor.

%prep
%setup -q -n %{name}

%build

%install
cd ..
cp -r %{name} $RPM_BUILD_ROOT/%{_datadir}/icons/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_datadir}/icons/%{name}

%changelog
* Fri Dec 19 2008 - glynn.foster@sun.com
- Update URL from Thorsten Reinbold (author)
* Thu Jan 17 2008 - glynn.foster@sun.com
- Initial version
