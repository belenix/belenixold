#
# spec file for package SFEsip
#
# includes module(s): sip
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEsip
Summary:		Python binding creator for C++ libraries
License:		Pythonish
Version:		4.7.9
Source:			http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/software/sip/intro
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
%include default-depend.inc
BuildRequires: SUNWPython-devel

%prep
%setup -q -n sip-%{version}

%build
export PYTHON="/usr/bin/python2.4"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
python configure.py 

# Use g++ in Makefiles
for mk in Makefile sipgen/Makefile siplib/Makefile
do
	[ ! -f ${mk}.orig ] && cp ${mk} ${mk}.orig
	cat ${mk} | sed '{s/CXX = CC/CXX = g++/g
s/LINK = CC/LINK = g++/g
s/LFLAGS = -G -znoversion -M sip.exp/LFLAGS = -G -Wl,-znoversion -Wl,-M -Wl,sip.exp/g
s/CXXFLAGS = -KPIC -O2 -w/CXXFLAGS = -fpic -O2 -w/g
}' > ${mk}.new
	cp ${mk}.new ${mk}
done
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sip
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/python2.4/sip.h
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Sun Mar 22 2009 - moinakg@belenix.org
- Import from SFE gate.
- Bump version, fix URL.
* Sat Mar 29 2008 - laca@sun.com
- create
