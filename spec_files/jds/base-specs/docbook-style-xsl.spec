#
# spec file for package docbook-style-xsl
#
# copied from fedora core 6
#
# Owner: laca
#
Name: docbook-style-xsl
Version: 1.69.1
Release: 5.1
Group: Applications/Text

Summary: Norman Walsh's XSL stylesheets for DocBook XML.

License: Distributable
URL: http://docbook.sourceforge.net/projects/xsl/

Provides: docbook-xsl = %{version}
PreReq: docbook-dtd-xml
# xml-common was using /usr/share/xml until 0.6.3-8.
PreReq: xml-common >= 0.6.3-8
# PassiveTeX before 1.21 can't handle the newer stylesheets.
Conflicts: passivetex < 1.21

BuildRoot: %{_tmppath}/%{name}-%{version}

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.bz2
Source1: %{name}.Makefile
Source2: http://prdownloads.sourceforge.net/docbook/docbook-xsl-doc-%{version}.tar.bz2

# owner:laca type:bug date:2007-02-15 state:upstream from fedore core
Patch1: docbook-style-xsl-01-pagesetup.diff
# owner:laca type:bug date:2007-02-15 state:upstream from fedore core
Patch2: docbook-style-xsl-02-marginleft.diff
# owner:laca type:bug date:2007-02-15 state:upstream from fedore core
Patch3: docbook-style-xsl-03-lists.diff
# owner:laca type:bug date:2007-02-15 state:upstream from fedore core
Patch4: docbook-style-xsl-04-sp.diff
# owner:fujiwara type:l10n date:2004-11-26 bugster:6199963
Patch5: docbook-style-xsl-05-g11n-i18n-ja.diff

%description
These XSL stylesheets allow you to transform any DocBook XML document to
other formats, such as HTML, FO, and XHMTL.  They are highly customizable.


%prep
%setup -q -n docbook-xsl-%{version}
pushd ..
gtar jxf %{SOURCE2}
popd
%patch1 -p1 -b .pagesetup
%patch2 -p1 -b .marginleft
%patch3 -p1 -b .lists
%patch4 -p1 -b .sp
%patch5 -p1
cp %{SOURCE1} Makefile
for f in $(find -name "*'*")
do
  mv -v "$f" $(echo "$f" | tr -d "'")
done


%build


%install
DESTDIR=$RPM_BUILD_ROOT
make install BINDIR=$DESTDIR/usr/bin DESTDIR=$DESTDIR/usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}
ln -s xsl-stylesheets-%{version}-%{release} \
	$DESTDIR/usr/share/sgml/docbook/xsl-stylesheets

# Don't ship the extensions (bug #177256).
rm -rf $DESTDIR/usr/share/sgml/docbook/xsl-stylesheets/extensions/*


%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR


%files
%defattr (-,root,root)
%doc BUGS
%doc ChangeLog
%doc README
%doc TODO
%doc doc
/usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}
/usr/share/sgml/docbook/xsl-stylesheets


%post
CATALOG=/etc/xml/catalog
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}" $CATALOG


%postun
CATALOG=/etc/xml/catalog
/usr/bin/xmlcatalog --noout --del \
 "file:///usr/share/sgml/docbook/xsl-stylesheets-%{version}-%{release}" $CATALOG


%changelog
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.69.1-5.1
- rebuild

* Tue Jan 24 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-5
- Don't ship docsrc/* (bug #177256).
- Don't ship the extensions (bug #177256).

* Thu Jan 19 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-4
- Better 'lists' patch (bug #161371).

* Thu Jan 19 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-3
- Apply patch to fix simpara manpage output, which asciidoc tends to use
  (bug #175592).

* Tue Jan  3 2006 Tim Waugh <twaugh@redhat.com> 1.69.1-2
- Patches from W. Michael Petullo:
  - Fix lists blocking (bug #161371).
  - Avoid proportional-column-width for passivetex (bug #176766).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug 12 2005 Tim Waugh <twaugh@redhat.com> 1.69.1-1
- 1.69.1.

* Mon Jul 18 2005 Tim Waugh <twaugh@redhat.com> 1.69.0-1
- 1.69.0.

* Mon Feb 14 2005 Tim Waugh <twaugh@redhat.com> 1.68.1-1
- 1.68.1.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1.68.0-1
- 1.68.0.

* Wed Dec  8 2004 Tim Waugh <twaugh@redhat.com> 1.67.2-2
- Prevent expressions in passivetex output from index.xsl (bug #142229).

* Thu Dec  2 2004 Tim Waugh <twaugh@redhat.com> 1.67.2-1
- 1.67.2.
- No longer need nbsp or listblock patches.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 1.67.0-3
- Avoid non-ASCII in generated man pages.

* Wed Nov 10 2004 Tim Waugh <twaugh@redhat.com> 1.67.0-1
- 1.67.0.

* Tue Nov  2 2004 Tim Waugh <twaugh@redhat.com> 1.66.1-1
- 1.66.1 (bug #133586).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 1.65.1-2
- Fix strange filenames (bug #125311).

* Tue Mar  9 2004 Tim Waugh <twaugh@redhat.com> 1.65.1-1
- 1.65.1.

* Mon Mar  1 2004 Tim Waugh <twaugh@redhat.com> 1.65.0-1
- 1.65.0.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-6
- Fix last margin-left fix (bug #113456).
- Reduce instances of itemized/ordered lists having misalignments.

* Sun Jan 18 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-5
- And another (bug #113456).

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-4
- Fixed another instance of bug #113456 in lists layout.

* Wed Jan 14 2004 Tim Waugh <twaugh@redhat.com> 1.64.1-3
- Hard-code the margin-left work around to expect passivetex (bug #113456).

* Wed Dec 24 2003 Tim Waugh <twaugh@redhat.com> 1.64.1-2
- Another manpage fix.

* Fri Dec 19 2003 Tim Waugh <twaugh@redhat.com> 1.64.1-1
- 1.64.1.

* Thu Dec 18 2003 Tim Waugh <twaugh@redhat.com> 1.64.0-2
- Another manpage fix.

* Tue Dec 16 2003 Tim Waugh <twaugh@redhat.com> 1.64.0-1
- 1.64.0.

* Fri Dec 12 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-3
- Use the fr.xml from 1.62.1 (bug #111989).

* Thu Dec 11 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-2
- Manpages fixes.

* Thu Dec 11 2003 Tim Waugh <twaugh@redhat.com> 1.62.4-1
- 1.62.4.
- No longer need hyphens patch.
- Avoid expressions in margin-left attributes, since passivetex does not
  understand them.

* Fri Jul  4 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-2.1
- Rebuilt.

* Fri Jul  4 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-2
- Rebuilt.

* Fri May 23 2003 Tim Waugh <twaugh@redhat.com> 1.61.2-1
- 1.61.2.

* Sun May 18 2003 Tim Waugh <twaugh@redhat.com> 1.61.1-1
- 1.61.1.

* Fri May  9 2003 Tim Waugh <twaugh@redhat.com> 1.61.0-1
- Prevent hyphenation-character confusing passivetex.
- 1.61.0.

* Thu Mar  6 2003 Tim Waugh <twaugh@redhat.com> 1.60.1-1
- 1.60.1.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  2 2002 Tim Waugh <twaugh@redhat.com> 1.58.1-1
- 1.58.1.
- No longer need marker patch.

* Mon Nov  4 2002 Tim Waugh <twaugh@redhat.com> 1.57.0-2
- Ship profiling directory (bug #77191).

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 1.57.0-1
- 1.57.0.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 1.56.1-1
- 1.56.1.
- Use value-of not copy-of for fo:marker content.
- Conflict with passivetex < 1.21.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Tim Waugh <twaugh@redhat.com> 1.50.0-1
- 1.50.0.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.49-1
- 1.49.
- Rebuild in new environment.

* Fri Feb  1 2002 Tim Waugh <twaugh@redhat.com> 1.48-4
- Put URIs instead of pathnames in the XML catalog.

* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 1.48-3
- Back to /usr/share/sgml.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.48-2
- automated rebuild

* Mon Jan  7 2002 Tim Waugh <twaugh@redhat.com> 1.48-1
- 1.48.

* Sat Dec  8 2001 Tim Waugh <twaugh@redhat.com> 1.47-2
- Conflict with PassiveTeX before 1.11.

* Tue Oct 16 2001 Tim Waugh <twaugh@redhat.com> 1.47-1
- 1.47-experimental.

* Tue Oct  9 2001 Tim Waugh <twaugh@redhat.com> 1.45-2
- Fix unversioned symlink.

* Mon Oct  8 2001 Tim Waugh <twaugh@redhat.com> 1.45-1
- XML Catalog entries.
- Move files to /usr/share/xml.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 1.45-0.1
- 1.45.
- Built for Red Hat Linux.

* Tue Jun 26 2001 Chris Runge <crunge@pobox.com>
- 1.40

* Fri Jun 09 2001 Chris Runge <crunge@pobox.com>
- added extensions and additional doc
- bin added to doc; the Perl files are for Win32 Perl and so need some
  conversion first

* Fri Jun 08 2001 Chris Runge <crunge@pobox.com>
- Initial RPM (based on docbook-style-dsssl RPM)
- note: no catalog right now (I don't know how to do it; and not sure why
  it is necessary)
