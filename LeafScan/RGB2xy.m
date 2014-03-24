function [ x,y ] = RGB2xy( A )
% Convert vector of rgb values into CIE corredinates using sRGB
% color space
sRGB = [.412 0.358 0.180; 0.213 0.715 0.072; 0.019 0.119 0.950];
B = sRGB*A;
x = B(1)/sum(B);
y = B(2)/sum(B);

end

