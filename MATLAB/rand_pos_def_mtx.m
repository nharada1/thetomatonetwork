function [ M ] = rand_pos_def_mtx( )
% Create a random positive definite matrix
    D = diag(rand(1,3));
    A = randn(3);
    [P,~] = eig((A+A')/2);
    M = P*D*P';
end

