function [runmatrix] = createrunmatrix(smallmat)

  % This creates the run-value matrix that calculates how many runs will
  %   score in each transition.  For example, the transition from "0 out,
  %   runner on 2nd base" to "0 out, 0 on base" must mean that 2 runs have
  %   scored (because all the baserunners and the batter must either be on
  %   base somewhere, be out, or have scored)

  % It's really a block-diagonal matrix since we're assuming a simplified
  %   model where no runners advance on outs.  So runs only score when the
  %   number of outs doesn't change.  
  % It's independent of number of outs and independent of the number of
  %   innings, so the same submatrix (smallmat) appears over and over
  %   in runmatrix.
  % Also, it's independent of the batter so we can store it explicitly
  %   in a small data file.

  runmatrix = zeros( 9*24+1 , 9*24+1 );

  for i = 1 : 9*3
      runmatrix( (i-1)*8+1 : (i-1)*8+8 , (i-1)*8+1 : (i-1)*8+8 ) = smallmat;
  end
