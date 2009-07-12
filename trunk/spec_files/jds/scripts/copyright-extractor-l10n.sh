#!/bin/sh

PROGNAME=`basename $0`
PROG_VERSION=0.1
CREATE_COPYRIGHT=0
TYPE_GNOME=1
TYPE_TJDS=2
TYPE_DESKTOP_OTHER=3
TYPE=$TYPE_GNOME
AVAILABLE_TYPES="gnome tjds desktop-other"
MERGE_BASE_COPYRIGHT=0
LANG=C

export LANG

init ()
{
  while [ $# -gt 0 ]
  do
    case "$1" in
    -c|--create)
      CREATE_COPYRIGHT=1;;
    -h|--help)
      usage
      exit 0;;
    -m|--merge)
      MERGE_BASE_COPYRIGHT=1;;
    -t|--type)
      shift
      case "$1" in
      desktop-other)
        TYPE=$TYPE_DESKTOP_OTHER;;
      gnome|GNOME)
        TYPE=$TYPE_GNOME;;
      tjds|TJDS)
        TYPE=$TYPE_TJDS;;
      *)
        echo "Unknown type $1" 1>&2
        echo "Please use the either type $AVAILABLE_TYPES" 1>&2
        exit 1;;
      esac
      ;;
    *)
      echo "$PROGNAME: processing error: $1" 1>&2
      exit 1;;
    esac
    shift
  done
}

usage ()
{
  printf "This script makes L10N copyright files from "
  printf "/usr/share/locale/LANG/LC_MESSAGES/COPYING.foo .\n"
  printf "\n"
  printf "usage: $PROGNAME Version $PROG_VERSION -c|-m [OPTIONS...]\n"
  printf "  -c, --create                      Create l10n copyright files.\n"
  printf "  -m, --merge                       Merge l10n copyright files with base ones.\n"
  printf "  -h, --help                        Show this message.\n"
  printf "                                    This option is used after -c is run.\n"
  printf "\n"
  printf "Options:\n"
  printf "  -t, --type TYPE                   $AVAILABLE_TYPES is available for TYPE.\n"
  printf "                                    the default is gnome.\n"
  printf "\n"
  printf "NOTE: This overrides the copyright files in $HOME/packages/spec-files/copyright/*.\n"
}

_get_group_copyright ()
{
  rm -f $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
  echo "Creating $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright ..."
  cat $COPY_ORG_DIR/${COPY_ORG}.copyright \
    >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright

  for LING in $LING_MESSAGE
  do
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "-------------------------------------------------------------" \
      >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright

    COPY_MESSAGES_DIR=/usr/share/locale/$LING/LC_MESSAGES
    gzcat $COPY_MESSAGES_DIR/$COPY_MESSAGES \
      >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
  done

  rm -f $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
  echo "Creating $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright ..."
  cat $COPY_ORG_DIR/${COPY_ORG}.copyright \
    >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright

  for LING in $LING_DOC
  do
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "-------------------------------------------------------------" \
      >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright

    COPY_MESSAGES_DIR=/usr/share/gnome/help/copyright/$LING
    gzcat $COPY_MESSAGES_DIR/$COPY_MESSAGES \
      >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
  done
}

_get_15lang_copyright ()
{
  for LING in cs de es fr hu it ja ko pl pt_BR ru sv zh_CN zh_HK zh_TW
  do
    TAG=`echo $LING | sed -e "s/_//"`

    rm -f $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "Creating $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright ..."
    cat $COPY_ORG_DIR/${COPY_ORG}.copyright \
      >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "-------------------------------------------------------------" \
      >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright
    COPY_MESSAGES_DIR=/usr/share/locale/$LING/LC_MESSAGES
    gzcat $COPY_MESSAGES_DIR/$COPY_MESSAGES \
      >> $COPY_ORG_DIR/${COPY_ORG}-m-$TAG.copyright

    rm -f $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "Creating $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright ..."
    cat $COPY_ORG_DIR/${COPY_ORG}.copyright \
      >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "-------------------------------------------------------------" \
      >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    echo "" >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
    COPY_MESSAGES_DIR=/usr/share/gnome/help/copyright/$LING
    gzcat $COPY_MESSAGES_DIR/$COPY_MESSAGES \
      >> $COPY_ORG_DIR/${COPY_ORG}-d-$TAG.copyright
  done
}

create_GNOME_copyright ()
{
  COPY_ORG=SUNWgnome-l10nmessages
  COPY_ORG_DIR=$HOME/packages/spec-files/copyright
  COPY_MESSAGES=COPYING.gnome.gz
  _get_15lang_copyright
  
  TAG=rtl
  LING_MESSAGE="ar az az_IR fa he ur ur_PK yi"
  LING_DOC="ar"
  _get_group_copyright
  
  TAG=extra
  LING_MESSAGE="bg ca ca@valencia da el et fi hi hr is lt lv mk mt nb nl nn no pt pt_PT ro sk sl sq sr sr@Latn sr@ije sr@latin ta te th tr"
  LING_DOC="bg ca da el fi mk nl ru sr"
  _get_group_copyright
  
  TAG=noinst
  LING_MESSAGE="aa af am ang as be be@latin bn bn_IN br bs byn cy dv dz eo eu fo fur ga gez gl gn gu gv haw hy ia id io iu ka kk kl km kn kok ku kw ky li lo mai mg mi ml mn mr ms my_MM nds@NFE ne nso oc om or pa ps rw sa si sid so sw syr tg ti tig tk tl tt ug uk uz uz@cyrillic ve vi wa wal wo xh yo zu"
  LING_DOC="eu oc pa uk vi"
  _get_group_copyright
}

create_desktop_other_copyright ()
{
  COPY_ORG=SUNWdesktop-other-l10n
  COPY_ORG_DIR=$HOME/packages/spec-files-other/copyright
  COPY_MESSAGES=COPYING.desktop-other.gz
  _get_15lang_copyright
  
  TAG=rtl
  LING_MESSAGE="ar he"
  LING_DOC="ar"
  _get_group_copyright
  
  TAG=extra
  LING_MESSAGE="bg ca da el et fi hi hr lt mk nb nl pt ro sk sl sr ta tr wo"
  LING_DOC="bg ca da el fi mk nl ru sr"
  _get_group_copyright
  
  TAG=noinst
  LING_MESSAGE="af bn bs cy gl gu id ka km lo mr pa uk vi xh zu"
  LING_DOC="eu oc pa uk vi"
  _get_group_copyright
}

_merge_base_copyright ()
{
  BASE_COPYRIGHTS_WZ_L10N=

  for COPYRIGHT in $BASE_ALL_COPYRIGHTS
  do
    SPEC=`basename $COPYRIGHT .copyright`.spec
    if [ ! -f $SPEC_DIR/$SPEC ] ; then
      continue;
    fi
    HAS_L10N_PKG=`grep "%package l10n" $SPEC_DIR/$SPEC`
    if [ x"$HAS_L10N_PKG" = x ] ; then
      continue;
    fi
    BASE_COPYRIGHTS_WZ_L10N="$BASE_COPYRIGHTS_WZ_L10N $COPYRIGHT"
  done

  if [ "$COPY_ORG" = "SUNWtgnome-l10n-ui" ] ; then
    TAGS="NONE"
  else
    TAGS="cs de es fr hu it ja ko pl ptBR ru sv zhCN zhHK zhTW rtl extra noinst"
  fi

  for TAG in $TAGS
  do
    if [ "$TAG" = "NONE" ] ; then
      L10N_COPYRIGHT_FILE_GROUP=`ls $COPY_ORG_DIR/${COPY_ORG}.copyright`
    else
      L10N_COPYRIGHT_FILE_GROUP=`ls $COPY_ORG_DIR/${COPY_ORG}*-${TAG}.copyright`
    fi

    if [ x"$L10N_COPYRIGHT_FILE_GROUP" = x ] ; then
      continue
    fi

    for L10N_COPYRIGHT_FILE in $L10N_COPYRIGHT_FILE_GROUP
    do
      echo "Merging $L10N_COPYRIGHT_FILE ..."
      for COPYRIGHT in $BASE_COPYRIGHTS_WZ_L10N
      do
        PKG=`basename $COPYRIGHT .copyright`

        echo "" >> $L10N_COPYRIGHT_FILE
        echo "-------------------------------------------------------------" \
          >> $L10N_COPYRIGHT_FILE
        echo "Copyright for $PKG" >> $L10N_COPYRIGHT_FILE
        echo "" >> $L10N_COPYRIGHT_FILE
        cat $COPY_ORG_DIR/$COPYRIGHT >> $L10N_COPYRIGHT_FILE
      done
    done
  done
}

merge_GNOME_base_copyright ()
{
  COPY_ORG=SUNWgnome-l10nmessages
  COPY_ORG_DIR=$HOME/packages/spec-files/copyright
  SPEC_DIR=`dirname $COPY_ORG_DIR`
  BASE_ALL_COPYRIGHTS=`(cd $COPY_ORG_DIR; ls *.copyright |\
    grep -v "SUNWacroread" |\
    grep -v "SUNWfirefox-" |\
    grep -v "SUNWmozilla-" |\
    grep -v "SUNWmyspell-dictionary" |\
    grep -v "SUNWtgnome-" |\
    grep -v "SUNWthunderbird-" |\
    grep -v "SUNWrealplayer" |\
    grep -v "$COPY_ORG" )`

  _merge_base_copyright
}

merge_TJDS_base_copyright ()
{
  COPY_ORG=SUNWtgnome-l10n-ui
  COPY_ORG_DIR=$HOME/packages/spec-files/copyright
  SPEC_DIR=`dirname $COPY_ORG_DIR`
  BASE_ALL_COPYRIGHTS=`(cd $COPY_ORG_DIR; ls SUNWtgnome-*.copyright |\
    grep -v "$COPY_ORG" )`

  _merge_base_copyright
}

merge_desktop_other_base_copyright ()
{
  COPY_ORG=SUNWdesktop-other-l10n
  COPY_ORG_DIR=$HOME/packages/spec-files-other/copyright
  SPEC_DIR=$HOME/packages/spec-files-other/core
  BASE_ALL_COPYRIGHTS=`(cd $COPY_ORG_DIR; ls *.copyright |\
    grep -v "$COPY_ORG" )`

  _merge_base_copyright
}

main ()
{
  init $@

  if [ $TYPE -eq $TYPE_DESKTOP_OTHER ] ; then
    if [ ! -d $HOME/packages/spec-files-other ] ; then
      echo "spec-files build tree is not dir: $HOME/packages/spec-files-other" 1>&2
      exit 1
    fi
  else
    if [ ! -d $HOME/packages/spec-files ] ; then
      echo "spec-files build tree is not dir: $HOME/packages/spec-files" 1>&2
      exit 1
    fi
  fi

  if [ $CREATE_COPYRIGHT -ne 0 -a $TYPE -eq $TYPE_GNOME ] ; then
    create_GNOME_copyright
  elif [ $CREATE_COPYRIGHT -ne 0 -a $TYPE -eq $TYPE_DESKTOP_OTHER ] ; then
    IS_X86=`uname -p | grep i386`

    if [ x"$IS_X86" = x ] ; then
      echo "Please run this script on x86 for desktop-other" 1>&2
      exit 1
    fi
    create_desktop_other_copyright
  fi
  if [ $MERGE_BASE_COPYRIGHT -ne 0 -a $TYPE -eq $TYPE_GNOME ] ; then
    merge_GNOME_base_copyright
  elif [ $MERGE_BASE_COPYRIGHT -ne 0 -a $TYPE -eq $TYPE_TJDS ] ; then
    merge_TJDS_base_copyright
  elif [ $MERGE_BASE_COPYRIGHT -ne 0 -a $TYPE -eq $TYPE_DESKTOP_OTHER ] ; then
    merge_desktop_other_base_copyright
  fi
}

main $@
