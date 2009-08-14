#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define python_version 2.6
Name:                SFEopencv
Summary:             Collection of algorithms for computer vision
Version:             1.0.0
License:             BSD
Source:              http://prdownloads.sourceforge.net/opencvlibrary/opencv-%{version}.tar.gz
URL:                 http://opencv.willowgarage.com/wiki/
Source1:             opencv-samples-Makefile
Patch1:              opencv-01-pythondir.diff
Patch2:              opencv-02-autotools.diff
Patch3:              opencv-03-pkgconfig.diff
Patch4:              opencv-04-gcc44.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgtk2
Requires: SFEjasper
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWTiff
Requires: SUNWPython26
Requires: SUNWzlib
BuildRequires: SUNWgtk2-devel
BuildRequires: SFEjasper-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFEswig
BuildRequires: SFEffmpeg-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWgtk2-devel
Requires: SFEjasper-devel
Requires: SUNWpng-devel
Requires: SUNWjpg-devel
Requires: SUNWTiff-devel
Requires: SUNWPython26-devel
Requires: SFEswig

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.

%prep
%setup -q -c -n %name-%version
cd opencv-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
sed -i 's/\r//' interfaces/swig/python/*.py \
                     samples/python/*.py
sed -i 's/^#!.*//' interfaces/swig/python/adaptors.py \
                        interfaces/swig/python/__init__.py
# Adjust timestamp on cvconfig.h.in
touch -r configure.in cvconfig.h.in
cd ..

%ifarch amd64 sparcv9
cp -rp opencv-%version opencv-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

OPATH=$PATH

%ifarch amd64 sparcv9
cd opencv-%{version}-64

export CFLAGS="-m64"
export CXXFLAGS="-m64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"
export PATH=%{_bindir}/%{_arch64}:${PATH}
export PYTHON=%{_bindir}/%{_arch64}/python%{python_version}

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --without-ffmpeg --with-python \
            --enable-apps --without-quicktime \
            --with-xine

gmake -j$CPUS

cd ..
%endif

cd opencv-%{version}
export CFLAGS=""
export CXXFLAGS=""
export LDFLAGS="%_ldflags"
export PATH=$OPATH
export PYTHON=%{_bindir}/python%{python_version}

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --without-ffmpeg --with-python \
            --enable-apps --without-quicktime \
            --with-xine

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd opencv-%{version}-64

gmake install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la \

mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages
mkdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/opencv/64
mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/opencv/*.so \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/opencv/64

cd ..
%endif

cd opencv-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p"
rm -f $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/build_all.sh \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/cvsample.dsp \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/cvsample.vcproj \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/facedetect.cmd \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/makefile.gcc \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/makefile.gen

mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages/opencv/* \
   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/opencv
rmdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages/opencv
rmdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages
cd ..

find $RPM_BUILD_ROOT -name "*.la" | xargs rm -f
install -pm644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/GNUmakefile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/opencv
%{_datadir}/opencv/haarcascades
%{_datadir}/opencv/readme.txt
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/opencv
%{_includedir}/opencv/*.h
%{_includedir}/opencv/*.hpp
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/opencv
%doc %{_datadir}/opencv/doc
%doc %{_datadir}/opencv/samples
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.a
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
