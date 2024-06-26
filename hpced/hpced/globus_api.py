import globus_sdk
import json
import os

# Constants
CLIENT_ID = os.getenv("CLIENT_ID") # App ID
INDEX_UUID = os.getenv("INDEX_UUID") # Database/catalog ID
TOKEN_FILE = 'globus_tokens.json' # Location to store API tokens for searching

# Function to load tokens from a file
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None

# Function to save tokens to a file
def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

# Function to refresh access token using refresh token
def refresh_access_token(refresh_token):
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    token_response = client.oauth2_refresh_token(refresh_token)
    new_tokens = token_response.by_resource_server['search.api.globus.org']
    return new_tokens['access_token'], new_tokens['refresh_token']

def queryHPC_ED(search_query: str, limit: int, filters: {str:any}):
    '''
    This function will query the HPC-ED catalog for the given query string and return
    a list of results, each of which is a dictionary of metadata.

    params:
    search_query    -> a string representing what to search for in the HPC-ED database/catalog
    limit           -> an integer representing the maximum number of search results to return
    filters         -> a dictionary with filter types as keys and the value to filter for as values
    '''
    # Check if tokens are stored and load them
    stored_tokens = load_tokens()

    if stored_tokens:
        access_token = stored_tokens['access_token']
        refresh_token = stored_tokens['refresh_token']
    else:
        # Perform initial authorization flow
        client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
        scopes = 'urn:globus:auth:scope:search.api.globus.org:all'
        client.oauth2_start_flow(requested_scopes=scopes)
        authorize_url = client.oauth2_get_authorize_url()
        print(f'Please go to this URL and login: {authorize_url}')
        auth_code = input('Enter the auth code here: ')
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)
        
        tokens = token_response.by_resource_server['search.api.globus.org']
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        save_tokens({'access_token': access_token, 'refresh_token': refresh_token})

    # Create a SearchClient with the access token
    authorizer = globus_sdk.AccessTokenAuthorizer(access_token)
    search_client = globus_sdk.SearchClient(authorizer=authorizer)

    # Refresh access token if needed
    try:
        search_client.get(f"/v1/index/{INDEX_UUID}")
    except globus_sdk.SearchAPIError as e:
        if e.http_status == 401:  # Unauthorized
            access_token, refresh_token = refresh_access_token(refresh_token)
            save_tokens({'access_token': access_token, 'refresh_token': refresh_token})
            authorizer = globus_sdk.AccessTokenAuthorizer(access_token)
            search_client = globus_sdk.SearchClient(authorizer=authorizer)

    search_result = search_client.search(
        index_id=INDEX_UUID,
        q=search_query,
        limit=limit,
    )

    entries = search_result["gmeta"]

    filtered_results = [] # A list containing a dictionary entry for each search result
    for entry in entries:
        metadata = entry["entries"][0]["content"] # Print metadata.keys() to show all of the keys to filter on
        
        # Apply each filter to the current entry and only add to results list if the entry matches the filters
        valid_filters = True # checks for valid filter string
        valid_filter_value = True # True if all filters apply to the current entry
        for filter_str in filters.keys():
            try:
                val = metadata[filter_str]
            except: # handle bad key error
                valid_filters = False
                break
            else:   # no error
                if val != filters[filter_str]:
                    valid_filter_value = False

        if not valid_filters or not valid_filter_value:
            continue

        filtered_results.append(entry)
    
    #for res in filtered_results:
        #print(json.dumps(res, indent=4))
    
    return filtered_results

#queryHPC_ED("*", 5, {"Rating":1.8, "Expertise_Level":["Intermediate"]})
#queryHPC_ED("*", 5, {})
