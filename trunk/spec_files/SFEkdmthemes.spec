#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEkdmthemes
License:             LGPL
Summary:             A collection of KDM themes
Version:             0.1
Source1:             http://www.kde-look.org/CONTENT/content-files/75534-Kdmworld.tar.gz
Source2:             http://www.kde-look.org/CONTENT/content-files/75036-SweetDarkness.tar.gz
Source3:             belenix_small.png
Source4:             belenix_small_grey.png
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SFEkdmtheme
Buildrequires:       SUNWgzip

%prep
rm -rf %name-%version
mkdir -p %name-%version

%build
cd %name-%version
gunzip -c %{SOURCE1} | tar xpf - 
gunzip -c %{SOURCE2} | tar xpf - 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/apps/kdm/themes
mkdir -p ${RPM_BUILD_ROOT}/usr/X11/lib/X11/fonts/TrueType
cd %name-%version

rm -f Readme\!
rm -f kdebackgroundStart.jpg
cp *.ttf ${RPM_BUILD_ROOT}/usr/X11/lib/X11/fonts/TrueType
rm -f *.ttf
gunzip -c Worldkdm.tar.gz | (cd ${RPM_BUILD_ROOT}/%{_datadir}/apps/kdm/themes; tar xpf -)
rm -f Worldkdm.tar.gz
rm -f SweetDarkness/logos/*
cp %{SOURCE3} SweetDarkness/logos/
cp %{SOURCE4} SweetDarkness/logos/

#
# Patch SweetDarkness theme file to load BeleniX logo
#
cat SweetDarkness/kdm-sweetdarkness.xml | sed 's/xxx.png/belenix_small.png/' > kdm-sweetdarkness.xml
mv kdm-sweetdarkness.xml SweetDarkness/kdm-sweetdarkness.xml

find * | cpio -pdum ${RPM_BUILD_ROOT}/%{_datadir}/apps/kdm/themes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_basedir}/X11
%{_basedir}/X11/*

%changelog
* Tue Mar 25 2008 - moinakg@gmail.com
- Initial spec.
