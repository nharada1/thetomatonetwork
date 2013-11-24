function [ M ] = rand_pos_def_mtx( )
D = diag(rand(1,3));
A = randn(3);
[P,ignore] = eig((A+A')/2);
M = P*D*P';
end

