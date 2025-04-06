# AI-Powered Website Builder (Backend)

An intelligent backend engine built using **Python (Django)** and **MongoDB**, designed to power an **AI-driven website generator**. This system leverages **Mistral 7B Instruct** (via OpenRouter) to dynamically generate SEO-friendly and industry-specific website content.

---

## 🎯 Objective

Develop a robust backend system to enable:
- AI-assisted website generation from user input
- Full user authentication and session management
- Website content editing, saving, and previewing
- Scalable and secure architecture using Django and MongoDB

---
<h2>🚀 Documentation</h2>

[Postman-documentation](https://documenter.getpostman.com/view/41200302/2sB2cUC3e2)

---

## 🛠️ Features

### 🔐 User Authentication
- JWT-based authentication system.
- Sign-up / Login using email.
- Password hashing and secure token storage.

### 🤖 AI-Powered Website Generation
- Uses **Mistral 7B Instruct** model (via OpenRouter API).
- Accepts `business_type` and `industry` as input.
- Generates dynamic content (homepage text, about us, services).
- Stores generated content in MongoDB.

### 🗃️ Website Management APIs
- Create, Read, Update, Delete operations for user websites.
- Save user-edited content (text, images, layout).
- Fetch website structure for front-end rendering.

### 🌐 Hosting & Preview
- Generate temporary live preview URLs for sharing and testing.

### 🔐 Security & Performance
- JWT Authentication.
- API rate limiting.
- SSL, SSH, and XSS protection best practices.
- Response caching using **Upstash Redis** for performance.

---

## 🧱 Technology Stack

| Layer           | Tech                              |
|----------------|-----------------------------------|
| Backend         | Python, Django REST Framework     |
| Database        | MongoDB (via `pymongo`)           |
| AI Model        | Mistral 7B Instruct (OpenRouter)  |
| Auth            | JWT (SimpleJWT)                   |
| Caching         | Upstash Redis                     |
| Security        | SSL, HTTPS, XSS protection        |

---


  
<h2>🛠️ Installation Steps:</h2>

1. Clone the repository:

```CMD
git clone https://github.com/aditya-Kumar421/GenieSite.git
```

To run the server, you need to have Python installed on your machine. If you don't have it installed, you can follow the instructions [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install it.

2. Install and Create a virtual environment:

```CMD
python -m venv venv
```

3. Activate the virtual environment

```CMD
venv\Scripts\activate
cd webgen
```

4. Install the dependencies:

```CMD
pip install -r requirements.txt
```

5. Add .env file and include:
SECRET_KEY=your_django_secret_key
MONGO_URI=mongodb://localhost:27017/ or atlas URL
OPENROUTER_API_KEY=your_openrouter_api_key
UPSTASH_REDIS_REST_URL=your_upstash_url
UPSTASH_REDIS_REST_TOKEN=your_upstash_token



6. Run the Development Server:

```
python manage.py runserver
```


---

## 📡 API Overview

### 🔐 Auth Endpoints

| Method | Endpoint               | Description         |
|--------|------------------------|---------------------|
| POST   | `/user/register/`  | Register new user   |
| POST   | `/user/login/`     | Login and get JWT   |
| GET   | `/user/profile/`     | User profile via JWT  |


---

### 🗃️ Website Management

| Method | Endpoint                  | Description               |
|--------|---------------------------|---------------------------|
| GET    | `/website/`          | List user's websites      |
| POST   | `/website/`          | Create new website        |
| PUT    | `/website/<id>/`     | Update website content    |
| DELETE | `/website/<id>/`     | Delete website            |
| GET    | `/website/<id>/`     | Retrieve website content  |

---

### 🌐 Live Preview

| Method | Endpoint                         | Description                 |
|--------|----------------------------------|-----------------------------|
| GET    | `/websites/<id>/preview/`    | Generate preview URL        |

---

## 🙌 Contributing

Pull requests are welcome! If you’d like to contribute, please fork the repo and open a PR. For major changes, open an issue first to discuss what you’d like to change.

---



