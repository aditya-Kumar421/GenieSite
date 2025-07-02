import requests
from django.conf import settings

def generate_page_content(industry):
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise Exception("Gemini API key not configured")

    prompt = f"""
    Generate content for a basic HTML webpage for a business in the '{industry}' industry. The content should include:
    - A title for the webpage
    - A short Home section (100-150 words)
    - An About section (150-200 words)
    - A Services section with 3-5 services (each with a title and 50-100 word description)
    - A Contact section with placeholder contact details (e.g., email, phone, address)
    Return the response in JSON format with the following structure:
    {{
        "title": "<page title>",
        "home": "<home section text>",
        "about": "<about section text>",
        "services": [
            {{"title": "<service title>", "description": "<service description>"}},
            ...
        ],
        "contact": "<contact section text>"
    }}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    result = response.json()
    content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
    import json
    return json.loads(content)  # Assuming Gemini returns JSON string

def create_html_page(content):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
            header {{ background-color: #333; color: white; text-align: center; padding: 1em; }}
            nav {{ background-color: #f4f4f4; padding: 1em; }}
            nav a {{ margin: 0 1em; text-decoration: none; color: #333; }}
            section {{ padding: 2em; }}
            footer {{ background-color: #333; color: white; text-align: center; padding: 1em; }}
        </style>
    </head>
    <body>
        <header>
            <h1>{title}</h1>
        </header>
        <nav>
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#services">Services</a>
            <a href="#contact">Contact</a>
        </nav>
        <section id="home">
            <h2>Home</h2>
            <p>{home}</p>
        </section>
        <section id="about">
            <h2>About</h2>
            <p>{about}</p>
        </section>
        <section id="services">
            <h2>Services</h2>
            {services}
        </section>
        <section id="contact">
            <h2>Contact</h2>
            <p>{contact}</p>
        </section>
        <footer>
            <p>&copy; {year} {title}. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """

    services_html = ""
    for service in content['services']:
        services_html += f"<h3>{service['title']}</h3><p>{service['description']}</p>"

    from datetime import datetime
    return html_template.format(
        title=content['title'],
        home=content['home'],
        about=content['about'],
        services=services_html,
        contact=content['contact'],
        year=datetime.now().year
    )