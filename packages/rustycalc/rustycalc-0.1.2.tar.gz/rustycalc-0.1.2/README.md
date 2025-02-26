# Rusty Calc

![old-rusty-calculator-with-yellow-black-design-rests-blue-metal-background-calculator-has-digital-display-with-numbers-quot78138780quot-displayed-indicating-calculation_783884-495565](https://github.com/user-attachments/assets/6a66785d-378a-4969-91f7-e2ecb18d3566)

---

## Setup the project

- Clone the repository.

```bash
git clone git@github.com:deependujha/rustycalc.git
cd rustycalc
```

- Run the project.

```bash
uv sync
uv build
pip install dist/rustycalc.{...}.whl --force-reinstall # choose according to yours
```

Or,

```bash
maturin develop --release
pip install -e .
```

---

## Usage

```python
import rustycalc as rc

print(f"{dir(rc)=}\n")
print("-"*50)
print(f"{rc.sum(5,4)=}\n")
print(f"{rc.diff(5,4)=}\n")
print(f"{rc.factorial(6)=}\n")
print(f"{rc.fibonacci(7)=}\n")
print("-"*50)
```
