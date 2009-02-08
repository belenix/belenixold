#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

Name:                    SUNWant
Summary:                 ant - The Jakarta ANT Java/XML-based build tool
Version:                 1.7.1
URL:                     http://ant.apache.org/
Source:                  http://www.mirrorgeek.com/apache.org/ant/source/apache-ant-%{version}-src.tar.bz2
Source1:                 ant.1.sunman

Patch1:                  ant-01-build_xml.patch
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWj6rt
BuildRequires: SUNWj6dev

%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

rm -rf %name-%version
mkdir %name-%version
cd %name-%version

rm -rf apache-ant-%{version}
bunzip2 -c %{SOURCE} | gtar xf - 

cd apache-ant-%{version}
cat %{PATCH1} | gpatch -p 0

%build
cd %name-%version

#
# Fetch latest Java 1.6 subdirectory
#
JDK_DIR=/usr/jdk/instances
dir=`ls -ltr ${JDK_DIR} | grep "1.6" | nawk '{ print $9 }' | tail -1`

BUILD_TOP=`pwd`
ANTBIN=jakarta-ant
#
# No, not ANT_HOME since user builds might have ANT_HOME
# set in the environment.
ANTHOME=${BUILD_TOP}/${ANTBIN}
ANTCMD=${ANTHOME}/bin/ant       # invoke this to run 'ant' within the makefile
JAVA_HOME=${JDK_DIR}/${dir}
JDK=${JAVA_HOME}
unset ANT_HOME

PATH=/opt/SUNWspro/bin:${JDK}/bin:${PATH}
export ANTHOME ANTCMD JAVA_HOME PATH

cd apache-ant-%{version}
ksh93 ./build.sh -Ddist.dir=${ANTHOME} dist


%install
cd %name-%version
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

cd jakarta-ant
ANTBIN=${RPM_BUILD_ROOT}/usr/bin
ANTLIB=${RPM_BUILD_ROOT}/usr/share/lib/ant
ANTDOC=${RPM_BUILD_ROOT}/usr/share/doc/ant
ANTETC=${ANTLIB}
ANTMAN=${RPM_BUILD_ROOT}/usr/share/man/man1

mkdir -p ${ANTBIN} ${ANTLIB} ${ANTDOC} ${ANTETC} ${ANTMAN}
cp bin/* ${ANTBIN}/
rm -f ${ANTBIN}/ant
sed -e '/^ANT_LIB/c\
ANT_LIB=${ANT_HOME}/share/lib/ant' \
        -e '6i\
\
JAVA_HOME=${JAVA_HOME:-/usr/java}\
ANT_HOME=${ANT_HOME:-/usr}' \
    bin/ant > ${ANTBIN}/ant
chmod 0755 ${ANTBIN}/*
cd docs
find . -depth -print | cpio -pdum ${ANTDOC}
cd ../etc
find . -depth -print | cpio -pdum ${ANTETC}
cd ../lib
find . -depth -print | cpio -pdum ${ANTLIB}
rm ${ANTLIB}/*.pom ${ANTLIB}/*.pom.md5 ${ANTLIB}/*.pom.sha1
cd ..
cp KEYS ${ANTDOC}
cp LICENSE ${ANTDOC}
cp README ${ANTDOC}
cp WHATSNEW ${ANTDOC}
chmod 0444 ${ANTDOC}/KEYS ${ANTDOC}/LICENSE ${ANTDOC}/README ${ANTDOC}/WHATSNEW

(cd ${ANTLIB}
  find . -type d -exec chmod 755 {} \;
  find . -type f -exec chmod 444 {} \;)
(cd ${ANTDOC}
  find . -type d -exec chmod 755 {} \;
  find . -type f -exec chmod 444 {} \;)

cp %{SOURCE1} ${ANTMAN}
mv ${ANTMAN}/ant.1.sunman ${ANTMAN}/ant.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/lib
%{_datadir}/lib/*

%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Sat Feb 07 2009 - moinakg@gmail.com
- Initial spec (migrated and merged from SFW gate).

