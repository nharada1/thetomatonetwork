function [ img_cropped ] = autocropleaf( img )
% Whiteout all pixels of an image that have a high B value
% or too low luminosity
b_thresh = 50;
rgb_thresh = 10;
img_cropped = img;
img_sum = sum(img,3);
for i=1:size(img,1)
    for j=1:size(img,2)
        if img(i,j,3)>b_thresh || ...
                img_sum(i,j) < rgb_thresh
            img_cropped(i,j,1) = 255;
            img_cropped(i,j,2) = 255;
            img_cropped(i,j,3) = 255;
        end
    end
end

end

