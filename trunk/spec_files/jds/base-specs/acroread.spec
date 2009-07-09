#
# Copyright (c) 2008 Sun Microsystems Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name:         acroread
License:      Commercial
Group:        Applications/Multimedia
Provides:     acroread
Version:      8.1.3
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Acrobat Reader for PDF files
URL:          http://www.adobe.com/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  no
PreReq:       firefox


Source:       http://ardownload.adobe.com/pub/adobe/reader/unix/8.x/8.1.3/enu/AdobeReader_enu-8.1.3-1.sparc.tar.gz
Source1:      http://ardownload.adobe.com/pub/adobe/reader/unix/8.x/8.1.3/jpn/AdobeReader_jpn-8.1.3-1.sparc.tar.gz
Source2:      http://ardownload.adobe.com/pub/adobe/reader/unix/8.x/8.1.2/misc/FontPack81_chs_sparc-solaris.tar.gz
Source3:      http://ardownload.adobe.com/pub/adobe/reader/unix/8.x/8.1.2/misc/FontPack81_cht_sparc-solaris.tar.gz
Source4:      http://ardownload.adobe.com/pub/adobe/reader/unix/8.x/8.1.2/misc/FontPack81_kor_sparc-solaris.tar.gz
Source6:      acroread-combined-langs
Source7:      acroread-reader_prefs

%define adobe_base_dir %{_libdir}/AdobeReader
%define adobe_doc_dir %{adobe_base_dir}/doc/acroread
%define plugin_dir %{_libdir}/firefox/plugins
%define plugin_link_target ../../AdobeReader/Adobe/Reader8/Browser/sparcsolaris/nppdf.so


%description
Acrobat reader for PDF files


%prep
%setup -q -c -n %{name}-%{version}

mkdir jpn
cd jpn
gunzip -c %SOURCE1 | tar xf -
cd ..

mkdir chs
cd chs
gunzip -c %SOURCE2 | tar xf -
cd ..

mkdir cht
cd cht
gunzip -c %SOURCE3 | tar xf -
cd ..

mkdir kor
cd kor
gunzip -c %SOURCE4 | tar xf -
cd ..


%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{adobe_base_dir}

# From the Asian font packs (chs, cht, kor), extract one of the LANGCOM.TAR
# files (they are all identical) and each of the other LANG*.TAR files.
# This gives us the localized font and cmap files.
# Files in common with the tarballs for the full Janapese and English releases
# get overwritten by later commands.

cd chs/CHSKIT
cat LANGCOM.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf - )
cat LANGCHS.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf - )
cd ../..

cd cht/CHTKIT
cat LANGCHT.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf - )
cd ../..

cd kor/KORKIT
cat LANGKOR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf - )
cd ../..

# From the SPARC Solaris releases (jpn and enu), just extract all the files
# (over-writting any common files as we go).

cd jpn/AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat SSOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ../..

cd AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat SSOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ..

# overwrite distributed script with new ver that supports all langs
install --mode=0755 %SOURCE6 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader8/bin/acroread

cd AdobeReader
install -d ${RPM_BUILD_ROOT}%{adobe_doc_dir}
install --mode=0644 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader8/Reader/Legal/en_US/License.txt \
	${RPM_BUILD_ROOT}%{adobe_doc_dir}
install --mode=0644 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader8/Reader/help/ENU/ReadMe.htm \
	${RPM_BUILD_ROOT}%{adobe_doc_dir}

# make a link to the executable acroread script from /usr/bin
install -d ${RPM_BUILD_ROOT}%{_bindir}
cd ${RPM_BUILD_ROOT}%{_libdir}/AdobeReader/Adobe/Reader8/bin
cd ${RPM_BUILD_ROOT}%{_prefix}/bin
ln -s ../lib/AdobeReader/Adobe/Reader8/bin/acroread .

# Make link in /usr/sfw/bin for backward compatability with prev acroread ver.
install -d ${RPM_BUILD_ROOT}%{_prefix}/sfw/bin
cd ${RPM_BUILD_ROOT}%{_prefix}/sfw/bin
ln -s ../../lib/AdobeReader/Adobe/Reader8/bin/acroread .

# Make a link for the .desktop file
install -d ${RPM_BUILD_ROOT}%{_datadir}/applications
cd ${RPM_BUILD_ROOT}%{_datadir}/applications
ln -s ../../lib/AdobeReader/Adobe/Reader8/Resource/Support/AdobeReader.desktop acroread.desktop

# Make links for the hicolor theme icons
install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor
cd ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor
for f in `cd  ../../../lib/AdobeReader/Adobe/Reader8/Resource/Icons/; /bin/ls -d *x*`
do 
  install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/$f/apps
  ln -s ../../../../../lib/AdobeReader/Adobe/Reader8/Resource/Icons/$f/AdobeReader8.png ./$f/apps
done

# Make a link for the Firefox plugin
install --mode=755 -d ${RPM_BUILD_ROOT}%{plugin_dir}
ln -s %{plugin_link_target} ${RPM_BUILD_ROOT}%{plugin_dir}/nppdf.so

# Overwrite the default global preferences file.
# New file turns off BeyondReader startup screen (which would fail
# anyway as the libgtkembedmoz dir has not been defined)
install --mode=0644 %SOURCE7 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader8/Reader/GlobalPrefs/reader_prefs


# This is Yuk!  This and the %post (and %preun) scripts are needed
# because we cannot handle paths with spaces in SVr4 pkgs
cd ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Help
mv "en_US/Adobe Reader" en_US/Adobe_Reader
mv "ja_JP/Adobe Reader" ja_JP/Adobe_Reader


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/acroread
%{plugin_dir}/nppdf.so
%{adobe_base_dir}

%changelog
* Mon Dec 08 2008 - dermot.mccluskey@sun.com
- Bump to 8.1.3
* Tue Jul 22 2008 - dermot.mccluskey@sun.com
- Bump to 8.1.2_SU1
* Wed Apr 02 2008 - dermot.mccluskey@sun.com
- Bump to 8.1.2
* Fri Jan 18 2008 - dermot.mccluskey@sun.com
- Up-revved to 8.1.1
* Fri Apr 13 2007 - dermot.mccluskey@sun.com
- add a private copy of libz to acroread
* Tue Feb 20 2007 - dermot.mccluskey@sun.com
- Up-revved to 7.0.9 due to Adobe security alert
* Fri Nov 24 2006 - darren.kenny@sun.com
- Create link for the .desktop file and the icon for it.
* Tue Jul 04 2006 - dermot.mccluskey@sun.com
- Up-revved to 7.0.8 and overwrite provided acroread script with version
  that supports the Asian LANGs
* Wed May 10 2006 - dave.lin@sun.com
- change the plugin dir to /usr/lib/firefox/plugins since firefox move
  from /usr/sfw/lib to /usr/lib
* Wed Nov 02 2005 - damien.carbery@sun.com
- Copy in v7 changes from JDS3.1 branch.
* Thu Oct 20 2005 - damien.carbery@sun.com
- Change mozilla references to firefox.
* Mon Oct 10 2005 - damien.carbery@sun.com
- Add symlink in /usr/sfw/bin for backward compatability. Fixes 6300634.
* Thu Aug 25 2005 - dermotm.mccluskey@sun.com
- move to version 7.0.1 - need to re-write prep and install sections
* Mon Dec 20 2004 - dermotm.mccluskey@sun.com
- bump to 5.0.10
  directory structure of tarballs changed slightly
* Fri Nov 26 2004 - laca@sun.com
- Removed jds-integration dependency
* Fri Nov 12 2004 - laca@sun.com
- add jds-integration dependency
* Wed Nov 10 2004 - damien.carbery@sunc.com
- Fix for 5089858 - add Asian font packages.
* Tue Oct 05 2004 - shirley.woo@sun.com
- CR 6174047 : moved acroread to install to /usr/sfw
  Bug 5110289 : changed plugin link to be relative for solaris
* Mon Aug 16 2004 - dermotm.mccluskey@sun.com
- parameterize platform_browser_dir
* Fri Aug 06 2004 - dermotm.mccluskey@sun.com
- initial version
