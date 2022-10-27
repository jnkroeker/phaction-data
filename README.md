### Python Virtual Environment must be created and requests, urllib3 packages installed to execute this script

	Laptop: venv in ~/Desktop/phaction_scripts/ * activate with  

### fetch_strava_data.py:

Fetch data from Strava API using personal ClientID and Client Secret.

You must upgrade your token access permissions to access Activity data. To do this:

1. in a browser execute `https://www.strava.com/oauth/authorize?client_id=<YOUR-CLIENT-ID> \
   &redirect_uri=http://localhost&response_type=code&scope=activity:read_all`

2. take the 'code' url param in the redirect url now in the browser

3. in Postman execute `https://www.strava.com/oauth/token?client_id=<YOUR-CLIENT-ID>&client_secret=<YOUR-SECRET> \
   &code=<FROM-PREVIOUS-STEP>&grant_type=authorization_code

4. post the ClientID, Client Secret and Authorization Code in approprate place in fetch_data.py

Credit:
https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde

### fetch_apple_health_data.py



Credit: http://www.markwk.com/data-analysis-for-apple-health.html
