Here's the **professional and refined README** for your **Ossarth** module:

---

# **Ossarth**

### **AI-Powered Open-Source OS Customization Framework**

An **AI-driven framework** for customizing **Ossarth OS** by dynamically creating and integrating **custom tools & helper functions**.

---

## **What is Ossarth?**

**Ossarth** is an **AI-powered customization framework** designed exclusively for **Ossarth OS**. It allows users to **extend their OS functionality dynamically** by creating **custom AI tools and general-purpose functions**.

With **Ossarth**, users can:  
✅ **Modify and enhance their OS in real-time.**  
✅ **Define and integrate LangChain-compatible AI tools.**  
✅ **Create automation scripts and system utilities.**  
✅ **Customize system monitoring and OS-level functionalities.**  
✅ **Run a Flask-based AI-powered backend for managing custom tools.**

---

## **Features**

- **AI-driven OS customization** with dynamic tool creation.
- **Create and integrate LangChain-compatible AI tools.**
- **Automate system tasks with helper functions.**
- **Predefined templates for structured function generation.**
- **Dynamic module generation for scalable OS enhancements.**
- **Designed specifically for Ossarth OS.**

---

## **Installation**

To install Ossarth, use **PyPI**:

```bash
pip install ossarth
```

Or install the latest version from **GitHub**:

```bash
pip install git+https://github.com/Siddharth-magesh/Ossarth.git
```

---

## **Quick Start**

### **1. Import the Module**

```python
from ossarth.tool_manager import ToolManager
```

### **2. Initialize the Tool Manager**

```python
manager = ToolManager()
```

### **3. Create a Custom AI Tool**

```python
manager.create_custom_tool(
    func_name="get_disk_usage",
    description="Retrieves disk usage statistics.",
    params="",
    args_doc="None",
    return_type="dict",
    return_desc="A dictionary with total, used, and free disk space in GB.",
    body="""
import shutil
path = "/"
total, used, free = shutil.disk_usage(path)
gb = 1024 * 1024 * 1024
return {
    "total": f"{total / gb:.2f} GB",
    "used": f"{used / gb:.2f} GB",
    "free": f"{free / gb:.2f} GB"
}
""",
    result_dir="custom_os_functions"
)
```

This will generate a Python file **`custom_os_functions/get_disk_usage.py`**, allowing **Ossarth OS** to retrieve disk usage dynamically.

---

## **Creating a Helper Function**

```python
manager.create_custom_function(
    func_name="calculate_cpu_load",
    description="Calculates the average CPU load over a given interval.",
    params="interval: int",
    args_doc="interval (int): The time interval for calculating CPU load.",
    return_type="float",
    return_desc="The average CPU load percentage.",
    body="""
import psutil
return psutil.cpu_percent(interval=interval)
""",
    result_dir="custom_helpers"
)
```

This will generate **`custom_helpers/calculate_cpu_load.py`**, a general Python function to monitor CPU load.

---

## **Folder Structure**

After defining tools and functions, your **directory structure** will look like this:

```
Ossarth/
│── custom_os_functions/
│   ├── get_disk_usage.py  # AI Tool for OS customization
│── custom_helpers/
│   ├── calculate_cpu_load.py  # General function
│── ossarth/
│   ├── tool_manager.py    # Core logic for tool management
│   ├── templates/
│   │   ├── general_template.py
│── README.md
│── setup.py
│── requirements.txt
```

---

## **Advanced Usage**

### **Adding Multiple Functions in a Single File**

To **append new functions** to an existing file instead of creating a new one:

```python
manager.create_custom_tool(
    func_name="get_memory_usage",
    description="Retrieves system memory usage statistics.",
    params="",
    args_doc="None",
    return_type="dict",
    return_desc="A dictionary with total, used, and available memory in GB.",
    body="""
import psutil
mem = psutil.virtual_memory()
gb = 1024 * 1024 * 1024
return {
    "total": f"{mem.total / gb:.2f} GB",
    "used": f"{mem.used / gb:.2f} GB",
    "available": f"{mem.available / gb:.2f} GB"
}
""",
    result_dir="custom_os_functions",
    filename="system_monitoring.py"
)
```

This will add **`get_memory_usage`** to **`system_monitoring.py`** instead of creating a new file.

---

## **Testing the Ossarth Module**

Use the following test cases to verify that **Ossarth** is correctly generating tools and functions:

```python
from ossarth.tool_manager import CustomFunctionManager

manager = CustomFunctionManager(result_dir="tests")

# Test AI tool creation
manager.create_custom_tool(
    func_name="test_tool",
    description="A test tool function.",
    params="param1: int, param2: str",
    args_doc="param1 (int): An integer.\nparam2 (str): A string.",
    return_type="str",
    return_desc="A formatted string.",
    body="return f'Test tool with {param1} and {param2}'",
    filename="new"
)

# Test helper function creation
manager.create_custom_function(
    func_name="test_function",
    description="A test helper function.",
    params="x: int, y: int",
    args_doc="x (int): First number.\ny (int): Second number.",
    return_type="int",
    return_desc="Sum of x and y.",
    body="return x + y",
    filename="new"
)
```

These tests will ensure that **Ossarth** is correctly generating **AI tools and helper functions** for the OS.

---

## **License**

**Ossarth** is licensed under the **MIT License**. You are free to modify and distribute it.

---

## **Contributing**

We welcome contributions!

To contribute:

1. **Fork the repository**.
2. **Make your changes in a new branch**.
3. **Submit a pull request**.

---

## **Contact & Support**

For any questions or support:  
📧 **Email:** siddharthmagesh007@gmail.com  
🐙 **GitHub:** [Siddharth-magesh](https://github.com/Siddharth-magesh/Ossarth)

---
