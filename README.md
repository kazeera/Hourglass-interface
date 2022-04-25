# Hourglass Desktop Application

This application serves as a graphical user interface to the R package, Hourglass, found [here](https://github.com/kazeera/Hourglass/).
It is a standalone desktop application supported by python and Kivy design language.

### Preview
Easily **accessible** for non-expert users.

<img src="ReadMe/upload_data.png?raw=true" width="500"></img>

**Advanced parameters** may be changed for experienced users to refine their analysis.

<img src="ReadMe/advanced_options.png?raw=true" width="500"></img>

Tremendously **customizable**, e.g. you may input hex codes for consistent colour schemes.

<img src="ReadMe/customize_colors.png?raw=true" width="500"></img>

Hit run at the end!

<img src="ReadMe/run_hourglass.png?raw=true" width="500"></img>

### Installation and Usage
1. Download single exe file for Windows / dmg for MacOS in this repository.
2. Run installer on computer.
3. Open application and follow tabs on top (left to right) to go through workflow.

* Note: R must be installed for application to work, but working knowledge of R programming is not necessary. 
For first-time R users, here are installation instructions: [URL for Windows](https://datag.org/resources/documents/spring-2018/37-de-barros-installing-r-on-windows/file) and [URL for Mac](https://people.umass.edu/biep540w/pdf/HOW%20TO%20install%20R%20and%20R%20Studio%20MAC%20Users%20Fall%202020.pdf)

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

