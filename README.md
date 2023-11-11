# Survey and Benchmark of Anomaly Detection in Business Processes

**Abstract**: Business processes are prone to anomalies that can arise from various factors, such as software malfunctions and operator errors. These anomalies can significantly impact the financial health of a business and impede our ability to extract valuable insights from event logs. As a result, anomaly detection has become an essential area of research in process mining to identify and resolve these issues.
Numerous methods for detecting anomalies in business processes have been proposed recently. However, the relative merits of each method remain unclear due to differences in their experimental setup, choice of datasets and evaluation measures. In this paper, we present a systematic literature review and taxonomy of business process anomaly detection methods. Additionally,  we select at least one method from each category, resulting in 14 methods that are cross-benchmarked against 32 synthetic logs and 19 real-life logs from different industry domains.
Our analysis provides insights into the strengths and weaknesses of different anomaly detection methods. Ultimately, our findings can help researchers and practitioners in the field of process mining make informed decisions when selecting and applying anomaly detection methods to real-life business scenarios.
Finally, some future directions are discussed in order to promote the evolution of business process anomaly detection.

### Studied Models
|    Model     | Year  |     Perspective     |   Granularity    |                                                                                                                                             Paper                                                                                                                                              |
|:------------:|:-----:|:-------------------:|:----------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    Naive     | 2013  |    Control-flow     |   Trace-level    |            [Algorithms for anomaly detection of traces in logs of process aware information systems](https://www.sciencedirect.com/science/article/abs/pii/S0306437912000567)             |
|   Sampling   | 2013  |    Control-flow     |   Trace-level    |            [Algorithms for anomaly detection of traces in logs of process aware information systems](https://www.sciencedirect.com/science/article/abs/pii/S0306437912000567)             |
|  Likelihood  | 2016  |  Multi-perspective  | Attribute-level  |                                                                           [Multi-perspective anomaly detection in business process execution events](https://link.springer.com/chapter/10.1007/978-3-319-48472-3_5)                                                                            |
|     DAE      | 2018  |  Multi-perspective  | Attribute-level  |                                                                                            [Analyzing business process anomalies using autoencoders](https://link.springer.com/article/10.1007/s10994-018-5702-8)                                                                                             |
|   BINetv2    | 2018  |  Multi-perspective  | Attribute-level  |                                                                                   [BINet: Multivariate business process anomaly detection using deep learning](https://link.springer.com/chapter/10.1007/978-3-319-98648-7_16)                                                                                   |
|     VAE      | 2019  |  Multi-perspective  | Attribute-level  |                                                                                            [Autoencoders for improving quality of process event logs](https://www.sciencedirect.com/science/article/abs/pii/S0957417419302829)                                                                                            |
|     LAE      | 2019  |  Multi-perspective  | Attribute-level  |                                                                                            [Autoencoders for improving quality of process event logs](https://www.sciencedirect.com/science/article/abs/pii/S0957417419302829)                                                                                            |
| Word2vecBPAD | 2020  |    Control-flow     |   Trace-level    |                                                                                           [Anomaly Detection on Event Logs with a Scarcity of Labels](https://ieeexplore.ieee.org/document/9230308)                                                                                            |
|   VAEOCSVM   | 2021  |    Control-flow     |   Trace-level    |                                                                              [Variational Autoencoder for Anomaly Detection in Event Data in Online Process Mining](https://arxiv.org/abs/2208.03326)                                                                              |
|     GAE      | 2021  |  Multi-perspective  |   Trace-level    |                                                                                           [Graph Autoencoders for Business Process Anomaly Detection](https://link.springer.com/chapter/10.1007/978-3-030-85469-0_26)                                                                                            |
|   Leverage   | 2022  |    Control-flow     |   Trace-level    | [Keeping our rivers clean: Information-theoretic online anomaly detection for streaming business process events](https://www.sciencedirect.com/science/article/abs/pii/S0306437921001125) |
|   BINetv3    | 2022  |  Multi-perspective  | Attribute-level  |                                                                                        [BINet: Multi-perspective business process anomaly classification](https://www.sciencedirect.com/science/article/abs/pii/S0306437919305101)                                                                                        |
|   GRASPED    | 2023  |  Multi-perspective  | Attribute-level  |                                                                           [GRASPED: A GRU-AE Network Based Multi-Perspective Business Process Anomaly Detection Model](https://ieeexplore.ieee.org/document/10088425)                                                                           |
|     GAMA     | 2023  |  Multi-perspective  | Attribute-level  |                                                                     [GAMA: A Multi-graph-based Anomaly Detection Framework for Business Processes via Graph Neural Networks](https://www.techrxiv.org/articles/preprint/GAMA_A_Multi-graph-based_Anomaly_Detection_Framework_for_Business_Processes_via_Graph_Neural_Networks/23627850)                                                                     |

## Requirements
- [PyTorch==1.13.0](https://pytorch.org)
- [TensorFlow==2.6.0](https://www.tensorflow.org/)
- [NumPy](https://numpy.org)
- [scikit-learn](https://scikit-learn.org)
- [pm4py](https://pm4py.fit.fraunhofer.de/)
- [pyg](https://pytorch-geometric.readthedocs.io/en/latest/index.html)
### Examples 
    ```
    python \generator\gen_anomalous_eventlog_syn.py  # get the synthetic dataset with anomalies
    python \generator\gen_anomalous_real_life_log.py  # get the real-life dataset with anomalies
    python main.py # get the result for each method.
    ```
