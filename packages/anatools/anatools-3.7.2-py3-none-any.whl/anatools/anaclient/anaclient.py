"""The client module is used for connecting to Rendered.ai's Platform API."""

envs = {
    'prod': {
        'name': 'Rendered.ai Platform',
        'url':  'https://deckard.rendered.ai',
        'statusAPI': 'https://api.rendered.ai/system',
        'api':  'https://api.rendered.ai/graphql' },
    'test': {
        'name': 'Rendered.ai Test Platform',
        'url':  'https://deckard-test.web.app',
        'statusAPI': 'https://api.test.rendered.ai/system',
        'api':  'https://api.test.rendered.ai/graphql' },
    'dev': {
        'name': 'Rendered.ai Development Platform',
        'url':  'https://deckard.dev.rendered.ai/',
        'statusAPI': 'https://api.dev.rendered.ai/system',
        'api':  'https://api.dev.rendered.ai/graphql' }
}

class AuthFailedError(Exception):
    pass

class client:

    def __init__(self, workspaceId=None, environment='prod', email=None, password=None, APIKey=None, local=False, endpoint=None, interactive=True, verbose=None):
        import getpass
        import os
        from anatools.anaclient.api import api
        from anatools.lib.print import print_color
        import requests
        self.verbose = verbose
        self.interactive = interactive
        if environment not in ['dev','test','prod','infra']:  raise Exception("Invalid environment argument, must be 'infra', 'dev', 'test' or 'prod'.")
        if local:
            os.environ['NO_PROXY'] = '127.0.0.1'
            self.__url = 'http://127.0.0.1:3000/graphql'
            self.__status_url = None
            self.__environment = 'Local'
            if self.interactive: print("Local is set to",self.__url)
        elif endpoint:
            self.__url = endpoint
            self.__status_url = None
            self.__environment = 'Rendered.ai'
        else: 
            self.__url = envs[environment]['api']
            self.__status_url = envs[environment]['statusAPI']
            self.__environment = envs[environment]['name']
        self.__password = password
        self.__logout = True
        self.__notificationId = None
        self.__APIKey = None
        self.email = email
        self.user = None
        self.organizations = {}
        self.workspaces ={}
        self.channels = {}
        self.volumes = {}
        self.organization = None
        self.environment = environment

        self.ana_api = api(self.__url, self.__status_url, None, self.verbose)

        # fetch system notification
        if self.__status_url and self.interactive:
            try:
                notification = self.ana_api.getSystemNotifications()
                if notification: print_color(notification['message'], 'ffff00')
            except Exception as e:
                print_color(f"Could not get notifications: {e}", 'ffff00')
            
        if(APIKey == None and 'RENDEREDAI_API_KEY' in os.environ and not email):
            if self.interactive: 
                print_color("Using environment RENDEREDAI_API_KEY key to login", 'ffff00')
            self.__APIKey = os.environ.get('RENDEREDAI_API_KEY')
            self.sign_in_apikey(interactive=interactive)
        
        elif (APIKey):
            if self.interactive:
                print_color("Using provided APIKey to login", 'ffff00')
            self.__APIKey = APIKey
            self.sign_in_apikey(interactive=interactive)

        else :        
            if not self.email:
                print(f'Enter your credentials for the {self.__environment}.') 
                self.email = input('Email: ')
            if not self.__password:
                while self.user is None:
                    self.__password = getpass.getpass()
                    try:
                        self.user = self.ana_api.login(self.email, self.__password)
                    except requests.exceptions.ConnectionError as e:
                        print_color(f'Could not connect to API to login. Try again or contact support@rendered.ai for assistance.', 'ffff00')
                        raise AuthFailedError()
                    except requests.exceptions.JSONDecodeError:
                        print_color(f'Failed to login with email {self.email} at endpoint {self.__url}. Please confirm this is the correct email and endpoint, contact support@rendered.ai for assistance.', 'ffff00')
                        raise AuthFailedError()
            if self.user is None:
                try: self.user = self.ana_api.login(self.email, self.__password)
                except AuthFailedError as e:
                    print_color(f'Failed to login to {self.__environment} with email {self.email}.', 'ffff00')
                    raise AuthFailedError()
                except requests.exceptions.ConnectionError as e:
                    print_color(f'Could not connect to API to login. Try again or contact support@rendered.ai for assistance.', 'ffff00')
                    raise AuthFailedError()
                except requests.exceptions.JSONDecodeError as e:
                    print_color(f'Failed to login with email {self.email} and endpoint {self.__url}. Please confirm this is the correct email and endpoint, contact support@rendered.ai for assistance.', 'ffff00')
                    raise AuthFailedError()
            if self.user is False: 
                print_color(f'Failed to login to {self.__environment} with email {self.email}.', 'ffff00') 
                raise AuthFailedError()
            if self.verbose == 'debug': print(f'{self.user["uid"]}\n{self.user["idtoken"]}')
            self.__logout = False
            self.ana_api = api(self.__url, self.__status_url, {'uid':self.user['uid'], 'idtoken':self.user['idtoken']}, self.verbose)
            self.get_organizations()
            if len(self.organizations) == 0: print("No organizations available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); return
            found_valid_org = False
            for organization in self.organizations:
                if organization['expired'] and self.interactive:
                    print("Warning!!!")
                    print(f"\tThe subscription has expired for {organization['name']} organization (organizationId {organization['organizationId']}).") 
                    print("\tUpdate the subscription by signing into deckard.rendered.ai or contact sales@rendered.ai.")
                else:
                    found_valid_org = True
            if not found_valid_org:
                print_color("Error: found no valid organizations. If you believe this is a mistake, contact Rendered.ai at bugs@rendered.ai.", 'ffff00')
                raise AuthFailedError()
            self.get_workspaces()
            if len(self.workspaces) == 0: 
                self.workspace = None
                if self.interactive:
                    print("No workspaces available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); 
            self.get_channels()
            self.get_volumes()
            if workspaceId:     
                workspaces = [workspace for workspace in self.workspaces if workspace['workspaceId'] == workspaceId]
                if len(workspaces) == 0: print(f'Workspace with workspaceId {workspaceId} not found.')
                else:
                    self.workspace = workspaces[0]['workspaceId']
                    self.organization = workspaces[0]['organizationId']
            else:
                self.workspace = self.workspaces[0]['workspaceId']
                self.organization = self.workspaces[0]['organizationId']
                if self.interactive: 
                    print(f'These are your organizations and workspaces:')
                    for organization in self.organizations:
                        print(f"    {organization['name']+' Organization'[:44]:<44}  {organization['organizationId']:<50}")
                        for workspace in self.workspaces:
                            if workspace["organizationId"] == organization["organizationId"]:
                                print(f"\t{workspace['name'][:40]:<40}  {workspace['workspaceId']:<50}")
            if self.interactive: 
                print(f'Signed into {self.__environment} with {self.email}')
                print(f'The current organization is: {self.organization}')
                print(f'The current workspace is: {self.workspace}')

    def sign_in_apikey(self, interactive):
        from anatools.anaclient.api import api
        from anatools.lib.print import print_color
        from datetime import datetime
        import requests

        self.__logout = False

        try:
            self.ana_api = api(self.__url, self.__status_url, {'apikey':self.__APIKey}, self.verbose)
            apikeydata = self.ana_api.getAPIKeyContext(apiKey=self.__APIKey)
            if not apikeydata:
                print_color("Invalid API Key", 'ffff00')
                raise AuthFailedError()
        except requests.exceptions.ConnectionError as e:
            print_color(f'Could not connect to API to login. Try again after a while or contact support@rendered.ai for assistance.', 'ffff00')
            return        

        # check the key is not expired
        apikey_date = datetime.strptime(apikeydata['expiresAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        current_date = datetime.now()
        if apikey_date < current_date:
            print_color(f"API Key expired at {apikey_date}", 'ffff00')
            raise AuthFailedError()
        

        self.organization = apikeydata['organizationId']
        self.organizations = self.get_organizations(apikeydata['organizationId'])

        # check the organization is not expired
        if self.organizations[0]['expired']:
            print("Warning!!!")
            print(f"    The subscription has expired for {self.organizations[0]['name']} organization (organizationId {self.organizations[0]['organizationId']}).") 
            print("    Update the subscription by signing into deckard.rendered.ai or contact sales@rendered.ai.")

        self.workspaces = self.get_workspaces(organizationId=self.organization)
        if len(self.workspaces) == 0: 
            self.workspace = None
            print("No workspaces available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); 
            return

        self.workspace = self.workspaces[0]['workspaceId']
        self.get_channels(organizationId=self.organization)
        self.get_volumes(organizationId=self.organization)

        if interactive: 
            print(f'This is your organization and workspaces:')
            print(f"    {self.organizations[0]['name']+' Organization'[:44]:<44}  {self.organizations[0]['organizationId']:<50}")
            for workspace in self.workspaces:
                print(f"\t{workspace['name'][:40]:<40}  {workspace['workspaceId']:<50}")

            print(f'The current organization is: {self.organization}')
            print(f'The current workspace is: {self.workspace}')

    def refresh_token(self):
        import time
        import requests
        from anatools.anaclient.api import api
        from anatools.lib.print import print_color
        if self.user:
            if int(time.time()) > int(self.user['expiresAt']):
                self.user = self.ana_api.login(self.email, self.__password)
                self.ana_api = api(self.__url, self.__status_url, {'uid': self.user['uid'], 'idtoken': self.user['idtoken']}, self.verbose)
                
                 # fetch system notification
                try:
                    notification = self.ana_api.getSystemNotifications()
                    self.__notificationId = notification['notificationId']
                    if notification and notification['notificationId'] != self.__notificationId:
                        self.__notificationId = notification['notificationId']
                        print_color(notification['message'], 'ffff00')
                except requests.exceptions.ConnectionError as e:
                        print_color(f"Could not get notifications: {e}", 'ffff00')
        
                
        

    def check_logout(self):
        if self.__logout: print('You are currently logged out, login to access the Rendered.ai Platform.'); return True
        self.refresh_token()
        return False


    def logout(self):
        """Logs out of the ana sdk and removes credentials from ana."""
        if self.check_logout(): return
        self.__logout = True
        del self.__password, self.__url, self.user


    def login(self, workspaceId=None, environment='prod', email=None, password=None, local=False, interactive=True, verbose=None):
        """Log in to the SDK. 
        
        Parameters
        ----------
        workspaceId: str
            ID of the workspace to log in to. Uses default if not specified.
        environment: str
            Environment to log into. Defaults to production.
        email: str
            Email for the login. Will prompt if not provided.
        password: str
            Password to login. Will prompt if not provided.
        local: bool
            Used for development to indicate pointing to local API.
        interactive: bool
            Set to False for muting the login messages.
        verbose: str
            Flag to turn on verbose logging. Use 'debug' to view log output.
        
        """
        self.__init__(workspaceId, environment, email, password, local, interactive, verbose)


    def get_system_status(self, serviceId=None, display=True):
        """Fetches the system status, if no serviceId is provided it will fetch all services. 
        
        Parameters
        ----------
        serviceId: str
            The identifier of the service to fetch the status of.
        display: bool
            Boolean for either displaying the status or returning as a dict.
        """
        from anatools.lib.print import print_color
        services = self.ana_api.getSystemStatus(serviceId)
        if services and display:
            spacing = max([len(service['serviceName']) for service in services])+4
            print('Service Name'.ljust(spacing, ' ')+'Status')
            for service in services:
                print(service['serviceName'].ljust(spacing, ' '), end='')
                if service['status'] == 'Operational': print_color('Operational', '00ff00')
                elif service['status'] == 'Degraded': print_color('Degraded', 'ffff00')
                elif service['status'] == 'Down': print_color('Down', 'ff0000')
                else: print('?')
            return
        return services



    
    from .organizations import get_organization, set_organization, get_organizations, edit_organization, get_organization_members, get_organization_invites, add_organization_member, edit_organization_member, remove_organization_member, remove_organization_invitation
    from .workspaces    import get_workspace, set_workspace, get_workspaces, create_workspace, edit_workspace, delete_workspace, remove_workspace_invitation
    from .graphs        import get_graphs, create_graph, edit_graph, delete_graph, download_graph, get_default_graph, set_default_graph
    from .staged_graphs import get_staged_graphs, create_staged_graph, edit_staged_graph, delete_staged_graph, download_staged_graph
    from .datasets      import get_datasets, get_dataset_jobs, create_dataset, edit_dataset, delete_dataset, download_dataset, cancel_dataset, upload_dataset, get_dataset_runs, get_dataset_log, get_dataset_files
    from .channels      import get_channels, get_channel_nodes, get_managed_channels, create_managed_channel, edit_managed_channel, delete_managed_channel, build_managed_channel, deploy_managed_channel, get_deployment_status, get_channel_documentation, upload_channel_documentation, get_node_documentation
    from .volumes       import get_volumes, get_managed_volumes, create_managed_volume, edit_managed_volume, delete_managed_volume, get_volume_data, download_volume_data, upload_volume_data, delete_volume_data, mount_volumes
    from .analytics     import get_analytics, download_analytics, get_analytics_types, create_analytics, delete_analytics
    from .annotations   import get_annotations, get_annotation_formats, get_annotation_maps, create_annotation, download_annotation, delete_annotation , get_managed_maps, create_managed_map, edit_managed_map, delete_managed_map, download_managed_map
    from .gan           import get_gan_models, get_gan_datasets, create_gan_dataset, delete_gan_dataset, create_managed_gan, delete_gan_model, get_managed_gans, edit_managed_gan, delete_managed_gan, download_managed_gan
    from .umap          import get_umaps, create_umap, delete_umap
    from .api_keys      import get_api_keys, create_api_key, delete_api_key, get_api_key_data
    from .llm           import get_llm_response, create_llm_prompt, delete_llm_prompt, get_llm_base_channels, get_llm_channel_node_types
    from .editor        import create_remote_development, delete_remote_development, list_remote_development, stop_remote_development, start_remote_development, prepare_ssh_remote_development, remove_ssh_remote_development
    from .ml            import get_ml_architectures, get_ml_models, create_ml_model, delete_ml_model, edit_ml_model, download_ml_model, upload_ml_model, get_ml_inferences, get_ml_inference_metrics, create_ml_inference, delete_ml_inference, download_ml_inference
    from .inpaint       import get_inpaints, get_inpaint_logs, create_inpaint, delete_inpaint
    from .preview       import get_preview, create_preview 
    from .image         import get_image_annotation, get_image_mask, get_image_metadata