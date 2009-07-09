#
# spec file for package libgpg-error
# Security team will take over ownership of libgpg-error
# So we stop upgrading it before that.
#
# Owner: jefftsai
#
Name:         libgpg-error
Version:      1.7
Release:      1
Summary:      libgpg-error - Common error codes for GnuPG, Libgcrypt etc.
License:      GPL v2, LGPL v2.1
Group:        Development/Libraries
Copyright:    LGPL
Autoreqprov:  on
URL:          http://www.gnupg.org/
Source:       ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
Source1:      l10n-configure.sh
# owner:laca type:feature date:2007-10-02
Patch1:       libgpg-error-01-gettext.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%prep
%setup -n %{name}-%{version}
%patch1 -p1

bash -x %SOURCE1 --enable-sun-linguas

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

glib-gettextize --force
aclocal $ACLOCAL_FLAGS -I ./m4
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --libdir=%{_libdir} \
    --infodir=%{_infodir} 

make -j$CPUS MSGFMT_OPTS=

%install
make DESTDIR=$RPM_BUILD_ROOT install MSGFMT_OPTS=
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -fr $RPM_BUILD_ROOT
make distclean

%post
%run_ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB AUTHORS README INSTALL NEWS ChangeLog
%attr(0755,root,root) %{_bindir}/gpg-error-config
%attr(0755,root,root) %{_bindir}/gpg-error
%attr(0755,root,root) %{_libdir}/*gpg-error.so*
%attr(0644,root,root) %{_libdir}/*gpg-error.a
%{_includedir}/gpg-error.h
%{_datadir}/aclocal/gpg-error.m4

%changelog -n libgpg-error
* Thu Jan 22 2008 - jeff.cai@sun.com
- Bump to 1.7
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Fri Jun 06 2008 - jeff.cai@sun.com
  Bump to 1.6
* Tue Oct  2 2007 - laca@sun.com
- add patch gettext.diff that fixes the l10n build
* Tue Mar 27 2007 - laca@sun.com
- clean up, enable parallel build
* Fri Mar 16 2007 - jeff.cai@sun.com
- Bump to 1.5.
* Sat Jul 22 2006 - halton.huo@sun.com
- Bump version to 1.3.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files part in linux spec. 
* Wed Aug 31 2005 - halton.huo@sun.com
- Initial version.
