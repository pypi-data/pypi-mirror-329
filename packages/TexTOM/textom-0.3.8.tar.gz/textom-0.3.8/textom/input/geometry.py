# directional vectors
detector_direction_origin = (0,0,1)
detector_direction_positive_90 = (0,-1,0)
inner_axis = (0,0,1) # inner rotation axis
outer_axis = (0,1,0) # outer rotation axis
beam_direction = (1,0,0) # p in mumott
transverse_horizontal = (0,1,0) # j in mumott
transverse_vertical = (0,0,1) # k in mumott

# beam size in um (FWHM)
Dbeam = 0.3 
# step size for scanning in um
Dstep = 0.5

# scanning mode
scan_mode = 'line' #'column' # 'line_snake' # 'column_snake'
