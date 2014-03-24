function [ c ] = lambda2chlorA( lambda )
% Convert average wavelength in nm to chlorophyll A concentration in g/L
% http://arxiv.org/ftp/arxiv/papers/1305/1305.1148.pdf

%if lambda > 565 && lambda < 567.5
if lambda < 567.5
    c = -0.6037*lambda^2+682.35*lambda-192808.55;
elseif lambda >= 567.5 && lambda < 571
    c = 5e239*exp(-0.9741*lambda);
else 
    c = 0;

end

