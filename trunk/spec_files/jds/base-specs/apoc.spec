#
# Copyright (c) 2004 Sun Microsystems Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# This spec file generates all packages necessary for the JDS APOC 
# (A Point Of Control) functionality. 
#
# Please find the project page at: http://so-doc.germany.sun.com/Projects/Apoc/

#==============================================================================
#  Package Information/Description Section
#
#==============================================================================

%define t_suffix -build70
%{?nightly:%define t_suffix -%(TZ=GMT date +%Y%m%d)}
%define PLATFORM unxlngi5

Name:           apoc
Version:        1.2
Release:        38
Distribution:   Sun Java(tm) Desktop System, Release 3
Vendor:         Sun Microsystems, Inc.
License:        Sun Microsystems Binary Code License (BCL)
URL:            http://www.sun.com/software/javadesktopsystem/
Autoreqprov:    on
BuildRoot:      %{_builddir}/apoc/%{PLATFORM}/class/packages_build_root
Source:         apoc-%{version}%{t_suffix}.tar.bz2
BuildRequires:  ant

Group:          Applications/Internet
Summary:        Sun Java(tm) Desktop System Configuration Agent
Requires:       apoc-base
Requires:       apoc-misc

%description
Sun Java(tm) Desktop System Configuration Agent

#------------------------------------------------------------------------------

%package base
Group:          Applications/Internet
Summary:        Sun Java(tm) Desktop System Configuration Shared Libraries

%description base
Sun Java(tm) Desktop System Configuration Shared Libraries

#------------------------------------------------------------------------------

%package misc
Group:          Applications/Internet 
Summary:        Configuration Agent Miscellaneous Files

%description -n apoc-misc
Sun Java(tm) Desktop System Configuration Agent Miscellaneous Files

#------------------------------------------------------------------------------

%package adapter-java
Group:          Applications/Internet 
Summary:        Configuration Adapter for Java Preferences
Requires:       apoc

%description -n apoc-adapter-java
Sun Java(tm) Desktop System Configuration Adapter for Java Preferences 

#------------------------------------------------------------------------------

%package config
Group:          Applications/Internet 
Summary:        Sun Java(tm) Desktop System Configuration Agent Wizard
Requires:       apoc

%description -n apoc-config
Sun Java(tm) Desktop System Configuration Agent Wizard

#------------------------------------------------------------------------------

%package cli
Group:          Applications/Internet 
Summary:        Configuration Management Command Line Interface
Requires:       apoc-base

%description -n apoc-cli
Sun Java(tm) Desktop System Configuration Management Command Line Interface

#------------------------------------------------------------------------------

%package manager
Group:          Applications/Internet 
Summary:        Sun Java(tm) Desktop System Configuration Manager
Requires:       SUNWmcon

%description -n apoc-manager
Sun Java(tm) Desktop System Configuration Manager, Release 2.0

#------------------------------------------------------------------------------

%package agent-templates
Group:          Applications/Internet
Summary:        Configuration Manager templates for Configuration Agent
Requires:       apoc-manager

%description -n apoc-agent-templates
Sun Java(tm) Desktop System Configuration Manager templates for Configuration Agent

#------------------------------------------------------------------------------

%package staroffice-templates
Group:          Applications/Internet
Summary:        Configuration Manager templates for StarOffice 7
Requires:       apoc-manager

%description -n apoc-staroffice-templates
Sun Java(tm) Desktop System Configuration Manager templates for StarOffice 7

#------------------------------------------------------------------------------

%package staroffice8-templates
Group:          Applications/Internet
Summary:        Configuration Manager templates for StarOffice 8
Requires:       apoc-manager

%description -n apoc-staroffice8-templates
Sun Java(tm) Desktop System Configuration Manager templates for StarOffice 8

#------------------------------------------------------------------------------

%package gnome26-templates
Group:          Applications/Internet 
Summary:        Configuration Manager templates for Gnome 2.6 
Requires:       apoc-manager

%description -n apoc-gnome26-templates
Sun Java(tm) Desktop System Configuration Manager templates for Gnome 2.6


#==============================================================================
#  Package Build Section
#
#==============================================================================

%prep
%setup -n apoc

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

export JAVA_HOME=/usr/java/j2sdk1.4.2_06
export PATH=${JAVA_HOME}/bin:$PATH
make PLATFORM=%{PLATFORM} all

%clean
rm -rf $RPM_BUILD_ROOT


#==============================================================================
#  Package Post(Un) Install Section
#
#==============================================================================

%preun
if [ $1 -eq 0 ]; then
    /usr/lib/apoc/apocd disable
fi

#------------------------------------------------------------------------------

%post config
if [ ! -r /usr/bin/apoc-config ]; then
   ln -s /usr/bin/consolehelper /usr/bin/apoc-config
fi

%postun config
if [ $1 = 0 ]; then
   rm /usr/bin/apoc-config
fi


#==============================================================================
#  Package Files Section
#
#==============================================================================

%files
%defattr(0644, root, root)
/usr/share/lib/apoc/apocd.jar
/usr/share/lib/apoc/db.jar

%dir %attr(0755, root, root) /usr/lib/apoc
%attr(0744, root, root) /usr/lib/apoc/apocd
%attr(0755, root, root) /usr/lib/apoc/libFileAccess.so
%attr(0755, root, root) /usr/lib/apoc/libdb.so.1
%attr(0755, root, root) /usr/lib/apoc/libdb_java-4.2.so

%attr(0755, root, root) /usr/lib/libapoc.so.1
/usr/lib/libapoc.so

#------------------------------------------------------------------------------

%files base
%defattr(0644, root, root)
%dir %attr(0755, root, root) /usr/share/lib/apoc
/usr/share/lib/apoc/policymgr.jar
/usr/share/lib/apoc/spi.jar
/usr/share/lib/apoc/ldapjdk.jar

#------------------------------------------------------------------------------

%files misc
%dir %attr(0755, root, root) /etc/apoc
%dir %attr(0755, root, root) /etc/init.d
%defattr(0644, root, root)
%config /etc/apoc/apocd.properties
%config /etc/apoc/os.properties
%config %attr(0600, root, root) /etc/apoc/policymgr.properties
%attr(0755, root, root) /etc/init.d/apocd

#------------------------------------------------------------------------------

%files adapter-java
%defattr(-, root, root)
/usr/share/lib/apoc/apocprefs.jar
/usr/lib/apoc/libapoc_java.so
%attr(0755, root, root) /usr/lib/apoc/apocjlaunch

#------------------------------------------------------------------------------

%files config
%attr(0644, root, root) /etc/X11/sysconfig/apoc.desktop
%attr(0644, root, root) /etc/security/console.apps/apoc-config
%attr(0755, root, root) /etc/pam.d/apoc-config
%attr(0755, root, root) /usr/sbin/apoc-config
%defattr(0755, root, root)
/usr/share/lib/apoc/ConfigurationWizard.class
/usr/share/lib/apoc/com

#------------------------------------------------------------------------------

%files cli
%attr(0755, root, root) /usr/bin/pgtool
%attr(0644, root, root) /usr/share/lib/apoc/apoc_cli.jar
%attr(0444, root, root) /usr/man/man1/pgtool.1.gz

#------------------------------------------------------------------------------

%files manager
%defattr (0744, noaccess, noaccess)
%dir /usr/share/webconsole/apoc
%dir /usr/share/webconsole/apoc/packages
/usr/share/webconsole/apoc/html
/usr/share/webconsole/apoc/js
/usr/share/webconsole/apoc/images
/usr/share/webconsole/apoc/jsp
/usr/share/webconsole/apoc/WEB-INF
/usr/share/webconsole/apoc/dtd
%config %attr(0644, root, root) /usr/share/webconsole/apoc/WEB-INF/policymgr.cfg

#------------------------------------------------------------------------------

%files agent-templates 
%defattr (0744, noaccess, noaccess)
%dir /usr/share/webconsole/apoc
%dir /usr/share/webconsole/apoc/packages
/usr/share/webconsole/apoc/packages/ConfigurationAgent_pkg

#------------------------------------------------------------------------------
%files staroffice-templates
%defattr (0744, noaccess, noaccess)
%dir /usr/share/webconsole/apoc
%dir /usr/share/webconsole/apoc/packages
/usr/share/webconsole/apoc/packages/StarOffice7_pkg

#------------------------------------------------------------------------------

%files staroffice8-templates
%defattr (0744, noaccess, noaccess)
%dir /usr/share/webconsole/apoc
%dir /usr/share/webconsole/apoc/packages
/usr/share/webconsole/apoc/packages/StarOffice8_pkg

#------------------------------------------------------------------------------

%files gnome26-templates
%defattr (0744, noaccess, noaccess)
%dir /usr/share/webconsole/apoc
%dir /usr/share/webconsole/apoc/packages 
/usr/share/webconsole/apoc/packages/Gnome2.6_pkg


#==============================================================================
#  Package Change Log Section
#
#==============================================================================

%changelog
* Thu Jul 13 2006 - Cyrille.Moureaux@Sun.COM
- Updated tarball for build 45.

* Fri Feb 10 2006 - geoff.higgins@sun.com
- Change version from 2.0 to 1.2

* Thu Dec 15 2005 - klaus.ruehl@sun.com
- Removed the LdapLoginModule.jar file from the apoc-manager package

* Fri Sep 09 2005 - katell.galard@sun.com
- Add man page to apoc-cli package

* Thu Aug 18 2005 - geoff.higgins@sun.com
- Move daemon startup to boot sequence

* Mon Nov 29 2004 - dermot.mccluskey@sun.com
- Bump source tarball to build 24

* Mon Nov 15 2004 - damien.carbery@sun.com
- Bump source tarball to build 23.

* Mon Nov 01 2004 - dermotm.mccluskey@sun.com
- new tarball for build 22

* Wed Oct 27 2004 - klaus.ruehl@sun.com
- removed apoc-cli-misc package

* Mon Oct 18 2004 - dermotm.mccluskey@sun.com
- new tarball for build 21

* Thu Oct 14 2004 - geoff.higgins@sun.com
- Move to bdb 4

* Mon Oct 04 2004 - dermotm.mccluskey@sun.com
- new tarball for build 20

* Wed Sep 29 2004 - thomas.pfohe@sun.com
- app.xml moved to WEB-INF

* Mon Sep 27 2004 - klaus.ruehl@sun.com
- Merged the content of all other APOC spec files into this single spec file

* Mon Sep 20 2004 - dermotm.mccluskey@sun.com
- new JAVA_HOME

* Mon Sep 20 2004 - dermotm.mccluskey@sun.com
- new tarball for build 19

* Mon Sep 06 2004 - dermotm.mccluskey@sun.com
- new tarball for build 18

* Wed Sep 01 2004 - dermotm.mccluskey@sun.com
- new tarball for build 17b

* Fri Aug 13 2004 - geoff.higgins@sun.com
- Correcting version

* Thu Aug 12 2004 - geoff.higgins@sun.com
- fix for libapoc.so link

* Fri Jul 23 2004 - klaus.ruehl@sun.com
- adapted source tarball name for build 15

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Tue Jul 06 2004 - damien.carbery@sun.com
- Change to use nightly tarballs.

*Mon May 31 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 1.0-0
	Changes relating to inetd enabled startup

*Tue May 04 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-26
	Reverting to "inetd enabled install"

*Tue Apr 27 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-25
	Merging apocd, apocdctl & setenv.sh into apocd

*Mon Apr 26 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-24
	Including os.properties in apocd.jar to provide correct default

*Thu Apr 15 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-23
	Turning off Autoreqprov

*Tue Apr 13 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0-1-22
	Changing name of libapi.so to libapoc.so

*Fri Feb 20 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-20
	Performance improvements

*Mon Feb 16 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-19
	Increasing MaxRequestSize to support larger Active Directory tokens

*Mon Feb 11 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-18
	papi reconnection & GSSAPI/Active Directory support

*Mon Feb 9 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-17
	ServiceName & ServiceContainer no longer configurable

*Wed Feb 4 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-16
	Don't overwrite properties files

*Mon Feb 2 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-15
	Change detection timers

*Fri Jan 30 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-14
	Exception logging, timers etc.

*Mon Jan 19 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-13
	Add argument for inetd start

*Tue Jan 13 2004 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-12
	And back to inetd again

*Mon Dec 22 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-11
	Switching from inetd to init

*Fri Dec 19 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-10
	Changing policymgr.properties permissions

*Mon Dec 1 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-9
	Update license

*Thu Nov 27 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-8
	Fix for 4960347

*Tue Nov 20 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-7
	Moving back to berkeley db 4 due to incompatability with StarOffice

*Tue Nov 18 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-6
	YaST modules moved to seperate rpm

*Fri Nov 14 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-5
	Moving to berkeley db version 4

*Wed Nov 12 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-4
	Fix for 4952794

*Thu Nov 6 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-2
	Feature complete apocd

*Fri Jul 11 2003 Geoff Higgins <geoff.higgins@@sun.com>
	Version 0.1-1
	Initial apocd

