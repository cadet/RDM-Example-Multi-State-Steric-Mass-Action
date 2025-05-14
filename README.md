# Multi-State Steric Mass Action with CADET

This repository contains an example simulation of the elution of a monoclonal antibody (mAb) on the tentacle resin Fractogel EMD SO₃⁻ using **CADET-Process** and **CADET-RDM**. A **Multi-State Steric Mass Action** binding model is used where the mAb in the mobile phase is able to bind to the stationary phase in two different states. 

This example reproduces part of the case study from:
* *"Multi-state steric mass action model and case study on complex high loading behavior of mAb on ion exchange tentacle resin"*
  Diedrich J, Heymann W, Leweke S, et al.
  *Journal of chromatography. A* vol. 1525 (2017): 60-70
  [doi:10.1016/j.chroma.2017.09.039](https://pubmed.ncbi.nlm.nih.gov/29055527/)

---

## Authors

* Katharina Paul
* Ronald Jäpel
* Hannah Lanzrath

---

## Running the Example Simulation

1. Clone this repository.
2. Set up the environment using the `environment.yml` file.
3. Run the simulation:

   ```bash
   python main.py
   ```

The results will be stored in the `src` folder inside the `output` directory.

> **Note**: Running `cadet-rdm` requires [**Git LFS**](https://git-lfs.com/), which needs to be installed separately.
>
> * **Ubuntu/Debian**:
>
>   ```bash
>   sudo apt-get install git-lfs
>   git lfs install
>   ```
>
> * **macOS** (with Homebrew):
>
>   ```bash
>   brew install git-lfs
>   git lfs install
>   ```
>
> * **Windows**:
>   Download and install from [https://git-lfs.com](https://git-lfs.com)

---

## Output Repository

The output data for this case study can be found here:
[https://github.com/cadet/RDM-Example-Multi-State-Steric-Mass-Action-Output](https://github.com/cadet/RDM-Example-Multi-State-Steric-Mass-Action-Output)