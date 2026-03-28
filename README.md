<img src="./public/demo.png" alt="Demo" width="100%" align="center"/>

---

[![wakatime](https://wakatime.com/badge/user/9a827e04-5df8-4525-ace8-e88326bbf87a/project/ae998970-e02b-47a4-acbe-a48650c8551f.svg)](https://wakatime.com/badge/user/9a827e04-5df8-4525-ace8-e88326bbf87a/project/ae998970-e02b-47a4-acbe-a48650c8551f) 
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/watch?v=9jkqToUvmZ4)

---

> [!NOTE]
> Main Backend server hosted on Render. It is a REST API server built using **[FastAPI](https://fastapi.tiangolo.com/)** and **[Agno](https://docs.agno.com/introduction)**. It is hosted on Render.
> The server is responsible for handling all the requests from the frontend and processing them.
> It also interacts with the Agno AI to get the predictions for the stock prices.


## Local Development

This project uses **[uv](https://github.com/astral-sh/uv)** for fast Python package management.

### Installation

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral-sh.uv.io/install.sh | sh
```

2. Sync dependencies and create a virtual environment:
```bash
uv sync
```

3. Run the server locally:
```bash
uv run uvicorn app:app --reload
```

## Deployment

The backend server can be locally deployed using Docker.
 Use the following command to build and run the server:

- **Build the Docker image**

```bash
docker-compose build
```

- **Run the Docker container**

```bash
docker-compose up
```

- **Access the server**

```bash
http://localhost:8000/
```

### API Documentation

The API documentation is available at the following URL:

```bash
http://localhost:8000/docs
```

This documentation provides a detailed overview of all the available endpoints, including their request and response formats. You can also test the endpoints directly from the documentation.

## Test the API

You can test the API using Postman or any other API testing tool. The following endpoints are available:

- /chat
- /agent
- /stock
- /stock-analysis
- /stock-news
- /top-stocks

## Tech Stack

<table>
    <tr>
        <td><img src="https://skillicons.dev/icons?i=fastapi" height=24 width=24></td>
        <td>FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.</td>
    </tr>
    <tr>
        <td><img src="https://avatars.githubusercontent.com/u/104874993?s=24"></td>
        <td>Agno is a lightweight library for building multi-modal Agents.
</td>
    </tr>
    <tr>
        <td><img src="https://github.com/user-attachments/assets/d7439975-103a-4251-a341-1758729f0ab6" height=24 width=36></td>
        <td>Render is a cloud provider that makes deploying your code as easy as deploying to localhost. You can deploy anything that runs on a single port.</td>
    </tr>
    <tr>
        <td><img src="https://skillicons.dev/icons?i=docker" height=24 width=24></td>
        <td>Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers</td>
    </tr>
    <tr>
        <td><img src="https://skillicons.dev/icons?i=redis" height=24 width=24></td>
        <td>Redis is a free, open-source, in-memory database that stores data as key-value pairs. It's often used as a cache, message broker, or database for quick responses.</td>
    </tr>
</table>

### Workflow:

<img src="./public/workflow.png" alt="Workflow" width="100%" align="center"/>






---

<a href="https://github.com/yashksaini-coder">
    <table>
        <tbody>
            <tr>
                <td align="left" valign="top" width="14.28%">
                    <img src="https://github.com/yashksaini-coder.png?s=60" width="130px;"/>
                    <br/>
                    <h4 align="center">
                        <b>Yash K. Saini</b>
                    </h4>
                    <div align="center">
                        <p>(Author)</p>
                    </div>
                </td>
                <td align="left" valign="top" width="85%">
                    <p>
                        👋 Hi there! I'm <u><em><strong>Yash K. Saini</strong></em></u>, a self-taught software developer and a computer science student from India.
                    </p>
                    <ul>
                     <li>
                        I love building & contributing to Open Source software solutions & projects that help solve real-world problems.
                    </li>
                    <li>
                        I want to build products & systems that can benefit & solve problems for many other DEVs.
                    </li>
                </td>
            </tr>
        </tbody>
    </table>
</a>

<p align="center">
    <strong>🌟 If you find this project helpful, please give it a star on GitHub! 🌟</strong>
</p>
