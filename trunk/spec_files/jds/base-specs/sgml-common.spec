#
# spec file for package sgml-common
#
# copied from fedora core 6
#
# Owner: laca
#
Name: sgml-common
Version: 0.6.3
Release: 18
Group: Applications/Text

Summary: Common SGML catalog and DTD files.

License: GPL

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Source0: ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tgz
# From openjade:
Source3: xml.dcl
Source4: xml.soc
Source5: html.dcl
Source6: html.soc
# owner:laca type:bug date:2007-02-12 state:upstream from Fedora Core 6
Patch0: sgml-common-01-umask.diff
# owner:laca type:bug date:2007-02-12 state:upstream from Fedora Core 6
Patch1: sgml-common-02-xmldir.diff
# owner:laca type:bug date:2007-02-12 state:upstream from Fedora Core 6
Patch2: sgml-common-03-quotes.diff
# owner:laca type:bug date:2007-02-12 state:upstream from Fedora Core 6
Patch3: sgml-common-04-automake.diff
# owner:laca type:bug date:2007-02-12 state:upstream from Fedora Core 6
Patch4: sgml-common-05-docdir.diff
# owner:mattman type:branding date:2009-02-27
Patch5: sgml-common-06-manpage.diff

Requires: sh-utils fileutils textutils grep
BuildRequires: libxml2 >= 2.4.8-2
BuildRequires: automake
BuildRequires: autoconf

%description
The sgml-common package contains a collection of entities and DTDs
that are useful for processing SGML, but that don't need to be
included in multiple packages.  Sgml-common also includes an
up-to-date Open Catalog file.

%package -n xml-common
Group: Applications/Text
Summary: Common XML catalog and DTD files.
License: GPL
URL: http://www.iso.ch/cate/3524030.html
Requires: sh-utils fileutils textutils grep

%description -n xml-common
The xml-common package contains a collection of entities and DTDs
that are useful for processing XML, but that don't need to be
included in multiple packages.


%prep
%setup -q
%patch0 -p1 -b .umask
%patch1 -p1 -b .xmldir
%patch2 -p1 -b .quotes
%patch3 -p1 -b .automake
%patch4 -p1 -b .docdir
%patch5 -p1 -b .docdir

%build
aclocal $ACLOCAL_FLAGS
autoconf
automake --add-missing --copy

./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --with-docdir=%{_docdir}


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/xml
mkdir -p $RPM_BUILD_ROOT/usr/share/sgml/docbook
# Create an empty XML catalog.
XMLCATALOG=$RPM_BUILD_ROOT/etc/xml/catalog
/usr/bin/xmlcatalog --noout --create $XMLCATALOG
# Now put the common DocBook entries in it
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//ENTITIES DocBook XML" \
	"file:///usr/share/sgml/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file:///usr/share/sgml/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegatePublic" \
	"ISO 8879:1986" \
	"file:///usr/share/sgml/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegateSystem" \
	"http://www.oasis-open.org/docbook/" \
	"file:///usr/share/sgml/docbook/xmlcatalog" $XMLCATALOG
/usr/bin/xmlcatalog --noout --add "delegateURI" \
	"http://www.oasis-open.org/docbook/" \
	"file:///usr/share/sgml/docbook/xmlcatalog" $XMLCATALOG
# Also create the common DocBook catalog
/usr/bin/xmlcatalog --noout --create \
	$RPM_BUILD_ROOT/usr/share/sgml/docbook/xmlcatalog

rm -f $RPM_BUILD_ROOT/usr/share/sgml/xml.dcl
install -m0644 %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
	$RPM_BUILD_ROOT/usr/share/sgml
rm -rf $RPM_BUILD_ROOT/usr/share/xml/*


%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR


%files
%defattr (-,root,root)
%dir /etc/sgml
%config(noreplace) /etc/sgml/sgml.conf
%dir /usr/share/sgml
%dir /usr/share/sgml/sgml-iso-entities-8879.1986
/usr/share/sgml/sgml-iso-entities-8879.1986/*
/usr/share/sgml/xml.dcl
/usr/share/sgml/xml.soc
/usr/share/sgml/html.dcl
/usr/share/sgml/html.soc
/usr/bin/sgmlwhich
/usr/bin/install-catalog
%{_mandir}/*/*
%{_docdir}/*

%files -n xml-common
%defattr (-,root,root)
%dir /etc/xml
%config(noreplace) /etc/xml/catalog
%dir /usr/share/sgml
%dir /usr/share/sgml/docbook
%config(noreplace) /usr/share/sgml/docbook/xmlcatalog
%dir /usr/share/xml

%changelog
* Fri Feb 27 2009 - matt.keenan@sun.com
- Add manpage patch for Attributes and ARC Comment
* Sun Apr  1 2007 - laca@sun.com
- add missing autoconf call
* Wed Mar 21 2007 - laca@sun.com
- add --sysconfdir configure option and use $RPM_BUILD_ROOT instead
  of %buildroot.
* Mon Feb 12 2007 - laca@sun.com
- rename patch to match JDS naming convention
* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.6.3-18
- Build requires automake and autoconf (bug #194709).
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt
* Wed Sep 22 2004 Than Ngo <than@redhat.com> 0.6.3-17
- rebuilt
* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt
* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.6.3-15
- Patch from Ville Skyttä <ville.skytta at iki.fi> (bug #111625):
  - Include /usr/share/xml in xml-common.
  - Own /usr/share/sgml and /usr/share/xml.
* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt
* Wed Oct 23 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-13
- Ship the installed documentation.
- Don't install files not packaged.
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild
* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild
* Wed Apr 24 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-10
- Ship {xml,html}.{dcl,soc} (bug #63500, bug #62980).
- Work around broken tarball packaging.
* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-9
- Rebuild in new environment.
* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-8
- Back to /usr/share/sgml.  Now install docbook-dtds.
- Use a real install-sh, not the symlink shipped in the tarball.
* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.6.3-7
- automated rebuild
* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-6
- Don't create a useless empty catalog.
- Don't try to put install things outside the build root.
- Build requires a libxml2 that actually works.
* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-4
- Use (and handle) catalog files with quotes in install-catalog.
* Thu Nov  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-3
- Create default XML Catalog at build time, not install time.
* Fri Oct  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-2
- Move XML things into /usr/share/xml, and split them out into separate
  xml-common package.
* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-1
- 0.6.3.  Incorporates oldsyntax and quiet patches.
- Make /etc/sgml/sgml.conf noreplace.
- Own /etc/sgml, various other directories (bug #47485, bug #54180).
* Wed May 23 2001 Tim Waugh <twaugh@redhat.com> 0.5-7
- Remove execute bit from data files.
* Mon May 21 2001 Tim Waugh <twaugh@redhat.com> 0.5-6
- install-catalog needs to make sure that it creates world-readable files
  (bug #41552).
* Wed Mar 14 2001 Tim Powers <timp@redhat.com> 0.5-5
- fixed license
* Wed Jan 24 2001 Tim Waugh <twaugh@redhat.com>
- Make install-catalog quieter during normal operation.
* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Require textutils, fileutils, grep (bug #24719).
* Wed Jan 17 2001 Tim Waugh <twaugh@redhat.com>
- Require sh-utils.
* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Fix typo in install-catalog patch.
* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Install by hand (man/en/...).  Use %%{_mandir}.
- Use %%{_tmppath}.
- Make install-catalog fail silently if given the old syntax.
- Add CHANGES file.
- Change Copyright: to License:.
- Remove Packager: line.
* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
