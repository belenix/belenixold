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
# ident "%Z%%M% %I%	%E% SMI"
#

my $slist = $ARGV[0];

open(LST, "<$slist") || die "Cannot open slist";

my %hash = ();
my %hash1 = ();
my @lst = ();
my $count = 2000000;
#my $count = 1993235;
#my $count = 2400000;
my $diff = 5;
my $ucount = 0;

while (my $line=<LST>) {

	chomp($line);
	my @entry = split(/ /, $line);
	my $upd = 0;

	if (exists($hash{"$entry[1]"})) {
		my $pos = $hash{"$entry[1]"};
		my @lentry = split(/ /, $lst[$pos]);
		if ($ucount - $lentry[1] <= $diff) {
			$lentry[0]++;
			my $lstent = "$lentry[0] $lentry[1] $lentry[2] $lentry[3]";
#print "Updating $lstent\n";
			$lst[$pos] = $lstent;
			$upd = 1;
		}
	}
	if ($upd == 0) {
		my $lstent = "1 $ucount $line";
#print "$lstent\n";
		$#lst++;
		$lst[$#lst] = $lstent;
		$hash{"$entry[1]"} = $#lst;
		$ucount++;
	}
}
close(LST);

foreach $lstent (@lst) {
	my @lentry = split(/ /, $lstent);
#print "$lstent\n";

	if (exists($hash1{"$lentry[3]"})) {
		my $hentry = $hash1{"$lentry[3]"};
#print "Got $lentry[3],$lentry[0]: $hentry->[3],$hentry->[0]\n";
		if ($lentry[0] > $hentry->[0]) {
#print "$hentry->[3] $hentry->[0] swapping to $lentry[3] $lentry[0]\n";
			$hentry->[0] = $lentry[0];
			$hentry->[1] = $lentry[1];
			$hentry->[2] = $lentry[2];
			$hentry->[3] = $lentry[3];
			$hash1{"$lentry[3]"} = $hentry;

		} elsif ($lentry[0] == $hentry->[0]) {
			if ($lentry[2] > $hentry->[2]) {
				$hentry->[0] = $lentry[0];
				$hentry->[1] = $lentry[1];
				$hentry->[2] = $lentry[2];
				$hentry->[3] = $lentry[3];
				$hash1{"$lentry[3]"} = $hentry;
			}
		}
	} else {
#print "Assigning hash1{$lentry[3]} = \@lentry\n";
		$hash1{"$lentry[3]"} = \@lentry;
	}
}

if (open(PRE, "<$LIVEKIT/iso.sort.pre")) {
	while ($line=<PRE>) {
		print $line;
	}
	close(PRE);
}

my @vals = (values(%hash1));
@vals = sort({$a->[1] <=> $b->[1]} @vals);
foreach my $ventry (@vals) {
	print "$ventry->[3]\t$count\n";
	$count--;
}

print "usr\t$count\n";
