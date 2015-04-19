function battingorder(filename)

  playermatrices = readdata(filename);
  load('smallmat.mat');
  runmatrix = createrunmatrix(smallmat);
  order = i2s(input('Enter a 9-digit batting order vector '));
  filename2 = strcat(filename,'.out');
  fid = fopen(filename2,'w');
    
  while ~ isempty(order)

     runs = calculate(order,playermatrices,runmatrix);
     fprintf('This lineup will score an average of %f runs per game.\n',runs); 

     for i=1:9
       fprintf(fid,'%d',order(i));
     end
     fprintf(fid,'\t\t%f\n',runs);

     order = i2s(input('Enter a 9-digit batting order vector '));

  end

  fclose(fid);
