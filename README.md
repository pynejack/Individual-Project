# Individual-Project
This contains files I used to run and analyse tandem flapping foil simulations for my third year individual project at the University of Southampton


The lotus.f90 file included here is the edited for the base case of a Strouhal number of 0.4 with an amplitude and frequency ratio of 1

The analysis file is used as the post-processing and will group and average the data for each case, it will print the thrust, power and efficiency values for both the hind and fore foils

The calibration folder contains the specific lotus.f90 file that was used to callibrate results between Lotus and Lily Pad, it also includes an out.txt which contains the Lily Pad results, these are used in the Calibration.py file to determine the differences between the two CFD methods.
The differences were found to be 10~15% which is quite high, but the two CFD methods use different pressure solvers and Lotus can be considered the most accuarte tool and should be used for research purposes such as this one
