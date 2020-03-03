# PostProcess

  A back-end logical interface for processing structured data results of front-end models.

## Function
* Detect human occlusion 
* Detect turning round 
* Detect the amount of persons
* Detect the access times of an identified person

![structure](https://github.com/zhubinQAQ/PostProcess/blob/master/utils/sample.png)

## How to use
> P = ProcessInterface(cfg_file='PostProcess/cfgs/params.yaml')
>> for i in range(frame_num):
        result = P(i)
