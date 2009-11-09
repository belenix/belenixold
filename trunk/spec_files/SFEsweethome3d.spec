#
# spec file for package SFEsweethome3d
#
# includes module(s): sweethome3d
#
%include Solaris.inc

%define src_name SweetHome3D
%define src_ver 2.1

Name:		SFEsweethome3d
Summary:	Sweet Home 3D is a free interior design application.
Version:	%{src_ver}
License:	GPL, MIT, Free Art
Group:		Application/Java
Source:		http://prdownloads.sourceforge.net/sweethome3d/%{src_name}-%{src_ver}-linux-x86.tgz
Source1:        SweetHome3D
Source2:        http://download.java.net/media/java3d/builds/release/1.5.2/j3d-1_5_2-solaris-x86.zip
URL:		http://www.sweethome3d.eu/index.jsp
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWj6rt
BuildRequires: SUNWj6dev

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
cd %{name}-%{version}
gunzip -c %{SOURCE} | gtar xvf -
unzip %{SOURCE2}
cd j3d-1_5_2-solaris-x86
unzip j3d-jre.zip

%build
cd %{name}-%{version}/%{src_name}-%{src_ver}
rm lib/*.so
cp ../j3d-1_5_2-solaris-x86/lib/i386/*.so lib
cp ../j3d-1_5_2-solaris-x86/lib/ext/* lib

%install
cd %{name}-%{version}/%{src_name}-%{src_ver}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{src_name}/lib
ginstall -m 0644 lib/*.jar $RPM_BUILD_ROOT%{_libdir}/%{src_name}/lib
ginstall -m 0555 lib/*.so $RPM_BUILD_ROOT%{_libdir}/%{src_name}/lib

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cat %{SOURCE1} | sed '{
    s#@prog@#%{src_name}#
    s#@progdir@#%{_libdir}/%{src_name}#
    s#@bindir@#%{_bindir}#
}' > SweetHome3D
ginstall -m 0555 SweetHome3D $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Fri Nov 06 2009 - Moinak Ghosh
- Initial version
