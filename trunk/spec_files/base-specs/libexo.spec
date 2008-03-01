#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


Name:			libexo
Summary:		Application library for the Xfce desktop environment
URL:			http://www.xfce.org/
%define src_name	exo
Version:		0.3.4
Source0:		%{xfce_src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			libexo-01-fixgccism.diff
#Patch2:			libexo-02-stdio.diff
#Patch3:			libexo-03-nosetmntent.diff

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1
#%patch2 -p1
#%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

   config=./configure

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
$config	--prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	%{gtk_doc_option}		\
	--enable-xfce-mcs-manager	\
	--enable-xsltproc		\
	--enable-debug=no		\
	--disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/xfce4/mcs-plugins/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Dec 9 2007 - sobotkap@centrum.cz
- Bump to 0.3.4
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
- add hack that decides whether to depend on SUNWgnome-panel or OSOLlibnotify
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added another fixgccism patch
* Fri Feb  9 2007 - dougs@truemail.co.th
- Added libnotify and change perl-ui requirement - Copied from SFE repository
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
