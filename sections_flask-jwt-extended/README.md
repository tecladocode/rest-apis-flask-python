# Flask-jwt-extended Section

This section presents the basic usage of an active flask JWT extension called `flask-jwt-extended`. We inherited and simplified the project structure from section 6 to demonstrate how to apply `flask-jwt-extended` to our project. 

## Features
 - JWT authentication
 - Token refreshing
 - Fresh token vs. Non-fresh token
 - Adding claims to JWT payload
 - Blacklist and token revoking
 - Customize JWT response/error message callbacks
 
## Related Resources

### UserLogin

- `POST: /login`
    - Description: authenticate a user and ,if authenticated, respond with a fresh access token and a refresh token.

### TokenRefresh

- `POST: /refresh`
    - Description: This endpoint is used to refresh an expired access token. If the refresh token is valid, respond with a new valid access token (non-fresh). 
    - Request header: `Authorization Bearer <refresh_token>`    

### Item

- `GET: /item/<name>`
    - Description: get an item by name, require a valid access token to access this endpoint.
    - Request header: `Authorization Bearer <access_token>`
- `POST: /item/<name>`
    - Description: create a new item, require a valid and fresh access token to access this endpoint.
    - Request header: `Authorization Bearer <access_token>`
- `DELETE: /item/<name>`
    - Description: delete an item by name, require a valid access token and admin privilege.
    - Request header: `Authorization Bearer <access_token>`
    
### ItemList

- `GET: /items`
    - Description: get all items, half protected. User can get more detailed info when providing an access token.  
    - Request header: `Authorization Bearer <access_token>`

        




