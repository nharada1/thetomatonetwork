function [ lambda ] = xy2lambda( x,y,CIE )
% Convert CIE coordinates into wavelength in nm
% Done by fitting the line through the whitepoint (whitex,whitey)
% of CIE and given chromatic coordinates (x,y), and seeing where
% it intersects the CIE boundary
whitex = 0.35;
whitey = 0.35;
slope = (y-whitey)/(x-whitex);
yintercept = whitey-whitex*slope;
if x > whitex
    xrange = whitex:0.005:0.8;
else 
    xrange = 0:0.005:whitex;
end
line = [xrange' (slope*xrange+yintercept)'];
[k,d] = dsearchn(CIE(:,1:2),line);
[min_d,ix] = min(d);
lambda = CIE(k(ix),3);

end

