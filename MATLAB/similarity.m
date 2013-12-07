function [ S ] = similarity( N,T,T_start,t_early,t,lambda )
% Return matrix of similarities based on nutrients, performance, and temp
% N: nutrient concentration matrix
% P: performance matrix
% T: temperature matrix
% T_start: vector of times where systems start
% t_early: number of rounds constituting early growth phase
% t: current time
% lambda: temperature weighting factor

    n = size(N,1);
    S = zeros(n);
    T_avg = zeros(1,n);
    for i=1:n
        if t > T_start(i)
            T_avg(i) = mean(T(i,T_start(i):t));
        end
    end

    for i=1:n
        for j=i:n
            % Only compute a similarity if plants are in later stages
            if t > T_start(i)+t_early && t > T_start(j)+t_early
                S(i,j) = exp(-1/lambda*(T_avg(i)-T_avg(j))^2)*...
                        cosine_sim(N(i,T_start(i):T_start(i)+t_early),...
                            N(j,T_start(j):T_start(j)+t_early));
            end
        end
    end

    % Symmetrize
    S = (S+S')-diag(diag(S));
end

