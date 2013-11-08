function [ E ] = suggest( N,P,T_start,t_early,early,t )
% Produce the vector of suggestions for each system
% N: nurient concentration matrix
% P: performance matrix
% T_start: vector of times where systems start
% t_early: number of rounds constituting early growth phase
% early: boolean indicating whether we are doing an early or non-early
%    suggestion
% t: current time.
n = size(N,1);
T_begin = zeros(1,n);
T_end = zeros(1,n);
E = zeros(1,n);
if early
    T_begin = T_start;
    T_end = min(T_start+t_early,t-1);
else
    T_begin = T_start;
    T_end = repmat(t-1,1,n);
end

for i=1:n
    % Gotta check if the bounds make sense for current plant
    if T_end(i) > T_begin(i)
        [mx,ind] = max(P(i,T_begin(i):T_end(i)));
        E(i) = N(i,ind+T_begin(i));
    end
end
if sum(E) > 0
    E = E/sum(E);
end
end

