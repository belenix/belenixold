%define tcl_v %(echo 'puts $tcl_version' | tclsh)
%define tcl_vers tcl%{tcl_v}

BuildArch: noarch
Summary: Tcl package helper for Graphviz
Name: graphviz-tclpkg
Version: 1
Release: 1%{?dist}
Group: Applications/Multimedia
License: CPL

%description
Custom Graphviz Tcl pkgIndex to load appropriate 64-bit or 32-bit
Tcl package based on interpreter bit-ness.

%prep

%build

%install
cd ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir32}/%{tcl_vers}/graphviz
cat > ${RPM_BUILD_ROOT}%{_libdir32}/%{tcl_vers}/graphviz/pkgIndex.tcl << EOT
#
# Load appropriate graphviz package based on interpreter bit-ness
# This assumes graphviz libdir is /usr/lib[/amd64]/graphviz and Tcl libdir is
# /usr/lib/tcl<version>/
#
global tcl_platform __d_name

if {\$tcl_platform(wordSize) == 8} {
        set __d_name [file join [file dirname [info script]] ../../amd64/graphviz/tcl]
} else {
        set __d_name [file join [file dirname [info script]] ../../graphviz/tcl]
}

package ifneeded Tcldot 2.26.3 "
        load [file join \$__d_name libtcldot.so.0] Tcldot"
package ifneeded Tclpathplan 2.26.3 "
        load [file join \$__d_name libtclplan.so.0] Tclpathplan"
package ifneeded Gdtclft 2.26.3 "
        load [file join \$__d_name libgdtclft.so.0] Gdtclft"
package ifneeded gv 0 "
        load [file join \$__d_name libgv_tcl.so] gv"
package ifneeded Tkspline 2.26.3 "
        package require Tk 8.3
        load [file join \$__d_name libtkspline.so.0] Tkspline"
# end
EOT

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir32}/%{tcl_vers}/graphviz
%{_libdir32}/%{tcl_vers}/graphviz/pkgIndex.tcl

