#!/usr/bin/perl -w

use strict;
use Data::Dumper;
#use Compress::Zlib;

my ($collections, $arch, $basedir, $verbose);
my ($opt, %collections_ro);

sub relative_path;


$verbose = 0;

while ( $opt = shift @ARGV ) {
	if ( $opt eq "-v" ) {
		$verbose = 1;
	}
}

# Base dir for OpenSolaris packages
$basedir = "/tanku/belipsds/belenix_0.7.1";

# Different repos
$collections = {
				'unstable'	=>	[ 'unstable' ],
				};

# Welche Architektur interessiert uns?
$arch = "i386";

# Welche Sourcen sind read-only, weil gesynct?
%collections_ro = (
		'unstable'	=>	0,
		);

foreach (keys %{$collections}) {
	mix_sources ($basedir, $arch, "collection/$_", @{$collections->{$_}});
}

print "Done!\n" if $verbose;

exit 0;

#########################################################

sub mix_sources {
	my $basedir = shift;
	my $arch = shift;
	my $targetdir = shift;
	my @sourcedirs = @_;

	my ($version);

	my ($srcdir, $srcdirh, $youngest, $age, $dir_age);
	my ($cath, $cat, @fields);
	
	my ($dsth, $dsch, $desc);

	my $destdir = "$basedir/$targetdir/$arch";

	print "Building $targetdir from " . (join ", ", @sourcedirs) . "\n";

	foreach $srcdir (@sourcedirs) {
		opendir ($srcdirh, "$basedir/$srcdir/$arch") or die "Can't open $basedir/$srcdir/$arch: $!";
		while ($version = readdir ($srcdirh)) {
			next if $version eq ".";
			next if $version eq "..";		
			next unless $version =~ /^\d+\.\d+$/;

			print "Examining $srcdir $version...\n" if $verbose;

			# Gibts die Solaris-Version schon in unserer Collection?
			unless ( -d "$destdir/$version" ) {
				mkdir "$destdir/$version";
				print "New version $version\n";
			}

			# Neue Pakete verlinken

			print "  Searching for new packages for $version\n" if $verbose;
			$youngest = link_new_packages ("$basedir/$srcdir/$arch/$version", "$basedir/$targetdir/$arch/$version");
			#$youngest = 360;
			
			# Auch nach dem Alter des Verzeichnisses schauen
			$dir_age = -M "$basedir/$srcdir/$arch/$version";
			
			if ( $dir_age < $youngest ) {
				$youngest = $dir_age;
			}
			

			# Alter von catalog und description file ueberpruefen

			unless ( $collections_ro{$srcdir} ) {
				if ( ! -f "$basedir/$srcdir/$arch/$version/catalog" or $youngest < -M "$basedir/$srcdir/$arch/$version/catalog" ) {
					print "  Generating catalog for $srcdir $version\n" if $verbose;
					generate_catalog ("$basedir/$srcdir/$arch/$version");
				}
			}

			print "  Reading catalog for $version\n" if $verbose;

			# Catalog und Description files einlesen
			open ($cath, "$basedir/$srcdir/$arch/$version/catalog") or die "Can't open $basedir/$srcdir/$arch/$version/catalog: $!";
			while (<$cath>) {
				next if /^-----/;
				next if /^[a-z0-9]: /;
				next if /^$/;
				next if /^#/;

				# Zeilen einlesen
				@fields = split;
				if ( @fields == 5 ) {
					$cat->{$version}->{$fields[0]} = $_;
				}
			}
			close ($cath);

			open ($dsch, "$basedir/$srcdir/$arch/$version/descriptions") or die "Can't open $basedir/$srcdir/$arch/$version/descriptions: $!";
			while (<$dsch>) {
				if ( /(.+) - / ) {
					$desc->{$version}->{$1} = $_;
				}
			}
			close ($dsch);
		}
	}



	# Catalog und Description files in collection erzeugen

	opendir ($dsth, $destdir) or die "Can't open $destdir: $!";
	while ($version = readdir ($dsth)) {
		next if $version eq ".";
		next if $version eq "..";
		
		print "  Searching for non-existing packages for $version\n" if $verbose;
		remove_dangling_symlinks ("$destdir/$version");
		
		print "Generating catalog for $version...\n" if $verbose;

		open ($cath, "> $destdir/$version/catalog") or die "Can't write $destdir/$version/catalog: $!";
		foreach (sort keys %{$cat->{$version}}) {
			print $cath $cat->{$version}->{$_};
		}
		close ($cath);

		print "Generating descriptions for $version...\n" if $verbose;

		open ($dsch, "> $destdir/$version/descriptions") or die "Can't write $destdir/$version/descriptions: $!";
		foreach (sort keys %{$desc->{$version}}) {
			print $dsch $desc->{$version}{$_};
		}
		close ($dsch);
	}
	closedir ($dsth);
}

sub generate_catalog {
	my $dir = shift;

	my ($file, $gz, $md5sum, $line, $pkg, $version, $summary, $name, $tfile);

	open (NEWCAT, "> $dir/catalog") or die "Can't write $dir/catalog: $!";
	open (NEWDESC, "> $dir/descriptions") or die "Can't write $dir/descriptions: $!";


	opendir (CDIR, $dir) or die "Can't open $dir: $!";
	while ($file = readdir CDIR) {
		next unless $file =~ /\.pkg/;

		print "      Reading $file...\n" if $verbose;

		chomp ($md5sum = `md5sum $dir/$file | cut -d' ' -f1`);

		$tfile = "/var/tmp/$file";
		system ("/usr/bin/7za e -so $dir/$file > $tfile");
		#$gz = gzopen("$dir/$file", 'rb') or die "Can't open $dir/$file: $!";
		open($gz, "<$tfile");
		$line = <$gz>;

		# package header
		#$gz->gzreadline($line);
		die "No package!\n" unless $line =~ /^# PaCkAgE DaTaStReAm/;

		# package name
		#$gz->gzreadline($line);
		$line = <$gz>;
		($pkg) = $line =~ m/^(\S+)/;

		$name = $version = $summary = "";

		# other fields
		while (<$gz>) {
			if ( /^VERSION=(.*)/ and not $version ) {
				$version = $1;
				next;
			} elsif ( /^NAME=(.*?) - (.*)/ and not $name ) {
				$name = $1;
				$summary = $2;
				next;
			} elsif ( /^NAME=(.*)/ and not $name ) {
				$name = $1;
			} elsif ( /^DESC=(.*)/ and not $summary ) {
				$summary = $1;
			}

			if ( $version and $summary and $name ) {
				last;
			}
		}
		#$gz->gzclose();
		close($gz);
		unlink($gz);

		## Hack fuer doofe Sun-Paket-Namen. Die enthalten Leerzeichen, deswegen nehmen wir dort
		## den einfachen Paketnamen

		#if ( $dir =~ m{/sun/sparc/} or $pkg =~ /^SUNW/ ) {
		#	print "        Resetting name from $name to $pkg\n" if $verbose;
		#	$name = $pkg;
		#}

		##
		## Use package name for NAME if NAME has multiple words
		##
		#my(@c) = split / /, $name;
		#if (@c > 1) {
			#$name = $pkg;
		#}
		$name = $pkg;

		print NEWCAT "$name $version $pkg $file $md5sum\n";
		print NEWDESC "$name - $summary\n";
	}
	closedir (CDIR);

	close (NEWCAT);
	close (NEWDESC);
}


sub link_new_packages {
	my $srcdir = shift;
	my $targetdir = shift;

	my ($file, $youngest, $age);

	my ($srch);

	undef $youngest;

	# Nach neuen Paketen suchen
	opendir ($srch, $srcdir) or die "Can't open $srcdir: $!";
	while ($file = readdir ($srch)) {
		next if $file eq ".";
		next if $file eq "..";

		# Nur Pakete
		next unless $file =~ /\.pkg/;

		$age = -M "$srcdir/$file";
		if ( ! defined $youngest or $age < $youngest) {
			$youngest = $age;
		}

		unless ( -l "$targetdir/$file") {
			print "New package in $targetdir: $file\n";
			symlink relative_path ($targetdir, $srcdir) . $file, "$targetdir/$file";
		}
	}
	closedir ($srch);

	return $youngest;
}

sub relative_path {
	my $from = shift;
	my $to = shift;
	
	my ($dots, $rel);
	my (@f, @t, $i);
	
	@f = split /\//, $from;
	@t = split /\//, $to;
	
	$i = 0;
	while ( $i < @f and $i < @t and ($f[$i] eq $t[$i]) ) {
		$i++;
	}
	
	# Ab $i sind die Pfade unterschiedlich
	
	$dots = "../" x (@f - $i);

	$rel = "";
	while ( $i < @t ) {
		$rel .= $t[$i] . "/";
		$i++;
	}
	
	return $dots . $rel;
}

sub remove_dangling_symlinks {
	my $dir = shift;
	
	my ($dirh, $file);
	
	# Nach geloeschten Paketen suchen
	opendir ($dirh, $dir) or die "Can't open $dir: $!";
	while ($file = readdir ($dirh)) {
		next if $file eq ".";
		next if $file eq "..";

		if ( -l "$dir/$file" && ! -e "$dir/$file" ) {
			print "    Deleting dangling symbolic link to package: $file\n";
			unlink "$dir/$file";
		}
	}
	closedir ($dirh);
}

