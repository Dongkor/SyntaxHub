use std::process::Command;

// #[tauri::command]
// fn greet(name: &str) -> String {
//     format!("Hello, {}! You've been greeted from Rust!", name)
// }

#[tauri::command]
fn run_python_compiler(mut file_path: String) {
    // Replace this with the path to your Python script
    let git_bash_path = "C:/Program Files/Git/git-bash.exe";

    // let python_command = format!(
    //     "python C:/Users/Dongkor/Desktop/junior/124/IDE/124_compiler/main.py {}",
    //     file_path
    // );

    // let test = format!("echo 'hello world'");
    file_path = file_path.replace("\\", "/");
    // Run the Python script using `python` or `python3`
    // println!(python_command);
    let command = format!(
        "python C:/Users/Dongkor/Desktop/junior/124/IDE/124_compiler/main.py {}; exec bash",
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
    // Replace this with the path to your Python script
    let git_bash_path = "C:/Program Files/Git/git-bash.exe";

    // let python_command = format!(
    //     "python C:/Users/Dongkor/Desktop/junior/124/IDE/124_compiler/main.py {}",
    //     file_path
    // );

    // let test = format!("echo 'hello world'");
    file_path = file_path.replace("\\", "/");
    // Run the Python script using `python` or `python3`
    // println!(python_command);
    let command = format!(
        "python C:/Users/Dongkor/Desktop/junior/124/IDE/124_compiler/main.py {} {}; exec bash",
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
    Command::new("C:/Program Files/Git/git-bash.exe")
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
