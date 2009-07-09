#
# spec file for package SUNWjdsrm
#
# includes module(s): SUNWjdsver.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
# DO NOT REMOVE NEXT LINE
# PACKAGE NOT ARC REVIEWED BY SUN JDS TEAM
#
%include Solaris.inc

%use jdsver = SunDesktopVersion.spec

Name:                    SUNWjdsrm
Summary:                 Java Desktop System upgrade package remove
# Note: increment the nano version in case of a respin.
#       New builds should start with a 0
#       110 means integrated into solaris 11.0
Version:                 %{jdsver.prodRelMajor}.%{jdsver.prodBuild}.0
SUNW_Category: 		 JDS,system,%{jds_version}
SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)


%post
#
# JDS clean up for packages with non-standard package version strings
# Note: Any pkg using SUNWjdsrm to remove a previous version, 
#	Must add SUNWjdsrm to it's package depend file to ensure the
#	removal of the previous version before the addition of the
#	new version.
#
PKG="SUNWglow SUNWjai-imageio SUNWjmf SUNWjmfmp3 SUNWjdsver SUNWjpeg SUNWjpegx SUNWtiff SUNWtiffx"
cat > /tmp/admin.dflt.$$ << EOF
mail=
instance=overwrite
partial=nocheck
runlevel=nocheck
idepend=nocheck
rdepend=nocheck
space=nocheck
setuid=nocheck
conflict=nocheck
action=nocheck
basedir=default
EOF

REM_SCRIPT=/tmp/pkgremoval.$PKGINST.$$
echo "PATH=/usr/sadm/bin:$PATH" > $REM_SCRIPT
do_pkgrm() {
  echo "sleep 3" >> $REM_SCRIPT
  echo "echo Now removing old instance of $1" >> $REM_SCRIPT
  eval echo `gettext SUNW_INSTALL_LIBSVC 'Removing package $1:'`
  if [ -n "${PKG_INSTALL_ROOT}" ]; then
    if [ -f ${PKG_INSTALL_ROOT}/var/sadm/pkg/$i/install/preremove ]; then
      sed -e 's: /usr: ${PKG_INSTALL_ROOT}/usr:' ${PKG_INSTALL_ROOT}/var/sadm/pkg/$i/install/preremove > /tmp/$i.pkgremove.$$
      cp /tmp/$i.pkgremove.$$ ${PKG_INSTALL_ROOT}/var/sadm/pkg/$i/install/preremove
      rm /tmp/$i.pkgremove.$$
    fi
    echo "pkgrm -M -R ${PKG_INSTALL_ROOT} -a /tmp/admin.dflt.$$ -n $1" >> $REM_SCRIPT
  else
    echo "pkgrm -M -a /tmp/admin.dflt.$$ -n $1" >> $REM_SCRIPT
  fi
}

for i in $PKG
do
  if [ -n "${PKG_INSTALL_ROOT}" ]; then
    (pkgparam -R ${PKG_INSTALL_ROOT} $i VERSION | egrep -v  '^[0-9.]+$|^[0-9.]+,REV=[0-9.]+$') > /dev/null 2>&1
  else
    (pkgparam  $i VERSION | egrep -v  '^[0-9.]+$|^[0-9.]+,REV=[0-9.]+$') > /dev/null 2>&1
  fi
  exist=$?
  if [ $exist -eq 0 ] ; then
    do_pkgrm $i
  fi
done

if [ -f $REM_SCRIPT ]; then
  sh $REM_SCRIPT &
fi

exit 0


%changelog
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - shirley.woo@sun.com
- Updated package version string to remove "110" from the VERSION. 
  This makes it consistent with SUNWjdsver.
* Tue Nov 05 2004 - shirley.woo@sun.com
- Bug 4810847 & 6185753:  Initial Creation
