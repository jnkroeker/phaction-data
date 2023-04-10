### Data sources to be extracted:

- [x] Apple Health
- [ ] GoPro Videos
- [ ] Peloton
- [ ] Photos
- [x] Strava
- [x] SugarWOD/Wodify

### Mantra

Derived views allow gradual evolution. If you want to restructure a dataset, you do
not need to perform the migration as a sudden switch. Instead, you can maintain the
old schema and the new schema side by side as two independently derived views onto
the same underlying data. You can then start shifting a small number of users to the
new view in order to test its performance and find any bugs, while most users con‐
tinue to be routed to the old view. Gradually, you can increase the proportion of
users accessing the new view, and eventually you can drop the old view [10].
The beauty of such a gradual migration is that every stage of the process is easily
reversible if something goes wrong: you always have a working system to go back to.
By reducing the risk of irreversible damage, you can be more confident about going
ahead, and thus move faster to improve your system [11].

[10] Jacqueline Xu: “Online Migrations at Scale,” stripe.com, February 2, 2017.

[11] Molly Bartlett Dishman and Martin Fowler: “Agile Architecture,” at O’Reilly
Software Architecture Conference, March 2015.


#### Python Virtual Environment must be created and notebook, requests, urllib3 packages
#### installed to execute scripts in this project

1. Create a virtual environment by selecting a directory in which it will live and execute:

   `python3 -m venv /path/to/new/virtual/environment`

2. Once venv is created, activate it:

   `source /path/to/new/virtual/environment/bin/activate`

3. Install required packages once venv is activated:

   `pip install fastai gradio ipywidgets matplotlib notebook nbdev numpy openpyxl pandas requests seaborn scikit-learn urllib3`
	
#### On your laptop, John: venv is in ~/phaction/  
#### Activate it with `source ~/phaction/bin/activate`
#### Exit venv with   `deactivate`

### fetch_strava_data.py:

Fetch data from Strava API using personal ClientID and Client Secret.

You must upgrade your token access permissions to access Activity data. To do this:

1. in a browser execute `https://www.strava.com/oauth/authorize?client_id=<YOUR-CLIENT-ID> \
   &redirect_uri=http://localhost&response_type=code&scope=activity:read_all`

2. take the 'code' url param in the redirect url now in the browser

3. in Postman execute `https://www.strava.com/oauth/token?client_id=<YOUR-CLIENT-ID>&client_secret=<YOUR-SECRET> \
   &code=<FROM-PREVIOUS-STEP>&grant_type=authorization_code

4. post the ClientID, Client Secret and Authorization Code in approprate place in 'payload' variable of fetch_strava_data.py

5. execute command: ./fetch_strava_data.py

Credit:
https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde

### fetch_apple_health_data.py

Process XML data manually exported from Apple Health.

1. Open Apple Health app, tap user icon, select "Export Health Data"

2. Save the autogenerated "export.zip" to iPhone file system

3. Airdrop from iPhone to MacBook

4. Expand export.zip and move export.xml file to root of this directory

5. Execute ./extract_apple_health_data.py ./export.xml

Credit: http://www.markwk.com/data-analysis-for-apple-health.html

#### **NOTE** There appears to be a problem with duplicate startDate attributes on the export.xml file from Apple Health

### parse_sugarwod_data.ipynb

SugarWOD data is provided as CSV. With python, we can easily parse csv into dataframes and start working with it.

No scripting required to get hold of the data, just go directly to jupyter notebook.

### GoPro Data

Could not get Open GoPro API working with `extract_gopro_media.py` script. Defaulting to reading the SD card.