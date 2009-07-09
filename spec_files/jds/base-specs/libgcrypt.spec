#
# spec file for package libgcrypt
#
# Copyright (c) 2003 SuSE Linux AG, Nuernberg, Germany.
# Copyright 2007 Sun Microsystems, Inc
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Security team will take over ownership of libgcrypt
# Currtnly we stop upgrading it.
# Owner: jefftsai
# bugdb: savannah.gnu.org
#

Name:         libgcrypt
Version:      1.4.4
Release:      1
Summary:      libgcrypt - The GNU crypto library
License:      GPL v2, LGPL v2.1
Group:        Development/Libraries/C and C++
Autoreqprov:  on
URL:          http://www.gnupg.org/
Source:       ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version)

%prep
%setup -n %{name}-%{version}

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    --sysconfdir=/etc \
    --libdir=%{_libdir} \
    --infodir=%{_infodir} \
    --enable-maintainer-mode \
    --disable-asm \
    --enable-ciphers=arcfour:blowfish:des:aes:twofish:serpent:rfc2268:seed:camellia

make -j$CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING COPYING.DOC COPYING.LIB ChangeLog INSTALL NEWS README README-alpha THANKS TODO VERSION
%doc %_infodir/gc*
%{_libdir}/*
/usr/include/*
/usr/bin/*
/usr/share/aclocal/*

%changelog -n libgcrypt
* Thu Feb 05 2008 - jeff.cai@sun.com
- Bump to 1.4.4
- Remove patch -01-random-void.diff, upstreamed
* Fri Dec 26 2008 - jeff.cai@sun.com
- Change the bug db.
* Wed Dec 03 2008 - jeff.cai@sun.com
- Bump to 1.4.3
- Add patch -01-random-void to fix #106568.
  The void function should not return a value.
* Fri Oct 31 2008 - jeff.cai@sun.com
- Changet the license info.
* Thu Jun 12 2008 - jeff.cai@sun.com
- Per as the suggestions from security team, disable cast5.
* Fri Jun 06 2008 - jeff.cai@sun.com
  bump to 1.4.1
* Thi Dec 20 2007 - patrick.ale@gmail.com
- Change download protocol to FTP instead of HTTP
  HTTP:// leads to download failure where FTP:// does not
* Tue Mar 27 2007 - laca@sun.com
- clean up, enable parallel build
* Fri Mar 16 2007 - jeff.cai@sun.com
- Bump to 1.2.4.
* Wed Oct 25 2006 - jedy.wang@sun.com
- Bump to 1.2.3.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec. 
* Mon Oct 10 2005 - halton.huo@sun.com
- Bump to 1.2.2.
* Wed Aug 31 2005 - halton.huo@sun.com
- Bump to 1.2.1
- Add URL and correct Source filed
- Remove the obsoleted patch libgcrypt-1.1.12-sexp-valgrind-error.diff
* Tue Sep 21 2004 - ghee.teo@sun.com
- Move the spec file back to spec-files/Solaris/extra-specs so that
  it is now a solaris only spec file. Also moved its patch back to
  spec-files/Solaris/patches.
* Wed Sep 01 2004 - ghee.teo@sun.com
- renamed libgcrypt-1.1.12-sexp-valgrind-error.patch to
  libgcrypt-1.1.12-sexp-valgrind-error.diff
* Wed May 14 2003 - mc@suse.de
- add libgcrypt-1.1.12-sexp-valgrind-error.patch from Ximian
  needed for rc
* Tue Feb 11 2003 - mc@suse.de
- switch to version 1.1.12
- gcry_pk_sign, gcry_pk_verify and gcry_pk_encrypt can now handle an
  optional pkcs1 flags parameter in the S-expression.  A similar flag
  may be passed to gcry_pk_decrypt but it is only syntactically
  implemented.
- New convenience macro gcry_md_get_asnoid.
- There is now some real stuff in the manual.
- New algorithm: MD4
- Implemented ciphertext stealing.
- Support for plain old DES
- Smaller bugs fixes and a few new OIDs.
* Thu Aug 01 2002 - poeml@suse.de
- create package
