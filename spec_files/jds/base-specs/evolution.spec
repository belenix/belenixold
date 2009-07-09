#
# spec file for package evolution
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
%include l10n.inc
Name:         evolution
License:      GPL v2, LGPL v2.1, FDL v1.1
Group:        System/GUI/GNOME
# major_version is generally a 'stable' build number i.e. has an even number.
%define major_version 2.26
Version:      2.26.1.1
Release:      1
Distribution: java-desktop-system
Vendor:       Sun Microsystems, Inc.
Summary:      Evolution
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source2:      l10n-configure.sh
%if %build_l10n
Source3:                 l10n-configure.sh
%endif
%endif
# date:2005-01-01 owner:jefftsai type:branding 
Patch1:       evolution-01-menu-entry.diff
# date:2005-12-21 bugzilla:319376 owner:jefftsai type:bug
Patch2:       evolution-02-display-mail.diff
# date:2005-10-10 owner:jefftsai type:branding
Patch3:       evolution-03-solaris-sed.diff
# date:2006-10-24 bugzilla:364618 owner:halton type:bug
Patch4:       evolution-04-charset.diff
# date:2006-12-26 bugzilla:389668 bugster:6504980 owner:halton type:bug
Patch5:       evolution-05-memo.diff
# date:2009-04-09 bugzilla:524497 bugster:6658080 owner:halton type:bug
Patch6:       evolution-06-reply-from.diff
# date:2007-06-26 bugzilla:237830 owner:jedy type:bug
Patch7:       evolution-07-lost-tab.diff
# date:2008-01-07 bugzilla:480502 owner:jedy type:bug
Patch8:       evolution-08-meeting.diff
# date:2008-06-11 bugzilla:537752 owner:jefftsai type:bug
Patch9:       evolution-09-mail-config.diff
# date:2008-09-19 bugster:6749034 bugzilla:556369 owner:jefftsai type:bug
Patch11:       evolution-11-iconv.diff
# date:2008-09-25 bugzilla:553535 owner:jefftsai type:bug
Patch12:       evolution-12-reply-signature.diff
# date:2009-04-27 defect.opensolaris.org:6546 bugzilla:573238 owner:jeffsai type:bug
Patch13:       evolution-13-disable-ldap-base-search.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/evolution
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       scrollkeeper
Prereq:       sh-utils
Prereq:       GConf


%define GConf_version 2.5.0
%define gtkhtml_version 3.2
%define gnome_pilot_version 2.0.10
%define libgnomeui_version 2.4.0
%define scrollkeeper_version 0.3.11
%define gtk_doc_version 1.1
%define evolution_data_server_version 1.0.0

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gtkhtml-devel >= %{gtkhtml_version}
BuildRequires: GConf-devel >= %{GConf_version}
BuildRequires: gnome-pilot-devel >= %{gnome_pilot_version}
BuildRequires: evolution-data-server-devel >= %{evolution_data_server_version}
BuildRequires: firefox
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: intltool
BuildRequires: bison
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      gtkhtml >= %{gtkhtml_version}
Requires:      GConf >= %{GConf_version}
Requires:      gnome-pilot >= %{gnome_pilot_version}
Requires:      evolution-data-server >= %{evolution_data_server_version}
Requires:      firefox
Requires:      scrollkeeper >= %{scrollkeeper_version}

%description
Evolution is a mail, calendar and addressbook client for the GNOME Desktop

%package devel
Summary:      Development Evolution Libraries
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: GConf-devel >= %{GConf_version}
BuildRequires: gtkhtml-devel >= %{gtkhtml_version}
BuildRequires: evolution-data-server-devel >= %{evolution_data_server_version}

%description devel
This package contains the development libraries for Evolution, the GNOME mail, calendar
and addressbook client.

%package pilot
Summary:      Pilot support for Evolution
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version
BuildRequires: gnome-pilot-devel >= %{gnome_pilot_version}

%description pilot
This package contains the pilot support for Evolution, the GNOME mail, calendar and
addressbook client, allowing you to synchronize your Palm with Evolution.

%prep
%setup -q
%if %build_l10n
# bugster 6558756
sh -x %SOURCE2 --disable-gnu-extensions
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
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
%define krb5_option --with-krb5=%{_prefix}
%define nss_libs %{_libdir}/mps
%define nspr_libs %{_libdir}/mps
%define nss_includes %{_includedir}/mps
%define nspr_includes %{_includedir}/mps
%endif
%define pilot_option --enable-pilot-conduits=yes --with-pisock=yes
%if %option_with_gnu_iconv
%define iconv_option --with-libiconv=/usr/gnu
%else
%define iconv_option
%endif

export LDFLAGS="$LDFLAGS -L%{nss_libs} -R%{nss_libs} -L%{nspr_libs} -R%{nspr_libs}"
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS -I%{nss_includes} -I%{nspr_includes}" 

glib-gettextize --force --copy
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix}						\
	    --libexecdir=%{_libexecdir}					\
	    --sysconfdir=%{_sysconfdir}					\
	    --localstatedir=/var					\
	    --enable-default-binary					\
	    --enable-nss=yes						\
	    --enable-smime=yes						\
	    --enable-nntp=yes						\
            %pilot_option						\
            %ldap_option						\
	    --with-nss-includes=%{nss_includes}				\
            --with-nss-libs=%{nss_libs}					\
	    --with-nspr-includes=%{nspr_includes}			\
            --with-nspr-libs=%{nspr_libs}				\
	    --with-krb4=%{_prefix}					\
	    --with-cde-path=no                                          \
            --without-weather                                           \
	    %krb5_option                                                \
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
for i in C zh_CN zh_TW ko_KR ja_JP de_DE es_ES fr_FR it_IT sv_SE ; do
        langtag=$i
        [ ${i:0:2} == "zh" ] || langtag=${i:0:2}
        [ -e  %{_datadir}/omf/evolution/evolution-2.0-$langtag.omf ] && \
        env LANG=$i LC_ALL=$i scrollkeeper-install -q %{_datadir}/omf/evolution/evolution-2.0-$langtag.omf
done
scrollkeeper-update -q
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="apps_evolution_addressbook-%{major_version}.schemas apps_evolution_calendar-%{major_version}.schemas apps_evolution_shell-%{major_version}.schemas evolution-mail-%{major_version}.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig
scrollkeeper-update -q

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%{_libexecdir}/evolution/%{major_version}/*
%{_libdir}/bonobo/servers
%{_libdir}/evolution/%{major_version}/*.so.*
%{_libdir}/evolution/%{major_version}/evolution-backup
%{_libdir}/evolution/%{major_version}/components/*.so
%{_libdir}/evolution/%{major_version}/plugins/*.so
%{_libdir}/evolution/%{major_version}/plugins/*.eplug
%{_libdir}/evolution/%{major_version}/plugins/*.xml
%{_libdir}/evolution/%{major_version}/plugins/*.glade
%{_datadir}/applications/*
%{_datadir}/evolution/%{major_version}/*
%{_datadir}/gnome/help/evolution-%{major_version}/*
%{_datadir}/mime-info/*
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%config %{_sysconfdir}/gconf/schemas/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr (-, root, root)
%{_includedir}/evolution-%{major_version}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/evolution/%{major_version}/*.so
%{_datadir}/idl/*

%files pilot
%defattr (-, root, root)
%{_libdir}/evolution/%{major_version}/conduits/*.so
%{_datadir}/gnome-pilot/*

%changelog
* Mon Apr 27 2009 - zhichao.wang@sun.com
- Add patch 13-disable-ldap-base-search.diff
  Fix defect.opensolaris.org:6546 bugzilla:573238 by disabling the
  search ldap base domain button.
* Thu Apr 16 2009 - jedy.wang@sun.com
- Bump to 2.26.1.1
* Tue Apr 14 2009 - jedy.wang@sun.com
- Bump to 2.26.1
* Thr Apr 09 2009 - jeff.cai@sun.com
- Add patch -06-reply-from to fix bugzilla #524497, bugster #6820016
  Change the order of guessing account.
* Tue Mar 17 2009 - jeff.cai@sun.com
- Bump to 2.26.0
* Tue Mar 03 2009 - jeff.cai@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - jeff.cai@sun.com
- Bump to 2.25.91
* Wed Feb 04 2009 - jeff.cai@sun.com
- Bump to 2.25.90
* Wed Jan 21 2009 - jijun.yu@sun.com
- Remade patch 4.
* Wed Jan 20 2009 - jeff.cai@sun.com
- Bump to 2.25.5
* Wed Jan 07 2009 - jeff.cai@sun.com
- Bump to 2.25.4
* Tue Dec 16 2008 - dave.lin@sun.com
- Bump to 2.25.3.1
- Remove -10-cal-model, upstreamed
- Remove -13-icon-info, upstreamed
- Add --withou-weather since GWeather is not shipped
* Mon Dec 08 2008 - jeff.cai@sun.com
- Change bug comment, add bug id for -10-cal-model.diff
* Mon Dec 08 2008 - jeff.cai@sun.com
- Remove patch -06-perl-path, patch for bug #433732 upstreamed
* Wed Dec 03 2008 - jeff.cai@sun.com
- Add patch -13-icon-info to fix the crash if gnome-settings-daemon
  not started, Fix bugzilla #563077 bugster #6779039
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Nov 04 2008 - jeff.cai@sun.com
- Bump to 2.25.1
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Wed Oct 29 2008 - jeff.cai@sun.com
- Bump to 2.24.1
* Wed Oct 15 2008 - jeff.cai@sun.com
- Add bugzilla bug id for patch -11-iconv.
* Thu Sep 25 2008 - jeff.cai@sun.com
- Add patch -12-reply-signature to fix 553535
* Mon Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0
* Fri Sep 19 2008 - jeff.cai@sun.com
- Add patch -11-iconv.diff, solve the charset conversion
  error.
* Mon Sep 09 2008 - jeff.cai@sun.com
- Bump to 2.23.92.
* Mon Sep 02 2008 - jeff.cai@sun.com
- Bump to 2.23.91.
* Mon Aug 20 2008 - jeff.cai@sun.com
- Bump to 2.23.90.
- Add patch -10-cal-model
* Tue Aug 04 2008 - jeff.cai@sun.com
- Bump to 2.23.6.
- Remove patch -10-em-migrate
* Tue Jul 23 2008 - jeff.cai@sun.com
- Bump to 2.23.5.
- Add patch -10-em-migrate.
* Tue Jun 17 2008 - jeff.cai@sun.com
- Bump to 2.23.4.
* Wed Jun 11 2008 - jeff.cai@sun.com
- Add patch -09-mail-config.diff to Fix 537752
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.1.
* Mon Jun 02 2008 - jeff.cai@sun.com
- Bump to 2.23.2. Commented patch 07-tab.
  The patch will be reworked by Jedy.
* Tue May 27 2008 - jeff.cai@sun.com
- Bump to 2.22.2. Remove patch 09-print.
* Fri May 01 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Mon Apr 30 2008 - jedy.wang@sun.com
- Bump to 2.22.1. Remove  patch 09-he-plural-msgs.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0. Remove upstream patch 10-backup.
* Thu Feb 28 2008 - jeff.cai@sun.com
- Add -10-backup.diff. Fix #6660218. Need to remove when gnome 2.22 is released.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92. Remove upstream patch 11-backup.
* Wed Feb 21 2008 - jeff.cai@sun.com
- Remove -12-edit-account.diff and -10-em-utils.diff, 
  because community has fixed in #513389
* Mon Feb 18 2008 - jeff.cai@sun.com
- Add 11-backuo.diff, make backup/store work
  Fix 516648
- Add 12-edit-account.diff, Fix 517131
- Ship evolution-backup.
* Fri Feb 15 2008 - jeff.cai@sun.com
- Add 10-em-utils.diff, fix 516610.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91. Remove upstream patch 10-exchange-url.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Add 09-he-plural-msgs to remove plural msgs from he.po. These were breaking
  the build.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2. Remove upstream patch, 08-unions.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Add patch 08-unions to name unnamed unions to build with Sun Studio compiler.
* Wed Oct 31 2007 - simon.zheng@sun.com
- Fix bugster bug #6610136, disable unuseful launch script.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.12.1.
* Thu Oct  4 2007 - laca@sun.com
- use the --with-libiconv=/usr/gnu option when building with GNU libiconv
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.12.0.
* Tue Sep 04 2007 - jijun.yu@sun.com
- Modify evolution-04-charset.diff patch.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri Aug 17 2007 - jedy.wang@sun.com
- Fix 'patch* -p0' - change to -p1 and change patch file too.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.11.90.
* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 2.11.6.1.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.11.6. Remove upstream patch, 08-create-new-meeting.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.11.5. Remove upstream patches, 07-empty-line and 09-save-all-parts.
* Thu Jul 05 2007 - simon.zheng@sun.com
- 10-create-new-meeting added.
* Tue Jul 03 2007 - simon.zheng@sun.com
- 09-save-all-parts.diff added.
* Tue Jun 26 2007 - jedy.wang@sun.com
- 07-empty-line.diff added.
- 08-lost-tab.diff added.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.11.4. Remove upstream patch, 03-kerberos.
* Wed Jun 13 2007 - takao.fujiwara@sun.com
- Add l10n-configure.sh to remove GNU extension from many .po
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.11.3. Remove upstream patches, 07-selected-mail and
  08-edit-account-button. Renumber rest.
* Wed May 30 2007 - jeff.cai@sun.com
- add patch selected-mail.diff
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.11.2. Remove upstream patches, 04-pixmap-new, 12-awk, 14-shutdown,
  15-evolution-addressbook-export, 17-calendar-localized-char. Renumber rest.
* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 2.11.1.1. Bump major_version to 2.12.
* Thu Apr 26 2007 - laca@sun.com
- add patch perl-path.diff
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.10.1. Remove upstream patches, 17-contact-preview and 
  18-delete-automatic-contacts. Renumber rest.
* Mon Apr 09 2007 - simon.zheng@sun.com
- Add patch evolution-19-calendar-localized-char.diff
  fix bugster #6542876, unable to copy and paste an appointment
  with localized characters
- Add patch evolution-18-delete-automatic-contacts.diff
  fix bugster #6542899, crash when deleting automatic contacts.
* Thu Apr 05 2007 - simon.zheng@sun.com
- Add patch evolution-17-contact-pane.diff,
  fix bugster #6538542.
* Mon Apr 02 2007 - simon.zheng@sun.com
- Add patch evolution-16-edit-account-button.diff,
  fix bugster #6538042.
* Wed Mar 21 2007 - jijun.yu@sun.com
- Modify the comments for patch evolution-11-memo.diff.
* Tue Mar 13 2007 - simon.zheng@sun.com
- Bump to 2.10.0. Remove upstream patch, 13-add-attachment. Renumber remainder.
* Mon Mar 05 2007 - jijun.yu@sun.com
- Change comment on evolution-11-memo.diff.
* Tue Feb 28 2007 - simon.zheng@sun.com
- Change comment on evolution-04-pixmap-new.diff.
* Tue Feb 28 2007 - simon.zheng@sun.com
- Bump to 2.9.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patches, 13-glade, 14-etext and
  16-mail-header. Renumber remainder.
* Fri Feb 09 2007 - jeff.cai@sun.com
- Add patch -16-mail-header to fix #400841.
* Fri Feb 09 2007 - jijun.yu@sun.com
- Modify patch evolution-11-memo.diff to fix bugster 6522186.
* Fri Feb 02 2007 - jeff.cai@sun.com
- Added new patch evolution-15-add-attachment.diff to fix bugzilla 399307 
  and bugster 6497879.
* Thu Jan 24 2007 - jedy.wang@sun.com
- Added new patch evolution-14-etext.diff to fix bugzilla 400121 and bugster
  6514112.
* Tue Jan 23 2007 - jeff.cai@sun.com
- Bump to 2.9.6.
* Thu Jan 18 2007 - jedy.wang@sun.com
- Added new patch evolution-13-glade.diff to fix bugzilla 397893 and bugster
  6514087.
* Thu Jan 09 2007 - jedy.wang@sun.com
- Added new patch evolution-12-awk.diff to fix bugzilla 394579 and bugster
  6510008.
* Thu Jan 04 2007 - jijun.yu@sun.com
- Its dependencies-gnome-pilot and pilot-link are updated to new version
* Fri Dec 27 2006 - jedy.wang@sun.com
- Added new patch evolution-08-todo.diff
- Added new patch evolution-09-menuitem.diff
* Fri Dec 22 2006 - simon.zheng@sun.com
- Added new patch evolution-07-mail-account.diff
* Tue Dec 19 2006 - jeff.cai@sun.com
- Bump version to 2.9.4.
* Wed Dec 13 2006 - jeff.cai@sun.com
- Change patch comments.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.9.3.
* Tue Tue 28 2006 - jeff.cai@sun.com
- Bump to 2.9.2.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.8.2.1.
* Mon Oct 23 2006 - irene.huang@sun.com
- Added new patch evolution-05-kerberos.diff
  and evolution-06-solaris-sed.diff (moved from Solaris/patches)
* Fri Oct 20 2006 - jeff.cai@sun.com
- Bump to 2.8.1.1
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.8.1.
* Thu Sep 28 2006 - simon.zheng@sun.com
- Add patch evolution-04-pixmap-new.diff
* Wed Sep 06 2006 - irene.huang@sun.com
- add patch 03-display-mail.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.8.0.
- Remove upstream patches, 01-display-mail and 04-local-account. Renumber rest.
* Tue Aug 20 2006 - simon.zheng@sun.com
- Add one patch evolution-04-local-account.diff
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.7.91.
* Mon Jun 24 2006 - damien.carbery@sun.com
- Bump to 2.7.90
* Fri Jun 21 2006 - jeff.cai@sun.com
- Bump to 2.7.4
  Remove following patches
     evolution-04-contact-print-dialog.diff
     evolution-05-message-list.diff
     evolution-06-e-sidebar.diff
     evolution-07-ecell-text.diff
  Change major version to 2.8
* Thu Jun 22 2006 - li.yuan@sun.com
- Add one patch:
  evolution-07-ecell-text.diff, make message can be grabbed by gok.
* Fri Jun 09 2006 - li.yuan@sun.com
- Add one patch:
  evolution-06-e-sidebar.diff, to fix an Evolution crash bug, CR6425103.
* Thu May 30 2006 - li.yuan@sun.com
- Add one patch:
  evolution-05-message-list.diff
* Tue May 30 2006 - halton.huo@sun.com
- Bump to 2.6.2.
- Remove upstreamed patch evolution-05-exchange-operation.diff.
* Thu Apr 29 2006 - simon.zheng@sun.com
- Add two patches:
  evolution-04-contact-print-dialog.diff
  evolution-05-exchange-operation.diff
* Wed Apr 26 2006 - halton.huo@sun.com
- Use JES's NSS/NSPR(/usr/lib/mps) instead of that provided by
  mozilla or firefox, to fix bug #6418049.
* Thu Apr 13 2006 - halton.huo@sun.com
- Firefox move from /usr/sfw to /usr.
* Tue Apr 11 2006 - halton.huo@sun.com
- Remove upstream patch: 03-remove-uri.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.6.1.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Alter "remove *.a/*.la files part" to SUNWevolution.spec
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.6.0.
- Remove upstream patches, 03-init-config and 05-show-border. Rename remainder.
* Fri Mar 3 2006 - jeff.cai@sun.com
- add three patches:
  evolution-03-init-config.diff
  evolution-04-remove-uri.diff
  evolution-05-show-border.diff
* Tue Feb 28 2006 - halton.huo@sun.com
- Bump to 2.5.92.
- Remove upstreamed patches:
  evolution-03-caldav-startup-fail.diff,
  evolution-04-return-fix.diff.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.5.91.
* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 2.5.90.
* Mon Jan 23 2006 - Irene.Huang@sun.com
- Add patch evolution-03-caldav-startup-fail.diff.
* Fri Jan 20 2006 - halton.huo@sun.com
- Bump to 2.5.5.1.
* Thu Jan 17 2006 - halton.huo@sun.com
- Bump to 2.5.5.
- Removed upstreamed patches and reorder:
  evolution-02-addressbook-config-ludcheck.diff
  evolution-04-build-fix.diff
  evolution-05-search-clear-crash.diff
* Thu Jan 12 2006 - Irene.Huang@sun.com
- Add patch evolution-05-search-clear-crash.diff 
  for bug 6371085 in bugzilla.
* Thu Jan 12 2006 - glynn.foster@sun.com
- Add upstream evolution-04-build-fix.diff which fixes
  send/receive crash.
* Tue Jan 10 2006 - halton.huo@sun.com
- Add patch evolution-03-conduit.diff.
- Set --enable-pilot-conduits=yes.
- Add define plink_prefix.
* Fri Jan 06 2006 - simon.zheng@sun.om
- Add patch evolution-02-dddressbook-config-ludcheck.diff.
* Wed Jan 04 2006 - halton.huo@sun.com
- Bump to 2.5.4.
- Remove upstreamed patches: 
  evolution-02-be-po.diff,
  evolution-03-alarm-hang.diff.
* Wed Dec 21 2005 - halton.huo@sun.com
- Rename evolution-01-6334819.diff 
  to evolution-01-display-mail.diff.
- Rename evolution-03-alarm-hang-6364800.diff 
  to evolution-03-alarm-hang.diff.
* Wed Dec 21 2005 - halton.huo@sun.com
- Correct Source filed.
- Change major_verion from 2.4 to 2.6.
- Add patch evolution-02-be-po.diff.
- Add patch evolution-03-alarm-hang-6364800.diff.
* Tue Dec 19 2005 - damien.carbery@sun.com
- Bump to 2.5.3.
* Tue Dec 13 2005 - halton.huo@sun.com
- Bump to 2.4.2.1.
* Fri Dec 02 2005 - dave.lin@sun.com
- Add evolution-02-6355700.diff for 2.4.2
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.4.2.
* Wed Nov 23 2005 - halton.huo@sun.com
- Add patch evolution-01-6334819.diff.
* Tue Nov 09 2005 - halton.huo@sun.com
- Add option --enable-default-binary, create evolution link to 
  evolution-2.4, fix bug #6344895, better than old one.
* Tue Nov 08 2005 - halton.huo@sun.com
- Add evolution link to evolution-2.4, fix bug #6344895.
* Fri Oct 21 2005 - halton.huo@sun.com
- Disable pilot-conduits on solaris for does not work now.
- Use firefox nss/nspr lib instead of mozilla's.
* Wed Oct 12 2005 - halton.huo@sun.com
- change --with-ldap to --with-sunldap.
* Mon Oct 10 2005 - halton.huo@sun.com
- Bump to 2.4.1.
- Move upstreamed patch evolution-01-configure-grep.diff.
* Thu Sep 15 2005 - halton.huo@sun.com
- Add define krb5_option, disable Kerberos 5 on Solaris.
* Thu Sep 8 2005 - halton.huo@sun.com
- Add krb5_prefix define and Enable Kerberos 5.
- Fix CFLAGS problem.
- Use aclocal, ..., ./configure steps, not ./autogen,
  because download tarball does not have autogen.sh.
* Wed Sep 7 2005 - damien.carbery@sun.com
- Bump to 2.4.0.
* Mon Sep 5 2005 - halton.huo@sun.com
- Temporarily --enable-exchange=no because e-d-s with Kerberos is not ready.
- Move patch evolution-01-solaris-ldap.diff to SUNWevolution.spec.
- Add patch evolution-01-configure-grep.diff for configure.in "grep -q" bug.
* Fri Sep 2 2005 - halton.huo@sun.com
- Remove gal since it is merged in evolution itself.
- Remove DB3 since it is merged in evolution-data-server.
- Add option --enable-nntp=yes to support news groups.
- Add option --enable-exchange=yes to support exchange plugin.
- Use SUN LDAP on solaris with %ldap_option.
- Use ./autogen.sh to replace libtoolize aclocal automake autoconf ./configure
  steps, because we need build code that checked out from community HEAD.
- Temporarily disable Kerberos for header files are not installed on Nevada.
* Tue Aug 30 2005 - glynn.foster@sun.com
- Bump to 2.3.8
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.3.7.
* Thu Jul 28 2005 - damien.carbery@sun.com
- Rename --with-openldap configure option to --with-ldap as a result of Jerry's
  patch from Jul 27. Also remove '%ifos' code around this option.
* Wed Jul 27 2005 - damien.carbery@sun.com
- Add patch from Jerry Pu (Shi.Pu@sun.com) to support LDAP on Solaris.
* Wed Jul 13 2005 - damien.carbery@sun.com
- Remove gnome2-macros dir from aclocal call as that dir no longer exists.
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 2.2.3
* Mon May 16 2005 - glynn.foster@sun.com
- Bump to 2.2.2
* Tue Nov 23 2004 - glynn.foster@sun.com
- Bump to 2.0.2
* Thu Jun 17 2004 - niall.power@sun.com
- rpm4'ified
* Thu Jun 17 2004 - glynn.foster@sun.com
- Bump to 1.5.9.2
* Tue Jun 08 2004 - glynn.foster@sun.com
- Bump to 1.5.9
* Fri May 21 2004 - glynn.foster@sun.com
- Bump to 1.5.8
* Tue Apr 20 2004 - glynn.foster@sun.com
- Bump to 1.5.7
* Mon Apr 19 2004 - glynn.foster@sun.com
- Initial spec file for Evolution 1.5.x
