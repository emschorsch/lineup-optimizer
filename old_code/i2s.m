function [ord] = i2s(instring)

  if (size(instring,2) > 1)   % if a string '123456789' is entered
    for i = 1:9
	ord(i) = instring(i) - 48;
    end
  elseif (size(instring,2) > 0)   % if a number 123456789 is entered
    for i = 9:-1:1
      ord(i) = mod(instring,10);
      instring = floor(instring/10);
    end
  else
    ord = '';
  end

  
