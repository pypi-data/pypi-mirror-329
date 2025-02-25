# Source Label Map

Converts news sources into human-friendly labels

# Quickstart

## Installation

Install the package with pip:

```bash
pip install -U bilbyai-source-label-map
```

## Usage

### Using `get_source_labels` directly

```python
from bilbyai.source_label_map import get_source_labels

get_source_labels("ben")
# 'Beijing Evening News'

get_source_labels(["gmwnews", "ben"]) 
# ['Enlightenment Daily', 'Beijing Evening News']

# Since the key 'cannot-be-found' is not in the dictionary, it returns the original input.
get_source_labels("cannot-be-found")
get_source_labels("cannot-be-found", when_not_found="preserve") # this is the default.
# 'cannot-be-found'

# When the option is set to 'set_none', the function returns None when the key is not found.
get_source_labels("cannot-be-found", when_not_found="set_none")
# None

# When the option is set to 'set_unknown', the function returns the string "unknown".
get_source_labels("cannot-be-found", when_not_found="set_unknown") 
# 'unknown'

# When the option is set to 'raise_error', the function raises a ValueError.
get_source_labels("ben", when_not_found="raise_error") 
# raises ValueError
```

### Using `get_source_labels` with DataFrames 

```python
import pandas as pd
from bilbyai.source_label_map import get_source_labels

df = pd.DataFrame(
    {
        "source": [
            "gmwnews",
            "ben",
            "cannot-be-found",
            "zqrb",
        ]
    }
)

# Option A: using list comprehension
df["source_label"] = get_source_labels(df["source"])

# Option B: using apply
df["source_label"] = df["source"].apply(get_source_labels)

df["source_label"]
# Outputs: 
# 0     Enlightenment Daily
# 1    Beijing Evening News
# 2         cannot-be-found
# 3        Securities Daily
# Name: source_label, dtype: object
```


# Function Specs
Get source labels for a list of inputs.

### Args

`source` (`str | Iterable[str]`): The string or list of strings to get source labels for.
  
`when_not_found`: The action to take when a source label is not found. Set to "preserve_source_name" by default.
- `"preserve"`: Preserve the source name as the source label. 
- `"set_none"`: Set the source label to None. 
- `"set_unknown"`: Set the source label to "unknown". 
- `"raise_error"`: Raise an error if a source label is not found. 

`source_label_dict`: A dictionary mapping source names to source labels. Set this value to override the default source label dictionary. It should be a dictionary mapping source names to source labels, like this:
```python
source_label_dict = {
    "gmwnews": "Enlightenment Daily",
    "sina_news": "Sina News",
    "xueqiu": "Xueqiu (Snowball Finance)",
    "peoplenews": "People's Daily",
}
```

### Returns
  A list of source labels for the inputs.

### Raises
  `ValueError`: If the when_not_found value is not recognized.
  `ValueError`: If the inputs are not a string or iterable of strings.
  `ValueError`: If when_not_found is set to "raise_error" and a source label is not found.

The project owner is [@leetdavid](https://github.com/leetdavid).

## Development

If not already in a virtual environement, create and use one.
Read about it in the Python documentation: [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

```
python3 -m venv .venv
source .venv/bin/activate
```

Install the pinned pip version:

```
pip install -r $(git rev-parse --show-toplevel)/pip-requirements.txt
```

Finally, install the dependencies:

```
pip install -r $(git rev-parse --show-toplevel)/dev-requirements.txt -r requirements.txt
```

## Testing

Execute tests from the library's folder (after having loaded the virtual environment,
see above) as follows:

```
python3 -m pytest tests/
```

Execute the library's CI locally with [act](https://github.com/nektos/act) as follows:

```
act -j ci-libs-source_label_map
```
