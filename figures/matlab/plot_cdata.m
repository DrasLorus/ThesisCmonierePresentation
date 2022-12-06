cdata_tmp = load('../../data/cdata_score_map.dat');

indeces = 1:2880;

cdata = cdata_tmp(indeces, 2:27)';


createfigure_cdata(cdata(:, indeces))

clear cdata_tmp cdata indeces
