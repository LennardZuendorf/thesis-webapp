# Links

- [GitHub Repository](https://github.com/LennardZuendorf/thesis-webapp) - The GitHub repository of this project.
- [HTW Berlin](https://www.htw-berlin.de/) - The University I have built this project for, as part of my thesis.
- [Thesis Print]() - Link to the thesis pdf (in English), containing more information about the project. And a full list of sources for this work as well as additional evaluations and fundamental information for the project.


# Credits
For full credits, please refer to the [thesis print]()

### Models
For this project, two different models are used. Both are used through Huggingface's [transformers](https://huggingface.co/docs/transformers/index) library.

##### LlaMa 2
LlaMa 2 is an open source model by Meta Research. See [offical paper](https://arxiv.org/pdf/2307.09288.pdf) for more information.

- the version used in this project is LlaMa 2 7B Chat HF (HF = special version for huggingface), see [huggingface model hub](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
- the model is fine-tuned for chat interactions by Meta Research

##### Mistral
Mistral is an open source model by Mistral AI. See [offical paper](https://arxiv.org/pdf/2310.06825.pdf) for more information.

- the version used in this project is Mistral Instruct, see [huggingface model hub](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1)
- the model is fine-tuned for instruction following by Mistral AI

### Libraries
This project uses a number of open source libraries, only the most important ones are listed below.

##### Shap
This application uses a custom version of the shap library, which is available at [GitHub](https://github.com/shap/shap).

- please refer to the [shap-adapter](https://github.com/LennardZuendorf/thesis-shap-adapter) repository for more information about the changes made to the library, specifically the README and CHANGES files
- the shap library and the used partition SHAP explainer are based on work by Lundberg et al. (2017), see [offical paper](https://arxiv.org/pdf/1705.07874.pdf) for more information

##### BertViz
This application uses a slightly customized version of the bertviz library, which is available at [GitHub](https://github.com/jessevig/bertviz)

- the bertviz was introduced by Vig et al. (2019), see [offical paper](https://arxiv.org/pdf/1906.05714.pdf) for more information
- there are no changes to the library itself, only to the way it is used in this project (adapted to use Mistral/LlaMa 2 instead of BERT)


# Data Protection
This is a non-commercial project, which does not collect any personal data. The only data collected is the data you enter into the application. This data is only used to generate the explanations and is not stored anywhere.
However, the application may be hosted with an external service (i.e. Huggingface Spaces), which may collect data. Please refer to the data protection policies of the respective service for more information.

If you use the "flag" feature, the data you enter will be stored in *publicly available* csv file.


# License
This Product is licensed under the MIT license. See [LICENSE](https://github.com/LennardZuendorf/thesis-webapp/blob/main/LICENSE.md) at GitHub for more information.
Please credit the original authors of this project (Lennard Zündorf) and the credits listed above if you use this project or parts of it in your own work.
