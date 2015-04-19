function [transmat] = createmat(h,t,d,s,w,o)

     if (w < 0) | (s < 0) | (d < 0) | (t < 0) | (h < 0) | (o < 0)
       disp('Error: probabilities can not be negative')
       return;
     end

     % convert counts to probabilities

     total = h + t + d + s + w + o;
     h = h / total;
     t = t / total;
     d = d / total;
     s = s / total;
     w = w / total;
     o = o / total;

     % this submatrix will appear for each inning and each number of outs -
     % it gives the probabilities of changing states when an out does not
     % occur.

     smallmat = zeros(8,8);
     smallmat(1,:) = [h w+s d t 0 0 0 0];
     smallmat(2,:) = [h 0 d/2 t w+s/2 s/2 d/2 0];
     smallmat(3,:) = [h s/2 d t w s/2 0 0];
     smallmat(4,:) = [h s d t 0 w 0 0];
     smallmat(5,:) = [h 0 d/2 t s/6 s/3 d/2 w+s/2];
     smallmat(6,:) = [h 0 d/2 t s/2 s/2 d/2 w];
     smallmat(7,:) = [h s/2 d t 0 s/2 0 w];
     smallmat(8,:) = [h 0 d/2 t s/2 s/2 d/2 w];

     transmat = zeros( 9*24+1 , 9*24+1 );

     for i = 1 : 9*3
       transmat( (i-1)*8+1 : (i-1)*8+8 , (i-1)*8+1 : (i-1)*8+8 ) = smallmat;
     end

     % Now, when an out occurs and it's not the third out, just advance to
     % the same inning and same on-base state with one more out.

     for i = 1 : 9
       for j = 1 : 2
         transmat( (i-1)*24+(j-1)*8+1 : (i-1)*24+(j-1)*8+8 , ...
                   (i-1)*24+(j-1)*8+9 : (i-1)*24+(j-1)*8+16 ) = o*eye(8);
       end

       % In each inning, the third out goes to the next inning's
       % "0 out, 0 on base" state regardless of who was on base before.
    
       transmat( (i-1)*24+17 : (i-1)*24+24 , i*24+1 ) = o*ones(8,1);

     end

     % The final "game over" state can only go to itself.

     transmat( 9*24+1 , 9*24+1 ) = 1;

    
