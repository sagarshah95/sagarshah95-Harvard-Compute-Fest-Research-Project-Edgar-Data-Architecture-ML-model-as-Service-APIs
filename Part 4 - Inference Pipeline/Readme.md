
### Inference Pipeline 

In this piepline we combine functionalities of the previous two pipelines and use the dockerized API we created to service our pipeline. We will take a csv file containing earning call urls as input, scrape the given urls and perform sentiment analysis of the text. To perform the analysis we will use the API we developed as endpoint, and write the generated result to the S3 bucket in csv format. 

#### Run Instructions 

```
python inference_pipeline.py --environment=conda run
```

The model of our inference pipeline looks like this:

![alt text](https://github.com/siddhant07/CaseStudy2/blob/master/Images/P3_model.png)
