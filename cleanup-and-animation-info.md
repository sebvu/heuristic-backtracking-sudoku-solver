# Final Pass Changes Made 

## main.py changes

1. **Moved Malloc Tracking from main to solver.py algorithms**
    - To track memory for each solve, the tracemalloc start and stop need to be tracked in the solver functions
    - Before, we had one instance of tracemalloc accross all the experimental runs
    - Memory used for uninformed was being carried over to the heiristic run

    - Changes to actual memory usage was minor, but it is more accurate now

2. **Changed it so that a fixed number of sudoku puzzles are ran through each solver. The sample are also the same between solvers to make comparison easier**
    - From the data fame, a random number of puzzles are chosen, this number can be changed in the constants file
    - The samples are fed into each solver function and are the same between them so that comparable values are produced

3. **Added some print functions to make it easier to see when solve runs are started and completed**

## solver.py Changes

1. **Changed each solver function to run tracemalloc within the function and calculate memory usage**
    - Added start/stop trace malloc within the uniformed and heuristic solve algos
    - Changed functions to calulate and report memory useage to the recordExperiment helper function to store the information
    - Removed the memory calculation that was previoulsy in the _recordExperiment function

2. **Adjusted how operations are counted in brute force and heuristic algorithms**
    - operationsCount was not consistent between the two algorithms. Operations were not being counted in the helper functions that are a part of each sover algorithm
    - Added some helper functions so make counting operations and clearing values easier so the counting can be done easier

3. **Added a new metric to calculate the number of nodes explored in each experiment**
    - New variable to track number of nodes explored in each experiment. Seemed like a good thing to track for the report and presentation
    - Added some helper functions so make counting operations and clearing values easier so the counting can be done easier

4. **Added a final verification to make sure the puzzle was actually solved and gets the final answer**

## world.py Changes

1. **Added the variable to track the number of nodes explored**
    - addExpData was changed to add the new variable and the code to add it to the log of data collected 
    - addExpData was updated to require and validate the new 6-field data structure

## benchmark.py Changes

1. **Added changes to add metrics measuring for number of nodes explored**
  - Added variables and matched the previous data analysis done, but added the new variable to the mix of data computed
  - Also adds summarization and plotting for the new metric

2. **Added changes to match new memory measurement from the information collected in tha solver algorithms instead of running its own tracemalloc**
  - Just matching the rest of experiment

## data_visualization.py Changes

1. **Made variable and import changes to add new nodesExplored metric**
    - Added nodes explored to summary text, interpretation metrics, and all relevant plot families

2. **Consolidated and added checks to make sure comparison data exists and is valid**
    - Added new helper function _metric_series_pair to clean the data and have a consistent code

## constants.py Changes

1. **Added two new constants to go with coincide with main.py changes**
    - MAX_RUNS_PER_ALGO: max number of runs that each solver algorithm should run
    - RANDOM_STATE: random number generator to allow for consistent tests

## solver_animation.py (New File)

**This is a new file to run a full uninformed and informed solver on a puzzle and store that information so that a visual of the informaiton can be made**

    - Primarily for demonstration and presentation use so that a clear visual difference can be established between the methods
    - Runs a full solve for one row and saves the state of the board and some metrics
        - Board is rendered for both with matplotlib
        - A frame with both boards side by side is built
        - Each frame is used to make a complete rendered animation

    - Since it would not be feasible to render every single frame, important ones are chosen
        - maxFrames set to 300
        - fps set to 12
        - Saves the animation to the figures folder

    _Sidenote:_ The modified_solver_comparison.gif is the gif made from this animation but it was modiified to start a little slower to show the heuristic work since it was too fast to see
        - gif is in the docs folder
