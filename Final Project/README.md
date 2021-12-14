# COVID-19 Detector Device

![](/Final%20Project/assets/img-dectectorad.png)

> Work in Progress, while converting [Final Project Writeup](https://docs.google.com/document/d/11MBfT8TGPx4SdjWUDcm1YmNk_BIYrDkTOPPInPOyHGI/edit?usp=sharing)

* Main code can be found in [covid_detector.py](covid_detector.py)
* Demonstration video hosted on [Youtube](#), later embedded here
* Images can be found in `assets` and will be added here later

# Big idea

For the final project, I would like to create an interactive device that can recognize COVID-19 symptoms. Moreover, the device can interconnect with other devices and be used for telehealth situations for alone people. Since, in general, testing the patient without PCR testing is not reliable for identifying a positive test, the device aims to provide comfort and social control for people who are isolated from others. This additional Human-Computer Interaction layer will focus on creating positive interactions without a GUI. In the best-case scenario, the multiple mock devices communicate to a dashboard where healthcare providers can monitor patients through telehealth. Besides, I want to focus on creating a privacy-first solution and making sure the video processing never leaves the device.

# Functioning Project


The functioning project is a combination of the interactive device and the envisioned dashboard. The device itself monitors the patient via camera en sound and recognizes coughing. When a patient is coughing, the device calculates a risk number and based on that the user should measure their temperature or nothing at all. To communicate with the user the device uses a small screen with the written instruction. For accessibility and legibility purposes, the system has a two-sense communication by design. Therefore, the instructions for the user are always spoken and displayed in text. 