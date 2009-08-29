#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWmysql5r
#
# includes module(s): MySQL 5.0.x
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc
%define  MYSQL_VERSION   5.0.84

Name:                    SUNWmysql5r
Summary:                 MySQL Database Management System (root component)
Version:                 %{MYSQL_VERSION}
License:                 GPLv2 with exceptions
URL:                     http://www.mysql.com/
Source:                  ftp://ftp.easynet.be/mysql/Downloads/MySQL-5.0/mysql-%{version}.tar.gz
Source1:                 mysql
Source2:                 mysql.1.sunman
Source3:                 mysql.xml
Patch1:                  mysql5-01-mysql_config.diff
Patch2:                  mysql5-02-federated_cnf.diff

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package -n SUNWmysql5u
Summary:                 MySQL Database Management System (usr component)
Version:                 %{MYSQL_VERSION}
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%package -n SUNWmysql5test
Summary:                 MySQL Database Management System (test component)
Version:                 %{MYSQL_VERSION}
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name

%prep
%if %cc_is_gcc
%else
	%error This spec file requires GCC, set the CC and CXX env variables
%endif
%setup -q -c -n %name-%version
cd mysql-%{version}
%patch1 -p0
(cd support-files
 cat %{PATCH2} | gpatch -p0)
cd ..

%ifarch amd64 sparcv9
cp -pr mysql-%{version} mysql-%{version}-64
%endif


%build
PREFIX=%{_prefix}/mysql/5.0
CONFDIR=%{_sysconfdir}/mysql/5.0
DATA_PREFIX=%{_localstatedir}/mysql/5.0

%ifarch amd64 sparcv9
cd mysql-%{version}-64
export CFLAGS="-O3 -march=opteron -m64 -fno-omit-frame-pointer -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -fPIC -fno-strict-aliasing -fwrapv"
export CXXFLAGS="-O3 -march=opteron -m64 -fno-omit-frame-pointer -fPIC -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -fno-strict-aliasing -fwrapv -felide-constructors -fno-rtti -fno-exceptions"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/gmake
export LDFLAGS="-64 %{gnu_lib_path64} -lstdc++"

./configure     --prefix=${PREFIX} \
                --libexecdir=${PREFIX}/bin/%{_arch64} \
                --bindir=${PREFIX}/bin/%{_arch64}  \
                --libdir=${PREFIX}/lib/%{_arch64} \
                --localstatedir=${DATA_PREFIX}/data \
                --datadir=${PREFIX}/share  \
                --sbindir=${PREFIX}/sbin/%{_arch64}  \
                --sharedstatedir=${PREFIX}/com  \
                --includedir=${PREFIX}/include \
                --oldincludedir=${PREFIX}/include \
                --infodir=${PREFIX}/docs \
                --mandir=${PREFIX}/man  \
                --sysconfdir=${CONFDIR}  \
                --with-server-suffix=   \
                --enable-thread-safe-client     \
                --with-mysqld-libs=-lmtmalloc   \
                --with-named-curses=-lcurses    \
                --with-client-ldflags=-static   \
                --with-mysql-ldflags=-static    \
                --with-pic \
                --with-big-tables \
                --with-yassl    \
                --with-readline \
                --with-archive-storage-engine   \
                --with-blackhole-storage-engine \
                --with-csv-storage-engine       \
                --with-example-storage-engine   \
                --with-federated-storage-engine \
                --with-innodb   \
                --with-extra-charsets=complex   \
                --enable-local-infile  \
                --with-ndbcluster \
                --with-embedded-server \
                --enable-thread-safe-client \
                --enable-largefile

${MAKE} INSTALL=${INSTALL}
cd ..
%endif

cd mysql-%{version}
export CFLAGS="-O3 -march=pentiumpro -fno-omit-frame-pointer -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -fPIC -fno-strict-aliasing -fwrapv"
export CXXFLAGS="-O3 -march=pentiumpro -fno-omit-frame-pointer -fPIC -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -fno-strict-aliasing -fwrapv -felide-constructors -fno-rtti -fno-exceptions"
export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/gmake
export LDFLAGS="%{gnu_lib_path} -lstdc++"

./configure     --prefix=${PREFIX} \
                --libexecdir=${PREFIX}/bin \
                --bindir=${PREFIX}/bin  \
                --libdir=${PREFIX}/lib \
                --localstatedir=${DATA_PREFIX}/data \
                --datadir=${PREFIX}/share  \
                --sbindir=${PREFIX}/sbin  \
                --sharedstatedir=${PREFIX}/com  \
                --includedir=${PREFIX}/include \
                --oldincludedir=${PREFIX}/include \
                --infodir=${PREFIX}/docs \
                --mandir=${PREFIX}/man  \
                --sysconfdir=${CONFDIR}  \
                --with-server-suffix=   \
                --enable-thread-safe-client     \
                --with-mysqld-libs=-lmtmalloc   \
                --with-named-curses=-lcurses    \
                --with-client-ldflags=-static   \
                --with-mysql-ldflags=-static    \
                --with-pic \
                --with-big-tables \
                --with-yassl    \
                --with-readline \
                --with-archive-storage-engine   \
                --with-blackhole-storage-engine \
                --with-csv-storage-engine       \
                --with-example-storage-engine   \
                --with-federated-storage-engine \
                --with-innodb   \
                --with-extra-charsets=complex   \
                --enable-local-infile  \
                --with-ndbcluster \
                --with-embedded-server \
                --enable-thread-safe-client \
                --enable-largefile

${MAKE} INSTALL=${INSTALL}
cd ..


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

ROOT=$RPM_BUILD_ROOT
PREFIX=${ROOT}%{_prefix}/mysql/5.0
CONFDIR=${ROOT}%{_sysconfdir}/mysql/5.0
DATA_PREFIX=${ROOT}%{_localstatedir}/mysql/5.0
SYSMAN1DIR=${ROOT}%{_mandir}/man1
MANIFESTDIR=${ROOT}%{_localstatedir}/svc/manifest/application/database
METHODDIR=${ROOT}/lib/svc/method
PREFIX=${ROOT}%{_prefix}/mysql/5.0

export INSTALL=/usr/ucb/install
export MAKE=/usr/bin/gmake

_install()
{
  _type=$1
  _src=$2
  _targ=$3
  _perm=$4

  case "$1" in
    N|S)
      # Install normal or executable script file
      rm -f $_targ
      cp $_src $_targ
      chmod $_perm $_targ
      ;;
  esac
}

install_dir()
{
  dstdir="$1"
  mode="$2"

  mkdir -p "$dstdir"
  chmod "$mode" "$dstdir"
}

%ifarch amd64 sparcv9
cd mysql-%{version}-64
${MAKE} install DESTDIR=${ROOT} INSTALL=${INSTALL}

# Remove unwanted files
(cd ${ROOT}/%{_prefix}/mysql/5.0/lib/%{_arch64}/mysql
 rm -f *.la libvio.a libheap.a libmysqlclient.a libmyisam.a \
       libmyisammrg.a libmsys.a libmystrings.a libmysqlclient_r.a \
       libdbug.a libmysys.a libndbclient.a
 cd ../..
 ln -s %{_arch64} 64)

(cd ${ROOT}/%{_prefix}/mysql/5.0/bin
 ln -s %{_arch64} 64)

# Fix permissions
(for dirs in "$PREFIX/bin" "$PREFIX/bin/%{_arch64}" "$PREFIX/lib/mysql" "$PREFIX/lib/%{_arch64}/mysql"
do
        cd "$dirs"
        find . -perm u=rwx,g=rx,o=rx -type f -exec chmod 555 {} \;
        echo "Permissions have been fixed for $dirs......"

done)

cd ..
%endif

cd mysql-%{version}
${MAKE} install DESTDIR=${ROOT} INSTALL=${INSTALL}

mkdir -p ${CONFDIR}
mkdir -p ${DATA_PREFIX}/data

(cd support-files
 # Ship a default my.cnf to simplify ease of use.
 _install N my-small.cnf "${CONFDIR}/my.cnf" 644

 # Ship the standard my.cnf files
 _install N my-small.cnf "${CONFDIR}/my-small-cnf.cnf" 644
 _install N my-huge.cnf  "${CONFDIR}/my-huge.cnf"  644
 _install N my-large.cnf "${CONFDIR}/my-large.cnf" 644
 _install N my-medium.cnf "${CONFDIR}/my-medium.cnf" 644
 _install N my-innodb-heavy-4G.cnf "${CONFDIR}/my.innodb-heavy-4G.cnf" 644

 # Set the correct permission for data directory
 install_dir "${DATADIR}" 700
 install_dir "${DATADIR}/5.0" 700
 install_dir "${DATADIR}/5.0/data" 700)

# Install standard man page
mkdir -p ${SYSMAN1DIR}
cp -f %{SOURCE2} ${SYSMAN1DIR}/mysql.1
chmod 444 ${SYSMAN1DIR}/mysql.1

# Fix permissions
(for dirs in "$PREFIX/share/mysql" \
        "$PREFIX/include/mysql" \
        "$PREFIX/man/man1" \
        "$PREFIX/man/man8" \
        "$PREFIX/docs"
do
        cd "$dirs"
        find . -type f -exec chmod 444 {} \;
        echo "Permissions have been fixed for $dirs......"
done)

 # Remove unwanted files
(cd ${ROOT}/%{_prefix}/mysql/5.0/lib/mysql
 rm -f *.la libvio.a libheap.a libmysqlclient.a libmyisam.a \
       libmyisammrg.a libmsys.a libmystrings.a libmysqlclient_r.a \
       libdbug.a libmysys.a libndbclient.a)

# Install SMF files
mkdir -p ${MANIFESTDIR}
cp -f %{SOURCE3} ${MANIFESTDIR}
chmod 444 ${MANIFESTDIR}/mysql.xml

mkdir -p ${METHODDIR}
cp -f %{SOURCE1} ${METHODDIR}
chmod 555 ${METHODDIR}/mysql

cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/mysql
%dir %attr (0755, root, bin) %{_sysconfdir}/mysql/5.0
%config %class(renamenew) %attr (0644, root, bin) %{_sysconfdir}/mysql/5.0/my.cnf
%attr (0644, root, bin) %{_sysconfdir}/mysql/5.0/my-*.cnf
%attr (0644, root, bin) %{_sysconfdir}/mysql/5.0/my.innodb-heavy-4G.cnf

%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0700, mysql, mysql) %{_localstatedir}/mysql
%dir %attr (0700, mysql, mysql) %{_localstatedir}/mysql/5.0
%dir %attr (0700, mysql, mysql) %{_localstatedir}/mysql/5.0/data

%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/database
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/application/database/mysql.xml

%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/mysql

%files -n SUNWmysql5u
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/mysql
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/include
%{_basedir}/mysql/5.0/include/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/docs
%{_basedir}/mysql/5.0/docs/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/bin
%attr (0555, root, bin) %{_basedir}/mysql/5.0/bin/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/share
%{_basedir}/mysql/5.0/share/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/lib
%{_basedir}/mysql/5.0/lib/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/man
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/man/man1
%attr (0444, root, bin) %{_basedir}/mysql/5.0/man/man1/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/man/man8
%attr (0444, root, bin) %{_basedir}/mysql/5.0/man/man8/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%attr (0444, root, bin) %{_mandir}/man1/*

%files -n SUNWmysql5test
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/mysql
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/sql-bench
%{_basedir}/mysql/5.0/sql-bench/*
%dir %attr (0755, root, bin) %{_basedir}/mysql/5.0/mysql-test
%{_basedir}/mysql/5.0/mysql-test/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial spec (migrated and modified from SFW gate).

