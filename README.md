# Statistical Analysis. 

Collection of different approaches to solve, interpret and uncover insights, patterns and trends. 

------------------------------------------------------------------------------------------------------------------------------
## Bivariate-Analysis

Showing different methods of analysing the statistical and graphical significant difference between two variables. 

------------------------------------------------------------------------------------------------------------------------------
## Categorising-under-maximising-CramerV-using-HyperOpt. 

Finding the optimum split for different sizes of bins for the metric variable "Salary" in reference to the binary variable "Clicked" such that the association measure CramerV is maximised.

- Part 2:	HyperOpt and fmin are used to find the maximum CramerV-association measure for 1, 2, 3, 4, 5, 10, 20 and 50 splits. The splits should range between 1K and 100K in 1K-steps.
- Part 3:	For each split and their optimum solution (according to the solver), the Chi-Square-Test is computed and the categorized "Salary"-variable is visualized.
- Part 4:	The total cycle is evaluated with two and three splits to find the true global optimum. That output is being compared to the Solver solution.

 - CramerV:		https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V
 - HyperOpt:	https://github.com/hyperopt/hyperopt
 -				https://towardsdatascience.com/hyperparameter-optimization-in-python-part-0-introduction-c4b66791614b

------------------------------------------------------------------------------------------------------------------------------

## Linear + Polynomial Regression

Regression from degree 1 to 16th degree. Comparing and finding the sweetspot in choosing the right number of degree.

 - Part 3:	Regression computation from degree 1 to 16.
 - Part 4:	Visualization of regression curves and error-metrics.
------------------------------------------------------------------------------------------------------------------------------

## Whittaker-Henderson-Smoothing

Discrete-time version of spline smoothing. Minimizing the trade-off between the fit and the smoothness. 
Allowing the decision-maker to whether increase the smoothness, the fit or the fit in local areas.

 - Part 3:	Smoothing demonstration with default parameters g = 1, m = 2 and equal-distributed weights.
 - Part 4:	Impact analysis of the smoothing parameter g. What happens if the smoothing parameter g is modefied ?
 - Part 5:	Impact analysis of the smoothing parameter m. What happens if the smoothing parameter m is modefied ?
 - Part 6:	Impact analysis of the weights. What happens if the weights are modefied ?

 - http://eceweb1.rutgers.edu/~orfanidi/aosp/aosp-ch08.pdf

------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------------