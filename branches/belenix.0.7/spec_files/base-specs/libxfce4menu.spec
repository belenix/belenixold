#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:			libxfce4menu
Summary:		Menu library for the Xfce desktop environment
URL:			http://www.xfce.org/
%define src_name	libxfce4menu
Version:		4.4.0
Source0:		http://www.us.xfce.org/archive/xfce-%{xfce_version}/src/%{src_name}-%{version}.tar.bz2
Patch1:			libxfce4menu-01-fixheaders.diff
Patch2:			libxfce4menu-02-libgobject.diff
Group:			Development/Libraries
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1
%patch2 -p1

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
* Sat Apr  7 2007 - dougs@truemail.co.th
- Initial version
