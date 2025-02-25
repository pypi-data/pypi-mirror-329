[简体中文](https://github.com/barkure/JuliaBridge/blob/main/README_zh_cn.md) [English](https://github.com/barkure/JuliaBridge/blob/main/README.md)

# JuliaBridge
A Python package for communication with Julia.

To enhance your two-step operation for using the `JuliaBridge` package, we can add more details and best practices to ensure a smooth experience. Here's an improved version of your instructions:

## Installation
1. **Install the package**:
   ```bash
   pip install juliabridge
   ```

2. **Install Julia** (if not already installed):
   - Download and install Julia from [https://julialang.org/downloads/](https://julialang.org/downloads/).
   - Ensure Julia is added to your system's PATH so it can be accessed from the command line.

3. **Install required Julia packages** (optional):
   If your Julia code relies on specific packages, you can install them using the Julia package manager:
   ```bash
   julia -e 'using Pkg; Pkg.add("PackageName")'
   ```

---

## Example Usage
1. **Basic usage**:
   ```python
   from juliabridge import JuliaBridge

   # Initialize the JuliaBridge instance
   jb = JuliaBridge()

   # Evaluate a simple Julia command
   jb.eval('println("Hello from Julia")')
   ```

2. **Include Julia Scripts and Call Functions**:
   Save your Julia code in a file (e.g., `script.jl`) and run it from Python:
   ```python
   jb.include('script.jl')

   # Suppose the script.jl file contains a function say_hello
   jb.say_hello("Julia")'  # Call the say_hello function
   ```

3. **Passing data between Python and Julia**:

   Create a `test.jl` with the following code:
   ```julia
   function plus(a::Int, b::Int)::Int
      return a + b
   end
   ```

   Use it in Python as follows:
   ```python
   julia.include("test.jl")

   result = julia.eval("1 + 1")
   print(result)  # 2
   ```

---

## Best Practices
- **Keep Julia sessions alive**: If you plan to execute multiple commands, reuse the same `JuliaBridge` instance to avoid the overhead of starting a new Julia session each time.
- **Use `jb.include` for large scripts**: For larger Julia scripts, save them in a `.jl` file and use `jb.include` to execute them.
- **Optimize data transfer**: When passing large datasets between Python and Julia, consider using efficient formats like JSON or binary files.

---

## Troubleshooting
1. **Julia not found**:
   - Ensure Julia is installed and added to your system's PATH.
   - Verify by running `julia` in your terminal.

2. **Package installation issues**:
   - If `pip install juliabridge` fails, ensure you have the latest version of `pip`:
     ```bash
     pip install --upgrade pip
     ```

3. **Performance issues**:
   - For computationally intensive tasks, consider running them directly in Julia instead of passing data back and forth.

---

By following these steps and best practices, you can effectively use `JuliaBridge` to integrate Julia's capabilities into your Python workflow. Let me know if you need further assistance!