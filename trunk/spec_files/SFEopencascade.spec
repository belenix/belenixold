#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc

Name:                SFEopencascade
Summary:             Tools for 3D surface and solid modeling, visualization, data exchange etc.
Version:             6.3.0
License:             GPL
URL:                 http://www.opencascade.org/
Source:              http://www.belenix.org/binfiles/OpenCASCADE_src.tar.gz
Patch1:              opencascade-01-solaris.diff

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWbzip
Requires: SFEsoqt
Requires: SFEcoin3d
Requires: SUNWzlib
Requires: SUNWxorg-mesa
Requires: SFEsimage
BuildRequires: SFEdoxygen
BuildRequires: SUNWxorg-headers
BuildRequires: SFEsimage-devel
BuildRequires: SFEsoqt-devel
BuildRequires: SFEcoin3d-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SFEsoqt-devel
Requires: SFEcoin3d-devel
Requires: SUNWxorg-headers
Requires: SUNWzlib
Requires: SUNWbzip
Requires: SFEsimage-devel

%prep
%setup -q -c -n %name-%version
cd OpenCASCADE%version
%patch1 -p1
(cd ros
 find . -type f | xargs ggrep -w CS | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" | while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<CS\>/_CS/g' -i ${f}
 done
 find . -type f | xargs ggrep -w SS | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<SS\>/_SS/g' -i ${f}
 done
 find . -type f | xargs ggrep -w DS | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<DS\>/_DS/g' -i ${f}
 done
 find . -type f | xargs ggrep -w ESP | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<ESP\>/_ESP/g' -i ${f}
 done
 find . -type f | xargs ggrep -w EIP | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<EIP\>/_EIP/g' -i ${f}
 done
 find . -type f | xargs ggrep -w GS | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<GS\>/_GS/g' -i ${f}
 done
 find . -type f | xargs ggrep -w FS | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<FS\>/_FS/g' -i ${f}
 done
 find . -type f | xargs ggrep -w ES | cut -f1 -d":" | uniq  | egrep -vw "Binary|config.guess" | egrep -v "\.orig$" |
 while read f
 do
   [ ! -f ${f}.orig ] && cp ${f} ${f}.orig
   /usr/gnu/bin/sed 's/\<ES\>/_ES/g' -i ${f}
 done)
cd ..

#%ifarch amd64 sparcv9
#cp -rp Coin-%version Coin-%{version}-64
#%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#%ifarch amd64 sparcv9
#cd Coin-%{version}-64

#export CFLAGS="%optflags64"
#export CXXFLAGS="%cxx_optflags64"
#export LDFLAGS="%_ldflags64"

#./configure --prefix=%{_prefix} \
#            --bindir=%{_bindir}/%{_arch64} \
#            --libdir=%{_libdir}/%{_arch64} \
#            --sysconfdir=%{_sysconfdir} \
#            --includedir=%{_includedir} \
#            --libexecdir=%{_libexecdir} \
#            --with-simage \
#            --with-mesa \
#            --enable-threadsafe \
#            --enable-html 

#gmake -j$CPUS

#cd ..
#%endif

cd OpenCASCADE%version/ros
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -fexceptions"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC"
export LDFLAGS="-L%{_libdir} -R%{_libdir} %{gnu_lib_path} -lstdc++ -lm"

[ ! -f ./configure.orig ] && cp ./configure ./configure.orig 
cat ./configure.orig | sed '{
    s/\-instances=static//
}' > ./configure

[ ! -f ./configure.orig ] && cp ./configure.in ./configure.in.orig 
cat ./configure.in.orig | sed '{
    s/\-instances=static//
}' > ./configure.in

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
            --with-tcl=%{_libdir} \
            --with-tk=%{_libdir} \
            --with-gl-include=%{_prefix}/X11/include \
            --with-gl-library=%{_prefix}/X11/lib \
            --with-xmu-include=%{_prefix}/X11/include \
            --enable-wrappers=no \
            --enable-wok=yes \
            --enable-draw=yes \
            --disable-debug --enable-production

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd Coin-%{version}-64
#
#gmake DESTDIR=$RPM_BUILD_ROOT install
#cd ..
#%endif

cd OpenCASCADE%version/ros
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:/lib:%{_libdir}:%{gnu_lib}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_prefix}/SunOS
rm -rf $RPM_BUILD_ROOT%{_prefix}/sun
mkdir -p $RPM_BUILD_ROOT%{_libdir}/opencascade
mv $RPM_BUILD_ROOT%{_prefix}/config.h $RPM_BUILD_ROOT%{_libdir}/opencascade
mv $RPM_BUILD_ROOT%{_prefix}/env_DRAW.sh $RPM_BUILD_ROOT%{_libdir}/opencascade
(cd $RPM_BUILD_ROOT%{_prefix}/bin
 ln -s ../lib/opencascade/env_DRAW.sh)
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{_prefix}/inc $RPM_BUILD_ROOT%{_includedir}/opencascade
mkdir $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/src $RPM_BUILD_ROOT%{_datadir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/opencascade
%{_libdir}/opencascade/env*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/src
%{_datadir}/src/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/opencascade
%{_includedir}/opencascade/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/opencascade
%{_libdir}/opencascade/config.h

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
#%{_libdir}/%{_arch64}/pkgconfig/*
#%endif

%changelog
* Sat Oct 10 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
