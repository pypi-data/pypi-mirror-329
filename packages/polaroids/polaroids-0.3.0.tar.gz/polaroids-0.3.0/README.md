# Polars on steroids!  

This package provides a generic extension to Polars `DataFrame`, allowing data validation and typing goodies.

## Features
- **Generic DataFrame**: Ensures type safety using Python's `TypedDict`.
- **Data Validation**: Checks that the DataFrame conforms to the expected schema.
- **Custom Checks**: Leverage the power of polars expression to add custom checks.
- **Lightweight**: No dependencies (except polars)!

## Installation

```sh
pip install polaroids
```

## Documentation

📖 **Read the full documentation here:** [Project Documentation](https://gab23r.github.io/polaroids/)

## Basic Usage


```python
from typing import Annotated, TypedDict
from polaroids import DataFrame, Field
from polaroids.types import int8
import polars as pl

class SubSchema(TypedDict):
    c: list[bool]
    d: str

class Schema(TypedDict):
    a: Annotated[int8, Field(
        sorted="ascending",
        coerce=True,
        unique=True,
        checks=[lambda d: d.ge(0)],
    )]
    b: int | None
    s: SubSchema

df = (
    pl.DataFrame({
        "a": [0.0, 1.0], 
        "b": [None, 0], 
        "s": [{"c": [True], "d": "0"}, {"c": [True, False], "d": "1"}]
    })   
    .pipe(DataFrame[Schema]) # <- Add a Schema to your dataframe
    .validate() # Validate it from the Schema annotations!
)
df
shape: (2, 3)
┌─────┬──────┬─────────────────────┐
│ a   ┆ b    ┆ s                   │
│ --- ┆ ---  ┆ ---                 │
│ i8  ┆ i64  ┆ struct[2]           │
╞═════╪══════╪═════════════════════╡
│ 0   ┆ null ┆ {[true],"0"}        │
│ 1   ┆ 0    ┆ {[true, false],"1"} │
└─────┴──────┴─────────────────────┘
```

## Typing Benefits with polaroids

One of the key advantages of polaroids is its strong typing support. You can use classic Polars functions while benefiting from improved type checking and autocompletion in your IDE, reducing runtime errors.


```python
row = df.row(0, named=True)
row["a"]  # ✅ Type checker agree; resulting type is `int`
row["s"]["c"][0]  # ✅ Type checker is happy; resulting type is `bool`
row["not_exists"] # ❌ Type error detected immediately!
```

### Comparison with Alternatives

Compared to Pandera and Patito, polaroids' typing system is based on **TypedDict** rather than Pydantic's BaseModel.

Pydantic is a great tool, but when validating large Polars DataFrames, it's preferable to use **Polars expressions** for efficiency. Given this, a dependency on Pydantic is not particularly relevant.

Moreover, to benefit from typing with Pandera or Patito, you need to instantiate Pydantic objects, which introduces a **runtime penalty**, especially when iterating over rows.

In contrast, polaroids relies on **stub-based typing**, meaning there is no runtime penalty. As a result, polaroids is extremely **lightweight**, with no dependencies (neither Pandas nor Pydantic).




## Contribution

We welcome contributions to **polaroids**! Follow these steps to set up your development environment and ensure your changes meet project standards.

### 1. Clone the Repository  
```bash
git clone git@github.com:gab23r/polaroids.git
cd polaroids
```

### 2. Set Up the Environment
```bash
uv sync
```

### 3. Pre-commit Hooks
```bash
uv run pre-commit install
```

To manually run checks before committing:

```bash
uv run pre-commit run --all-files
```

### 4. Running Tests
```bash
uv run pytest tests
```

Thanks and happy coding! 🚀