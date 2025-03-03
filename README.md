## GA_variation v2.0

### Environmental dependencies:
python3.10+

pip install opencv
pip install numpy


### Running Instructions

The main function defaults to using the image firefox.jpg, which can be modified as needed.

The output folder is also set to firefox in the current directory by default, but this can be changed as required.

unit_num represents the number of triangles. In theory, the higher the number, the clearer the image, but the execution speed will be slower.

IMG_SIZE defines the width and height of the output image.

By default, the process terminates after 100,000 iterations, but you can modify this setting as needed.

The first part of the output image filename represents the iteration count, while the latter part indicates the fitness value. In this code, a lower fitness value means a better fitting result.


### Introduction to Genetic Algorithm

1. What is a Genetic Algorithm?
A Genetic Algorithm (GA) is an optimization search algorithm based on the principles of natural selection and genetics. It was first introduced by John Holland in the 1970s and is inspired by Darwin's theory of evolution, utilizing mechanisms such as selection, crossover, and mutation to find optimal solutions from a set of possible solutions.

Genetic algorithms are widely used in optimization problems, machine learning, artificial intelligence, and engineering design, especially for problems with large search spaces where traditional methods struggle to find solutions.

2. Basic Workflow of Genetic Algorithm
The core idea of genetic algorithms is to simulate biological evolution, progressively optimizing solutions based on the principle of survival of the fittest. The basic workflow is as follows:

Initialization (Population Generation)

A group of possible solutions (individuals) is randomly generated, forming the initial population. Each individual is usually represented using binary encoding (e.g., 11001) or real-number encoding.
Fitness Evaluation

The fitness value of each individual is calculated to measure how good the solution is. The fitness function varies depending on the problem. For example:
In path optimization, fitness could be the total path length (shorter is better).
In image fitting, fitness could be the error value (lower is better).
Selection

The best individuals are chosen for reproduction based on their fitness. Common selection methods include:
Roulette Wheel Selection
Tournament Selection
Crossover (Recombination)

Selected individuals exchange genetic information to generate new offspring. Common crossover methods include:
Single-point crossover: A random point is chosen, and the latter part is swapped.
Multi-point crossover: Multiple points are chosen for swapping.
Uniform crossover: Each gene is swapped with a certain probability.
Mutation

Some genes are randomly altered to maintain population diversity and avoid premature convergence. Examples:
Binary encoding: Flip 0 → 1 or 1 → 0.
Real-number encoding: Apply a small random perturbation to a value.
New Generation Formation

After selection, crossover, and mutation, a new population is formed. The process repeats until a termination condition is met (e.g., reaching the maximum number of iterations or finding an optimal solution).
3. Advantages and Disadvantages of Genetic Algorithms
✅ Advantages

Suitable for complex, nonlinear optimization problems without requiring an explicit mathematical model.
Strong global search ability, making it less likely to get stuck in local optima.
Can be executed in parallel, improving computational efficiency.
❌ Disadvantages

Computationally expensive, especially for large-scale problems.
Requires careful design of the fitness function, as it directly impacts optimization performance.
May suffer from premature convergence, failing to find the global optimum.
4. Applications of Genetic Algorithms
Due to their powerful optimization capabilities, genetic algorithms are widely used in various fields, including:

Artificial Intelligence (e.g., Neural network optimization)
Machine Learning (Feature selection, hyperparameter tuning)
Industrial Engineering (Production scheduling, process optimization)
Automation and Control (Robot path planning)
Financial Analysis (Portfolio optimization)
Computer Vision (Image matching, triangle fitting)
5. Conclusion
Genetic algorithms are a powerful optimization technique inspired by biological evolution. Despite challenges such as high computational cost and premature convergence, improvements like adaptive genetic algorithms and genetic programming continue to enhance their effectiveness.

If you have a specific application in mind, adjusting parameters (such as population size and mutation rate) can help achieve better optimization results!