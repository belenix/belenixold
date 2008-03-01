#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


Name:			libxfcegui4
Summary:		Various gtk widgets for xfce
URL:			http://www.xfce.org/
%define src_name        libxfcegui4
Version:		4.4.2
Source0:		%{xfce_src_url}/libxfcegui4-%{version}.tar.bz2
Patch1:			libxfcegui4-01-fixgccism.diff
Group:			Development/Libraries

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1

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
        --datadir=%{_datadir}		\
        --mandir=%{_mandir}		\
        --sysconfdir=%{_sysconfdir}	\
        %{gtk_doc_option}		\
        --disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
- Version bumped to 4.4.1
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Mar  8 2007 - Menno.Lageman@Sun.COM
- added fixgccism patch
* Wed Feb 21 2007 - Menno.Lageman@Sun.COM
- fix some gcc G_BEGIN_DECLS for Sun Studio build niceness
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
