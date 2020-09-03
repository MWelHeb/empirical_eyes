# empirical_eyes

# Publishing a data science project

# 1 - Starting point - to have a (data science) question. 

# In my case - at the beginning of the covid crisis - I was very much interested in having an overview on the status of covid19 infections in the various countries at each point in time. Working in the airline industry I was particularly interested in so-called online countries, i.e. countries which had formerly, i.e. before the covid19 breakout, been online connected by the airline under consideration. Idea was to early identify those countries which had covid19 "under control", because these would be the first countries, where airline travel demand would pick up again. My goal was not to rely on any third party reports which I could not modidfy or update according to my interests and needs (e.g. which countries are displayed, which figures are shown, which time comparison is displayed etc.) but to build up a report/analysis which reflected my approach of describing the current covid situation. The basic idea was to somehow scan the typical (i.e. "bell shaped") covid curve of new infections for each and every country and then to position each country on a "typical generic bell shaped covid curve" in order to get an overview on one page. 

# 2 - Data science software

# Apart from the (data science) question you obviously have to have access to a data science software that provides the required functionalities you need in order to collect, modify/manipulate and finally analyse and display the data and results.

# Having worked in data science over many years I have gained some experience in data science, econometrics and statistics related software such as GAUSS, SAS, SPSS, LIMDEP, R, etc. as well as data handling related/programing languages, e.g. SQL, PHP, Perl, etc.. Python however I had not touched so far and hence looking into some statistics on data science software usage showed me that the usage of Python was substantially increasing over the last years. Hence I wanted to get an understanding of Python descided to use Python for this project.

# How to install python in which version and with which modules? There are various tutorials and videos in the internet available which provide a very good description on how to install Python. My first approach was to intall python directly from the python page https://www.python.org/downloads/windows/ which worked out very smooth. However later on, when I was interested in having an environement which also contains addtional to pyhton respective programming editors and IDEs as was as potential interfaces to other data science software such as R, etc.. For that purpuse the distribution manager Anaconda (https://en.wikipedia.org/wiki/Anaconda_(Python_distribution)) is suited very well. As package manager I used pip (https://de.wikipedia.org/wiki/Pip_(Python)), but there is also conda as alternative https://en.wikipedia.org/wiki/Conda_(package_manager) - for differences between both package managers see e.g. https://www.anaconda.com/blog/understanding-conda-and-pip. 

# After having installed Anaconda you have set of programming editors and IDEs (e.g. Jupyter Notebook, JupytherLab, Spyder, PyCharm, etc.) at hand. For a nice overview and comparsion of such Python IDEs and code editors see e.g. https://www.datacamp.com/community/tutorials/top-python-ides-for-2019?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=332602034343&utm_targetid=aud-299261629574:dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=9044490&gclid=Cj0KCQjw4f35BRDBARIsAPePBHz7KBVXOrqqH-RUDjRI3LKEgtOWdrHTfnPk-xjJx0MkDRNyAKwneQ8aAnhlEALw_wcB. I have started of with JupytherLab and later additionally also used Spyder.

# 3 - Data analysis
# Every data analysis starts of with finding/getting an appropriate data source to be analyzed. In my case basically in a first step a Google search directed me to the GitHub Datasource: D2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE. Moreover in order to extract the data from the John Hopkins University GitHub Data Repository and to further work with it in Python it is very usfull to install pandas, which is a very powerful Python data analysis library. The installation of pandas is done very easily via the package manager pip using the following command: "pip install pandas". Once pandas has been installed following compands will extract you the respective COVID-19 data (in my case only the confirmed Covid19 cases) into a pandas dataframe:

import pandas as pd

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

confirmed = pd.read_csv(url, error_bad_lines=False)



# More data is needed and the internet provides a lot - but sometimes very unstructured --> noSQL 

# 4 - From local to cloud
