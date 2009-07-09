#
# spec file for package SUNWmyspell-dictionary-l10n
#
# includes module(s): all modules which include l10n files
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: fujiwara
#
%include Solaris.inc

# http://wiki.services.openoffice.org/wiki/Dictionaries is the front page.
# The URL is changed from
# http://ftp.services.openoffice.org/pub/OpenOffice.org/contrib/dictionaries/foo.zip
# to
# http://dlc.sun.com/osol/jds/downloads/extras/myspell/foo-YYYY-MM-DD.zip
# since RE needs the version number in filenames.
%define dictionary_source http://dlc.sun.com/osol/jds/downloads/extras/myspell
%define _myspelldir %_datadir/spell/myspell
%define _firefoxdir %_libdir/firefox/dictionaries
%define _thunderbirddir %_libdir/thunderbird/dictionaries
%define s_l_dict_extra bg_BG,ca_ES,da_DK,el_GR,en_AU,en_GB,et_EE,he_IL,hr_HR,lt_LT,lv_LV,nb_NO,nl_NL,nn_NO,pt_PT,ro_RO,sk_SK,sl_SI,th_TH,uk_UA

Name:                    SUNWmyspell-dictionary
Summary:                 Myspell and Hunspell spell dictionary files
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version}
Docdir:                  %{_datadir}/doc/myspell-dictionary
%if %build_l10n
## English (United States)
Source:                  %dictionary_source/en_US-2004-06-23.zip
## Afrikaans (South Africa)
#Source1:                 %dictionary_source/af_ZA-2006-01-17.zip
## Catalan (Spain)
Source2:                 %dictionary_source/ca_ES-2002-10-15.zip
## Czech (Czech Republic)
Source3:                 %dictionary_source/cs_CZ-2003-01-01.zip
## Danish (Denmark)
Source4:                 %dictionary_source/da_DK-2007-01-06.zip
## German (Germany)
# original URL is http://j3e.de/hunspell/de_DE.zip
Source5:                 %dictionary_source/de_DE-2003-06-17.zip
## Greek (Greece)
Source6:                 %dictionary_source/el_GR-2004-12-20.zip
## English (Australia)
# original URL is http://www.justlocal.com.au/clients/oooau/
# Not reviewed yet
#Source7:                 http://www.justlocal.com.au/clients/dictionaryfree/en-AU-full-V2.2.2.zip
## English (United Kingdom)
# original URL is http://en-gb.pyxidium.co.uk/dictionary/en_GB.zip
# Not reviewed yet
#Source8:                 %dictionary_source/en_GB-2006-11-30.zip
## English (South Africa)
# Not reviewed yet
#Source9:                 %dictionary_source/en_ZA-2006-01-20.zip
## Spanish (Spain-etal)
Source10:                %dictionary_source/es_ES-2005-05-10.zip
## Esperanto (anywhere)
# Not reviewed yet
#Source11:                %dictionary_source/eo-2004-11-29.zip
## Estonian (Estonia)
# original URL is:
# http://www.meso.ee/~jjpp/speller/et_EE.aff
# http://www.meso.ee/~jjpp/speller/et_EE.dic
# http://www.eki.ee/eki/litsents.html
# Since there is no date on web, create a custom directory.
# Not reviewed yet
#Source12:                %dictionary_source/et_EE-sun-2009-03-20.zip
## Faroese (Faroe Islands)
Source13:                %dictionary_source/fo_FO-2005-03-07.zip
## French (France)
Source14:                %dictionary_source/fr_FR-2006-09-19.zip
## Irish (Ireland)
Source15:                %dictionary_source/ga_IE-2007-10-29.zip
## Scottish Gaelic (Scotland)
Source16:                 %dictionary_source/gd_GB-2005-01-08.zip
## Galician (Spain)
# Not reviewed yet
#Source17:                http://downloads.sourceforge.net/ispell-gl/gl_ES-05.zip
## Hebrew (Israel)
Source18:                %dictionary_source/he_IL-2005-01-12.zip
## Croatian (Croatia)
# Not reviewed yet
#Source19:                %dictionary_source/hr_HR-2006-06-07.zip
## Hungarian (Hungary)
# original URL is http://magyarispell.sourceforge.net/hu_HU.zip
Source20:                %dictionary_source/hu_HU-2006-07-27.zip
## Kurdish (Turkey, Syria)
Source21:                %dictionary_source/ku_TR-2005-01-21.zip
## Lithuanian (Lithuania)
# Not reviewed yet
#Source22:                http://files.akl.lt/ispell-lt/lt_LT-1.2.1.zip
## Latvian (Latvia)
# original URL is ftp://ftp.stardiv.de/pub/OpenOffice.org/contrib/dictionaries/lv_LV.zip
Source23:                %dictionary_source/lv_LV-2008-02-22.zip
## Italian (Italy)
Source24:                http://prdownloads.sf.net/linguistico/italiano_2_3_beta_2006_07_23.zip
## Norwegian Bokmaal (Norway)
Source25:                %dictionary_source/nb_NO-2006-05-08.zip
## Dutch (Netherlands)
Source26:                %dictionary_source/nl_NL-2005-07-20.zip
## Norwegian (Bokmal)
# Not reviewed yet
#Source27:                http://alioth.debian.org/frs/download.php/2357/no_NO-pack2-2.0.10.zip
## Ndebele (South Africa)
Source28:                %dictionary_source/nr_ZA-2006-01-20.zip
## Northern Sotho (South Africa)
Source29:                %dictionary_source/ns_ZA-2006-01-20.zip
## Polish (Poland)
# original URL is http://pl.openoffice.org/pliki/pl_PL.zip
Source30:                %dictionary_source/pl_PL-2006-12-02.zip
## Portuguese (Brazil)
Source31:                http://www.deso-se.com.br/downloads/download.php/pt_BR-2700g.zip
## Romanian (Romania)
# Not reviewed yet
#Source32:                http://downloads.sourceforge.net/rospell/ro_RO.3.2.zip
## Russian (Russia)
Source33:                %dictionary_source/ru_RU-2004-04-06.zip
## Slovak (Slovakia)
Source34:                %dictionary_source/sk_SK-2005-09-11.zip
## Slovenian (Slovenia)
Source35:                %dictionary_source/sl_SI-2007-01-27.zip
## Swazi/Swati (South Africa)
# Not reviewed yet
#Source36:                %dictionary_source/ss_ZA-2006-07-05.zip
## Southern Sotho (South Africa)
Source37:                %dictionary_source/st_ZA-2006-01-20.zip
## Swedish (Sweden)
# original URL is http://hem.bredband.net/dsso1/sv_SE.zip
Source38:                %dictionary_source/sv_SE-2006-12-07.zip
## Kiswahili (East Africa)
Source39:                %dictionary_source/sw_KE-2004-05-16.zip
## Thai (Thailand)
# Not reviewed yet
#Source40:                %dictionary_source/th_TH-2006-12-12.zip
## Setswana (Africa)
# Not reviewed yet
#Source41:                %dictionary_source/tn_ZA-2004-05-16.zip
## Tsonga (South Africa)
#Source42:                %dictionary_source/ts_ZA-2006-01-23.zip
## Ukrainian (Ukraine)
# Not reviewed yet
#Source43:                %dictionary_source/uk_UA-2009-01-25.zip
## Venda (South Africa)
Source44:                %dictionary_source/ve_ZA-2006-07-06.zip
## Xhosa (South Africa)
Source45:                %dictionary_source/xh_ZA-2006-01-23.zip
## Zulu (Africa)
Source46:                %dictionary_source/zu_ZA-2006-01-20.zip

# Source101 - 199 are OOo-spell-*.zip
## Bulgarian (Bulgaria)
Source101:               http://downloads.sourceforge.net/bgoffice/OOo-spell-bg-4.1.zip

# Source201 - 299 are *.oxt
## German (de-CH-frami)
# Not reviewed yet
#Source201:               http://extensions.services.openoffice.org/files/1699/0/dict-de_CH-frami_2008-12-06.oxt

# Source301 - 399 are *.tar.gz
## Armenian (Eastern)
Source301:               http://downloads.sourceforge.net/armspell/myspell-hy-0.10.1.tar.gz
## Portuguese (Portugal)
# Not reviewed yet
#Source302:               http://natura.di.uminho.pt/download/sources/Dictionaries/myspell/myspell.pt-20081113.tar.gz
## Manx Gaelic
Source303:               http://borel.slu.edu/ispell/ispell-gv-1.0.tar.gz

# Source401 - 499 are *.tar.bz2
## Persian (Iran)
# original URL is http://hunspell.sourceforge.net/fa_IR.tar.bz2
Source401:               %dictionary_source/fa_IR-2007-08-16.tar.bz2

# Source501 - 599 are hunspell-*.zip
## Slovak (Slovakia)
Source501:               http://www.sk-spell.sk.cx/file_download/38/hunspell-sk-20080525.zip

%include default-depend.inc
SUNW_Copyright:          %{name}.copyright

BuildRoot:               %{_tmppath}/%{name}-%{version}

#%define GROUP0  %SOURCE0   %SOURCE2   %SOURCE3   %SOURCE4   %SOURCE5   %SOURCE6   %SOURCE7   %SOURCE8   %SOURCE9
%define GROUP0  %SOURCE0   %SOURCE2   %SOURCE3   %SOURCE4   %SOURCE5   %SOURCE6
#%define GROUP1  %SOURCE10  %SOURCE11  %SOURCE12  %SOURCE13  %SOURCE14  %SOURCE15  %SOURCE16  %SOURCE17  %SOURCE18  %SOURCE19
%define GROUP1  %SOURCE10  %SOURCE13  %SOURCE14  %SOURCE15  %SOURCE16  %SOURCE18
#%define GROUP2  %SOURCE20  %SOURCE21  %SOURCE22  %SOURCE23  %SOURCE24  %SOURCE25  %SOURCE26  %SOURCE27  %SOURCE28  %SOURCE29
%define GROUP2  %SOURCE20  %SOURCE21  %SOURCE23  %SOURCE24  %SOURCE25  %SOURCE26  %SOURCE28  %SOURCE29
#%define GROUP3  %SOURCE30  %SOURCE31  %SOURCE32  %SOURCE33  %SOURCE34  %SOURCE35  %SOURCE36  %SOURCE37  %SOURCE38  %SOURCE39
%define GROUP3  %SOURCE30  %SOURCE31  %SOURCE33  %SOURCE34  %SOURCE35  %SOURCE37  %SOURCE38  %SOURCE39
#%define GROUP4  %SOURCE40  %SOURCE41  %SOURCE43  %SOURCE44  %SOURCE45  %SOURCE46
%define GROUP4  %SOURCE44  %SOURCE45  %SOURCE46
%define GROUP101 %SOURCE101
#%define GROUP201 %SOURCE201
%define GROUP201 ""
#%define GROUP301 %SOURCE301 %SOURCE302 %SOURCE303
%define GROUP301 %SOURCE301 %SOURCE303
%define GROUP401 %SOURCE401
%define GROUP501 %SOURCE501
%define GROUP_NONE_OO2 %GROUP101 %GROUP201 %GROUP301 %GROUP401 %GROUP501
%define ALL_SOURCES %GROUP0 %GROUP1 %GROUP2 %GROUP3 %GROUP4 %GROUP_NONE_OO2


%package -n              SUNWmyspell-dictionary-en
Summary:                 %{summary} for English
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version}
%include default-depend.inc
SUNW_Copyright:          %{name}-en.copyright

%package -n              SUNWmyspell-dictionary-cs
Summary:                 %{summary} for Czech
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10ncs
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                cs_CZ
%include default-depend.inc
SUNW_Copyright:          %{name}-cs.copyright

%package -n              SUNWmyspell-dictionary-de
Summary:                 %{summary} for German
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nde
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                de
%include default-depend.inc
SUNW_Copyright:          %{name}-de.copyright

%package -n              SUNWmyspell-dictionary-es
Summary:                 %{summary} for Spanish
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nes
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                es
%include default-depend.inc
SUNW_Copyright:          %{name}-es.copyright

%package -n              SUNWmyspell-dictionary-fr
Summary:                 %{summary} for French
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nfr
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                fr
%include default-depend.inc
SUNW_Copyright:          %{name}-fr.copyright

%package -n              SUNWmyspell-dictionary-hu
Summary:                 %{summary} for Hungarian
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nhu
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                hu_HU
%include default-depend.inc
SUNW_Copyright:          %{name}-hu.copyright

%package -n              SUNWmyspell-dictionary-it
Summary:                 %{summary} for Italian
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nit
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                it
%include default-depend.inc
SUNW_Copyright:          %{name}-it.copyright

%package -n              SUNWmyspell-dictionary-pl
Summary:                 %{summary} for Polish
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10npl
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                pl_PL
%include default-depend.inc
SUNW_Copyright:          %{name}-pl.copyright

%package -n              SUNWmyspell-dictionary-ptBR
Summary:                 %{summary} for Portugese Brazilian
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nptbr
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                pt_BR
%include default-depend.inc
SUNW_Copyright:          %{name}-ptBR.copyright

%package -n              SUNWmyspell-dictionary-ru
Summary:                 %{summary} for Russian
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nru
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                ru_RU
%include default-depend.inc
SUNW_Copyright:          %{name}-ru.copyright

%package -n              SUNWmyspell-dictionary-sv
Summary:                 %{summary} for Swedish
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version},l10nsv
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                sv
%include default-depend.inc
SUNW_Copyright:          %{name}-sv.copyright

%package -n              SUNWmyspell-dictionary-extra
Summary:                 %{summary} for extra languages
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version}
SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
SUNW_Loc:                %s_l_dict_extra
%include default-depend.inc
SUNW_Copyright:          %{name}-extra.copyright

%package -n              SUNWmyspell-dictionary-noinst
Summary:                 %{summary} for extra languages (not in /usr/lib/locale)
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           GNOME2,application,%{jds_version}
# Comment out because SUNW_PkgList needs SUNW_Loc.
#SUNW_PkgList:            SUNWfirefox,SUNWgnome-spell,SUNWthunderbird
#SUNW_Loc:                
%include default-depend.inc
SUNW_Copyright:          %{name}-noinst.copyright


%prep
rm -rf myspell-dictionary-%version
mkdir myspell-dictionary-%version
cd myspell-dictionary-%version
for SOURCE in %ALL_SOURCES
do
  DIR=`basename $SOURCE .zip`

  case $DIR in
  *.tar.gz)
    gzcat $SOURCE | tar xf -
    ;;
  *.tar.bz2)
    bzcat $SOURCE | tar xf -
    DIR=`basename $SOURCE .tar.bz2`
    if [ -d fa ] ; then
      mv fa $DIR
    fi
    ;;
  *.oxt)
    DIR=`basename $DIR .oxt | sed -e "s|dict-||"`
    mkdir $DIR
    cd $DIR
    unzip $SOURCE
    cd ..
    ;;
  OOo-spell-*)
    unzip $SOURCE
    ;;
  gl_ES-??)
    unzip $SOURCE
    mv gl_ES $DIR
    ;;
  hunspell-*)
    unzip $SOURCE
    ;;
  lt_LT-*.*.*)
    unzip $SOURCE
    ;;
  no_NO-pack*)
    mkdir $DIR
    cd $DIR
    unzip $SOURCE
    cd ..
    for FILE in `/bin/ls $DIR/*.zip | grep -v "/th_" | grep -v "/hyph_"`
    do
      SUBDIR=`basename $FILE .zip`
      mkdir $SUBDIR
      cd $SUBDIR
      unzip ../$FILE
      cd ..
    done
    /bin/rm -r $DIR
    ;;
  *)
    mkdir $DIR
    cd $DIR
    unzip $SOURCE
    cd ..
    ;;
  esac
done

# Generating Copyright template...
# SUNWmyspell-dictionary-$ling.copyright can be generated below.
#for ling in cs de en es extra fr hu it pl ru sv
#do
#  cat copyright/SUNWmyspell-dictionary.copyright \
#    > copyright/SUNWmyspell-dictionary-$ling.copyright
#  cat /packages/BUILD/myspell-dictionary-*/copyright-$ling \
#    >> copyright/SUNWmyspell-dictionary-$ling.copyright
# done
for file in `find . -name "README*" -o -name "COPYING" -o -name "Copyright" | sort`
do
  dir=`echo $file | sed -e "s|^\./||" | sed -e "s|/.*||" | sed -e "s|myspell-||" |\
       sed -e "s|OOo-spell-||" | sed -e "s|ispell-||" | sed -e "s|hunspell-||" |\
       sed -e "s|myspell\.||" | sed -e "s|-.*||" | sed -e "s|\..*||"`

  copyright=copyright
  case $dir in
  en_US*) copyright=copyright-en;;
  cs*) copyright=copyright-cs;;
  de*) copyright=copyright-de;;
  es*) copyright=copyright-es;;
  fr*) copyright=copyright-fr;;
  hu*) copyright=copyright-hu;;
  it*) copyright=copyright-it;;
  pl*) copyright=copyright-pl;;
  pt_BR*) copyright=copyright-ptBR;;
  ru*) copyright=copyright-ru;;
  sv*) copyright=copyright-sv;;
  *) 
    copyright=copyright-extra
    IS_EXTRA=`echo "%s_l_dict_extra" | grep "$dir"; echo "" > /dev/null`
    if [ x"$IS_EXTRA" = x ] ; then
      copyright=copyright-noinst
    fi
    ;;
  esac

  echo "$dir Copyright" >> $copyright
  echo "" >> $copyright
  cat $file | sed -e 's/^/  /' >> $copyright
  echo "" >> $copyright
  echo "--------------------------------------------------------------------" \
    >> $copyright
  echo "" >> $copyright
done

%build

%install
if [ -d "$RPM_BUILD_ROOT" ] ; then
  rm -r $RPM_BUILD_ROOT
fi
mkdir -p $RPM_BUILD_ROOT/usr

cd myspell-dictionary-%version
for DICT in `/bin/ls */*.aff */*.dic */*_frami/*_frami.aff */*_frami/*_frami.dic`
do
  if [ ! -d $RPM_BUILD_ROOT%_myspelldir ] ; then
    install -d $RPM_BUILD_ROOT%_myspelldir
  fi
  GNOME_FILE=`basename $DICT | sed -e "s|_frami\.|.|" | sed -e "s|gv\.|gv_IE.|"`
  install --mode=0644 $DICT $RPM_BUILD_ROOT%_myspelldir/$GNOME_FILE
  ( \
    BROWSER_FILE=`echo $GNOME_FILE | sed -e 's/_/-/'`; \
    \
    if [ ! -d $RPM_BUILD_ROOT%_thunderbirddir ] ; then \
      install -d $RPM_BUILD_ROOT%_thunderbirddir; \
    fi; \
    cd $RPM_BUILD_ROOT%_thunderbirddir; \
    ln -s ../../../..%_myspelldir/$GNOME_FILE $BROWSER_FILE; \
    \
    if [ ! -d $RPM_BUILD_ROOT%_firefoxdir ] ; then \
      install -d $RPM_BUILD_ROOT%_firefoxdir; \
    fi; \
    cd $RPM_BUILD_ROOT%_firefoxdir; \
    ln -s ../../../..%_myspelldir/$GNOME_FILE $BROWSER_FILE; \
  )
done

for SOURCE in %ALL_SOURCES
do
  SOURCE_DIR=`basename $SOURCE .zip`
  SOURCE_DIR=`basename $SOURCE_DIR .tar.bz2`
  SOURCE_DIR=`basename $SOURCE_DIR .tar.gz`
  SOURCE_DIR=`basename "$SOURCE_DIR" .oxt | sed -e "s/^dict-//" |\
  sed -e "s/no_NO-pack2*/nb_NO/"`
  DEST_DIR=`echo $SOURCE_DIR | sed -e 's/\([^0-9]*\)[-_][0-9-]*/\1/' |\
            sed -e "s/-frami//" | sed -e "s/ispell-//" | sed -e "s/hunspell-//" |\
            sed -e 's/myspell[.-]//' |\
            sed -e 's/\([^.0-9]*\)[.0-9-]*/\1/' | sed -e "s/-sun//"`
  case $DEST_DIR in
  OOo-spell-bg*)    DEST_DIR=bg_BG;;
  en-AU*)           DEST_DIR=en_AU;;
  eo*)              DEST_DIR=eo_l3;;
  gv*)              DEST_DIR=gv_IE;;
  hy*)              DEST_DIR=hy_AM;;
  italiano*)        DEST_DIR=it_IT;;
  pt)               DEST_DIR=pt_PT;;
  pt_BR*)           DEST_DIR=pt_BR;;
  ro*)              DEST_DIR=ro_RO;;
  sk)               DEST_DIR=sk_SK;;
  *) ;;
  esac

  for FILE in `find $SOURCE_DIR ! -name "*.aff" ! -name "*.dic" -type f`
  do
    install -d $RPM_BUILD_ROOT%{_docdir}/myspell-dictionary/$DEST_DIR
    install --mode=0644 $FILE $RPM_BUILD_ROOT%{_docdir}/myspell-dictionary/$DEST_DIR
  done
done

#rm -f $RPM_BUILD_ROOT/%_myspelldir/en_US.aff
#rm -f $RPM_BUILD_ROOT/%_firefoxdir/en-US.aff
#rm -f $RPM_BUILD_ROOT/%_thunderbirddir/en-US.aff

%clean
rm -rf $RPM_BUILD_ROOT

# The *-en package includes en_US only due to the size of LiveCD.
# en_AU,en_GB are moved to *-extra. en_ZA is moved to *-noinst
%files -n SUNWmyspell-dictionary-en
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/en_US.aff
%{_myspelldir}/en_US.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/en-US.aff
%{_thunderbirddir}/en-US.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/en-US.aff
%{_firefoxdir}/en-US.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/en_US
%{_docdir}/myspell-dictionary/en_US/*


%files -n SUNWmyspell-dictionary-cs
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/cs_*.aff
%{_myspelldir}/cs_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/cs-*.aff
%{_thunderbirddir}/cs-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/cs-*.aff
%{_firefoxdir}/cs-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/cs_CZ
%{_docdir}/myspell-dictionary/cs_CZ/*


%files -n SUNWmyspell-dictionary-de
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/de_*.aff
%{_myspelldir}/de_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/de-*.aff
%{_thunderbirddir}/de-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/de-*.aff
%{_firefoxdir}/de-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/de_CH
#%{_docdir}/myspell-dictionary/de_CH/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/de_DE
%{_docdir}/myspell-dictionary/de_DE/*

%files -n SUNWmyspell-dictionary-es
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/es_*.aff
%{_myspelldir}/es_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/es-*.aff
%{_thunderbirddir}/es-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/es-*.aff
%{_firefoxdir}/es-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/es_ES
%{_docdir}/myspell-dictionary/es_ES/*

%files -n SUNWmyspell-dictionary-fr
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/fr_*.aff
%{_myspelldir}/fr_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/fr-*.aff
%{_thunderbirddir}/fr-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/fr-*.aff
%{_firefoxdir}/fr-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/fr_FR
%{_docdir}/myspell-dictionary/fr_FR/*

%files -n SUNWmyspell-dictionary-hu
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/hu_*.aff
%{_myspelldir}/hu_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/hu-*.aff
%{_thunderbirddir}/hu-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/hu-*.aff
%{_firefoxdir}/hu-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/hu_HU
%{_docdir}/myspell-dictionary/hu_HU/*

%files -n SUNWmyspell-dictionary-it
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/it_*.aff
%{_myspelldir}/it_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/it-*.aff
%{_thunderbirddir}/it-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/it-*.aff
%{_firefoxdir}/it-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/it_IT
%{_docdir}/myspell-dictionary/it_IT/*

%files -n SUNWmyspell-dictionary-pl
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/pl_*.aff
%{_myspelldir}/pl_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/pl-*.aff
%{_thunderbirddir}/pl-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/pl-*.aff
%{_firefoxdir}/pl-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/pl_PL
%{_docdir}/myspell-dictionary/pl_PL/*

%files -n SUNWmyspell-dictionary-ptBR
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/pt_BR.aff
%{_myspelldir}/pt_BR.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/pt-BR.aff
%{_thunderbirddir}/pt-BR.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/pt-BR.aff
%{_firefoxdir}/pt-BR.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/pt_BR
%{_docdir}/myspell-dictionary/pt_BR/*

%files -n SUNWmyspell-dictionary-ru
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/ru_*.aff
%{_myspelldir}/ru_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/ru-*.aff
%{_thunderbirddir}/ru-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/ru-*.aff
%{_firefoxdir}/ru-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ru_RU
%{_docdir}/myspell-dictionary/ru_RU/*

%files -n SUNWmyspell-dictionary-sv
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/sv_*.aff
%{_myspelldir}/sv_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/sv-*.aff
%{_thunderbirddir}/sv-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/sv-*.aff
%{_firefoxdir}/sv-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/sv_SE
%{_docdir}/myspell-dictionary/sv_SE/*

%files -n SUNWmyspell-dictionary-extra
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/bg_*.aff
%{_myspelldir}/bg_*.dic
%{_myspelldir}/ca_*.aff
%{_myspelldir}/ca_*.dic
%{_myspelldir}/da_*.aff
%{_myspelldir}/da_*.dic
%{_myspelldir}/el_*.aff
%{_myspelldir}/el_*.dic
#%{_myspelldir}/en_AU.aff
#%{_myspelldir}/en_AU.dic
#%{_myspelldir}/en_GB.aff
#%{_myspelldir}/en_GB.dic
#%{_myspelldir}/et_*.aff
#%{_myspelldir}/et_*.dic
%{_myspelldir}/he_*.aff
%{_myspelldir}/he_*.dic
#%{_myspelldir}/hr_*.aff
#%{_myspelldir}/hr_*.dic
#%{_myspelldir}/lt_*.aff
#%{_myspelldir}/lt_*.dic
%{_myspelldir}/lv_*.aff
%{_myspelldir}/lv_*.dic
%{_myspelldir}/nb_*.aff
%{_myspelldir}/nb_*.dic
%{_myspelldir}/nl_*.aff
%{_myspelldir}/nl_*.dic
#%{_myspelldir}/nn_*.aff
#%{_myspelldir}/nn_*.dic
#%{_myspelldir}/pt_PT.aff
#%{_myspelldir}/pt_PT.dic
#%{_myspelldir}/ro_*.aff
#%{_myspelldir}/ro_*.dic
%{_myspelldir}/sk_*.aff
%{_myspelldir}/sk_*.dic
%{_myspelldir}/sl_*.aff
%{_myspelldir}/sl_*.dic
#%{_myspelldir}/th_*.aff
#%{_myspelldir}/th_*.dic
#%{_myspelldir}/uk_*.aff
#%{_myspelldir}/uk_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/bg-*.aff
%{_thunderbirddir}/bg-*.dic
%{_thunderbirddir}/ca-*.aff
%{_thunderbirddir}/ca-*.dic
%{_thunderbirddir}/da-*.aff
%{_thunderbirddir}/da-*.dic
%{_thunderbirddir}/el-*.aff
%{_thunderbirddir}/el-*.dic
#%{_thunderbirddir}/en-AU.aff
#%{_thunderbirddir}/en-AU.dic
#%{_thunderbirddir}/en-GB.aff
#%{_thunderbirddir}/en-GB.dic
#%{_thunderbirddir}/et-*.aff
#%{_thunderbirddir}/et-*.dic
%{_thunderbirddir}/he-*.aff
%{_thunderbirddir}/he-*.dic
#%{_thunderbirddir}/hr-*.aff
#%{_thunderbirddir}/hr-*.dic
#%{_thunderbirddir}/lt-*.aff
#%{_thunderbirddir}/lt-*.dic
%{_thunderbirddir}/lv-*.aff
%{_thunderbirddir}/lv-*.dic
%{_thunderbirddir}/nb-*.aff
%{_thunderbirddir}/nb-*.dic
%{_thunderbirddir}/nl-*.aff
%{_thunderbirddir}/nl-*.dic
#%{_thunderbirddir}/nn-*.aff
#%{_thunderbirddir}/nn-*.dic
#%{_thunderbirddir}/pt-PT.aff
#%{_thunderbirddir}/pt-PT.dic
#%{_thunderbirddir}/ro-*.aff
#%{_thunderbirddir}/ro-*.dic
%{_thunderbirddir}/sk-*.aff
%{_thunderbirddir}/sk-*.dic
%{_thunderbirddir}/sl-*.aff
%{_thunderbirddir}/sl-*.dic
#%{_thunderbirddir}/th-*.aff
#%{_thunderbirddir}/th-*.dic
#%{_thunderbirddir}/uk-*.aff
#%{_thunderbirddir}/uk-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/bg-*.aff
%{_firefoxdir}/bg-*.dic
%{_firefoxdir}/ca-*.aff
%{_firefoxdir}/ca-*.dic
%{_firefoxdir}/da-*.aff
%{_firefoxdir}/da-*.dic
%{_firefoxdir}/el-*.aff
%{_firefoxdir}/el-*.dic
#%{_firefoxdir}/en-AU.aff
#%{_firefoxdir}/en-AU.dic
#%{_firefoxdir}/en-GB.aff
#%{_firefoxdir}/en-GB.dic
#%{_firefoxdir}/et-*.aff
#%{_firefoxdir}/et-*.dic
%{_firefoxdir}/he-*.aff
%{_firefoxdir}/he-*.dic
#%{_firefoxdir}/hr-*.aff
#%{_firefoxdir}/hr-*.dic
#%{_firefoxdir}/lt-*.aff
#%{_firefoxdir}/lt-*.dic
%{_firefoxdir}/lv-*.aff
%{_firefoxdir}/lv-*.dic
%{_firefoxdir}/nb-*.aff
%{_firefoxdir}/nb-*.dic
%{_firefoxdir}/nl-*.aff
%{_firefoxdir}/nl-*.dic
#%{_firefoxdir}/nn-*.aff
#%{_firefoxdir}/nn-*.dic
#%{_firefoxdir}/pt-PT.aff
#%{_firefoxdir}/pt-PT.dic
#%{_firefoxdir}/ro-*.aff
#%{_firefoxdir}/ro-*.dic
%{_firefoxdir}/sk-*.aff
%{_firefoxdir}/sk-*.dic
%{_firefoxdir}/sl-*.aff
%{_firefoxdir}/sl-*.dic
#%{_firefoxdir}/th-*.aff
#%{_firefoxdir}/th-*.dic
#%{_firefoxdir}/uk-*.aff
#%{_firefoxdir}/uk-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/bg_BG
%{_docdir}/myspell-dictionary/bg_BG/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ca_ES
%{_docdir}/myspell-dictionary/ca_ES/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/da_DK
%{_docdir}/myspell-dictionary/da_DK/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/el_GR
%{_docdir}/myspell-dictionary/el_GR/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/en_AU
#%{_docdir}/myspell-dictionary/en_AU/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/en_GB
#%{_docdir}/myspell-dictionary/en_GB/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/et_EE
#%{_docdir}/myspell-dictionary/et_EE/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/he_IL
%{_docdir}/myspell-dictionary/he_IL/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/hr_HR
#%{_docdir}/myspell-dictionary/hr_HR/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/lt_LT
#%{_docdir}/myspell-dictionary/lt_LT/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/lv_LV
%{_docdir}/myspell-dictionary/lv_LV/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/nb_NO
%{_docdir}/myspell-dictionary/nb_NO/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/nl_NL
%{_docdir}/myspell-dictionary/nl_NL/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/pt_PT
#%{_docdir}/myspell-dictionary/pt_PT/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ro_RO
#%{_docdir}/myspell-dictionary/ro_RO/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/sk_SK
%{_docdir}/myspell-dictionary/sk_SK/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/sl_SI
%{_docdir}/myspell-dictionary/sl_SI/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/th_TH
#%{_docdir}/myspell-dictionary/th_TH/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/uk_UA
#%{_docdir}/myspell-dictionary/uk_UA/*

%files -n SUNWmyspell-dictionary-noinst
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spell
%dir %attr (0755, root, bin) %{_myspelldir}
%{_myspelldir}/af_*.aff
%{_myspelldir}/af_*.dic
#%{_myspelldir}/en_ZA.aff
#%{_myspelldir}/en_ZA.dic
#%{_myspelldir}/eo_*.aff
#%{_myspelldir}/eo_*.dic
%{_myspelldir}/fa_*.aff
%{_myspelldir}/fa_*.dic
%{_myspelldir}/fo_*.aff
%{_myspelldir}/fo_*.dic
%{_myspelldir}/ga_*.aff
%{_myspelldir}/ga_*.dic
%{_myspelldir}/gd_*.aff
%{_myspelldir}/gd_*.dic
#%{_myspelldir}/gl_*.aff
#%{_myspelldir}/gl_*.dic
%{_myspelldir}/gv_*.aff
%{_myspelldir}/gv_*.dic
%{_myspelldir}/hy_*.aff
%{_myspelldir}/hy_*.dic
%{_myspelldir}/ku_*.aff
%{_myspelldir}/ku_*.dic
%{_myspelldir}/nr_*.aff
%{_myspelldir}/nr_*.dic
%{_myspelldir}/ns_*.aff
%{_myspelldir}/ns_*.dic
#%{_myspelldir}/ss_*.aff
#%{_myspelldir}/ss_*.dic
%{_myspelldir}/st_*.aff
%{_myspelldir}/st_*.dic
%{_myspelldir}/sw_*.aff
%{_myspelldir}/sw_*.dic
#%{_myspelldir}/tn_*.aff
#%{_myspelldir}/tn_*.dic
%{_myspelldir}/ts_*.aff
%{_myspelldir}/ts_*.dic
%{_myspelldir}/ve_*.aff
%{_myspelldir}/ve_*.dic
%{_myspelldir}/xh_*.aff
%{_myspelldir}/xh_*.dic
%{_myspelldir}/zu_*.aff
%{_myspelldir}/zu_*.dic
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/thunderbird
%dir %attr (0755, root, bin) %{_thunderbirddir}
%{_thunderbirddir}/af-*.aff
%{_thunderbirddir}/af-*.dic
#%{_thunderbirddir}/en-ZA.aff
#%{_thunderbirddir}/en-ZA.dic
#%{_thunderbirddir}/eo-*.aff
#%{_thunderbirddir}/eo-*.dic
%{_thunderbirddir}/fa-*.aff
%{_thunderbirddir}/fa-*.dic
%{_thunderbirddir}/fo-*.aff
%{_thunderbirddir}/fo-*.dic
%{_thunderbirddir}/ga-*.aff
%{_thunderbirddir}/ga-*.dic
%{_thunderbirddir}/gd-*.aff
%{_thunderbirddir}/gd-*.dic
#%{_thunderbirddir}/gl-*.aff
#%{_thunderbirddir}/gl-*.dic
%{_thunderbirddir}/gv-*.aff
%{_thunderbirddir}/gv-*.dic
%{_thunderbirddir}/hy-*.aff
%{_thunderbirddir}/hy-*.dic
%{_thunderbirddir}/ku-*.aff
%{_thunderbirddir}/ku-*.dic
%{_thunderbirddir}/nr-*.aff
%{_thunderbirddir}/nr-*.dic
%{_thunderbirddir}/ns-*.aff
%{_thunderbirddir}/ns-*.dic
#%{_thunderbirddir}/ss-*.aff
#%{_thunderbirddir}/ss-*.dic
%{_thunderbirddir}/st-*.aff
%{_thunderbirddir}/st-*.dic
%{_thunderbirddir}/sw-*.aff
%{_thunderbirddir}/sw-*.dic
#%{_thunderbirddir}/tn-*.aff
#%{_thunderbirddir}/tn-*.dic
%{_thunderbirddir}/ts-*.aff
%{_thunderbirddir}/ts-*.dic
%{_thunderbirddir}/ve-*.aff
%{_thunderbirddir}/ve-*.dic
%{_thunderbirddir}/xh-*.aff
%{_thunderbirddir}/xh-*.dic
%{_thunderbirddir}/zu-*.aff
%{_thunderbirddir}/zu-*.dic
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_firefoxdir}
%{_firefoxdir}/af-*.aff
%{_firefoxdir}/af-*.dic
#%{_firefoxdir}/en-ZA.aff
#%{_firefoxdir}/en-ZA.dic
#%{_firefoxdir}/eo-*.aff
#%{_firefoxdir}/eo-*.dic
%{_firefoxdir}/fa-*.aff
%{_firefoxdir}/fa-*.dic
%{_firefoxdir}/fo-*.aff
%{_firefoxdir}/fo-*.dic
%{_firefoxdir}/ga-*.aff
%{_firefoxdir}/ga-*.dic
%{_firefoxdir}/gd-*.aff
%{_firefoxdir}/gd-*.dic
#%{_firefoxdir}/gl-*.aff
#%{_firefoxdir}/gl-*.dic
%{_firefoxdir}/gv-*.aff
%{_firefoxdir}/gv-*.dic
%{_firefoxdir}/hy-*.aff
%{_firefoxdir}/hy-*.dic
%{_firefoxdir}/ku-*.aff
%{_firefoxdir}/ku-*.dic
%{_firefoxdir}/nr-*.aff
%{_firefoxdir}/nr-*.dic
%{_firefoxdir}/ns-*.aff
%{_firefoxdir}/ns-*.dic
#%{_firefoxdir}/ss-*.aff
#%{_firefoxdir}/ss-*.dic
%{_firefoxdir}/st-*.aff
%{_firefoxdir}/st-*.dic
%{_firefoxdir}/sw-*.aff
%{_firefoxdir}/sw-*.dic
#%{_firefoxdir}/tn-*.aff
#%{_firefoxdir}/tn-*.dic
%{_firefoxdir}/ts-*.aff
%{_firefoxdir}/ts-*.dic
%{_firefoxdir}/ve-*.aff
%{_firefoxdir}/ve-*.dic
%{_firefoxdir}/xh-*.aff
%{_firefoxdir}/xh-*.dic
%{_firefoxdir}/zu-*.aff
%{_firefoxdir}/zu-*.dic
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/af_ZA
%{_docdir}/myspell-dictionary/af_ZA/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/en_ZA
#%{_docdir}/myspell-dictionary/en_ZA/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/eo_l3
#%{_docdir}/myspell-dictionary/eo_l3/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/fa_IR
%{_docdir}/myspell-dictionary/fa_IR/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/fo_FO
%{_docdir}/myspell-dictionary/fo_FO/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ga_IE
%{_docdir}/myspell-dictionary/ga_IE/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/gd_GB
%{_docdir}/myspell-dictionary/gd_GB/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/gl_ES
#%{_docdir}/myspell-dictionary/gl_ES/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/gv_IE
%{_docdir}/myspell-dictionary/gv_IE/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/hy_AM
%{_docdir}/myspell-dictionary/hy_AM/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ku_TR
%{_docdir}/myspell-dictionary/ku_TR/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/nr_ZA
%{_docdir}/myspell-dictionary/nr_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ns_ZA
%{_docdir}/myspell-dictionary/ns_ZA/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ss_ZA
#%{_docdir}/myspell-dictionary/ss_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/st_ZA
%{_docdir}/myspell-dictionary/st_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/sw_KE
%{_docdir}/myspell-dictionary/sw_KE/*
#%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/tn_ZA
#%{_docdir}/myspell-dictionary/tn_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ts_ZA
%{_docdir}/myspell-dictionary/ts_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/ve_ZA
%{_docdir}/myspell-dictionary/ve_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/xh_ZA
%{_docdir}/myspell-dictionary/xh_ZA/*
%dir %attr (0755, root, bin) %{_docdir}/myspell-dictionary/zu_ZA
%{_docdir}/myspell-dictionary/zu_ZA/*

%endif

%changelog
* Mon Mar 23 2009 - takao.fujiwara@sun.com
- Add af, bg, fa, fo, ga, gd, gv, hy, ku, lv, nr, ns, ss, st, sw, ts, ve, xh,
  zu myspell dictionaries. CR 6820626.

* Fri Apr 04 2008 - takao.fujiwara@sun.com
- Add a copyright merging.

* Fri Jun 08 2007 - takao.fujiwara@sun.com
- Add symbolic links for firefox l10n dictionaries. Fixes 6566162.

* Fri May 18 2007 - damien.carbery@sun.com
- Remove SUNW_PkgList from base package so that it can be integrated to WOS.

* Thu May 17 2007 - damien.carbery@sun.com
- Correct invalid locale in -extra package: s/nb_NO.UTF-8/nb_NO/.

* Wed May 09 2007 - takao.fujiwara@sun.com
- Removed SUNW_LOC=C at the moment.

* Thu May 03 2007 - takao.fujiwara@sun.com
- Fix typo.
- Modify the correct URL.

* Thu May 03 2007 - damien.carbery@sun.com
- Change all the source file names to be static, removing the _with_download
  modifier.

* Thu May 03 2007 - damien.carbery@sun.com
- Modify dictionary_source url to append 'myspell' as the files have been moved
  to a subdir on the download centre server.

* Tue May 01 2007 - takao.fujiwara@sun.com
- Revised the implementation - no log.

* Tue May 01 2007 - yuriy.kuznetsov@sun.com
- Initial implementation

