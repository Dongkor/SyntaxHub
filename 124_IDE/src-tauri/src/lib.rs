use std::process::Command;

#[tauri::command]
fn run_python_compiler(mut file_path: String) {
    let git_bash_path = "C:/path/to/git-bash.exe"; // Replace this with the path to your git-bash executable file

    file_path = file_path.replace("\\", "/");

    let command = format!(
        //Replace this with the path to the compiler script file from IDE folder
        "python C:/path/to/project-directory/compiler/main.py {}; exec bash",
        file_path
    );

    match Command::new(git_bash_path).arg("-c").arg(command).spawn() {
        Ok(_) => {
            println!("Git Bash started successfully with Python compiler!");
        }
        Err(e) => {
            eprintln!("Failed to start Git Bash: {}", e);
        }
    }
}

#[tauri::command]
fn compile_only(mut file_path: String) {
    let git_bash_path = "C:/path/to/git-bash.exe"; // Replace this with the path to your git-bash executable file

    file_path = file_path.replace("\\", "/");
    let command = format!(
        //Replace this with the path to the compiler script file from IDE folder
        "python C:/path/to/project-directory/compiler/main.py {} {}; exec bash",
        file_path, "yes"
    );

    match Command::new(git_bash_path).arg("-c").arg(command).spawn() {
        Ok(_) => {
            println!("Git Bash started successfully with Python compiler!");
        }
        Err(e) => {
            eprintln!("Failed to start Git Bash: {}", e);
        }
    }
}

#[tauri::command]
fn open_git_bash() -> Result<String, String> {
    println!("Hey");
    Command::new("C:/path/to/git-bash.exe")
        .spawn()
        .map_err(|e| format!("Failed to open Git Bash: {}", e))?;
    Ok("Git Bash launched successfully!".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_clipboard_manager::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            open_git_bash,
            run_python_compiler,
            compile_only
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
