import requests
import json
# https://docs.getxray.app/display/XRAYCLOUD/Authentication+-+REST+v2
# https://docs.getxray.app/display/XRAYCLOUD/Import+Execution+Results+-+REST+v2#ImportExecutionResultsRESTv2-CucumberJSONresults

# Replace with your Jira and Xray credentials and URLs
xray_base_url = 'https://xray.cloud.getxray.app'
clientId = 'clientId'
password = 'password'

def get_access_token():
    xray_url_auth = f'{xray_base_url}/api/v2/authenticate'
    headers_xray = {
    "Content-Type": "application/json"
    }
    auth = {"client_id": clientId,"client_secret": password }

    response_auth = requests.post(url=xray_url_auth, headers=headers_xray, data=json.dumps(auth))
    response_auth.raise_for_status()  # Raise an exception for HTTP errors
    return response_auth.json()

# List releases
def import_test_result(test_results):
    import_result_url =  f'{xray_base_url}/api/v2/import/execution/cucumber'
    access_token = get_access_token()
    headers_xray_import = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response_import_result = requests.post(
        url= import_test_result,
        headers= headers_xray_import,
        data= test_results
    )
    response_import_result.raise_for_status() # This will raise an HTTPError for bad responses
    print(response_import_result.json())

if __name__ == '__main__':
    with open('testResultJsonFile.json') as f:
        test_results = f.read()
    import_test_result(test_results=test_results)
