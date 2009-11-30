#
# spec file for package SFEfreeimage.spec
#
# includes module(s): freeimage
#
%include Solaris.inc

%define src_name	FreeImage
%define _version        3100
%define major           3 

Name:                   SFEfreeimage
Summary:                Multi-format image decoder library
Version:                3.10.0
%define maj_ver         3
Group:                  System Environment/Libraries
License:                GPL+ or MPLv1.0
Source:                 %{sf_download}/freeimage/%{src_name}%{_version}.zip
URL:                    http://freeimage.sourceforge.net/
Patch1:			freeimage-01-makefile.diff
Patch3:                 freeimage-03-doxygen.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
FreeImage is a library for developers who would like to support popular
graphics image formats like PNG, BMP, JPEG, TIFF and others as needed by
today's multimedia applications.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}
%patch1 -p1
%patch3 -p1

%build
export CXXFLAGS="%cxx_optflags -Wno-ctor-dtor-privacy"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"
gmake LDFLAGS="${LDFLAGS}" -f Makefile.solaris

# Build libfreeimageplus DIY, as the provided makefile makes libfreeimageplus
# contain a private copy of libfreeimage <sigh>
FIP_OBJS=
for i in Wrapper/FreeImagePlus/src/fip*.cpp; do
	gcc -o $i.o $RPM_OPT_FLAGS -fPIC -fvisibility=hidden \
	    -ISource -IWrapper/FreeImagePlus -c $i
	    FIP_OBJS="$FIP_OBJS $i.o"
done
gcc -shared -LDist -o Dist/libfreeimageplus-%{version}.so \
    -Wl,-h,libfreeimageplus.so.%{major} $FIP_OBJS -lfreeimage-%{version} %{gnu_lib_path}
 	
pushd Wrapper/FreeImagePlus/doc
doxygen FreeImagePlus.dox
popd

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.solaris install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.la" | xargs rm -f

ginstall -m 755 Dist/libfreeimage-%{version}.so $RPM_BUILD_ROOT%{_libdir}
ginstall -m 755 Dist/libfreeimageplus-%{version}.so $RPM_BUILD_ROOT%{_libdir}
ln -s libfreeimageplus-%{version}.so \
    $RPM_BUILD_ROOT%{_libdir}/libfreeimageplus.so.%{major}
ln -s libfreeimageplus-%{version}.so $RPM_BUILD_ROOT%{_libdir}/libfreeimageplus.so
 	
ginstall -p -m 644 Source/FreeImage.h $RPM_BUILD_ROOT%{_includedir}
ginstall -p -m 644 Wrapper/FreeImagePlus/FreeImagePlus.h \
    $RPM_BUILD_ROOT%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
