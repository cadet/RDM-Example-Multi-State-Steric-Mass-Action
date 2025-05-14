# Project repo

This repo contains the code for an example simulation of the elution of a monoclonal antibody (mAb) on the tentacle resin Fractogel EMD SO₃⁻ using CADET-Process and CADET-RDM. A `MultiStateStericMassAction` binding model is used where the mAb in the mobile phase is able to bind to the stationary phase in two different states. This example is a reproduction of part of the results published in "Multi-state steric mass action model and case study on complex high loading behavior of mAb on ion exchange tentacle resin" (Diedrich J, Heymann W, Leweke S, et al., J Chromatogr A. 2017;1525:60-70. doi:10.1016/j.chroma.2017.09.039). <br>
https://pubmed.ncbi.nlm.nih.gov/29055527/

Authors: Katharina Paul, Ronald Jäpel

To run this case study use an environment that contains at least all of the packages given in the environment.yml <br>
The example code can be found in the `src` folder. 
Tracking your output with CADET-RDM: After cloning this repo, run `main.py` in a terminal. The results will be stored in the src folder inside of the output folder.


The output repository can be found at:
[output_repo](https://github.com/cadet/RDM-Example-Multi-State-Steric-Mass-Action-Output)
