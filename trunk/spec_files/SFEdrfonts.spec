#
# spec file for package SFEdrfonts
#
#
%include Solaris.inc
%include base.inc

%define x11_dir %{_prefix}/X11
%define x11_ttf_dir %{x11_dir}/lib/X11/fonts/TTF

Name:			SFEdrfonts
License:		Public Domain/GPLv2
Group:			Fonts
Version:		1.0
Summary:		Dustismo Roman Fonts
Source:			http://img.dafont.com/dl/?f=dustismo_roman

URL:			http://www.dafont.com/dustismo-roman.font
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:		%{name}.copyright

%description
4 GPL Fonts from Dafont.COM.

%prep
rm -rf %name-%version
mkdir %name-%version
cd %name-%version
cp %{SOURCE} dustismo_roman.zip
unzip dustismo_roman.zip

%build

%install
rm -rf $RPM_BUILD_ROOT
cd %name-%version
mkdir -p $RPM_BUILD_ROOT%{x11_ttf_dir}
cp *.ttf $RPM_BUILD_ROOT%{x11_ttf_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{x11_dir}/bin/mkfontdir %{x11_ttf_dir}
%{x11_dir}/bin/mkfontscale %{x11_ttf_dir}

%postun
%{x11_dir}/bin/mkfontdir %{x11_ttf_dir}
%{x11_dir}/bin/mkfontscale %{x11_ttf_dir}

%files
%defattr (-, root, bin)
%{x11_ttf_dir}/*.ttf

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
