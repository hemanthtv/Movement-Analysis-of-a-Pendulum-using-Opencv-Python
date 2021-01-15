## Movement Analysis of a Pendulum using Opencv Python
Finding Angle and distance made by the bob of Pendulum wrt to Mean Position 

## Objective
Basically our childhood education starts with Pendulum -Physics. We are very fascinated to know how the angle changes with motion , how much deviation it takes from mean position , how much distance it from mean position to extreme position etc . 

With this project,I came up with most of Answers to the above Questions using Computer Vision Techniqes and Image Proccessing 

## Procedure Followed 
* Reading frames from video
* Loop back Video when it ends
* Changiing Colour Space BGR2HSV
* Extracting Only Saturation Channel Since it shows amount of white content     from frame which indirectly points out Objects
* Applying Threshold to the frame to convert into Binary format
* Applying MedianBlur to reduce Noice
* Finding Contours in MedianFiltered
* Finding Angle and Distance made by the centre with Vertical Line
* Displaying output frames

# Results 
## Output
![](https://github.com/hemanthtv/Movement-Analysis-of-a-Pendulum-using-Opencv-Python/blob/main/Result/ezgif.com-gif-maker.gif)
