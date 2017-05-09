# Canvas LMS Analytics
Generates analytical reports using data from UT Austin's Canvas LMS Instance

## How to Generate Authentication Token
Go to https://<your canvas instance>.instructure.com/profile/settings

From there, generate a new access token. You should see the following modal:

![authentication token](images/auth_token_gen.png)

Modify the following line of code with your newly generated authentication token:

'''
# authentication token for testing
auth_token = "<Your authentication token>"

'''


