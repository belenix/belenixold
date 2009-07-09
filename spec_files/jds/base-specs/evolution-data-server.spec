# spec file for package evolution-data-server
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
Name:         evolution-data-server
License:      LGPL v2
Group:        System/Libraries/GNOME
Version:      2.26.1.1
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Backend Library for Evolution
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
%endif
# date:2006-09-28 owner:sh162551 type:branding
Patch1:       evolution-data-server-01-libexec.diff

%if %option_with_sun_branding
# date:2009-03-11 owner:jefftsai defect.opensolaris.org:6752 bugster:6791003 type:bug
Patch2:       evolution-data-server-02-open-address-book-sparc.diff
%endif
Docdir:       %{_defaultdocdir}/evolution-data-server
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define api_version 1.2
%define base_version 1.6

%define libbonobo_version 2.4.2
%define gnome_vfs_version 2.4
%define libgnome_version 2.4
%define GConf_version 2.4
%define libsoup_version 2.2.3
%define gtk_doc_version 1.1
%define openldap2_version 2.1.4

Requires:       libbonobo >= %{libbonobo_version}
Requires:       gnome-vfs >= %{gnome_vfs_version}
Requires:       libgnome >= %{libgnome_version}
Requires:       GConf >= %{GConf_version}
Requires:       libsoup >= %{libsoup_version}
Requires:       openldap2-client >= %{openldap2_version}

BuildRequires:  libbonobo-devel >= %{libbonobo_version}
BuildRequires:  gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires:  libgnome-devel >= %{libgnome_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  openldap2-devel >= %{openldap2_version}
BuildRequires:  gtk-doc >= %{gtk_doc_version}
BuildRequires:  bison
BuildRequires:  heimdal-devel

%description
evolution-data-server is the backend library for Evolution, providing
support for calendar and addressbook.

%package devel
Summary:      Development Backend Library for Evolution
Group:        Development/Libraries/GNOME
Autoreqprov:  on
Requires:     %name = %version
BuildRequires:  libbonobo-devel >= %{libbonobo_version}
BuildRequires:  gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires:  libgnome-devel >= %{libgnome_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  openldap2-devel >= %{openldap2_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}

%description devel
evolution-data-server is the backend library for Evolution, providing
support for calendar and addressbook.

%prep
%setup -q
%if %build_l10n
# bugster 6558756
sh -x %SOURCE1 --disable-gnu-extensions
%endif
%patch1 -p1
%if %option_with_sun_branding
%patch2 -p0
%endif

%build

%ifos linux
%define ldap_option --with-openldap=%{_prefix}
%define krb5_option --with-krb5=%{_prefix}
%define nss_libs %{_libdir}/firefox
%define nspr_libs %{_libdir}/firefox
%define nss_includes %{_includedir}/firefox/nss
%define nspr_includes %{_includedir}/firefox/nspr
%else
%define ldap_option --with-sunldap=%{_prefix}
%if %is_s10
%define krb5_option --without-krb5
%else
%define krb5_option --with-krb5=%{_prefix}
%endif
%define nss_libs %{_libdir}/mps
%define nspr_libs %{_libdir}/mps
%define nss_includes %{_includedir}/mps
%define nspr_includes %{_includedir}/mps
%endif
%if %option_with_gnu_iconv
%define iconv_option --with-libiconv=/usr/gnu
%else
%define iconv_option
%endif

export LDFLAGS="$LDFLAGS -L%{nss_libs} -R%{nss_libs} -L%{nspr_libs} -R%{nspr_libs}"
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS -I%{nss_includes} -I%{nspr_includes}"

aclocal $ACLOCAL_FLAGS
libtoolize --force
glib-gettextize --force --copy
intltoolize --force --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

autoheader
automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix}						\
	    --libexecdir=%{_libexecdir}					\
	    --sysconfdir=%{_sysconfdir}					\
	    --enable-nss=yes						\
	    --enable-smime=yes						\
	    --enable-nntp=yes						\
	    --with-nss-includes=%{nss_includes}				\
	    --with-nss-libs=%{nss_libs}					\
	    --with-nspr-includes=%{nspr_includes}			\
	    --with-nspr-libs=%{nspr_libs}				\
            --without-weather                                              \
	    %ldap_option						\
	    --with-krb4=%{_prefix}					\
	    %krb5_option						\
            %gtk_doc_option                                             \
	    %bdb_option                                                 \
            %iconv_option

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*
%{_libdir}/evolution-data-server-%{api_version}/extensions/*.so
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.so
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*urls
%{_libdir}/bonobo/servers/*
%{_libexecdir}/*
%{_datadir}/evolution-data-server-%{base_version}/*
%{_datadir}/pixmaps/evolution-data-server-%{base_version}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr (-, root, root)
%{_libdir}/*.so
%{_includedir}/evolution-data-server-%{base_version}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/*
%{_datadir}/idl/*

%changelog
* Thu Apr 16 2009 - jedy.wang@sun.com
- Bump to 2.26.1.1
* Tue Apr 14 2009 - jedy.wang@sun.com
- Bump to 2.26.1
* Tue Mar 16 2009 - jeff.cai@sun.com
- Bump to 2.26.0
- Remove -02-conditional-if and -03-imap-mail, upstreamed.
- Rename -04-open-address-book-sparc to -02-open-address-book-sparc
* Wed Mar 11 2009 - jeff.cai@sun.com
- Not apply the patch -04-open-address-book-sparc on OpenSolaris.
* Wed Mar 11 2009 - zhichao.wang@sun.com
- Add patch -04-open-address-book-sparc to fix d.o.o bug #6752 
  To resolve the address book can not be open on sparc matchine.
  This patch can be removed after BDB is upgraded to 4.8.
* Mon Mar 09 2009 - jeff.cai@sun.com
- Add -03-imap-mail, Fix #574236
* Tue Mar 03 2009 - jeff.cai@sun.com
- Bump to 2.25.92
- Remove -02-view-local-mail, upstreamed
- Add -02-conditional-if, Fix #573870. Use the
  standard conditional if sentence.
* Tue Feb 17 2009 - jeff.cai@sun.com
- Bump to 2.25.91
- Remove patch -03-libical, upstreamed.
* Thu Feb 05 2009 - jedy.wang@sun.com
- Add patch 02-libical.diff to fix bugzilla 569459.
* Wed Feb 04 2009 - jeff.cai@sun.com
- Add patch -02-view-local-mail, This is a tempoary fix.
  Maybe the community can give a better solution.
  Fix bugster 6791021, bugzilla 567008.
* Wed Feb 04 2009 - jeff.cai@sun.com
- Bump to 2.25.90
* Wed Jan 20 2009 - jeff.cai@sun.com
- Bump to 2.25.5
* Wed Jan 07 2009 - jeff.cai@sun.com
- Bump to 2.25.4
* Tue Dec 15 2008 - dave.lin@sun.com
- Bump to 2.25.3
- Remove -02-func, upstreamed.
- Add --without-weather since GWeather is not shipped.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Nov 04 2008 - jeff.cai@sun.com
- Bump to 2.25.1
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Wed Oct 29 2008 - jeff.cai@sun.com
- Bump to 2.24.1
* Wed Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0
* Wed Sep 09 2008 - jeff.cai@sun.com
- Bump to 2.23.92
- Add patch -02-func.diff
* Wed Sep 02 2008 - jeff.cai@sun.com
- Bump to 2.23.91
- Remove upstream patch -02-local.
* Wed Aug 27 2008 - jeff.cai@sun.com
- Add patch -02-local to fix 213072
* Mon Aug 20 2008 - jeff.cai@sun.com
- Bump to 2.23.90.1
- Remove patch -02-errno and -03-mbox-spool
* Tue Aug 05 2008 - jeff.cai@sun.com
- Roll back to 2.23.6
- Add patch -03-mbox-spool to fix 
  #6732079, #6732076
- Bump to 2.23.6.2
* Tue Aug 05 2008 - jeff.cai@sun.com
- Bump to 2.23.6.2
* Tue Aug 04 2008 - jeff.cai@sun.com
- Bump to 2.23.6
* Tue Jul 29 2008 - jedy.wang@sun.com
- Add patch -05-summary.
* Wed Jul 23 2008 - jeff.cai@sun.com
- Add patch -04-google-backend. Fix 544264
- Remove -04-no-google-backend.
- Remove -02-google-calendar.
- Add -02-gtk-doc. Fix 543855
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5. Remove upstream patches 04-attachment and 05-ldap. Add patch
  to work around build failure in google backend (04-no-google-backend).
* Wed Jul 04 2008 - jeff.cai@sun.com
- Add patch -04-attachment.diff. Fix #534080.
* Wed Jul 03 2008 - jeff.cai@sun.com
- Add patch -03-errno.diff. Fix #538074.
* Tue Jun 17 2008 - jeff.cai@sun.com
- Bump to 2.23.4.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3. Remove upstream patch 03-build.
* Thu Jun 02 2008 - jeff.cai@sun.com
- Bump 2.23.2, add patch -03-build.diff. 
* Thu May 29 2008 - damien.carbery@sun.com
- Revert to 2.22.2 because of build error. Module owner notified.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - jeff.cai@sun.com
- Bump to 2.22.2
* Fri May 01 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Mon Apr 23 2008 - jedy.wang@sun.com
- Bump to 2.22.1. Remove upstream patch 02-libical.diff.
  Add 02-google-calendar.diff. Fix 527544.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92. Remove upstream patch 03-decode.
* Wed Feb 20 2008 - jeff.cai@sun.com
- Remove -02-camel-message.diff. Community has fixed
  in 513389.
* Mon Feb 18 2008 - jeff.cai@sun.com
- Add -03-decode.diff, Fix 517190
* Fri Feb 15 2008 - jeff.cai@sun.com
- Add -02-camel-message.diff, Fix 516598
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Fri Jan 18 2008 - damien.carbery@sun.com
- Bump to 2.21.5.1.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1. Remove upstream patch, 02-function.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 1.12.1. Add patch 02-function to fix bugzilla 488173.
* Wed Oct  3 2007 - laca@sun.com
- use the --with-libiconv=/usr/gnu option when building with GNU libiconv
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.12.0.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 1.11.92.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 1.11.91. Remove upstream patches 02-endian and 03-timezone.
* Fri Aug 17 2007 - jedy.wang@sun.com
- Fix 'patch* -p0' - change to -p1 and change patch file too.
* Thu Aug 16 2007 - jedy.wang@sun.com
- Remove the commands to autotoolize libical.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 1.11.90.
* Tue Aug 15 2007 - jedy.wang@sun.com
- Update patch 02-endian.diff and 03-timezone.diff
* Tue Aug 07 2007 - jeff.cai@sun.com
- Add patch 03-timezone.diff to use zone_sun.tab instead 
  of zone.tab. Fix #464252
* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 1.11.6.1. Add patch 02-endian to fix build errors, #462499.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 1.11.6.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 1.11.5.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 1.11.4. Remove upstream patch, 01-kerberos.
* Wed Jun 13 2007 - takao.fujiwara@sun.com
- Add l10n-configure.sh to remove GNU extension from de.po, et.po, hu.po,
  it.po and ja.po
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 1.11.3.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 1.11.2.
* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 1.11.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 1.10.1. Remove upstream patch 03-libbdb.
* Wed Apr 04 2007 - simon.zheng@sun.com
- Add patch evolution-data-server-03-libbdb.diff, 
  to fix bugster bug #6538754.
* Tue Mar 13 2007 - simon.zheng@sun.com
- Bump to 1.10.0.
* Tue Feb 28 2007 - simon.zheng@sun.com
- Bump to 1.9.92.
* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 1.9.91. Remove upstream patch, 03-mail-header.
* Fri Feb 09 2007 - jeff.cai@sun.com
- Add patch, 03-mail-header, to fix #400841.
* Sun Jan 28 2007 - laca@sun.com
- disable krb5 support on s10
* Wed Jan 24 2007 - damien.carbery@sun.com
- Bump to 1.9.6.1. Remove upstream patch, 03-gnome-keyring.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Add patch, 03-gnome-keyring, to fix build error, #399706.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 1.9.6.
* Tue Jan 09 2007 - jeff.cai@sun.com
- Bump to 1.9.5.
- Remove build patch for bug 387397.
* Wed Dec 20 2006 - jeff.cai@sun.com
- Add bugzilla bug number for patch 3.
* Tue Dec 19 2006 - jeff.cai@sun.com
- Add patch evolution-data-server-03-exchange-account.diff
  to resolve building broken on Solaris.
* Tue Dec 19 2006 - jeff.cai@sun.com
- Bump to 1.9.4.
* Wed Dec 13 2006 - jeff.cai@sun.com
- Change patch comments.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 1.9.3.
* Tue Nov 28 2006 - jeff.cai@sun.com
- Bump to 1.9.2 and remove patch:
  evolution-data-server-03-mail-rlimit.diff
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 1.8.2.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Nov 04 2006 - irene.huang@sun.com
- Change owner to be opensolaris account.
* Mon Oct 23 2006 - irene.huang@sun.com
- moved evolution-data-server-01-kerberos.diff
  and evolution-data-server-02-libexec.diff and 
  evolution-data-server-03-mail-rlimit.diff from
  Solaris/patches
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 1.8.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 1.8.0.
- Remove upstream patch, 01-attachment.
* Tue Aug 21 2006 - jedy.wang@sun.com
- Add one patch, 01-attachment.diff, for 6461581.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 1.7.91.
* Wed Jul 26 2006 - halton.huo@sun.com
- Use system BerkeleyDB.
* Wed Jul 26 2006 - jeff.cai@sun.com
- Bump to 1.7.90.1
  Remove patches/evolution-data-server-01-libebook-files.diff.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Add patch to include files missing from tarball (but in cvs).
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 1.7.90
* Fri Jul 21 2006 - jeff.cai@sun.com
- Bump to 1.7.4
* Tue May 30 2006 - halton.huo@sun.com
- Bump to 1.6.2.
* Wed Apr 26 2006 - halton.huo@sun.com
- Use JES's NSS/NSPR(/usr/lib/mps) instead of that provided by
  mozilla or firefox, to fix bug #6418049.
* Thu Apr 13 2006 - halton.huo@sun.com
- Firefox move from /usr/sfw to /usr.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 1.6.1.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec.
* Thu Mar 30 2006 - halton.huo@sun.com
- Alter "remove *.a/*.la files part" to SUNWevolution-data-server.spec
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.6.0.
* Tue Feb 28 2006 - halton.huo@sun.com
- Bump to 1.5.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 1.5.91.
* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 1.5.90.
* Thu Jan 19 2006 - halton.huo@sun.com
- Bump to 1.5.5.
* Wed Jan 04 2006 - halton.huo@sun.com
- Bump to 1.5.4.
* Wed Dec 21 2005 - halton.huo@sun.com
- Correct Source filed.
- Remove upstreamed patch evolution-data-server-6341837.diff.
- Remove upstreamed patch evolution-data-server-6359639.diff.
* Fri Dec 19 2005 - damien.carbery@sun.com
- Bump to 1.5.3.
- Bump to 1.4.2.1.
* Fri Dec 09 2005 - dave.lin@sun.com
- Add the patch evolution-data-server-6359639.diff
* Fri Dec 02 2005 - dave.lin@sun.com
- Bump to 1.4.2.1.
- Add the patch evolution-data-server-6341837.diff
* Thu Dec 01 2005 - damien.carbery@sun.com
- Remove upstream patch, patches/evolution-data-server-01-6340601.diff.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 1.4.2.
* Wed Nov 23 2005 - halton.huo@sun.com
- Add patch evolution-data-server-01-6340601.diff.
* Fri Oct 21 2005 - halton.huo@sun.com
- Use firefox nss/nspr lib instead of mozilla's.
* Wed Oct 12 2005 - halton.huo@sun.com
- change --with-ldap to --with-sunldap.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 1.4.1.1.
* Mon Oct 10 2005 - halton.huo@sun.com
- Bump to 1.4.1.
- Move obsolete patches:
  evolution-data-server-01-libgobject.diff,
  evolution-data-server-02-pretty_function.diff.
- Move upstreamed patches:
  evolution-data-server-03-lock-helper.diff.
* Thu Sep 15 2005 - halton.huo@sun.com
- Add define krb5_option, disable Kerberos 5 on Solaris.
* Thu Sep 8 2005 - halton.huo@sun.com
- Add krb5_prefix define and enable Kerberos 5.
- Fix CFLAGS problem.
* Wed Sep 7 2005 - halton.huo@sun.com
- Bump to 1.4.0.
* Tue Sep 6 2005 - damien.carbery@sun.com
- Call configure instead of autogen.sh because autogen.sh not in 1.3.8 tarball.
  Remove some ver nums from %files because there is no consistency.
  Remove patch3 and reorder.
* Tue Sep  6 2005 - halton.huo@sun.com
- Move patch evolution-data-server-04-ldap-ssl.diff and Source1 
  evolution-data-server-ldap-ssl-patch.tar to SUNWgnutls.spec.
* Fri Sep 2 2005 - halton.huo@sun.com
- Add option --enable-nntp=yes to support news groups.
- Use SUN LDAP on solaris with %ldap_option.
- Add Source1 Patch4 to support SUN LDAP
- Use ./autogen.sh to replace libtoolize aclocal automake autoconf ./configure 
  steps, because we need build code that checked out from community HEAD.
- Temporarily disable Kerberos for header files are not installed on Nevada.
* Tue Aug 30 2005 - damien.carbery@sun.com
- Redefine major_version to 1.2 so that %files section can use while patch 03 
  redefines it to 1.2.
* Tue Aug 30 2005 - glynn.foster@sun.com
- Bump to 1.3.8
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 1.3.7.
* Thu Jul 28 2005 - damien.carbery@sun.com
- Rename --with-openldap configure option to --with-ldap as a result of Jerry's
  patch from Jul 27. Also remove '%ifos' code around this option.
* Wed Jul 27 2005 - damien.carbery@sun.com
- Add patch from Jerry Pu (Shi.Pu@sun.com) to support LDAP on Solaris.
* Thu Jul 14 2005 - damien.carbery@sun.com
- Add 5 patches to build on Solaris.
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 1.2.3
* Tue May 10 2005 - glynn.foster@sun.com
- Bump to 1.2.2
* Tue Nov 23 2004 - glynn.foster@sun.com
- Bump to 1.0.2
* Thu Jun 17 2004 - niall.power@sun.com
- rpm4´ified
* Thu Jun 17 2004 - glynn.foster@sun.com
- Bump to 0.0.94.1
* Tue Jun 08 2004 - glynn.foster@sun.com
- Bump to 0.0.94
* Fri May 21 2004 - glynn.foster@sun.com
- Bump to 0.0.93
* Tue Apr 20 2004 - glynn.foster@sun.com
- Bump to 0.0.92
* Mon Apr 19 2004 - glynn.foster@sun.com
- Initial spec file for evolution-data-server 0.0.91
