# Urban or Rural

In this Data Analysis Project, I take in geospatial data and determine whether a given location is urban or rural.

## Outline

- [Project Structure](#project-structure)
- [Sources](#sources)
  - [GADM Dataset](#gadm-dataset)
  - [GADM Labelling](#gadm-labelling)
- [Setup](#setup)

## Sources

Check the `data/` folder for details on how to download, import, clean, and use the datasets used in this analysis.

### GADM Dataset

Downloaded [version 4.1](https://gadm.org/download_world.html) as a single database.

<!-- Download link: https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_410-gpkg.zip -->

This dataset contains strictly geographical data.

**GADM.** *GADM Database of Global Administrative Areas, Version 4.1*. 2022. https://gadm.org. Accessed July 24, 2026.

<!-- ```bibtex
@misc{gadm41,
  author       = {{GADM}},
  title        = {GADM Database of Global Administrative Areas, Version 4.1},
  year         = {2022},
  howpublished = {\url{https://gadm.org}},
  note         = {Accessed: 2026-07-24}
}
``` -->

### GADM Labelling

This dataset labels the GADM regions as urban or rural based on the degree of urbanisation. 

Schiavina M., Melchiorri M., Freire S. (2023):
GHS-DUC R2023A - GHS Degree of Urbanisation Classification, application of the Degree of Urbanisation methodology (stage II) to GADM 4.1 layer, multitemporal (1975-2030).European Commission, Joint Research Centre (JRC)
PID: http://data.europa.eu/89h/dc0eb21d-472c-4f5a-8846-823c50836305, doi: https://10.2905/DC0EB21D-472C-4F5A-8846-823C50836305

<!-- Download link: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_DUC_GLOBE_R2023A/V2-0/GHS_DUC_MT_GLOBE_R2023A_V2_0.zip -->



## Setup

To run this project locally, set it up as follows. I use uv, so that's the default, but you can use any other package manger.

1. Create and activate a virtual environment using `uv`:

```bash
# Create a virtual environment
uv venv

```

2. Activate the virtual environment

```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

```

3. Install dependencies

```bash
uv pip install -r requirements.txt
```
