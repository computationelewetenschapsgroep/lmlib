## Using `lmlib` Locally

Follow these steps to use `lmlib` locally:

### 1. Clone the Repository


1. `cd lmlib` 

### 2. Set Up a Virtual Environment

-   Create the virtual environment:
     
    `python -m venv venv` 
    
-   Activate the virtual environment:
    
    -   macOS:
        `source venv/bin/activate` 

### 3. Install the Library

`pip install  .` 
or
`pip install -e .`  (installs the package in _editable_ mode, meaning any changes made to the source code will be immediately available without needing to reinstall the package)

### 4. Use the Library

1. 

    from lmlib.trajectory_processing import processor
    
    processor = processor.Processor()
    processor.calculate_distance()

2. 

    from lmlib.schedule_monitor import ScheduleMonitor
    sm = ScheduleMonitor()
    sm.monitor_schedule()