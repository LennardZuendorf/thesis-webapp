# Credits

### Models
This implementation is build on GODEL by Microsoft, Inc.

##### GODEL
GODEL is an open source model by Microsoft. See [offical paper](https://arxiv.org/abs/2206.11309) for more information.

- the version used in this project is GODEL Large, see [huggingface model hub](https://huggingface.co/microsoft/GODEL-v1_1-large-seq2seq?text=Hey+my+name+is+Thomas%21+How+are+you%3F)
- the model as is a generative seq2seq transformer fine-tuned for goal directed dialog
- it supports context and knowledge base inputs

### Libraries
This project uses a number of open source libraries, only the most important ones are listed below.

##### Shap
This application uses a custom version of the shap library, which is available at [GitHub](https://github.com/shap/shap).

- Please refer to the [thesis-shap](https://github.com/LennardZuendorf/thesis-custom-shap) repository for more information about the changes made to the library, specifically the README file.
- The shap library and the used partition SHAP explainer are based on work by Lundberg et al. (2017), see [offical paper](https://arxiv.org/pdf/1705.07874.pdf) for more information.

##### Visualizations
This application uses attention visualization inspired by the bertviz library, which is available at[GitHub](https://github.com/jessevig/bertviz). It doesn't actually use BERTViz.

- The bertviz was introduced by Vig et al. (2019), see [offical paper](https://arxiv.org/pdf/1906.05714.pdf) for more information.
- This project only uses cross attention visualization with gradio and matplotlib.


# Data Protection
This is a non-commercial research project, which does not collect any personal data. The only data collected is the data you enter into the application. This data is only used to generate the explanations and is not stored anywhere.

> However, the application may be hosted with an external service (i.e. Huggingface Spaces), which may collect data.

Please refer to the data protection policies of the respective service for more information. If you use the "flag" feature, the data you enter will be stored in *publicly available* csv file.


# License
This Product is licensed under the MIT license. See [LICENSE](https://github.com/LennardZuendorf/thesis-webapp/blob/main/LICENSE.md) at GitHub for more information.
Please credit the original authors of this project (Lennard Zündorf) and the credits listed above if you use this project or parts of it in your own work.
