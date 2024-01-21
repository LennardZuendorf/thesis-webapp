# About

This is a non-commercial research projects as part of a Bachelor Thesis with the topic **"Building an Interpretable Natural Language AI Tool based on Transformer Models and Approaches of Explainable AI".**

This research tackles the rise of LLM based applications such a chatbots and explores the possibilities of model interpretation and explainability. The goal is to build a tool that can be used to explain the predictions of a LLM based chatbot.

## Links

- [GitHub Repository](https://github.com/LennardZuendorf/thesis-webapp) - The GitHub repository of this project.
- [HTW Berlin](https://www.htw-berlin.de/) - The University I have built this project for, as part of my thesis.


## Implementation

This project is an implementation of PartitionSHAP into GODEL by Microsoft - [GODEL Model](https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq) which is a generative seq2seq transformer fine-tuned for goal directed dialog. It supports context and knowledge base inputs.

The UI is build with Gradio, utilizing some custom components and FastAPI.

### Usage

You can chat with the model by entering a message into the input field and pressing enter. The model will then generate a response. You can also enter a context and knowledge base by clicking on the respective buttons and entering the data into the input fields. The model will then generate a response based on the context and knowledge base.

To explore explanations, chose one of the explanations methods (HINT: The runtime can increase significantly). Then keep on chatting and explore the explanations in the respective tab.

### Self Hosted

You can run this application locally by cloning this repository, setting up a python environment and installing the requirements from the requirements.txt. Then run the `app.py` file or use "uvicorn main:app --reload" in the *python terminal*.

For self-hosting you can use the Dockerfile to build a docker image and run it locally or directly use the provided docker image on the [GitHub page](https://github.com/lennardzuendorf/thesis-webapp/).

## Credit & License
This Product is licensed under the MIT license. See [LICENSE](https://github.com/LennardZuendorf/thesis-webapp/blob/main/LICENSE.md) at GitHub for more information.

Please credit the original authors of this project (Lennard Zündorf) and the credits listed below if you use this project or parts of it in your own work.

## Contact

### Author

- Lennard Zündorf
- [lennard.zuendorf@student.htw-berlin.de](mailto:lennard.zuendorf@student.htw-berlin.de) or [lennard@zuendorf.me](mailto:lennard@zuendorf.me)
- [GitHub](https://zuendorf.me/github)
- [LinkedIn](https://zuendorf.me/github)


### University
Hochschule für Technik und Wirtschaft Berlin (HTW Berlin) - University of Applied Sciences for Engineering and Economics Berlin

Supervisor: Prof. Dr. Katarina Simbeck
2. Corrector : Prof. Dr. Axel Hochstein
