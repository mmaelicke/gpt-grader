## Exercise Handout: Prompt Engineering for MATLAB & Python

### 1. The Sine Wave

* **Asset:** (None/Blank Slate)
* **Goal:** Write a single prompt to generate a 10Hz sine wave plot.
* **Challenge:** Ensure the sampling frequency () is at least 1000Hz and the plot has professional labels.

### 2. The Data Cleaner

* **Asset:**
```text
RECORD_ID: 001 | USER: "Alice" | SCORE: 88%
RECORD_ID: 002 | USER: "Bob"   | SCORE: 92%
RECORD_ID: 003 | USER: "Charlie" | SCORE: 75%

```


* **Goal:** Convert this unstructured text into a MATLAB `table` or a Python `pandas.DataFrame`.
* **Challenge:** The "Score" column must be converted to numeric values (e.g., 0.88) instead of strings.

### 3. The Unit Converter

* **Asset:** (Logic Task)
* **Goal:** Create a function called `convert_temp`.
* **Challenge:** It must accept Celsius and return a data structure (Struct in MATLAB, Dict in Python) containing Kelvin and Fahrenheit.

### 4. The Regex Rescue

* **Asset:**
```text
Processing file_v1_20230501.dat. 
Backup created at file_v2_20231225.dat.
Last modified on 20240115.

```


* **Goal:** Extract only the dates (YYYYMMDD) using Regular Expressions.
* **Challenge:** Format the output as a list of strings.

### 5. Matrix Solver

* **Asset:**


* **Goal:** Represent these as matrices  and , then solve for .
* **Challenge:** Solve it using the most computationally efficient built-in function for your language.

### 6. Plot Styling

* **Asset (Python):** `plt.plot([1, 2, 3], [1, 4, 9])`
* **Asset (MATLAB):** `plot([1, 2, 3], [1, 4, 9])`
* **Goal:** Make this plot "Publication Quality."
* **Challenge:** Use a specific font (e.g., Times New Roman), add a legend, and use a LaTeX string for the title: .

### 7. The Logic Debugger

* **Asset:**
```python
# Python
def get_average(nums):
    return sum(nums) / len(nums)
print(get_average([]))

```


```matlab
% MATLAB
data = [10, 20, 30];
for i = 1:4
    disp(data(i))
end

```


* **Goal:** Ask the AI to fix the code to handle the specific error (Empty list or Index out of bounds).

### 8. Mock Data Generation

* **Asset:** (None)
* **Goal:** Generate a JSON-formatted string for 5 test users.
* **Challenge:** Each user must have a unique `ID`, a `timestamp` for "last_login," and a random `float` between 0 and 1 for "reliability_score."

### 9. Vectorization

* **Asset:**
```matlab
% MATLAB
A = 1:10000;
for i = 1:length(A)
    B(i) = A(i)^2;
end

```


* **Goal:** Rewrite this code to remove the `for` loop.
* **Challenge:** In Python, use NumPy; in MATLAB, use array operators.

### 10. Language Translation

* **Asset:**
```matlab
theta = linspace(0, 2*pi, 100);
rho = abs(sin(2*theta) .* cos(2*theta));
polarplot(theta, rho)

```


* **Goal:** Translate this MATLAB code into Python.
* **Challenge:** The Python version must use `matplotlib`'s polar projection and look identical to the MATLAB output.

