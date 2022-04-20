# Data Science Approaches to Cultural Analytics: Genre and Tropes in Popular Media using TVTropes
BSc Individual Project - Isabel Sebire

The code submission is structured as follows:

* Tropescraper Edits - tropescraper was used to scrape the trope-work relationships from TVTropes. Note that I did *not* write this code (tropescraper is developed by García-Ortega et al, in 

[https://arxiv.org/abs/2006.05380]

), although it is included in the submission as I edited the code to make it suitable to this project.
* Datasets - contains copies of the datasets; code for scraping trope data from TVTropes, IMDb data, and RAWG.io data; and construction of the datasets.
* Exploratory Statistics - contains files exploring the dataset. The file nestedness_calculator was written by Straka, available at 

[https://github.com/tsakim/nestedness]

.
* Sentence Embeddings - contains files concerning producing and clustering SBERT embeddings.
* Community Detection (Related Tropes) - contains files for running Louvain community detection on the network of related tropes.
* hLDA - code experimenting with hLDA implementations. These implementations were not used on the project, but the report discusses why hLDA was not used as the primary model or for evaluation.
* topSBM - contains files for running and analysing the results of the topSBM model. Note the file sbmtm.py was developed by Gerlach et al and is available at 

[https://github.com/martingerlach/hSBM_Topicmodel]

, however as above, this code is included in the submission as edits (including major efficiency improvements) were made to this code in this project.
* topSBM Evaluation - files for evaluating the performance of the topSBM model (across datasets).
* Zeta - files to calculate Zeta diversity. The file nestedness_calculator was written by Straka, available at 

[https://github.com/tsakim/nestedness]

.

(Please note, the directory structure and so filepaths in code files may have changed between the time the code was run and this submission.)

All code was written in Python, with the exception of some files in the Zeta directory being written in R.
