# Credits

### Models
This implementation is build on GODEL by Microsoft, Inc. and Mistral 7B Instruct by Mistral AI.

##### Mistral 7B Instruct
Mistral 7B Instruct is an open source model by Mistral AI. See [offical paper](https://arxiv.org/abs/2310.06825) for more information.

- the version used in this project is Mistral 7B Instruct v0.2, see [huggingface model hub](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)
- the model is an autoregressive language model fine-tuned for instruction following

##### GODEL
GODEL is an open source model by Microsoft. See [offical paper](https://arxiv.org/abs/2206.11309) for more information.

- the version used in this project is GODEL Large, see [huggingface model hub](https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq?text=Hey+my+name+is+Thomas%21+How+are+you%3F)
- the model as is a generative seq2seq transformer fine-tuned for goal directed dialog

### Libraries
This project uses a number of open source libraries, only the most important ones are listed below.

#### captum
This application uses the captum library for the interpretation of the Mistral 7B Instruct model. The captum library is available at [GitHub](https://github.com/pytorch/captum).

- Please refer to the [captum](https://captum.ai/) website for more information about the library.
- The used KernelExplainer is based on work by Lundberg et al. - see below for more information.
- For original paper about captum see [Inital Paper](https://arxiv.org/pdf/2009.07896.pdf).

##### Shap
This application uses a custom version of the shap library, which is available at [GitHub](https://github.com/shap/shap).

- Please refer to the [thesis-shap](https://github.com/LennardZuendorf/thesis-custom-shap) repository for more information about the changes made to the library, specifically the README file.
- The shap library and the used partition SHAP explainer are based on work by Lundberg et al. (2017), see [offical paper](https://arxiv.org/pdf/1705.07874.pdf) for more information.

##### Visualizations
This application uses attention visualization inspired by the bertviz library, which is available at[GitHub](https://github.com/jessevig/bertviz). It doesn't actually use BERTViz.

- The bertviz was introduced by Vig et al. (2019), see [offical paper](https://arxiv.org/pdf/1906.05714.pdf) for more information.
- This project only uses decoder attention visualization with gradio and matplotlib and not BERTViz itself.


# Data Protection
This is a non-commercial research project, which does not collect any personal data. The only data collected is the data you enter into the application. This data is only used to generate the explanations and is not stored anywhere.

> However, the application may be hosted with an external service (i.e. Huggingface Spaces), which may collect data.

Please refer to the data protection policies of the respective service for more information. If you use the "flag" feature, the data you enter will be stored in *publicly available* csv file.


# License
This Product is licensed under the MIT license. See [LICENSE](https://github.com/LennardZuendorf/thesis-webapp/blob/main/LICENSE.md) at GitHub for more information.
Please credit the original authors of this project (Lennard Zündorf) and the credits listed above if you use this project or parts of it in your own work.
