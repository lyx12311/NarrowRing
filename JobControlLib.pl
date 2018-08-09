#!/usr/bin/perl library for hndodyM/hndragM etc.
# Written 12/2009 by DPH

sub main {
    local($searchfile, $executable, $CPUs)=@_;
    local($numdirs,$command,@dirs);

    if ($#ARGV == -1) {&printUSAGE();}    
    @files = &parseARGV(*ARGV,*patterns,*flags);
    &SetFlags($flags);
    if ($verbose) {&printARGV(*files,*patterns,*flags);}
    @dirs = &gethndirs($searchfile,@ARGV);
    if ($#dirs==-1) {
        print "no valid directories\n";
	exit();
    }
    $numdirs = $#dirs +1;
    print "Run the command '$executable' using $CPUs CPUs\n";
    print "on these $numdirs directores [@dirs]?\n";
    print "  Press any Key to Contine, Control C to Abort. >> ";
    $command = <STDIN>;
    if ($command !~ "n") {&runjobs($CPUs,@dirs);}
    &printtime();        
    print "All jobs submitted.\n";
#    system("hnbmonitor $elapsedtime @dirs");
    &MonitorJobs(@dirs);
}


sub runjobs {
    local($CPUs,@dirs)=@_;
    local($dir,$openCPUs,$numjobs,$curdir);

    $dir=0;
    $numjobs = $#dirs+1;
    while ($dir <= $#dirs) {
        $openCPUs = $CPUs - &runningjobs(@dirs);
        while($openCPUs>0 && $dir<=$#dirs) {
	    $curdir = $dirs[$dir];
            $openCPUs -= &run1job($dirs[$dir]);
            $dir++;
            &printtime();
            print "starting $curdir ($dir of $numjobs) - ";
   	    print "openCPUs = $openCPUs\n";
        }
        if ($dir> $#dirs) {return;}
        sleep 1;
    }
}

sub run1job {
    local($dir)=@_;
    $running = "$dir/job.running";
    if (-e "$running") {
        print "file $dir/job.running exists!" ;
        return 0;
    } else {
        open(RUNNING,"> $running");
        print RUNNING "running";
        print RUNNING " [cd $ENV{PWD}/$dir] ";        
        close(RUNNING);
#	print "dir = $ENV{PWD}/$dir\n";
        chdir "$ENV{PWD}/$dir";
        system("($executable; unlink $ENV{PWD}/$running) &");
        chdir "$ENV{PWD}";
    }
    return 1;
}

sub runningjobs {
    local(@dirs)=@_;
    local($dir, $jobs);

    $jobs=0;
    foreach $dir (@dirs) {
        if (-e "$dir/job.running") {$jobs++;}        
    }
#    print "jobs running= $jobs \n";
    return $jobs;
}


sub gethndirs {
    local($searchfile,@ARGV)=@_;

    foreach $i (@ARGV) {
	open(INFILE,"find $i -path \"*/$searchfile\" -print |");                                                                                                          
	while (<INFILE>) {    
	    #	    $_ =~ /^(.*)\/$searchfile/;
	    $_ =~ /^(.*)\/$searchfile/;    	    
	    push @dirs, $1;
#	    print "$1\n";
	}
    }
    @dirs;
}
    

sub printUSAGE {
local($program,$USAGE);

$program = $0;
if ($0 =~ /\/([^\/\s]+)$/) {$program=$1;}  # \ followed by not slashes.
$USAGE = <<"end_of_input";

Program $program drops into all directories on the command line and runs 
the command "$executable" on the local machine using $CPUs cpus. 
The user can edit the executable and/or the number of cpus at the top 
of the program.
  Example:  $program r*

end_of_input
print $USAGE;
exit(1);
}


sub SetFlags {
    local($flags) = @_;
    local($x);
    $x=0;
    if (defined ($flags)) {
        if    ($flags =~ /e(\d+)/) {$x= $1;}
        if    ($flags =~ /h/)      {&printUSAGE();exit();}
        if    ($flags =~ /v/)      {$verbose = 1;}
    }
}

sub MonitorJobs {
    local($lastrunning,$numrunning);
    $lastrunning= -999;   # need to be different
    $numrunning = 0;
    @runningdirs = ();
    foreach $i (@dirs) {
        if (-T "$i/job.running") {
            $numrunning++;
            @runningdirs = (@runningdirs, $i);
        }
    }
    while ($numrunning !=0) {
        if ($numrunning != $lastrunning) {
            &printtime();
            print "$numrunning job";
            if ($numrunning >1) {print "s";}
            print " still running (@runningdirs)\n";             
        }
        sleep 1;
        $lastrunning = $numrunning;
        $numrunning = 0;        
        @runningdirs = ();
        foreach $i (@dirs) {
            if (-T "$i/job.running") {
                $numrunning++;
                @runningdirs = (@runningdirs, $i);
            }
        }
    }
    &printtime();    
    print "All jobs finished.\n"; 
}


sub printtime{
    local($DATE);
    $DATE = localtime;
    $DATE =~ /(..\:..\:..)/;
    print "Time $1 - ";
}


                
######################################################################                       
# FROM lib.pl
                 
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
      


1; #return true
