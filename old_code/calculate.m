function [runs] = calculate(order,playermatrices,runmatrix)

  % initial probability is 1 for 0 out, 0 on base, 1st inning
  % all other probabilities are initially zero

  situation = zeros( 1 , 9*24+1 );   
  situation(1) = 1;

  runs = 0;
  batter = 1;

  while situation(9*24+1) < 0.99     % while prob(game not over) >= 0.01

    % If you've already read the descriptions of playermatrices and runmatrix
    %   then you're in good shape to understand what goes on here.
    % For each batter, we re-calculate our situation probability vector based
    %   on the state transition probability matrix of the batter.  If S is
    %   the situation vector and P is the matrix, the formula is just 
    %   S := S*P
    % We also need to keep track of how many runs were scored in those
    %   transitions.  If R is the matrix of runs for each transition, 
    %   then R.*P is the expected number of runs the player will create for
    %   each transition.  And, S*(R.*P) is the vector of the expected number 
    %   of runs the player will create if he comes to bat in each state,
    %   weighted by the probability of each state.  So sum(S*(R.*P)) gives 
    %   the total number of expected runs the batter contributes this time up.

    % playermatrix is 9x217x217; to multiply by a single player's matrix,
    % so we need to reshape the player's 1x217x217 matrix to be 217x217

   runs = runs + sum(situation * ...
      (runmatrix .* reshape(playermatrices(order(batter),:,:),9*24+1,9*24+1)));

    situation = situation * ...
      reshape(playermatrices(order(batter),:,:),9*24+1,9*24+1);      

    % Get next batter

    batter = batter + 1;
    if batter > 9
      batter = 1;
    end

  end
