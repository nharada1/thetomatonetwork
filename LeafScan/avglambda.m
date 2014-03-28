function [ lambda_avg ] = avglambda( img )
% Return the average wavelength reflected by leaf using
% a scanned image
load locus
CIE = [locus(:,1) locus(:,2) (359:359+size(locus,1)-1)'];
% preprocesss image
lambda_avg = 0;
iter = 0;
for i=1:size(img,1)
    for j=1:size(img,2)
        % Ignore black pixels
        if img(i,j,1) ~= 0 && img(i,j,2) ~= 0 && img(i,j,3) ~= 0
            [x,y] = RGB2xy(squeeze(img(i,j,:)));
            lambda = xy2lambda(x,y,CIE);
            lambda_avg = (iter*lambda_avg+lambda)/(iter+1);
            iter = iter+1;
        end
    end
end

end

