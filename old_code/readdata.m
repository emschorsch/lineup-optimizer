function [playermatrices] = readdata(filename)

  % Here's how we get the dimensions (this is true for all files):
  % In each inning, there are 24 possible states:
  %   3 possible numbers of outs (0,1,2) and 8 on-base combinations
  %   (each base is binary - either occupied or not - for 2^3 = 8 total)
  %   So 3 out possibilities * 8 on-base possibilities = 24 states per inning.
  % There are 9 innings, so there are 9*24 total states, plus one more final
  %   state for "end of game" for a total of 9*24 + 1 = 217.
  % Each player's matrix gives the probability of going to state j given
  %   that we're in state i now.  That's a 217x217 matrix (could go from any
  %   state to any state).  Each player has one of these matrices so the
  %   whole thing is a 9x217x217 matrix.

  playermatrices = zeros( 9 , 9*24+1 , 9*24+1 );

  fid = fopen(filename);

  for i = 1 : 9
     homeruns = fscanf(fid,'%d',1);
     triples = fscanf(fid,'%d',1);
     doubles = fscanf(fid,'%d',1);
     singles = fscanf(fid,'%d',1);
     walks = fscanf(fid,'%d',1);
     outs = fscanf(fid,'%d',1);
     name = fscanf(fid,'%s',1);
     playermatrices(i,:,:) = ...
         createmat(homeruns,triples,doubles,singles,walks,outs);
  end

  fclose(fid);
