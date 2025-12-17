# Copilot instructions for `mcu` repository

Summary
- Small Python project that models a device register layer and contains example signal-processing/ML scripts.
- Useful areas: register table modeling (`reg/`), device calibration wrappers (`calib/`), algorithm examples (`alg/`), and simple dev demos/tests (`test/`).

Quick start (commands you can run locally)
- Run the register example/demo: `python test/test_mcu.py` (uses `Reg_Handle` and `Eq`).
- Run the small ML demos: `python alg/noliner.py` or `python alg/memory_noliner.py` (these are script-style examples that execute on import).
- There is no CI configured; add tests to `test/` and run them with `pytest` or `python -m pytest` after installing test deps.

Key files & responsibilities
- `reg/regTbl.py` — Register layout using `ctypes.Structure/Union`. Each register has a `bits` Structure (bitfields) and `value` union field.
  - `dict_cfgs` maps logical config names (e.g. `"ffe_taps"`) to register instances (e.g. `"reg0"`).
  - Use `regoffset(reg)` to compute offsets from `RegTbl`.
- `reg/Reg_Handle.py` — thin abstraction over an SPI/IO instance. It instantiates register objects (`Reg0`, `Reg1`) and implements `read_reg` / `write_reg` which currently contain placeholders / commented-out SPI calls.
  - Tests pass a dummy value (e.g. `Reg_Handle(1)`) — hardware integration requires replacing the placeholder SPI calls with the real interface (`spi.read(address)` / `spi.write(address, value)`).
- `calib/Eq.py` — small device-level class that uses `Reg_Handle` to set/get configuration values.
- `alg/` — example algorithm scripts (signal distortion and CNN compensation examples). These are runnable scripts, not importable modules (they execute on import).
  - `alg/noliner.py` — single-sample 1D-CNN example (Conv1d expects shapes of `[batch, channel, length]`). Watch out: script uses `x_train.unsqueeze(1).permute(0,2,1)` to produce `[N,1,1]`.
  - `alg/memory_noliner.py` — sequence-windowed CNN with residual blocks. Uses a sliding-window `X_seq` → `Y_seq` approach and demonstrates memory effects.

Patterns & conventions (project-specific)
- Registers are modeled with `ctypes` bitfields; the canonical way to add a config is:
  1. Add a bitfield entry in a `RegXbits` Structure.
  2. Add/adjust the `RegX` Union to expose `bits` and `value`.
  3. Add mapping in `dict_cfgs` for the config key → register name.
  4. Use `Reg_Handle.write_reg(name, value)` and `read_reg(name)` to interact.
- `Reg_Handle` prints writes for visibility and does not perform real SPI I/O by default.
- Scripts in `alg/` are example experiments — they train or plot directly. They are not packaged functions and often run top-level code immediately.

Common pitfalls and how to fix them (concrete examples)
- Conv1d shape error: Conv1d expects `[batch, channel, length]`. If you have N samples with single scalar inputs you should have `x.shape == [N, 1, 1]`. Example:

```py
# given x: [N, 1]
x_train_cnn = x_train.unsqueeze(1).permute(0, 2, 1)  # [N, 1, 1]
# when testing a single value y=3:
y_test = torch.tensor([[3.0]], dtype=torch.float32)        # [1,1]
y_test_cnn = y_test.unsqueeze(1).permute(0,2,1)           # [1,1,1]
with torch.no_grad():
    output = model(y_test_cnn)
    print(output.item())
```

- Normalization: ML scripts do not always scale inputs. If predictions are poor, standardize inputs and targets (e.g., `sklearn.preprocessing.StandardScaler`) and inverse-transform predictions for plotting.
- Scripts execute on import: when turning scripts into library functions, wrap executable code under `if __name__ == "__main__":`.

Testing & adding tests
- Add unit tests under `test/` following the style used in `test/test_mcu.py` (simple scripts that import modules and exercise core interfaces).
- There is no `requirements.txt`; if you add dependencies (e.g., `torch`, `matplotlib`, `sklearn`), add a `requirements.txt` and mention it in the README.

Integration points / external dependencies
- CPU ML experiments depend on `torch`, `numpy`, `matplotlib` (not pinned in repo).
- Hardware integration for registers expects an SPI-like object with `read`/`write` — replace `Reg_Handle` placeholders with the real device API.

If something is unclear or you want the instructions to emphasize a different part of the repo (for example, more hardware-integration detail or more ML best-practices specific to these examples), tell me which parts to expand or add examples for.