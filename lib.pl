#!/usr/bin/perl -TW
# note last line is required!

# available subroutines:
#  byNumber
#  max
#  maxarray
#  min
#  minarray
#  TimeIt

######################################################################

sub printARGV {
    local(*ARGV,*patterns,*flags) = @_;
    print("files    = " . join(" ",@ARGV) . "\n");
    print("patterns = " . join(" ",@patterns) . "\n");
    print("flags    = " );
    if (defined ($flags)) {print $flags;}
    print ("\n");          
}


sub parseARGV {
    local(*ARGV,*patterns,*flags) = @_;
    local($i,@files);
    foreach $i (@ARGV) {
	if (-e $i) { # a file
	    @files = (@files, $i);
	    next;  # advance to next argument
	} else {
	    if   ($i =~ /^(\-.*)$/) {$flags .= $1;} #add to flag var
	    else {@patterns = (@patterns, $i);} # add to pattern list
	}
    }
    @files;
}


sub FindDatafiles {
    local($datapath) = @_;
    open(FILE, "ls $datapath |");
    while (<FILE>) {
        s/\n//g;   #replace \n w/ nothing
        @filelist = (@filelist, $_);
    }
    @filelist; 
}


sub sleepf {
    local ($time)=@_;
    select(undef, undef, undef, $time);
    1;
}



######################################################################

# no arguments, returns a list
sub ReadInputParagraphs {
    local($questions,$thetest);
    $/ = "xxxxXXXXxxxx";   # enable whole file mode (no reg. exp.)
#    $* = 1;  # enable multi-line patterns              # removed 3/20/06
    $thetest = <>;
#    $thetest =~ s/(\S)\s*\n\s*\n\s*(\S)/$1\n\n$2/g;
#    $thetest =~ s/(\S\s*)\n+\s+\n+(\s*\S)/$1\n\n$2/g;  # original version
    $thetest =~ s/(\S)\s*\n+\s*\n+\s*(\S)/$1\n\n$2/gm;  # new 9/8/98 
#    print $thetest;                                    # m 3/11/06
    @questions = split(/\n\n/,$thetest);
#    &PrettyPrintParagraphs(60,@questions);
    @questions;
}

sub PrettyPrintParagraphs {
    local($linesperpage, @questions) = @_;
    local($i,$cnt,$page,$numlines) =("",0,"",0);
    foreach $i (@questions) {
	$i .= "\n\n";
	$numlines = $i =~s/\n/\n/g;  #counts the number of blank lines
	$cnt += $numlines;
	if ($cnt <= $linesperpage) {
	    $page .= $i;
	} else {
	    $page .= "\n" x ($linesperpage - ($cnt - $numlines));
	    print $page;  
	    $page=$i;
	    $cnt=$numlines;
	}
    }
    print $page;
}


sub PrintParagraphs {
    local($linesperpage, @questions) = @_;
    local($i,$cnt,$page,$numlines) =("",0,"",0);
    foreach $i (@questions) {
	print $i;
        print "\n\n";
    }
}

######################################################################
####################### ways to sort data #############################

sub byNumber {$a <=> $b;}

sub bylastnumber {
    local($tmp1,$tmp2,@words);
    @words = split(/\s+/,$a);
    $tmp1 = $words[$#words];
    @words = split(/\s+/,$b);
    $tmp2 = $words[$#words];
    $tmp1 <=> $tmp2;
}

sub byAnumber {
    local($tmp1,$tmp2,@words);
    @words = split(/\s+/,$a);
    $tmp1 = $words[$thesortnumber];
    @words = split(/\s+/,$b);
    $tmp2 = $words[$thesortnumber];
    $tmp1 <=> $tmp2;
}

sub byAnumber2 {
    local($tmp1,$tmp2,@words);
    @words = split(/\|/,$a);
    $tmp1 = $words[$thesortnumber];
    @words = split(/\|/,$b);
    $tmp2 = $words[$thesortnumber];
    $tmp1 <=> $tmp2;
}

sub byfirstnumber {
    local($tmp1,$tmp2,@words);
    @words = split(/\s+/,$a);
    $tmp1 = $words[0];
    @words = split(/\s+/,$b);
    $tmp2 = $words[0];
    $tmp1 <=> $tmp2;
}

sub bylastword {
    local($tmp1,$tmp2);
    $a =~ /\s+(\S+)\s*\n/;
    $tmp1=$1;
    $b =~ /\s+(\S+)\s*\n/;
    $tmp2=$1;
    $tmp1 cmp $tmp2;
}


sub bysecondword {
    local($tmp1,$tmp2);
    $a =~ /^\s*\S+\s*(.*)/;
    $tmp1=$1;
    $b =~ /^\s*\S+\s*(.*)/;
    $tmp2=$1;
    $tmp1 cmp $tmp2;
}

######################################################################

sub max {
    local($a,$b) = @_;
    ($a > $b) ? $a : $b;
}

sub maxarray {
    local(@array)=@_;
    local($i,$max);
    $max=$array[0];
    foreach $i (@array) {
	if ($i > $max) {$max = $i};
    }
    $max;
}

sub minarray {
    local(@array)=@_;
    local($i,$min);
    $min=$array[0];
    foreach $i (@array) {
	if ($i < $min) {$min = $i};
    }
    $min;
}

sub min {
    local($a,$b) = @_;
    ($a < $b) ? $a : $b;
}

######################################################################


# pass TimeIt a subroutine name and it will time the execution of 
# the subroutine
sub TimeIt {
  local($subroutine) =@_;
  local($start,$end);
  $start=(times)[0];    
  eval($subroutine);
  $end=(times)[0];
  printf "that took %.2f CPU seconds\n", $end-$start;
}


1; #return true


######################################################################
