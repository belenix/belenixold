#
# spec file for package freetts
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:         freetts
License:      Other
Group:        System/Libraries
Version:      1.2.1
Release:      40
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      FreeTTS Speech Synthesis System
Source:       http://easynews.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-src.zip
URL:          http://sourceforge.net/projects/freetts/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

BuildRequires: jdk
Requires:      jdk

%description
FreeTTS Speech Synthesis System
FreeTTS is a speech synthesis system written entirely in the Java
programming language. It is based upon Flite, a small, fast, run-time speech
synthesis engine, which in turn is based upon University of Edinburgh's
Festival Speech Synthesis Sytem and Carnegie Mellon University's
FestVox project.

%prep
%setup -q -c -n freetts
%build
cd freetts-%{version}
%ifos solaris
export JAVA_HOME="/usr/java"
%else
export JAVA_HOME="/usr/java/jdk1.5.0_03"
%endif
ant

%install
cd freetts-%{version}
cd lib
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lib/freetts
cp freetts.jar cmudict04.jar cmulex.jar en_us.jar cmu_us_kal.jar $RPM_BUILD_ROOT%{_datadir}/lib/freetts
cd ../bin
cp FreeTTSEmacspeakServer.jar $RPM_BUILD_ROOT%{_datadir}/lib/freetts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, root) %{_datadir}/lib/freetts
%defattr(-,root,root)
%{_datadir}/lib/freetts/*

%changelog
* Fri Jul 29 2005 - damien.carbery@sun.com
- Use stable JAVA_HOME directory, not the one that changes each Java release.
* Mon May 09 2005 - dermot.mccluskey@sun.com
- New jdk (1.5.0_03)
* Mon Feb 28 2005 - william.walker@sun.com
- Upgrade to FreeTTS 1.2.1, fix for bug #6228329.
* Fri Oct 08 2004 - bill.haneman@sun.com
- cp SOURCE1 to the right place.
* Fri Oct 08 2004 - bill.haneman@sun.com
- Replace freetts.jar with %SOURCE1, patched jarfile from
  Philip Kwok of SunLabs.  Part of fix for #5087408.
* Mon Jul 05 2004 - damien.carbery@sun.com
- Updated to 1.2beta2 tarball.
* Thu Jun 10 2004 - damien.carbery@sun.com
- Correct name of source tarball, including replacing hard coded ver number
  with %{version}.
* Thu Jun 10 2004 - bill.haneman@sun.com
- Updated spec file to freetts 1.2 (beta); changed jarfiles to match 1.2.
* Thu Mar 11 2004 - damien.carbery@sun.com
- Created new spec file for freetts
