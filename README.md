# Hourglass (Desktop Application)

Hourglass is a toolkit to interrogate multiparameteric data from well-annotated patient cohorts, mainly from bioimage analysis. This desktop application serves as a graphical user interface for the R package with the same name, found [here](https://github.com/kazeera/Hourglass/). It was built using python and the Kivy design language. 

### Installation

1. If not already installed, install the R statistical environment. Check this [URL](https://kazeera.github.io/Hourglass/installation.html) to get R.

> Note: R must be installed for the application to work, but working knowledge of R programming is not necessary. 

2. Download file (see table below). Click on link and press file name to download.

  | Operating System | Download Link | Size | Latest Version | 
  |:-:|:-:|:-:|:-:| 
  | Windows | [*.exe* file ](https://github.com/kazeera/Hourglass-interface/tree/main/Executables/Windows) | 108 MB | v1.03 | 
  | MacOS | [*.dmg* file ](https://github.com/kazeera/Hourglass-interface/tree/main/Executables/MacOS) | 53 KB | v1.03 | 

**Windows**  

3. Locate the downloaded exe installer file on your computer.
4. Double-click file to run and follow the instructions. Windows will run a setup wizard to install Hourglass.

**MacOS**  

3. Locate the downloaded dmg file on your computer.
4. Drag contents to the "Application" folder.



### How to Use

Open application and follow tabs on top (left to right) to go through workflow. Refer to the complete guide: [URL](https://kazeera.github.io/Hourglass/how-to-use-the-desktop-application.html).

### Preview
Easily **accessible** for non-expert users.

<img src="ReadMe/upload_data.png?raw=true" width="500"></img>

**Advanced parameters** may be changed for experienced users to refine their analysis.

<img src="ReadMe/advanced_options.png?raw=true" width="500"></img>

Tremendously **customizable**, e.g. you may input hex codes for consistent colour schemes.

<img src="ReadMe/customize_colors.png?raw=true" width="500"></img>

Hit run at the end!

<img src="ReadMe/run_hourglass.png?raw=true" width="500"></img>


### What is Hourglass?
**Hourglass** is a computational toolkit that streamlines processing and visualization of massive multiparametric datasets. 
Hourglass was built around the pancreatic ductal adenocarcinoma (PDAC) tissue microarray (TMA) published in Grünwald *et al.*, Cell, 2021. Read [here](https://www.sciencedirect.com/science/article/pii/S0092867421011053?via%3Dihub). 
It was used to integrate quantified image analysis output with clinical data from patient cohorts to explore subgroups.

#### Overall Workflow
![](ReadMe/workflow.JPG?raw=true)

#### Main Features
- Facilitates fully reproducible data exploration for non-expert users
- Leverages metrics of heterogeneity from standard TMA designs:
  - Resolves regional (sample-level) vs global (patient-level) differences
  - Allows definitions for exclusion/inclusion criteria (ie. filters), within subgroups, e.g. exclude Smokers
  - Uses internal data to stratify patients/samples, e.g. expression of a gene can group cohorts into low/high subgroups
  - Option to impute dropouts and run imputed dataset in parallel, particularly useful for patchy datasets
- Proposes method of quality control by providing boxplots for all feature/parameter combinations
- Creates publication-ready plots in semi-automated manner in organized file hierarchy
- Generic input design supports any type of numerical dataset with clinical/sample annotations, including omics data

