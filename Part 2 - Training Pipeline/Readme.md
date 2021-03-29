
### Training Pipeline 

In this pipeline we train a ML model using tensorflow hub's pre-trained model (universal sentence encoder), we train this model on the labeled dataset that we generated in the Annotation Pipeline using Edgar earning calls.

#### Run Instructions 

```
python training_pipeline.py --environment=conda run
```

This is the model for our training pipeline:

![alt text](https://github.com/siddhant07/CaseStudy2/blob/master/Images/T2_model.png)
