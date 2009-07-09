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
Version:      9.1.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Acrobat Reader for PDF files
URL:          http://www.adobe.com/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  no
PreReq:       firefox



Source:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/enu/AdbeRdr9.1.0-1_i486solaris_enu.tar.bz2
Source1:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/jpn/AdbeRdr9.1.0-1_i486solaris_jpn.tar.bz2
Source2:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/fra/AdbeRdr9.1.0-1_i486solaris_fra.tar.bz2
Source3:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/deu/AdbeRdr9.1.0-1_i486solaris_deu.tar.bz2

Source4:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_chs_i386-solaris.tar.bz2 
Source5:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_cht_i386-solaris.tar.bz2
Source6:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_kor_i386-solaris.tar.bz2
Source7:     http://ardownload.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_jpn_i386-solaris.tar.bz2

Source8:     acroread-combined-langs-x86


%define adobe_base_dir %{_libdir}/AdobeReader
%define adobe_doc_dir %{adobe_base_dir}/doc/acroread
%define plugin_dir %{_libdir}/firefox/plugins
%define plugin_link_target ../../AdobeReader/Adobe/Reader9/Browser/intelsolaris/nppdf.so


%description
Acrobat reader for PDF files


%prep
%setup -q -c -n %{name}-%{version}

mkdir jpn
cd jpn
bunzip2 -c %SOURCE1 | tar xf -
cd ..

mkdir fra
cd fra
bunzip2 -c %SOURCE2 | tar xf -
cd ..

mkdir deu
cd deu
bunzip2 -c %SOURCE3 | tar xf -
cd ..

mkdir chs
cd chs
bunzip2 -c %SOURCE4 | tar xf -
cd ..

mkdir cht
cd cht
bunzip2 -c %SOURCE5 | tar xf -
cd ..

mkdir kor
cd kor
bunzip2 -c %SOURCE6 | tar xf -
cd ..

cd jpn
bunzip2 -c %SOURCE7 | tar xf -
cd ..


%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{adobe_base_dir}

# From the Asian font packs (chs, cht, kor, jpn), extract one of the LANGCOM.TAR
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

cd jpn/JPNKIT
cat LANGJPN.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf - )
cd ../..

# From the x86 Solaris releases (enu/jpn/fra/deu), just extract all the files
# (over-writting any common files as we go).

cd jpn/AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat ISOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ../..

cd fra/AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat ISOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ../..

cd deu/AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat ISOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ../..

cd AdobeReader
cat COMMON.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cat ISOLR.TAR | (cd ${RPM_BUILD_ROOT}%{adobe_base_dir}; tar xvf -)
cd ..

# overwrite distributed script with new ver that supports all langs
install --mode=0755 %SOURCE8 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader9/bin/acroread

cd AdobeReader
install -d ${RPM_BUILD_ROOT}%{adobe_doc_dir}
install --mode=0644 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader9/Reader/Legal/en_US/License.txt \
	${RPM_BUILD_ROOT}%{adobe_doc_dir}
install --mode=0644 ${RPM_BUILD_ROOT}%{adobe_base_dir}/Adobe/Reader9/Reader/help/ENU/ReadMe.htm \
	${RPM_BUILD_ROOT}%{adobe_doc_dir}

# make a link to the executable acroread script from /usr/bin
install -d ${RPM_BUILD_ROOT}%{_bindir}
cd ${RPM_BUILD_ROOT}%{_libdir}/AdobeReader/Adobe/Reader9/bin
cd ${RPM_BUILD_ROOT}%{_prefix}/bin
ln -s ../lib/AdobeReader/Adobe/Reader9/bin/acroread .

# Make a link for acroread.1 manpage file
install -d ${RPM_BUILD_ROOT}%{_mandir}/man1
cd ${RPM_BUILD_ROOT}%{_mandir}/man1
gunzip ../../../lib/AdobeReader/Adobe/Reader9/Resource/Shell/acroread.1.gz
ln -s ../../../lib/AdobeReader/Adobe/Reader9/Resource/Shell/acroread.1 .

# Make a link for .xml file
install -d ${RPM_BUILD_ROOT}%{_datadir}/mime/packages
cd ${RPM_BUILD_ROOT}%{_datadir}/mime/packages
ln -s ../../../lib/AdobeReader/Adobe/Reader9/Resource/Support/AdobeReader.xml acroread.xml

# Make a link for the .desktop file
install -d ${RPM_BUILD_ROOT}%{_datadir}/applications
cd ${RPM_BUILD_ROOT}%{_datadir}/applications
ln -s ../../lib/AdobeReader/Adobe/Reader9/Resource/Support/AdobeReader.desktop acroread.desktop

# Make links for the hicolor theme icons
install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor
cd ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor
for f in `cd  ../../../lib/AdobeReader/Adobe/Reader9/Resource/Icons/; /bin/ls -d *x*`
do 
  for p in `cd  ../../../lib/AdobeReader/Adobe/Reader9/Resource/Icons/$f/; /bin/ls *.png` 
  do
  install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/$f/apps
  ln -s ../../../../../lib/AdobeReader/Adobe/Reader9/Resource/Icons/$f/$p ./$f/apps
  if test "x"$p != "xAdobeReader9.png" ; then
    install -d ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/$f/mimetypes
    ln -s ../../../../../lib/AdobeReader/Adobe/Reader9/Resource/Icons/$f/$p ./$f/mimetypes/application-`echo $p | /bin/awk -F'.' '{print $(NF-1)}'`.png
  fi
  done
done

# Make a link for the Firefox plugin
install --mode=755 -d ${RPM_BUILD_ROOT}%{plugin_dir}
ln -s %{plugin_link_target} ${RPM_BUILD_ROOT}%{plugin_dir}/nppdf.so


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/acroread
%{plugin_dir}/nppdf.so
%{adobe_base_dir}

%changelog
* Wed Apr 08 2009 - elaine.xiong@sun.com
- initial version
