#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


Name:			xfce4-session
Summary:		Xfce Session manager
URL:			http://www.xfce.org/
%define src_name	xfce4-session
Version:		4.4.2
Source0:		%{xfce_src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			xfce4-session-01-fixgccism.diff

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

   config=./configure

export ICEAUTH=/usr/openwin/bin/iceauth
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"
$config --prefix=%{_prefix}             \
	--libdir=%{_libdir}             \
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}           \
	--mandir=%{_mandir}             \
	--sysconfdir=%{_sysconfdir}     \
	%{gtk_doc_option}                \
	--enable-debug=no		\
	--enable-gnome			\
	--disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/xfce4/splash/engines/*.la
rm $RPM_BUILD_ROOT%{_libdir}/xfce4/mcs-plugins/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Dec 10 2007 - sobotkap@centrum.cz
- Version bumped to 4.4.2
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
- Version bumped to 4.4.1
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
