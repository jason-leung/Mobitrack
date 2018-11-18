function [segments] = extractSegments(t, roll, pitch, segment_inds)

segments = [];

for i = 1:size(segment_inds, 1)
    currentSegment = struct;
    start_ind = segment_inds(i,1);
    end_ind = segment_inds(i,2);
    currentSegment.roll = roll(start_ind: end_ind);
    currentSegment.pitch = pitch(start_ind: end_ind);
    currentSegment.t = t(start_ind: end_ind);
    
    segments = [segments; currentSegment];
end
end

