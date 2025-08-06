# ResumeManager

A lightweight desktop app to manage and download resume files without cluttering your Downloads folder with duplicates like `resume(1).pdf`. Selecting a resume and downloading it will automatically save it to your computer and automatically replace the exisitng `your_name_resume.pdf` file that may exist already. Built with Python and Tkinter.

![alt text](https://github.com/arnav-42/ResumeManager/blob/main/demo.png?raw=true)

## Features

- Upload and store multiple PDF (or other supported) files
- Download any stored file as a single consistent name (e.g., `john_smith_resume.pdf`)
- Automatically deletes any existing file with the same name before downloading
- File storage persists across app restarts
- Delete uploaded files from the app
- Easily edit settings via a built-in configuration panel


## Configuration

Settings are stored in `config.json`:

```json
{
  "target_name": "john_smith_resume",
  "file_extension": ".pdf",
  "download_folder": "~/Downloads"
}
```

* `target_name`: The filename the selected file will download as.
* `file_extension`: The allowed file type (e.g., `.pdf`, `.docx`)
* `download_folder`: The folder to save the downloaded file to.

You can edit this manually or by clicking the **Settings** button inside the app.

## Storage

All uploaded files are stored locally at:

```
~/.resume_app_storage/
```

Files are renamed to unique IDs, and a persistent index tracks their original names.