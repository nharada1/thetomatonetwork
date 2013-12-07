function [ out ] = cosine_sim( v,w )
% Compute the cosine similarity between two vectors
% v,w: the two vectors

    out = v*w'/(norm(v)*norm(w));
end

