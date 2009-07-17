#
# spec file for package SFEsjfonts
#
#
%include Solaris.inc
%include base.inc

%define x11_dir %{_prefix}/X11
%define x11_ttf_dir %{x11_dir}/lib/X11/fonts/TTF

Name:			SFEsjfonts
License:		GPLv2 + Exception
Group:			Fonts
Version:		2.0.2
Summary:		Some Juicy Fonts
Source:			%{sf_download}/sjfonts/sjfonts.%{version}.tar.bz2

URL:			http://sjfonts.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:		%{name}.copyright

%description
Two fonts by Steve Jordi released under the GPL.

%prep
%setup -q -c -n %name-%version

%build

%install
rm -rf $RPM_BUILD_ROOT
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
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial spec.
