# Smart Home Control System (Python)

Command-line smart home controller built with object-oriented Python.

## Features

- Device types with inheritance: **Light** (brightness), **Thermostat** (temperature), **Camera** (angle) – all extend a base `Device` class
- Users with access levels (Admin / Guest) – only admins can add or remove users and devices
- Turn devices on/off and edit their settings
- Scheduler for timed device actions
- Users and devices saved to JSON files (`users.json`, `devices.json`)

## Run

```bash
python project.py
```

A project report is included in `project_report.docx`.
