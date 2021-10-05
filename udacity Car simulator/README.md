# Udacity-Self-Driving-Car-Simulation
Source Code of Udacity Self Driving Car Simulation on the simulator provided by Udacity on Seaside, Mountain and Jungle Track.
## Description:
### Files:
##### .h5 files are the saved models which I have already trained.
##### car_model2(i).ipynb is the source code of the trained model.
##### drive.py and related drive named files are the files that will move the car in the simulator.
### Model[car_model2(i).ipynb]:
#### DataSet Collection:
Each Model has been trained with different parameters to obtain the best possible accuracy. However, I could not upload the dataset due to its large size in Gigabytes! 
Here you need to create your own dataset by playing the car game on the Udacity Self Driving Car Simulator in the training mode. Create your dataset keeping various important points in mind:
1. Try to move your car in center for as long as possible with smoothness and zero collisions.Try again and again to get the best possible dataset. Remember to remove first dataset if it is not created up to the mark as it keeps on adding the data in to the same csv file.
2. Make your dataset on various tracks: Seaside, Mountain and Jungle tracks. However, you can make your own Unity Car Games and train your models with them. 
3. Remember here that more the training data in various tracks- more will the accuracy of your model and it will be a more Robust Model.
##### I trained the model only on the first track- Seaside Track and obtained ~77% Accuracy(the best). The maximum speed achieved by my car was 18 mph on seaside and mountain tracks. The worst speed was 12mph in the Jungle Track. Though my model completed all the tracks smoothly but it is not very fast. For making it fast, remember the points mentioned above.
#### Preprocessing of Data:
##### loadData function:
Loads the dataset.
##### balance_data function: 
After the data has been collected, we need to normalize and balance our data. First we crop our images in order to point to certain specific details about a particular frame. For example we don't need the sky portion of our image. Also a histogram has been plotted for the turning angles for all the frames. If you look at it, you will see certain angles at which more than required in the dataset. So I have balanced the histogram by reducing those images with very large angles from the dataset. If this step is skipped your model will turn the car at large angles and increases the chances of the collision.
##### brightness_change function:
This function changes the brightess of the image. It increases the brightness of the image for worst case performances where the brightness is insufficient.
##### data_augmentation function:
This function is created to flip the images. If you observe closely, the tracks have more number of left turns than the right turns. To make our model smoothly function in the right turns on unseen tracks, this function is created which flips the left images and appends them to the dataet. After flipping left becomes right!
##### network_model function:
A sequential model is made with input layer as the lambda layer which inputs normalized data. After that a cropping layer is made that crops the sky portion from the image. Two convolutional layers with each of 32 and 64 neurons respectively with ReLu activation have been made along with pooling and dropout layers for regularization and prevention of overfitting of the model. Two more Convolutional2D layers of 128 and 256 Neurons have been made with ReLu activation. 
After the convolutional layers Flattening layer is made and 3 Dense layers are created out of which the last one is the Output Layer.
##### generator function:
A generator function is made to run the model in order to consume less time and less memory. You can do without the generator function also but it would be very inefficient. The basic difference between a 'with generator' and 'without generator' model is that in a 'with generator' model, a batch of images is taken and preprocessed(data augemtation) where as in a 'without generator' model all the images are taken in 1 batch and preprocessed. Hence large memory is required in the latter case.
##### Optimizer Used: Adam Optimizer.
### Driving File(drive.py files):
You can read about this file in the Udacity website as it is a default file provided by them. However, let me mention certain changes which I have made in this(refer drive2.py and drive_best_acc.py). I have added a class SimplePIController that implements PID(Proportional Integrator Differentiator-here only PI is used) Mechanism to control the speed of the car and make it move smoothly at a constant speed. Rest code remains the same.
### To run the Model:
1. Clone the repo.
###### git clone https://github.com/adipro7/Udacity-Self-Driving-Car-Simulation.git
2. Convert the ipynb file to .py file. Go to the jupyter notebook->files.
3. Run the following command:
###### python <drive_file_to_be_executed> <model_to_be_executed>
eg: 
###### python car_model2(i).py model1.h5
## Remember to change the car_model2(i).ipynb and drive.py related files with appropriate file names of models and images dataset which you want to run.
