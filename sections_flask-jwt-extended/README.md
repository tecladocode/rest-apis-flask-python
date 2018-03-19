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
    - Description: authenticate a user and ,if authenticated, respond with an access token and a refresh token.

### UserFreshLogin
- `POST: /fresh_login`
    - Description: authenticate a user and ,if authenticated, respond with a fresh access token.    

### Item

- `GET: /item/<name>`
    - Description: require a valid JWT to access this endpoint.
    - Request header: `Authorization Bearer <access_token>`
- `POST: /item/<name>`
    - Description: require a valid and fresh JWT to access this endpoint.
    - Request header: `Authorization Bearer <fresh_access_token>`
    
### ItemList

- `GET: /items`
    - Description: require a valid JWT and appropriate user privilege to access this endpoint. The user privilege is provided as claims within the JWT payload. 
    - Request header: `Authorization Bearer <access_token>`
    
### TokenRefresh

- `POST: /refresh`
    - Description: This endpoint is used to refresh an expired access token. If the refresh token is valid, respond with a new valid access token. 
    - Request header: `Authorization Bearer <refresh_token>`
        




