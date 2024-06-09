


# 🥛- Hacktimel Checker-🥛
> ## Checker **netflix**, amazon & disney **(NL/ML)** adapté en bot Telegram

### Vidéo présentative 
https://github.com/capabl1/checker-hacktimel/assets/137472232/1db388e4-6e34-4b3d-abc6-ea155c32666b
### Fonction du bot
La source ressemble à n'importe quoi et y'a 0 organisation, c'est normal si vous comprennez rien et ne vous retrouvez pas
C'est pareil pour ce readme, il est fait à l'arrache mais au moins j'ai mits un peu d'effort

Ah et non pas besoin de dénicher ou quoi j'ai pas mits de stealer sayez on est en 2024 faut murire un peu
| Fonctions     | Disponibilité |
| ---      | ---       |
| Trieur d'opérateur                  | ✅                               |
| Bin checker         | ✅                               |
| Checker Disney         | ✅             |
| Checker amazon           | ✅                                  |
| Checker netflix NL            | ✅                                |
| Checker netflix ML              | ❌                                      |
| Générateur de Numéro                  | ✅                      |
| Debouncer ML                    | ❌                     |


### Si vous avez besoin d'aide -> @NEWS4CTIMEL 

> [!NOTE]
> Cetain fonctions marchent probablement plus et ont été patch suite à une modification externe ne concernant pas la source directement, notamment le checker netflix ML ( plus d'info en bas )



## Crédits & License
Je souhaite à remercier ses 2 personnes à avoir bosser sur le projet ( Même si ça pas vraiment été sérieux ou concratiser )

👤 Billy: [@**billythegoat356**](https://github.com/billythegoat356)<br>
👤 Bluered: [@**BlueRed**](https://github.com/CSM-BlueRed)<br>
👤 KazenLpb: [@**Kazen**](https://github.com/capabl1)<br>

# Fonctionement du checker Disney
## J'ai fais le texte en anglais de base pour une autre de mes repos donc flemme de la traduire 
# Disney-Checker

**Simple disney checker no ratelimite with auth req**


- Fetch all the registered email on Disney plus based on a email list ( txt file )
  
``` 
[GET] https://disney.api.edge.bamgrid.com/v1/public/graphql
```


> function that extracts and returns THE authorization token from THE request's headers SINCE it is expiring every 1 hour ( or maybe + ), removing the "Bearer " prefix if present for a correct string, you can try first with getting it manually

```JS
const auth = (request) => {
  const authorizationHeader = request.headers['authorization'];
  const authorizationToken = authorizationHeader ? authorizationHeader.replace(/^Bearer /, '') : '';
  return authorizationToken;
};
```




| Name     | Headers |
| ---      | ---       |
| Accept                  | application/json                                |
| Accept-Encoding         | gzip, deflate, br                               |
| Accept-Language         | fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7             |
| authorization           | ( explained  )                                  |
| Content-Type            | application/json                                |
| Connection              | keep-alive                                      |
| Host                    | disney.api.edge.bamgrid.com                     |
| Origin                  | https://www.disneyplus.com                      |
| Referer                 | https://www.disneyplus.com/                     |
| Sec-Ch-Ua               | "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111" |
| Sec-Ch-Ua-Mobile        | ?0                                              |
| Sec-Ch-Ua-Platform      | "Windows"                                       |
| Sec-Fetch-Dest          | empty                                           |
| Sec-Fetch-Mode          | cors                                            |
| Sec-Fetch-Site          | cross-site                                      |
| User-Agent              | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 |
| X-Application-Version   | 1.1.2                                           |
| X-Bamsdk-Client-Id      | disney-svod-3d9324fc                            |
| X-Bamsdk-Platform       | javascript/windows/chrome                       |
| X-Bamsdk-Platform-Id    | browser                                         |
| X-Bamsdk-Version        | 22.1                                            |
| X-Dss-Edge-Accept       | vnd.dss.edge+json; version=2                    |
| X-Request-Id            | 857325bc-a6b5-4561-90ee-190596333826            |




Made with 🫀 by kAzen ( capabl1 )

# Fonctionement du checker NETFLIX
## Pour commencer, j'aimerais vous dire que celle-ci n'a pas été écris pour être publier sur une repo github. De base, c'était un petit rapport "Bug-Bounty" ( Oui je sais, c'est pas ouf pour un rapport mais bon ). Aussi, j'ai fais le texte en anglais de base, donc un peu la flemme de traduire moi tout seul à la main le texte donc si c'est pas parfaitement exprimé c'est normal, merci à gpt pour le chantier.

Format bugcrowd mes couilles
> VRT : Server Security Misconfiguration > Directory Listing Enabled > Sensitive Data Exposure

> Target category : Web App

> Bug URL : https://www.netflix.com/login

# Phone Number Validation Vulnerability on Netflix.com (Low Severity)

## Overview of the Vulnerability

### Introduction

I'm relatively new to this field and have observed significant traffic related to email and phone numbers, specifically concerning Netflix. There's a surge in "Fake Netflix phishing" activities where malicious individuals create domains and websites that closely mimic Netflix's support and billing pages to exfiltrate sensitive data, such as credit card information and Netflix subscription details.

The core of this vulnerability lies in the scammers' ability to verify if phone numbers are associated with Netflix accounts, streamlining their phishing efforts.

### Technical Details

1 - **Bypassing reCAPTCHA**: Scammers attempt to bypass the reCAPTCHA security measure implemented on the Netflix website. They achieve this by sending a GET request to the URL "https://www.google.com/recaptcha/enterprise/anchor" to obtain a reCAPTCHA token. The token is extracted from the response HTML using tools like BeautifulSoup.

2 - **Obtaining reCAPTCHA information**: After bypassing the reCAPTCHA, scammers send a POST request to "https://www.google.com/recaptcha/enterprise/reload" to gather additional information related to reCAPTCHA. This information helps them bypass the reCAPTCHA based on its version (using the "recaptcha" header, for example).

3 - **Checking phone number validity**: Once the reCAPTCHA is bypassed, scammers check if a phone number is valid by directly sending a request to the Netflix login page at "https://www.netflix.com/login". They analyze the response content to determine if the phone number is registered with Netflix. If the response does not contain any content, they follow the redirection specified in the "Location" header.

4 - **Extracting the authURL**: Scammers extract the "authURL" value from the login page HTML. This value is crucial for authentication and varies depending on the IP flags and country associated with the request.

5 - **Detecting phone number prefix**: A request is made to "https://www.netflix.com /personalization/cl2/freeform/WebsiteDetect?" to detect the phone number prefix. Scammers check the syntax and correctness of the prefix, and modify the country accordingly if necessary.

6 - **Crafting the request**: Scammers create a URL-encoded data dictionary and generate a random string for the password. They retrieve the necessary cookies from the session object and generate the required cookie string. The headers for the POST request to the login URL are constructed using these cookies and the content type.

7 - **Validating the phone number**: Scammers make the POST request to the login URL with the crafted data and headers to check if the phone number is valid or not based on the response.

### Suggested Mitigation Measures

- **Strengthen reCAPTCHA**: Enhance the reCAPTCHA mechanism to resist bypass attempts more effectively.
- **Implement Sophisticated Rate Limiting**: Introduce rate limiting to prevent repeated requests from the same sources.
- **Restrict Public Access to Phone Number Validity**: Ensure the public cannot access information about phone number registration status.

### Proof of Concept (PoC)
g plus et flm de retrouver, t'facon vous avez le code vous pouvez comprendre
