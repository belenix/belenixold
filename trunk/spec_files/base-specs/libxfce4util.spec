#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


Name:			libxfce4util
Summary:		Utility library for the Xfce desktop environment
URL:			http://www.xfce.org/
%define src_name	libxfce4util
Version:		4.4.2
Source0:		%{xfce_src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			%{src_name}-01-fixheaders.diff
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

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
	--sbindir=%{_sbindir}		\
	--libdir=%{_libdir}		\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir} 	\
	%{gtk_doc_option}		\
	--enable-debug=no		\
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
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
