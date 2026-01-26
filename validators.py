VALIDATORS = {
    1: {
        "python": "\nimport matplotlib.pyplot as plt\nimport sys\n# Check if figure was created and has labels\nassert len(plt.get_fignums()) > 0, 'No plot detected'\nax = plt.gca()\nassert ax.get_xlabel() != '', 'X-axis label is missing'\nassert ax.get_ylabel() != '', 'Y-axis label is missing'\n",
        "octave": "\nif isempty(findall(0,'Type','figure')), error('No plot detected'); end\nif isempty(get(gca, 'XLabel')), error('Missing XLabel'); end\nif isempty(get(gca, 'YLabel')), error('Missing YLabel'); end\n"
    },
    2: {
        "python": "\nimport pandas as pd\nassert isinstance(df, pd.DataFrame), 'Variable df must be a DataFrame'\nassert df.shape[0] == 3, 'Table should have 3 rows'\nassert pd.api.types.is_numeric_dtype(df['SCORE']), 'Score column must be numeric'\n",
        "octave": "\nassert(isstruct(T), 'T must be a struct');\nassert(length(T) == 3, 'T should have 3 rows');\nassert(isfield(T, 'SCORE'), 'T must have SCORE field');\nassert(isnumeric([T.SCORE]), 'SCORE must be numeric');\n"
    },
    3: {
        "python": "\nres = convert_temp(0)\nassert abs(res['kelvin'] - 273.15) < 0.01\nassert abs(res['fahrenheit'] - 32) < 0.01\n",
        "octave": "\nres = convert_temp(0); \nassert(abs(res.kelvin - 273.15) < 0.01 && abs(res.fahrenheit - 32) < 0.01);\n"
    },
    4: {
        "python": "\nassert len(dates) >= 3, 'Should find at least 3 dates'\nassert all(len(d) == 8 for d in dates), 'Dates should be in YYYYMMDD format'\n",
        "octave": "\nassert(length(dates) >= 3);\n"
    },
    5: {
        "python": "\nimport numpy as np\n# x+y=5, x-y=-1 -> x=2, y=3\nassert np.allclose(x, [2, 3]) or np.allclose(x, [[2],[3]]), f'Expected [2, 3], got {x}'\n",
        "octave": "\nassert(all(abs(x(:) - [2; 3]) < 1e-5));\n"
    },
    6: {
        "python": "\nimport matplotlib.pyplot as plt\nax = plt.gca()\nassert ax.get_legend() is not None, 'Legend missing'\nassert '$' in plt.gca().get_title().get_text(), 'Title should contain LaTeX (e.g., using $...$)'\n",
        "octave": "\nif isempty(get(gca, 'Legend')), error('Legend missing'); end\n"
    },
    7: {
        "python": "\nassert get_average([10, 20]) == 15\ntry:\n    get_average([])\nexcept Exception as e:\n    raise AssertionError(f'Empty list caused an error: {e}')\n",
        "octave": "\n% Check if data variable exists and we can access it\nassert(exist('data', 'var') == 1);\n"
    },
    8: {
        "python": "\nimport json\nd = json.loads(json_data)\nassert len(d) == 5, 'Should have 5 users'\nassert 'reliability_score' in d[0], 'Missing reliability_score'\n",
        "octave": "\nassert(ischar(json_data) && length(json_data) > 50);\n"
    },
    9: {
        "python": "\nimport numpy as np\nassert 'for' not in code, 'Loops are forbidden for vectorization task'\nassert 'np.' in code or 'numpy' in code, 'NumPy must be used'\n",
        "octave": "\nassert(~contains(code, 'for'), 'Loops are forbidden for vectorization task');\n"
    },
    10: {
        "python": "\nimport matplotlib.pyplot as plt\nassert any(isinstance(ax, plt.PolarAxes) for ax in plt.gcf().axes), 'Must use polar projection'\n",
        "octave": "\nassert(exist('theta', 'var') == 1 && exist('rho', 'var') == 1);\n"
    }
}
