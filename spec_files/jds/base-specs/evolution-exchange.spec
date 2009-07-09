#
# spec file for package evolution-exchange
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
Name:         evolution-exchange
License:      GPL v2
Group:        System/Libraries/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Evolution connector for Microsoft Exchange
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/ximian-connector
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define evolution_version 2.2
%define libgnomeui_version 2.10.0
%define libglade_version 2.5.0
%define libsoup_version 2.2.3
%define GConf_version 2.10.0
%define openldap2_version 2.2.6
%define gtk_doc_version 1.3
%define oxygen2_version 1.4

Requires:       evolution >= %{evolution_version}
Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       libglade >= %{libglade_version}
Requires:       libsoup >= %{libsoup_version}
Requires:       GConf >= %{GConf_version}
Requires:       openldap2-client >= %{openldap2_version}

BuildRequires:  evolution-devel >= %{evolution_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libglade-devel >= %{libglade_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  openldap2-devel >= %{openldap2_version}
BuildRequires:  gtk-doc >= %{gtk_doc_version}

Obsoletes:	oxygen2  <= %{oxygen2_version}
Obsoletes:      ximian-connector <= 2.2.2
Provides:       ximian-connector = 2.2.2

%description
Provides a connector library for Evolution to access Microsoft Exchange.

%prep
%setup -q

%build

%ifos linux
%define ldap_option --with-openldap=%{_prefix}
%define krb5_option --with-krb5=%{_prefix}
%else
%define ldap_option --with-sunldap=%{_prefix}
%define krb5_option --with-krb5=no
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"

aclocal $ACLOCAL_FLAGS
libtoolize --force
glib-gettextize --force --copy
intltoolize --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

autoheader
automake -a -f -c --gnu
autoconf

./configure  --prefix=%{_prefix}				\
	    --sysconfdir=%{_sysconfdir}		\
	     %ldap_option					\
	     %krb5_option

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-*/camel-providers/*.la
rm $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-*/camel-providers/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/evolution-data-server-1.2/camel-providers/*.so*
%{_libdir}/evolution-data-server-1.2/camel-providers/*.urls
%{_libexecdir}/evolution/2.6/*
%{_datadir}/gtk-doc/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/evolution-exchange/*
%config %{_sysconfdir}/gconf/schemas/*

%changelog
* Tue Apr 14 2008 - jedy.wang@sun.com
- Bump to 2.26.1
* Thu Mar 19 2008 - jedy.wang@sun.com
- Bump to 2.26.0
* Thu Mar 06 2008 - jedy.wang@sun.com
- Bump to 2.25.92
* Thu Feb 05 2008 - jedy.wang@sun.com
- Bump to 2.25.90
* Thu Jan 22 2008 - jedy.wang@sun.com
- Bump to 2.25.5
* Wed Jan 14 2008 - jedy.wang@sun.com
- Bump to 2.25.4
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wec Nov 05 2008 - jedy.wang@sun.com
- Update license version.
* Tue Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0.
* Tue Sep 16 2008 - jedy.wang@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - jedy.wang@sun.com
- Bump to 2.23.91.
* Thu Aug 21 2008 - jedy.wang@sun.com
- Bump to 2.23.90.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4. Remove upstream patch, 01-libebackend.
* Wed Jun 03 2008 - jedy.wang@sun.com
- Bump to 2.23.3 and add 01-libebackend.diff.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - jedy.wang@sun.com
- Bump to 2.22.2.
* Wed May 14 2008 - damien.carbery@sun.com
- Bump to 2.22.1.2.
* Fri May 01 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Mon Apr 23 2008 - jedy.wang@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Mon Jan 14 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.12.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.12.0.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.11.91. Remove upstream patch, 01-pretty-function.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.11.90.
* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 2.11.6.1.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.11.6.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Add patch 01-pretty-function to fix build error 455858.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.11.5.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.11.4. Remove upstream patch, 01-sun-ldap.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.11.2.
* Thu May 10 2007 - simon.zheng@sun.com
- Bump to 2.11.1.
* Thu Apr 12 2007 - simon.zheng@sun.com
- Bump to 2.10.1.
* Tue Mar 13 2007 - simon.zheng@sun.com
- Bump to 2.10.0.
* Tue Feb 28 2007 - simon.zheng@sun.com
- Bump to 2.9.92.
- Rework evolution-exchanged-01-sun-ldap.diff.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.9.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.9.6.
* Tue Jan 9 2007 - jeff.cai@sun.com
- Bump version to 2.9.5
* Tue Dec 19 2006 - jeff.cai@sun.com
- Bump version to 2.9.4
* Mon Dec 18 2006 - jedy.wang@sun.com
- 01-solaris-eutil.diff removed.
- 02-sun-ldap renamed to 01-sun-ldap.
* Mon Dec 18 2006 - jedy.wang@sun.com
- Update patch comments.
* Thu Dec 14 2006 - jedy.wang@sun.com
- Set sysconfdir to /etc.
* Wed Dec 13 2006 - jedy.wang@sun.com
- Ship schema.
- 02-sol-macros replaced by 03-sun-ldap.
* Wed Dec 13 2006 - damien.carbery@sun.com
- Add patch, 03-sun-ldap, to build with Solaris LDAP defines. Bugzilla 385354.
* Wed Dec 13 2006 - jeff.cai@sun.com
- Change patch comments.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Add patch 02-sol-macros to use portable macros (G_GNUC_PRETTY_FUNCTION).
  Bugzilla 383064.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.9.3. Remove obsolete patch, 02-evo-api-ver-hack.
* Wed Nov 29 2006 - jeff.cai@sun.com
- Add patch 02-evo-api-ver-hack so that the evolution 2.9 module can be found. 
  It will be removed when evolution-exchange is bumped to 2.9.
* Tue Nov 28 2006 - jeff.cai@sun.com
- Should be 2.8.1 on trunk.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.8.2.
* Mon Oct 23 2006 - irene.huang@sun.com
- Moved evolution-exchange-01-solaris-eutil.diff
from Solaris/patches
* Fri Oct 20 2006 - damien.carbery@sun.com
- Remove 'find' call that remove .a/.la files because none are installed.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.8.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.8.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.7.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.7.90.
* Sun Jul 23 2006 - Jeff.Cai@sun.com
- Bump to 2.7.4
  Remove patch evolution-exchange-01-rename.diff
* Thu Jun 02 2006 - Irene.Huang@sun.com
- Add patch evolution-exchange-01-rename.diff 
* Tue May 30 2006 - halton.huo@sun.com
- Bump to 2.6.2.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.6.1.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec.
* Thu Mar 30 2006 - halton.huo@sun.com
- Alter "remove *.a/*.la files part" to SUNWevolution-exchange.spec
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.6.0.
* Tue Feb 28 2006 - halton.huo@sun.com
- Bump to 2.5.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.5.91.
* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 2.5.9.0.
* Thu Jan 19 2006 - halton.huo@sun.com
- Bump to 2.5.5.
* Wed Jan 04 2006 - halton.huo@sun.com
- Bump to 2.5.4.
* Wed Dec 21 2005 - halton.huo@sun.com
- Correct Source filed.
* Mon Dec 19 2005 - damien.carbery@sun.com
- Bump to 2.5.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.4.2.
* Wed Oct 12 2005 - halton.huo@sun.com
- change --with-ldap to --with-sunldap.
* Mon Oct 10 2005 - halton.huo@sun.com
- Bum to 2.4.1.
* Thu Sep 15 2005 - halton.huo@sun.com
- Use aclocal, ..., ./configure steps, not ./autogen,
  because download tarball does not have autogen.sh.
- Add define krb5_option, disable Kerberos 5 on Solaris.
* Wed Sep 7 2005 - halton.huo@sun.com
- Bump to 2.4.0.
* Fri Sep 2 2005 - halton.huo@sun.com
- Use --with-openldap=no on solaris with %ldap_option because patch is not ready.
- Use ./autogen.sh to replace libtoolize aclocal automake autoconf ./configure
  steps, because we need build code that checked out from community HEAD.
* Wed Aug 24 2005 - glynn.foster@sun.com
- Move the ximian-connector component over to evolution-exchange
  and bump to 2.3.8
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.2.3.
* Thu Jul 21 2005 - damien.carbery@sun.com
- Turn off OpenLDAP support on Solaris as it is too old.
* Thu Jul 14 2005 - damien.carbery@sun.com
- Remove obsolete gnome2-macros dir from aclocal call.
* Mon Jun 27 2005 - matt.keenan@sun.com
- Bump to 2.2.2
* Thu Jun 17 2004 - glynn.foster@sun.com
- Initial spec file for ximian-connector 1.5.9
