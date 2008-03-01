#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:			thunar
Summary:		Thunar File Manager
URL:			http://www.xfce.og/
%define src_name	Thunar
Version:		0.9.0
Source0:		%{xfce_src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			thunar-01-fixgccism.diff
#Patch2:			thunar-02-anon_union.diff
Patch3:         thunar-03-fixmoregccism.diff
Patch4:         thunar-04-fixmoregccism2.diff
Patch5:         thunar-05-fixgccismagain.diff

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

   config=./configure

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
$config	--prefix=%{_prefix}		\
	--sbindir=%{_sbindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	%{gtk_doc_option}		\
	--enable-debug=no		\
	--enable-dbus			\
	--enable-xsltproc		\
	--disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/thunarx-1/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Dec  9 2007 - sobotkap@centrum.cz
- Bump to 0.9.0
* Mon Apr 16 2007 - laca@sun.com
- fix tarball download url
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  9 2007 - dougs@truemail.co.th
- Added SUNWpcre requirement
* Thu Feb  2 2007 - dougs@truemail.co.th
- Initial version
