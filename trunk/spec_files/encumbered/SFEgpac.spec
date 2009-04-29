#
# spec file for package SFEgpac
#
# includes module(s): gpac
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define	src_name gpac
%define	src_url	http://downloads.sourceforge.net/gpac

Name:                SFEgpac
Summary:             Open Source multimedia framework
Version:             0.4.5
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch4:		     gpac-04-inaddr.diff
Patch5:              gpac-05-crazy.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SUNWfreetype2
Requires: SUNWfreetype2
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEwxwidgets-gnu

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

cd gpac
%patch4 -p1
%patch5 -p1
cd .. 

%ifarch amd64 sparcv9
cp -rp gpac gpac-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd gpac-64

ORIG_PATH=${PATH}

export PATH=/usr/gnu/bin/%{_arch64}:/usr/bin/%{_arch64}:/usr/sfw/bin/%{_arch64}:${ORIG_PATH}
export LD_OPTIONS="-i -L/usr/gnu/lib/%{_arch64} -L/usr/X11/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}:/usr/X11/lib/%{_arch64}:/usr/sfw/lib/%{_arch64}"
export CXX=g++
RPM_OPT_FLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer -m64"

#
# No 64Bit theora yet so disable theora for 64Bit build
#
chmod 755 ./configure
./configure --prefix=%{_prefix}		\
            --mandir=%{_mandir}		\
	    --cc=gcc			\
	    --extra-ldflags="-fPIC -m64"	\
	    --extra-libs="-lrt -lm"	\
	    --disable-opt		\
	    --mozdir=/usr/lib/firefox	\
	    --use-theora=no             \
	    --extra-cflags="$RPM_OPT_FLAGS"

#
# Lot of unfortunate massaging needed as Gpac configure and Makefiles are
# broken for 64Bit builds
#
echo "CXX=g++" >> config.mak
cat config.mak | sed '{
    s#LDFLAGS=#LDFLAGS= -fPIC -m64 -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} -lgtk-x11-2.0 -lgdk-x11-2.0 -L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%_arch64} -lX11 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -lstdc++#
    s#SHFLAGS=#SHFLAGS=-m64 #
    s#moddir=/usr/lib/gpac#moddir=/usr/lib/%{_arch64}/gpac#
    s#moddir_path=/usr/lib/gpac#moddir_path=/usr/lib/%{_arch64}/gpac#
    s#libdir=lib#libdir=lib/%{_arch64}#
    s#X11_LIB_PATH=/usr/X11R6/lib#X11_LIB_PATH=/usr/X11R6/lib/%{_arch64}#
}' > config.mak.new
cp config.mak.new config.mak

cat modules/jack/Makefile | sed 's#-L/usr/lib#-L/usr/lib/%{_arch64}#' > modules/jack/Makefile.new
chmod +w modules/jack/Makefile
cp modules/jack/Makefile.new modules/jack/Makefile

cat Makefile | sed '{
    s#\(prefix\)/bin#\(prefix\)/bin/%{_arch64}#
    s#\(prefix\)/lib#\(prefix\)/lib/%{_arch64}#
}' > Makefile.new
chmod +w Makefile
cp Makefile.new Makefile

make
cd ..
%endif

cd gpac
export PATH=/usr/gnu/bin:${ORIG_PATH}
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i -L/usr/gnu/lib -L/usr/X11/lib -R/usr/gnu/lib:/usr/X11/lib:/usr/sfw/lib"
export CXX=g++
RPM_OPT_FLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer"

chmod 755 ./configure
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --cc=gcc                    \
            --extra-ldflags="-fPIC"        \
            --extra-libs="-lrt -lm"     \
            --disable-opt               \
            --mozdir=/usr/lib/firefox   \
            --extra-cflags="$RPM_OPT_FLAGS"
echo "CXX=g++" >> config.mak
cat config.mak | sed 's#LDFLAGS=#LDFLAGS= -fPIC -L/usr/lib -R/usr/lib -lgtk-x11-2.0 -lgdk-x11-2.0 -L/usr/X11/lib -R/usr/X11/lib -lX11 -L/usr/gnu/lib -R/usr/gnu/lib -lstdc++#' > config.mak.new
cp config.mak.new config.mak

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd gpac-64
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/MP* $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/O* $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
cd ..
%endif

cd gpac
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/MP4*
%{_bindir}/O*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.a
%{_libdir}/gpac

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/MP4*
%{_bindir}/%{_arch64}/O*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/lib*.a
%{_libdir}/%{_arch64}/gpac
%endif

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gpac
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 0.4.5 and add 64Bit build.
* Sat Jun 21 2008 - moinakg@gmail.com
- Remove dependency from SFEfreetype. It is no longer needed since
- SUNWfreetype is updated to new version.
* Thu Feb 21 2008 - moinak.ghosh@sun.com
- Add patch to fix silly problem building in Indiana-like environment.
* Mon Dec 31 6 2007 - markwright@internode.on.net
- Add patch 4 to fix trivial compiler error missing INADDR_NONE.
- Add --extra-libs="-lrt -lm".
* Mon Jul 30 2007 - dougs@truemail.co.th
- Install headers
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
