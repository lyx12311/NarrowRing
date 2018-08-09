#!/usr/bin/perl -W
# The first line defines the Perl Interpreter
# Written  by DPH


&main();

sub main {
    #printf ("#ARGV= $#ARGV\n");
    # print "1st argument [$ARGV[0]]\n";
    if ($#ARGV < 0) {&printUSAGE();} # needs one arguments
    @inputlines = &readinputfile($ARGV[0]);
#    &printlines(@inputlines);
    @lines = &removecomments(@inputlines);
#    &printlines(@lines);    
    &initialize();
    &parseinput(@lines);
    &errorcheck();
    &loadvariables();
#    &printvalues();
    &writeheader();
    @nuArray = (0.0);    # unused zero 
    @uArray = (0.0);    
    @cwArray = (0.0);
    @eArray = (0.0);
    @WArray = (0.0);
    @iArray = (0.0);
    &Modes(*radialMode,*radialAmp,*radialPhase,*nuArray,*cwArray,*eArray); # set (e,cw,nu)
    &Modes(*verticalMode,*verticalAmp,*verticalPhase,*uArray,*WArray,*iArray); # set (i,W)
    &printfile();   
}




sub loadvariables {
    local ($Phase);
    $pi = 3.14159265358979;
    $twopi = 2.0*$pi;
    $r2d = 180.0/$pi;
    $d2r = $pi/180.0;
    $M=  $values[1];
    $Ns= $values[2];
    $N=  $values[3];    
    $aInner=  $values[4];
    $da= $values[5];
    @radialMode    = split(/ /,$values[6]);    
    @radialAmp     = split(/ /,$values[7]);    
    @radialPhase   = split(/ /,$values[8]);    
    @verticalMode  = split(/ /,$values[9]);    
    @verticalAmp   = split(/ /,$values[10]);    
    @verticalPhase = split(/ /,$values[11]);
    foreach $Phase (@radialPhase)   {$Phase *= $d2r;}  # Phases in radians
    foreach $Phase (@verticalPhase) {$Phase *= $d2r;}    
#    print "radialPhase = @radialPhase\n";    
}

sub Modes {
    local(*radialMode,*radialAmp,*radialPhase,*nuArray,*cwArray,*eArray) = @_;
    local($i,$j,$k,$kk,$arg);   # $k and $kk reserved to count modes
    local($nu,$cw,$a2e2,$e);
    
    
    for ($i=1;$i<=$Ns;$i++) {  # loop over all streamlines
	$a = $aInner +($i-1)*$da;	
	for ($j=1;$j<=$N;$j++) {   #loop over all particles
	    $Lon = $j * $twopi/$N;    
	    $num=0.0;               # get (w,nu) 
	    $den=0.0;
	    for ($k=0;$k<=$#radialMode;$k++) {
		$num += $radialAmp[$k]*sin($radialMode[$k]*$Lon + $radialPhase[$k]);
		$den += $radialAmp[$k]*cos($radialMode[$k]*$Lon + $radialPhase[$k]);
	    }
	    $nu = atan2($num,$den);
#    if (cos($nu)/$den < 0) {$nu +=$pi;}     # quadrants
#    if ($Lon>$pi) {$nu +=$pi;}     # quadrants
	    $cw = $Lon-$nu;
	    while ($nu >  $pi) {$nu-=$twopi;}    # center nu
	    while ($nu < -$pi) {$nu+=$twopi;}
	    push (@nuArray, $nu);
	    while ($cw  >  $pi) {$cw-=$twopi;}     # center w
	    while ($cw  < -$pi) {$cw+=$twopi;}
	    push (@cwArray, $cw);	    
	    $a2e2=0.0;
	    for ($k=0;$k<=$#radialMode;$k++) {
		for ($kk=0;$kk<=$#radialMode;$kk++) {    # get (e)
		    $arg = ($radialMode[$k]*$Lon  + $radialPhase[$k]);
		    $arg-= ($radialMode[$kk]*$Lon + $radialPhase[$kk]);
		    $a2e2 += $radialAmp[$k]*$radialAmp[$kk]*cos($arg);
		#	    print ("a2e2= $a2e2\n");
		}
	    }
	    $e=sqrt($a2e2)/$a;
	    push (@eArray, $e);	    	    
	}
    }
#    print "eArray = @eArray\n";
}

sub printfile  {
    local($i,$j,$linenum);

    $Mp = $M/($N*$Ns);  # Particle Mass 
    for ($i=1;$i<=$Ns;$i++) {  # loop over all streamlines
	$a = $aInner + ($i-1)*$da;
	for ($j=1;$j<=$N;$j++) {  # loop over particles on streamline
	    $linenum = ($i-1)*$N+$j; 
	    printf("%11.6le ",$Mp);	
	    printf("%11.6lf %9.6lf ",$a,$eArray[$linenum]);
	    printf("%6.2lf % 7.2lf ",$iArray[$linenum]*$r2d,$WArray[$linenum]*$r2d);	
	    printf("% 7.2lf % 7.2lf ",$cwArray[$linenum]*$r2d,$nuArray[$linenum]*$r2d);
	    printf("  # ($i,$j); Particle $linenum \n");
	}
    }
}

sub writeheader {
    my($k,$Amag,$Nmodes); # $k reserved to count modes

    $Amag = 0;
    for ($k=0;$k<=$#radialMode;$k++) {
	$Amag += $radialAmp[$k];
    }
    printf("# Created with command:  $0 $ARGV[0]\n");
    if ($#radialMode>0) {
	$Nmodes = $#radialMode +1;
	printf("# Mixture of $Nmodes radial modes:   (");
    } else {
	printf("# Pure radial mode:   j(");	
    }
    for ($k=0;$k<=$#radialMode;$k++) {
	printf("%5.2lf%% M=$radialMode[$k]",100*$radialAmp[$k]/$Amag);
	if ($k!=$#radialMode) {print ", ";}
    }
    print(")\n");

    $Amag = 0;
    for ($k=0;$k<=$#verticalMode;$k++) {
	$Amag += $verticalAmp[$k];
    }
    if ($#verticalMode>0) {
	$Nmodes = $#verticalMode +1;	
	printf("# Mixture of $Nmodes vertical modes: (");
    } else {
	printf("# Pure vertical mode: (");	
    }
    for ($k=0;$k<=$#verticalMode;$k++) {
	printf("%5.2lf%% M=$verticalMode[$k]",100*$verticalAmp[$k]/$Amag);
	if ($k!=$#verticalMode) {print ", ";}
    }
    print(")\n");
    
    printf("# Elements are in the following order:\n");
    printf("# Mass          Semi       Ecc       Inc ");
    printf("AscNode LongPeri MeanAnom\n");
}


sub readinputfile {
    local ($infile)=@_;

    open(FILE,"< $infile");
    $filelinenum=0;
    while(<FILE>) {
	$inputlines[++$filelinenum]=$_;
    }
    close(FILE);
    @inputlines;
}

sub removecomments {
    local (@inputlines)=@_;
    for ($i=1;$i<=$#inputlines;$i++) {
	$inputlines[$i] =~ s/^([^\#]*)\#.*$/$1/;  # remove comment characters
	$inputlines[$i] =~ s/^\s*(\S.*\S)\s*$/$1/;  # remove excess leading&trailing white space
	$inputlines[$i] =~ s/^\s+$//;  # remove excess white space on blank lines
	$inputlines[$i] =~ s/(\S)\s\s+(\S)/$1 $2/g;  # remove excess white space ...
	$inputlines[$i] =~ s/(\S)\s\s+(\S)/$1 $2/g;  # between words
	$inputlines[$i] =~ s/(\S)\s+=\s+(\S)/$1=$2/g;  # between words	
	$inputlines[$i] .= "\n";
    }
    @inputlines;
}


sub printlines {
    local (@lines)=@_;
    local($j);
    for ($j=1;$j<=$#lines;$j++) {
	print $lines[$j];
    }
    print "\n";
}

sub parseinput {
    local (@lines)=@_;
    local($j,$keyword,$value,@words);
    for ($j=1;$j<=$#lines;$j++) {
	if ($lines[$j] =~ /^\n$/) {next;}  # skip blank lines
	@words = split(/=/,$lines[$j]);
#	print $#words;
	if ($#words > 1) {streamerror($j,"extraneous equal sign(s)");}
	if ($#words < 1) {streamerror($j,"missing equal sign");}	
#	print "words[0] = [$words[0]]\n";
	$keyword = $words[0];
	$words[1] =~ s/^(.*)\n$/$1/;	# clip trailing \n
	$value = $1;
	&parseline($j,$keyword,$value);
    }
}

sub parseline {
    local ($j,$keyword,$value)=@_;
    local($i,$match);
    $i=0;
    $match=0;
    for ($i=1;$i<=$#validkeywords;$i++) {	    
	if    ($keyword eq $validkeywords[$i]) {$values[$i] = $value;$match++;}
    }
    if ($match==0) {
	&streamerror($j,"keyword [$keyword] not recognized");}
    if ($match > 1) {
	&streamerror($j,"keyword [$keyword] duplicated!");}    
}


sub errorcheck {
    &errorcheckkeywords();
    &errorcheckvalues();    	
    
}

sub errorcheckvalues {
    local($i,$k);  # $k reserved to count modes

    if ($values[1] <= 0) {
	&streamerror(0,"Keyword [$validkeywords[1]] must be non-negative");}
    for ($i=2;$i<=5;$i++) {
	if ($values[$i] <= 0) {
	    &streamerror(0,"Keyword [$validkeywords[$i]] must be positive");}
    }
    @radialMode    = split(/ /,$values[6]);    
    @radialAmp     = split(/ /,$values[7]);    
    @radialPhase   = split(/ /,$values[8]);
    if ($#radialMode != $#radialAmp || $#radialMode != $#radialPhase) {
	&streamerror(0,"Radiall Mode keywords must have equal number of values");}
    for ($k=0;$k<=$#radialMode;$k++) {
	if ($radialMode[$k] != int($radialMode[$k])) {
	    &streamerror(0,"radialMode keyword must have integer arguments");}
    }
    for ($k=0;$k<=$#radialAmp;$k++) {
	if ($radialAmp[$k]<0 || $radialAmp[$k]>1) {
	    &streamerror(0,"radialAmp keyword must be between zero and one");}
    }
    for ($k=0;$k<=$#radialPhase;$k++) {
	if ($radialPhase[$k]<-180 || $radialPhase[$k]>360) {
	    &streamerror(0,"radialPhase keyword must be between -180 and 360 degrees");}
    }    

    @verticalMode  = split(/ /,$values[9]);    
    @verticalAmp   = split(/ /,$values[10]);    
    @verticalPhase = split(/ /,$values[11]);
    if ($#verticalMode != $#verticalAmp || $#verticalMode != $#verticalPhase) {
	&streamerror(0,"Vertical Mode keywords must have equal number of values");}
    for ($k=0;$k<=$#verticalMode;$k++) {
	if ($verticalMode[$k] != int($verticalMode[$k])) {
	    &streamerror(0,"verticalMode keyword must have integer arguments");}
    }
    for ($k=0;$k<=$#verticalMode;$k++) {
	if ($verticalAmp[$k]<0 || $verticalAmp[$k]>1) {
	    &streamerror(0,"verticalAmp keyword must be between zero and one");}
    }
    for ($k=0;$k<=$#verticalMode;$k++) {
	if ($verticalPhase[$k]<-180 || $verticalPhase[$k]>360) {
	    &streamerror(0,"verticalPhase keyword must be between -180 and 360 degrees");}
    }    
}

sub errorcheckkeywords {
    local($radialset,$verticalset,$i);
   
    for ($i=1;$i<=5;$i++) {
	if ($values[$i] eq "") {
	    &streamerror(0,"Must set keyword [$validkeywords[$i]]");}
    }
    $radialset=0;
    for ($i=6;$i<=8;$i++) {	
	if ($values[$i] ne "") {$radialset++;}
    }
    $verticalset=0;    
    for ($i=9;$i<=11;$i++) {	
	if ($values[$i] ne "") {$verticalset++;}
    }
    if ($radialset == 0 && $verticalset == 0) {
	&streamerror(0,"Must set at least one radial or vertical mode");}
    if ($radialset != 0 && $radialset != 3) {
	for ($i=6;$i<=8;$i++) {	
	    if ($values[$i] eq "") {
		&streamerror(0,"Must set [$validkeywords[$i]]");}
	}
    }
    if ($verticalset != 0 && $verticalset != 3) {
	for ($i=9;$i<=11;$i++) {	
	    if ($values[$i] eq "") {
		&streamerror(0,"Must set [$validkeywords[$i]]");}
	}
    }
}

sub printvalues {
    local($i);
    print "[keyword]:[value]\n";
    for ($i=1;$i<=$#validkeywords;$i++) {	    
	print "[$validkeywords[$i]] = [$values[$i]]\n"; 
    }
}
    

sub initialize {
    local($i);
    $i=0;
    $validkeywords[++$i] = "M";
    $validkeywords[++$i] = "Ns";
    $validkeywords[++$i] = "N";
    $validkeywords[++$i] = "a";
    $validkeywords[++$i] = "da";
    $validkeywords[++$i] = "radialMode";
    $validkeywords[++$i] = "radialAmp";
    $validkeywords[++$i] = "radialPhase";
    $validkeywords[++$i] = "verticalMode";
    $validkeywords[++$i] = "verticalAmp";
    $validkeywords[++$i] = "verticalPhase";
    for ($i=1;$i<=$#validkeywords;$i++) {	    
	$values[$i] = ""; 
    }
}
	
sub streamerror {
    local ($j,$errmsg) = @_;
    print ("ERROR: $errmsg\n");
    if ($j>0 && $j<=$#inputlines) {
	print ("  >> line $j: $inputlines[$j]");
    }
    exit(0);
}

sub printUSAGE {
    local($program,$USAGE);
    $program=$0;

    if ($program =~ /\/([^\/\s]+)$/) {$program=$1;}  #\ followed by not slashes

    $USAGE = <<"end_of_input";

Program $program takes one argument, the name of an input file with an 
example file format given below.
   Example: $program stream.in 

#  Input file for streamline generator                                  
#  Comment Character
M  = 1e-6                             # total ring mass                 
Ns = 2                                # number of streamlines           
N  = 6                                # Particles per streamline        
a  = 2.001                            # semimajor axis                  
da = 0.001                            # streamline separation           
radialMode     =    0    1            # list of radial modes            
radialAmp      =    0.1  0.1          # mode amplitudes                 
radialPhase    =    0    90           # mode phases (degrees)           
verticalMode   =    0    1            # list of vertical modes          
verticalAmp    =    0.1  0.1          # mode amplitudes                 
verticalPhase  =    0    90           # mode phases (degrees)      

end_of_input
    print $USAGE;
exit();
}
              
