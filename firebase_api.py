import requests, os
import firebase_admin
from firebase_admin import credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
ROOT_DIR = os.path.abspath(os.curdir)

class FirebaseDownloadApp:
    # Initialize the Firebase Admin SDK
    def __init__(self, sa, app_id, project_number, app_version):
        self.sa = os.path.abspath(f'{ROOT_DIR}/service_account/{sa}')
        self.appId = app_id
        self.project_number = project_number
        self.app_version = app_version
        cred = credentials.Certificate(self.sa)
         # Firebase App Distribution API base URL
        self.base_url = f'https://firebaseappdistribution.googleapis.com/v1/projects/{self.project_number}/apps/{self.appId}/releases'
        firebase_admin.initialize_app(cred)

    # Obtain an OAuth 2.0 access token
    def _get_access_token(self):
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        service_account_info = service_account.Credentials.from_service_account_file(
            self.sa, scopes=scopes)
        service_account_info.refresh(Request())
        return service_account_info.token

    # List releases
    def _list_releases(self):
        access_token = self._get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(self.base_url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()

    # Download APK for a specific release
    def _download_function(self, download_url, output_file):        
        access_token = self._get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {output_file}")
    
    def download_track_apk(self):
        output_file = os.path.abspath(f'{ROOT_DIR}/test_data/app.apk') 
        # Remove apk files if exits
        file_names = os.listdir(os.path.abspath(f'{ROOT_DIR}/test_data'))
        for file in file_names:
            if file.endswith(".apk"):
                os.remove(f'{ROOT_DIR}/test_data/{file}')
        # Grab the app build list and find the one we want
        app_build_list = self._list_releases()
        app_version_exist = False              
        for release in app_build_list.get('releases', []):
            if release['displayVersion'] == self.app_version:
                app_version_exist = True
                download_url = release['binaryDownloadUri']
                break
        # Make sure the app version can be found
        if not app_version_exist:
            assert False, "Cannot find the app vesion, please check if it is correct"
        else:
            self._download_function(download_url, output_file)
        # Make sure app is really downloaded
            if not os.path.exists(output_file):
                assert False, "Downloading error, check your downloading process"
    

class downloadApp(FirebaseDownloadApp):
    def __init__(self, displayVersion):
        self.displayVersion = displayVersion
        app_id = "appId, need to check in firebase"
        project_number = 'project number, need to check in firebase'
        sa = "serviceAccount.json"
        super().__init__(sa=sa, 
                         app_id = app_id, 
                         project_number = project_number,
                         app_version = self.displayVersion
                         )

if __name__ == '__main__':
    download_track = downloadApp(displayVersion="6.2.1.410")
    download_track.download_track_apk()
