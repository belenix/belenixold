#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEslocate
Summary:             Finds files on a system via a central database.
Version:             2.7
License:             GPL
URL:                 http://slocate.trakker.ca/
Source:              http://slocate.trakker.ca/files/slocate-%{version}.tar.gz
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %cc_is_gcc
Requires: SFEgccruntime
BuildRequires: SFEgcc
%endif

%description
Slocate is a security-enhanced version of locate. Just like locate,
slocate searches through a central database (which is updated nightly)
for files which match a given pattern. Slocate allows you to quickly
find files anywhere on your system.

%prep
%setup -q -n slocate-%{version}

%build
#cd src
#ln -s %{_libdir}/libast.so.1 libast.so
#cp Makefile Makefile.orig 
#cat Makefile.orig | sed '{
    #s@CFLAGS=@CFLAGS=-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fsigned-char -march=pentium3 -I%{_includedir} -I%{_includedir}/ast @
    #s@#LDFLAGS\+=\-lefence@LDFLAGS=-L. -last -R%{_libdir}@
#}' > Makefile
#make

ln -s %{_bindir}/automake-1.10 automake
ln -s %{_bindir}/aclocal-1.10 aclocal
PATH=.:${PATH}
export PATH
INSTALL=ginstall
export INSTALL

./autogen.sh --prefix=%{_prefix}
gmake

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp slocate $RPM_BUILD_ROOT%{_bindir}
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/locate
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/updatedb
gunzip -c doc/slocate.1.other.gz > $RPM_BUILD_ROOT%{_mandir}/man1/slocate.1
gunzip -c doc/updatedb.1.gz > $RPM_BUILD_ROOT%{_mandir}/man1/slocate.1
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/db/slocate
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

#gmake install DESTDIR=$RPM_BUILD_ROOT

cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/updatedb.conf
# This file sets environment variables which are used by updatedb

# filesystems which are pruned from updatedb database
PRUNEFS="NFS nfs fd proc smbfs autofs auto hsfs dev devfs tmpfs objfs ctfs mntfs"
export PRUNEFS
# paths which are pruned from updatedb database
PRUNEPATHS="/tmp /var/tmp"
export PRUNEPATHS
# netpaths which are added
NETPATHS=""
export NETPATHS
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep "^slocate" /etc/group > /dev/null
if [ $? -ne 0 ]
then
	groupadd slocate
fi

%post
# Add the updatedb script to crontab if needed
DEST=${PKG_INSTALL_ROOT:-/}/var/spool/cron/crontabs/root
grep -s updatedb $DEST >/dev/null 2>&1
if [ $? -ne  0 ]; then
        echo "0 10 * * * [ -x /usr/bin/updatedb ] && /usr/bin/updatedb" >>$DEST
fi

%preun
rm -f %{_localstatedir}/lib/slocate/slocate.db

%postun
groupdel slocate

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%attr (2755, root, slocate) %{_bindir}/slocate
%{_bindir}/locate
%{_bindir}/updatedb
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/db
%dir %attr (0750, root, slocate) %{_localstatedir}/db/slocate
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr (0644, root, bin) %{_sysconfdir}/updatedb.conf

%changelog
* Mon Oct 12 2009 - Moinak Ghosh
- Initial spec
