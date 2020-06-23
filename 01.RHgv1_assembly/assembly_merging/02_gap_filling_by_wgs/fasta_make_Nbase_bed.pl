#!/usr/bin/perl

$die = "

ARGV0 = input scaffolds fasta

STDOUT = bed file of N-base regions

";

if (!defined $ARGV[0]) {die $die}

open IN, "$ARGV[0]";
$chr = <IN>;
chomp $chr;
$chr =~ s/\s.*$//;
$chr =~ s/^>//;
$pos = 0;
$Nrun = 0;
while ($l = <IN>) {
	chomp $l;
	if ($l =~ /^>/) {
		if ($Nrun>0.5) {
			print "$chr\t$Nstart\t$pos\n";
		}
		$chr = $l;
		$chr =~ s/\s.*$//;
		$chr =~ s/^>//;
		$pos = 0;
		$Nrun = 0;
	} else {
		@S = split(//, $l);
		for ($i = 0; $i < @S; $i++) {
			$pos++;
			if ($S[$i] =~ /N/i) {
				if ($Nrun<0.5) {
					$Nstart = $pos;
					$Nrun = 1;
				}
			} else {
				if ($Nrun>0.5) {
					print "$chr\t$Nstart\t".($pos-1)."\n";
					$Nrun = 0;
				}
			}
		}
	}
} close IN;