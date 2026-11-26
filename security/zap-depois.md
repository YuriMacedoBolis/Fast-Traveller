# fast Traveller - OWASP ZAP

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 2 |
| Low | 1 |
| Informational | 5 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP errors logged - see the zap.log file for details | 1    |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 99    |
| Info | Informational |  | Percentage of network failures | 1 % |
| Info | Informational | http://localhost:8000 | Percentage of responses with status code 2xx | 55 % |
| Info | Informational | http://localhost:8000 | Percentage of responses with status code 3xx | 1 % |
| Info | Informational | http://localhost:8000 | Percentage of responses with status code 4xx | 43 % |
| Info | Informational | http://localhost:8000 | Percentage of endpoints with content type application/javascript | 4 % |
| Info | Informational | http://localhost:8000 | Percentage of endpoints with content type application/json | 16 % |
| Info | Informational | http://localhost:8000 | Percentage of endpoints with content type text/html | 79 % |
| Info | Informational | http://localhost:8000 | Percentage of endpoints with method GET | 87 % |
| Info | Informational | http://localhost:8000 | Percentage of endpoints with method POST | 12 % |
| Info | Informational | http://localhost:8000 | Count of total endpoints | 24    |
| Info | Informational | http://localhost:8000 | Percentage of slow responses | 4 % |
| Info | Informational | https://localhost:8000 | Percentage of endpoints with method GET | 100 % |
| Info | Informational | https://localhost:8000 | Count of total endpoints | 1    |




## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| HTTP Only Site | Medium | 1 |
| Sub Resource Integrity Attribute Missing | Medium | Systemic |
| Server Leaks Version Information via "Server" HTTP Response Header Field | Low | Systemic |
| Authentication Request Identified | Informational | 3 |
| Modern Web Application | Informational | 1 |
| Session Management Response Identified | Informational | 6 |
| User Agent Fuzzer | Informational | Systemic |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 9 |




## Alert Detail



### [ HTTP Only Site ](https://www.zaproxy.org/docs/alerts/10106/)



##### Medium (Medium)

### Description

The site is only served under HTTP and not HTTPS.

* URL: http://localhost:8000/viagens/nova/
  * Node Name: `https://localhost:8000/viagens/nova/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: `Failed to connect.
ZAP attempted to connect via: https://localhost:8000/viagens/nova/`


Instances: 1

### Solution

Configure your web or application server to use SSL (https).

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
* [ https://letsencrypt.org/ ](https://letsencrypt.org/)


#### CWE Id: [ 311 ](https://cwe.mitre.org/data/definitions/311.html)


#### WASC Id: 4

#### Source ID: 1

### [ Sub Resource Integrity Attribute Missing ](https://www.zaproxy.org/docs/alerts/90003/)



##### Medium (High)

### Description

The integrity attribute is missing on a script or link tag served by an external server. The integrity tag prevents an attacker who have gained access to this server from injecting a malicious content.

* URL: http://localhost:8000
  * Node Name: `http://localhost:8000`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`
  * Other Info: ``
* URL: http://localhost:8000/
  * Node Name: `http://localhost:8000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`
  * Other Info: ``
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`
  * Other Info: ``
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`
  * Other Info: ``
* URL: http://localhost:8000/login/%3Fnext=/viagens/
  * Node Name: `http://localhost:8000/login/ (next)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">`
  * Other Info: ``

Instances: Systemic


### Solution

Provide a valid integrity attribute to the tag.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity ](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)


#### CWE Id: [ 345 ](https://cwe.mitre.org/data/definitions/345.html)


#### WASC Id: 15

#### Source ID: 3

### [ Server Leaks Version Information via "Server" HTTP Response Header Field ](https://www.zaproxy.org/docs/alerts/10036/)



##### Low (High)

### Description

The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.

* URL: http://localhost:8000/
  * Node Name: `http://localhost:8000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `WSGIServer/0.2 CPython/3.13.17`
  * Other Info: ``
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `WSGIServer/0.2 CPython/3.13.17`
  * Other Info: ``
* URL: http://localhost:8000/robots.txt
  * Node Name: `http://localhost:8000/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `WSGIServer/0.2 CPython/3.13.17`
  * Other Info: ``
* URL: http://localhost:8000/sitemap.xml
  * Node Name: `http://localhost:8000/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `WSGIServer/0.2 CPython/3.13.17`
  * Other Info: ``
* URL: http://localhost:8000/viagens/
  * Node Name: `http://localhost:8000/viagens/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `WSGIServer/0.2 CPython/3.13.17`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.

### Reference


* [ https://httpd.apache.org/docs/current/mod/core.html#servertokens ](https://httpd.apache.org/docs/current/mod/core.html#servertokens)
* [ https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10) ](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10))
* [ https://www.troyhunt.com/shhh-dont-let-your-response-headers/ ](https://www.troyhunt.com/shhh-dont-let-your-response-headers/)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (Low)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: `password1`
  * Other Info: `userParam=email
userValue=zaproxy@example.com
passwordParam=password1
referer=http://localhost:8000/cadastro/
csrfToken=csrfmiddlewaretoken`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=ZAP
passwordParam=password
referer=http://localhost:8000/login/
csrfToken=csrfmiddlewaretoken`
* URL: http://localhost:8000/login/%3Fnext=/viagens/
  * Node Name: `http://localhost:8000/login/ (next)(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=ZAP
passwordParam=password
referer=http://localhost:8000/login/?next=/viagens/
csrfToken=csrfmiddlewaretoken`


Instances: 3

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Modern Web Application ](https://www.zaproxy.org/docs/alerts/10109/)



##### Informational (Medium)

### Description

The application appears to be a modern web application. If you need to explore it automatically then the Ajax Spider may well be more effective than the standard one.

* URL: http://localhost:8000/api/docs/
  * Node Name: `http://localhost:8000/api/docs/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script src="/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.js"></script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`


Instances: 1

### Solution

This is an informational alert and so no changes are required.

### Reference




#### Source ID: 3

### [ Session Management Response Identified ](https://www.zaproxy.org/docs/alerts/10112/)



##### Informational (Medium)

### Description

The given response has been identified as containing a session management token. The 'Other Info' field contains a set of header tokens that can be used in the Header Based Session Management Method. If the request is in a context which has a Session Management Method set to "Auto-Detect" then this rule will change the session management to use the tokens identified.

* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://localhost:8000/login/%3Fnext=/viagens/
  * Node Name: `http://localhost:8000/login/ (next)(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`


Instances: 6

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/)



#### Source ID: 3

### [ User Agent Fuzzer ](https://www.zaproxy.org/docs/alerts/10104/)



##### Informational (Medium)

### Description

Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.

* URL: http://localhost:8000/viagens/2/relatorio/
  * Node Name: `http://localhost:8000/viagens/2/relatorio/`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:8000/viagens/2/relatorio/csv/
  * Node Name: `http://localhost:8000/viagens/2/relatorio/csv/`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:8000/viagens/nova/
  * Node Name: `http://localhost:8000/viagens/nova/`
  * Method: `GET`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution



### Reference


* [ https://owasp.org/wstg ](https://owasp.org/wstg)



#### Source ID: 1

### [ User Controllable HTML Element Attribute (Potential XSS) ](https://www.zaproxy.org/docs/alerts/10031/)



##### Informational (Low)

### Description

This check looks at user-supplied input in query string parameters and POST data to identify where certain HTML attribute values might be controlled. This provides hot-spot detection for XSS (cross-site scripting) that will require further review by a security analyst to determine exploitability.

* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
email=zaproxy@example.com

The user-controlled value was:
zaproxy@example.com`
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `first_name`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
first_name=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `password1`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password1=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `password2`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password2=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/cadastro/
  * Node Name: `http://localhost:8000/cadastro/ ()(csrfmiddlewaretoken,email,first_name,password1,password2,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `password`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/login/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/login/
  * Node Name: `http://localhost:8000/login/ ()(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/login/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/login/%3Fnext=/viagens/
  * Node Name: `http://localhost:8000/login/ (next)(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `password`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/login/?next=/viagens/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password=ZAP

The user-controlled value was:
zap`
* URL: http://localhost:8000/login/%3Fnext=/viagens/
  * Node Name: `http://localhost:8000/login/ (next)(csrfmiddlewaretoken,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://localhost:8000/login/?next=/viagens/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=ZAP

The user-controlled value was:
zap`


Instances: 9

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


