# Application that detects humans from in-built camera and predicts their age
Introduction to Machine Learning project

<h2>Overview:</h2>
The main use scenario of the ready solution is as follows: user launches the application. The application collects live video from the in-built camera. On the captured video the application marks a bounding box for each person’s face and predicts their age. The program terminates when the user closes the window. Recognition is in (close to) real time.

<h2>Goals:</h2>
<ul>
  <li>It is ok to prepare several variants of the model and let the user decide which one to launch. In such a case, selection must be done via some graphical components in the GUI or loaded to a clearly named folder. Console arguments cannot be the way of selecting the model or providing any parameters to the program. All such assumptions must be described in the documentation.</li>
  <li>Model quality must be verified using standard measures such as precision, recall, F1 score, sensitivity, accuracy (classification of humans) and errors such as RMSE or MAPE (age prediction). There must be evidence of changes/versions that the group worked on to improve the model.</li>
  <li>Optionally, you may use LIME to perform post-training explanations.</li>
  <li>Age detection can be turned to classification of an age group.</li>
  <li>Please note that there must be a clear manner of communicating errors to the user
(for example, there must be a clear error message that some resource X (file, model, ..) that was supposed to be in location Y (file path) is not there. You cannot reuse the same error message for each exception.</li>
  <li>It is ok to assume that the project directory contains some folders with specific names. All such assumptions must be described in the documentation.</li>
</ul>

