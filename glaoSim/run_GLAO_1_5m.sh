#TEST
#=====================================================================================================================
#           Image generation
#=====================================================================================================================
# ------------------------   CLOSE LOOP TESTS   ------------------------
#CASE1

#generate rmx
python SCAO_solar.py params_newIm.py --init="gainFactor=0.65; decayFactor=0.96;centroidPower=0.1; rcond=0.015;r0=80.1"

# iterate..(npup:300--> SR 500it: 0.721, npup:150--> SR 500it: 0.751)
python SCAO_solar.py params_newIm.py --user="nopoke" --iter=500 --init="gainFactor=0.8; decayFactor=0.99;centroidPower=0.1; rcond=0.01;r0=0.10"
