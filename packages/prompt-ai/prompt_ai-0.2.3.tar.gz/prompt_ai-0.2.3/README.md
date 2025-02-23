# Prompt-AI

## Overview

Prompt-AI is a Python library that automates the process of generating AI-powered newsletters. It scrapes content from a given URL, generates a structured newsletter using Google's Gemini API, and provides features for parsing content, sending emails, and creating blog page links.

## Features

- **AI Content Generation:** Uses Google's Gemini API to generate newsletters based on scraped content.
- **Email Sending:** Sends AI-generated newsletters via SMTP.
- **Blog Page Link Generation:** Creates links for blog pages in both local and live environments.

## Usage

### 1. Generate AI-Powered Newsletter
#### *api_key*:
- Generate your api key from [Gemini API](https://ai.google.dev/gemini-api/docs) 

#### *link*:
- Enter reference link for which you want to generate newsletter and blog article.
```python
from promptai import generate_content

api_key = "your-google-gemini-api-key"
title = "Latest Tech Trends"
category = "Technology"
link = "https://example.com/tech-news"

newsletter = generate_content(title, category, link, api_key)
print(newsletter)
```
#### Response (Success):
```json
{
  "title": "generated-title",
  "content": [
    {
      "subtitle": "generated-subtitle",
      "paragraph": "generated-inner-paragraph"
    },
    {
      "subtitle": "generated-subtitle",
      "paragraph": "generated-inner-paragraph"
    },
    {},
    ...
    //and many more according to the reference URL
  ],
  "tags": "generated tags for the blog",
  "category": "assigned category"
}
```

#### Response (Failed):

```json
{
  "status":203,
  "message":"Content not generated",
  "reason":"internal issue"
}
```

### 2. Send Newsletter via Email

#### SMTP Configuration

- Update `SMTP_SERVER` and `SMTP_PORT` for your email provider and keep it in environment variables.
- Use an app-specific password for secure email authentication.
```python
from promptai import send_email

receiver_email = "recipient@example.com" or ["comma separated multiple emails"]
sender_email = "your-email@example.com"
email_app_password = "your-email-app-password"
link = "generated-link-of-blog"
title = "generated-title"
description = "first-para-of-first-subtitle"
subject = "Your-subject-here"

send_email(receiver_email, sender_email, email_app_password, link, title, description, subject)
```
#### Response (Success):
```json
{"status":200, "message":"Email sent successfully"}
```

#### Response (Failed):
```json
{
  "status":203, 
  "message":"error in sending mail", 
  "reason":"reason-of-error" // Particular reason will be sent
}
```
### 3. Create Blog Page Link
#### *domain_name*:
- Enter only specific part of domain name.
- For `domain_type:"local"` example: `http://localhost:3000`, then `domain_name: localhost:3000`, if your domain also has a path then `domain_name: localhost:3000/path`.
- For `domain_type:"live"` example: `https://example.com`, then `domain_name:example.com`, if your domain also has a path then `domain_name: example.com/path`.
#### *domain_type*:
- "local": Use this if you are using promptai on unsecured network or on localhost, example: `http://localhost:3000`
- "live": For domains hosted on secured networks, `https://your-domain.com`

#### *title*:
- Send the same title which you got as response on using `generate_content` function.

```python
from promptai import create_blog_page

domain_name = "yourwebsite.com"
domain_type = "live"
title = "The Future of AI"

blog_link = create_blog_page(title, domain_type, domain_name)
print(blog_link)
```
#### Response (Success):
```json
{
  "status": 200, 
  "message": "Link generated",
  "link": "generated_link"  // Link generated will already be passed here
}
```

#### Response (Failed):
```json
{
  "status":203, 
  "message":"error generating link", 
  "reason":"domain type not specified" // If domain_type not specified
}
```

## License

This project is licensed under the MIT License.

## Contributions

Feel free to submit pull requests or report issues on GitHub.

## Contact

For inquiries or support, reach out at `gauravpatel29@outlook.in`.

