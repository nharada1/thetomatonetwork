lambdas = zeros(5,1);

for i=0:4
    path = ['img/raw/' int2str(t) '/plant' int2str(i) '.jpg'];
    img = imresize(imread(path),0.25);
    midx = floor(size(img,2)/2);
    midy = floor(size(img,1)/2);
    nbhd_size = 5;
    xlist = [midx midx+nbhd_size midx midx+nbhd_size];
    ylist = [30 30 nbhd_size+30 nbhd_size+30];
    tolerance = midy;
    mask = magicwand(img,ylist,xlist,tolerance);
    img_cropped = uint8(zeros(size(img)));
    for j=1:3
        img_cropped(:,:,j) = img(:,:,j).*uint8(mask);
    end
    iamge(img_cropped)
    img_double = double(img_cropped);
    lambdas(i) = avglambda(img_double);
end
%{
 path = ['img/cropped/' int2str(t) '/plant' int2str(1) '.jpg'];
    img = imresize(imread(path),0.25);
    midx = floor(size(img,2)/2);
    midy = floor(size(img,1)/2);
    nbhd_size = 5;
    xlist = [midx midx+nbhd_size midx midx+nbhd_size];
    ylist = [30 30 nbhd_size+30 nbhd_size+30];
    tolerance = midy;
    mask = magicwand(img,ylist,xlist,tolerance);
    img_cropped = uint8(zeros(size(img)));
    for j=1:3
        img_cropped(:,:,j) = img(:,:,j).*uint8(mask);
    end
    img_double = double(img_cropped);
    inv_lambdas(1) = 1/avglambda(img_double);
%}

