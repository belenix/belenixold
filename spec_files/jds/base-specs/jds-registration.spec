#
# spec file for package jds-registration
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name: jds-registration
License: GPL
Group: System/GUI
Version: 1.3
Release: 40
Distribution: Java Desktop System
Vendor: Sun Microsystems, Inc.
Summary: Customer registration application.
Source: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Autoreqprov: on

PreReq: j2re-integration
BuildRequires: jdk
Requires:      jdk

%description
The JDS registration program allows the user to enter registration
information, such as the product serial number, email address and
optional personal information. The serial number is used to perform
online patch updates using JSUS (Java System Update Services).

%prep
%setup -q


%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%ifos linux
export JAVA_HOME="/usr/java/jdk1.5.0_03"
%else
export JAVA_HOME="/usr/java"
%endif
make -j $CPUS

%install
%ifos linux
export JRE_HOME="/usr/java/j2redefault"
%else
export JRE_HOME="/usr/j2se/jre2"
%endif
make install DESTDIR=$RPM_BUILD_ROOT
echo "$JRE_HOME/lib/ext/jds-registration.jar" > jds-registration.files

%clean
make clean
rm -rf $RPM_BUILD_ROOT

%files -f jds-registration.files
%defattr(-,root,root)

%changelog
* Tue Aug 23 2005 - damien.carbery@sun.com
- Remove unneeded java related variables.
* Fri Jul 29 2005 - damien_carbery@sun.com
- Drop intermediate java_home/jre_home vars and set env vars directly.
* Fri Jun 10 2005 - damien.carbery@sun.com
- Change how java_home and jre_home are defined - remove the use of tmp files.
* Mon May 09 2005 - dermot.mccluskey@sun.com
- New jdk (1.5.0_03)
* Mon Nov 22 2004 - johan.steyn@sun.com
- change version to make use of latest (1.3) source tarball
  that removes embargoed countries for export compliance.
* Thu Sep 30 2004 - johan.steyn@sun.com
- change version to make use of latest (1.2) source tarball
  that includes all the I18N'd properties files.
* Wed Sep 15 2004 - dermot.mccluskey@sun.com
- new install dir for JDK 1.5.0
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jul 05 2004 - johan.steyn@sun.com
- Changed version number and release for new I18N'd version
* Tue Jun 01 2004 - damien.carbery@sun.com
- Correct JDK path in CFLAGS for Solaris 10.
* Sun May 30 2004 - dermot.mccluskey@sun.com
- New JDK
* Fri May 21 2004 - johan.steyn@sun.com
- Added PreReq for j2re-integration on Dermot's request.
- Changed OSTYPE check for solaris since Solaris build seems
  to have OSTYPE variable set to solaris2.9.
* Mon May 17 2004 - johan.steyn@sun.com
- Fixed JAVA_HOME and JRE_HOME to no longer use %ifos.
  This allows us to differentiate between different JDK and JRE
  locations on different versions of Solaris.
* Thu May 06 2004 - johan.steyn@sun.com
- removed j2re-integration from BuildRequires and Requires
- fixed JAVA_HOME and JRE_HOME to use %ifos instead
- added %{_prefix} to jre_home for solaris
- fixed %files to use jre_home instead of .rpm-files with -f option
* Mon May 03 2004 - dermot.mccluskey@sun.com
- fix JAVA_HOME
* Mon May 03 2004 - dermot.mccluskey@sun.com
- change Linux JAVA_HOME to 1.5.0
