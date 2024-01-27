---
title: Thesis
emoji: 🎓
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 4.7.1
app_file: main.py
pinned: true
license: mit
app_port: 8080
models: ["microsoft/GODEL-v1_1-large-seq2seq"]
tags: ["CHAT", "XAI", "SHAP", "GODEL", "Gradio"]
disable_embedding: true
---

# Bachelor Thesis Webapp

## 📜 Info:
This is the ui showcase for my thesis about interpretability in a LLM based chatbot application and applications of XAI.

### 🔗 Links:

**[Github Repository](https://github.com/LennardZuendorf/thesis-webapp)**

**[Huggingface Spaces Showcase](https://huggingface.co/spaces/lennardzuendorf/thesis-webapp-docker)**

**[Non-Public Showcase]()**

### 🏗️ Tech Stack:

**Language and Framework:** Python

**Noteable Packages:** 🤗 Transformers, FastAPI, Gradio, SHAP, BERTViz

## 👨‍💻 Author:

**Author: [@LennardZuendorf](https://github.com/LennardZuendorf)**

**Thesis Supervisor: [Prof. Dr. Simbeck](https://www.htw-berlin.de/hochschule/personen/person/?eid=9862)**
<br> Second Corrector: [Prof. Dr. Hochstein](https://www.htw-berlin.de/hochschule/personen/person/?eid=10628)

This Project was part of my studies of Business Computing at University of Applied Science for Technology and Business Berlin (HTW Berlin).

##  Running the Project:

### 🐍 Python:

(This assumes you have set up a python environment, I recommend using a virtual environment.)

1. Clone the repository using git or GitHub cli.
2. Start the (virtual) environment.
3. Install the requirements using `pip install -r requirements.txt`
4. Run the app using `uvicorn main:app`. You can add `--reload` to enable hot reloading. The app will be available at `localhost:8000`.

### 🐳 Dockerfile:

(This assumes you have set up docker desktop or are using a hosting service able to handle Dockerfiles.)

1. Clone the repository using git or GitHub cli.
2. Build the docker image using `docker build -t thesis-webapp .`, the command commented in the docker file or the command referenced by your hosting service.
3. Run the docker image using `docker run -p 8080:8080 thesis-webapp`, the command commented in the docker file or the command referenced by your hosting service.
4. The app will be available at `localhost:8080`. If you are using a hosting service, the port may be different.

### 🐳 Docker Image:

(This assumes you have set up docker desktop or are using a hosting service able to handle Docker images.)

1. Pull the docker image from ghcr using `docker pull ghcr.io/LennardZuendorf/thesis-webapp:latest`.
2. Run the docker image using `docker run -p 8080:8080 lennardzuendorf/thesis-webapp:latest`, the command commented in the docker file or the command referenced by your hosting service.
3. The app will be available at `localhost:8080`. If you are using a hosting service, the port may be different.

## 📝 License and Credits:

This project is licensed under the MIT License, see [LICENSE](LICENSE.md) for more information. Please cite this project, it's author and my university if you use it in your work.

- Title: Building an Interpretable Natural Language AI Tool based on Transformer Models and approaches of Explainable AI.
- Date: 2024-01-27
- Author: Lennard Zündorf
- University: HTW Berlin

See code for in detailed credits, work is strongly based on:
#### GODEL
- [HGF Model Page](https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq?text=Hey+my+name+is+Mariama%21+How+are+you%3F)
- [Paper on HGF](https://huggingface.co/papers/2206.11309)
- [Paper Print](https://arxiv.org/abs/2206.11309)

#### SHAP
- [Github](https://github.com/shap/shap)
- [Inital Paper](https://arxiv.org/abs/1705.07874)
