#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"%Z%%M%	%I%	%E% SMI"
#
my $cluster = $ARGV[0];
my $wos = $ARGV[1];
my $toc = $ARGV[2];
my (@lines);
my ($product_prefix) = "$wos";

#print "Processing $cluster from $wos\n";
#print "Cluster TOC: $toc \n";

open(TOC, "<$toc") || die "Unable to open $toc";

while (my $line=<TOC>) {
	chomp($line);
	$lines[++$#lines] = $line;
}
close(TOC);

#print "Loaded TOC\n";

sub scan_depends($) {
	my ($name1) = shift(@_);
	my ($dcount) = 0;

	if ( -e "$product_prefix/$name1/install/depend" ) {
		open(DEP, "<$product_prefix/$name1/install/depend") || die "Unable to open $product_prefix/$name1/install/depend";
		while ( my $dep=<DEP> ) {
			chomp($dep);

			if ($dep =~ /^P/) {
				my ($d, $pkg) = split(/\s+/, $dep);
				$pkg =~ s/\s+//g;
				print "$name1 $pkg\n";
				$dcount++;

			} elsif ($dep =~ /^R/) {
				my ($d, $pkg) = split(/\s+/, $dep);
				$pkg =~ s/\s+//g;
				print "$pkg $name1\n";
				$dcount++;
			}
		}
		close (DEP);
		if ($dcount == 0) {
			print "$name1 SUNWdummy\n";
		}
	} else {
		print "$name1 SUNWdummy\n";
	}
}

sub scan_toc($) {
	my ($name) = @_;
	my ($state) = 1;
	my ($tag, $value);

	for $line (@lines) {
		if ($state == 1) {
			# Searching for given cluster/metacluster name
			if ($line =~ /=$name$/) {
				($tag, $value) = split(/=/, $line);
				if ($tag eq "CLUSTER" || $tag eq "METACLUSTER") {
					$state = 2;

				} elsif ($tag eq "SUNW_CSRMEMBER") {
					# Found a leaf package.
					# Print it along with partial dependencies.
					scan_depends($value);
					return;

				} else {
					die "Invalid entry $line";	
				}
			}
		} elsif ($state == 2) {
			# Scanning for SUNW_CSRMEMBER entries in current cluster/metacluster
			if ($line =~ /^END/) {
				return;

			} elsif ($line =~ /SUNW_CSRMEMBER=/) {
				($tag, $value) = split(/=/,$line);
				scan_toc($value);
			}
		}
	}
}

#print "Dumping TOC\n";
scan_toc($cluster);

