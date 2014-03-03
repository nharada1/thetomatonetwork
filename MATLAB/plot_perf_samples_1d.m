scatter(N(cluster_indices,t-1), P(cluster_indices,t-1),10,colors)
% SHOULD USE REPMAT HERE BUT FUCK ITx
plot(0:.1:1,(Y_intercepts(cluster_indices(1))*[1 1 1 1 1 1 1 1 1 1 1])+(Gradient_approx(cluster_indices(1))*0:.1:1));