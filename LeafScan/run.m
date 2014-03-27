lambdas = zeros(5);
for i=0:4
    path = ['img/cropped/' int2str(t) '/plant' int2str(i) '.jpg'];
    img = double(imresize(imread(path),0.25));
    lambdas(i+1) = avglambda(img);
end
