from google import genai
from google.genai import types
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
SMTP_SERVER = "smtp.gmail.com"  # GoDaddy Professional Email (Microsoft 365)
SMTP_PORT = 587

def scrape_paragraph_content(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text within paragraph (<p>) tags
        paragraphs = soup.find_all('p')
        paragraph_content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return paragraph_content
    except Exception as e:
        return f"An error occurred: {e}"

def parse_content(content, category):
    # Match the title (content between single * symbols)
    title_match = re.search(r"\*(.*?)\*", content)
    parsed_title = title_match.group(1).strip() if title_match else "Untitled"

    # Match the tag (content between **** symbols)
    tag_match = re.search(r"\*\*\*\*(.*?)\*\*\*\*", content)
    parsed_tag = tag_match.group(1).strip() if tag_match else "No tags formed"

    # Match sections with **subtitle** ***paragraph***
    sections_regex = re.compile(r"\*\*(.*?)\*\*\s*\*\*\*(.*?)\*\*\*")
    matches = sections_regex.findall(content)
    parsed_sections = [{"subtitle": match[0].strip(), "paragraph": match[1].strip()} for match in matches]

    # Get the current date
    current_date = datetime.now().date()

    # Create the data object
    data_obj = {
        "title": parsed_title,
        "tag": parsed_tag,
        "category": category,
        "date": current_date,
        "content": parsed_sections,
    }

    return data_obj

def generate_content(title, category, link, apikey):
    client = genai.Client(api_key=apikey)
    refer = scrape_paragraph_content(link)
    sys_instruct = f"You are a newsletter generating AI. Keep title within * symbol, subtitles within ** symbol, and paragraphs within *** symbol, and keep tags within two **** symbol and each tag must separate with a comma. generate newsletter taking reference from here: {refer} and keep the title relative to user input and refernce data provided"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct),
        contents= title
    )
    resp = response.candidates[0].content.parts[0].text
    result = parse_content(resp, category)
    return result

def send_email(receiver_email, sender_email, email_app_password, link, title, des, subject):
    try:
        # Email Content
        html_body = f"""
        <html>
            <body>
            <div style="text-align:center; width:100%; display:flex; justify-content:center">
                <div style="width:100%;text-align:center; align-items:center">
                    <h2 style="text-align:center; font-weight:600;">NewsletterAI</h2>
                    <p>An AI generated accurate & informative newsletter</p>
                    <br>
                    <a href={link}><h3>{title}</h3></a>
                    <p>{des}</p>
                    <br>
                    <p style="font-size:12px;color:gray;">If you did not subscribe, please ignore this email.</p>
                </div>
            </div>
            </body>
        </html>
        """

        # Set up the email message
        message = MIMEMultipart()
        message["From"] = sender_email  # Use the alias email here
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the HTML body
        message.attach(MIMEText(html_body, "html"))

        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(sender_email, email_app_password)  # Authenticate with the primary email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close the connection
        server.quit()

        print(f"Email sent successfully to {receiver_email} from {sender_email}")
        return {"status":200, "message":"Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status":203, "message":"error in sending mail", "reason":f"{e}"}

def create_blog_page(title, domain_type, domain_name):
    if domain_type == "local":
        parsed_title = urllib.parse.quote(title)
        generated_link = f"http://{domain_name}/?={parsed_title}"
        return {"status":200, "message":"Link generated", "link":generated_link}
    elif domain_type == "live":
        parsed_title = urllib.parse.quote(title)
        generated_link = f"https://{domain_name}/?={parsed_title}"
        return {"status": 200, "message": "Link generated", "link": generated_link}
    else:
        return{"status":203, "message":"error generating link", "reason":"domain type not specified"}