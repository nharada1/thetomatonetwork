function [ c ] = chlorAcontent( img )
% Return the estimated chlorophyll content of a leaf using 
% a scanned image
load locus
CIE = [locus(:,1) locus(:,2) (359:359+size(locus,1)-1)'];
% preprocesss image
lambda_avg = 0;
iter = 0;
for i=1:size(img,1)
    for j=1:size(img,2)
        % Ignore white pixels
        if img(i,j,1) ~= 255 && img(i,j,2) ~= 255 && img(i,j,3) ~= 255
            [x,y] = RGB2xy(squeeze(img(i,j,:)));
            lambda = xy2lambda(x,y,CIE);
            lambda_avg = (iter*lambda_avg+lambda)/(iter+1);
            iter = iter+1;
        end
    end
end
disp(lambda_avg)
c = lambda2chlorA(lambda_avg);
end

