import os
import zipfile
import subprocess
import shutil
from pathlib import Path

current_dir = Path("./ZIP")
out_dir = Path("./JAR")
dependency_jar = Path("./elevator2.jar")
os.makedirs(out_dir, exist_ok=True)


def find_main_class(classes_dir):
    main_classes = []
    for class_file in classes_dir.glob("**/*.class"):
        relative_path = class_file.relative_to(classes_dir)
        class_name = str(relative_path).replace(os.sep, '.')[:-6]
        result = subprocess.run(
            ['javap', '-public', class_name],
            cwd=classes_dir,
            capture_output=True,
            text=True
        )
        if 'public static void main(java.lang.String[])' in result.stdout:
            main_classes.append(class_name)
    if not main_classes:
        raise ValueError("未找到包含main方法的类")
    elif len(main_classes) > 1:
        raise ValueError(f"发现多个主类: {', '.join(main_classes)}")
    return main_classes[0]


def create_executable_jar(classes_dir, jar_path):
    manifest = None
    try:
        main_class = find_main_class(classes_dir)
        print(f"检测到主类: {main_class}")
        manifest = classes_dir / "MANIFEST.MF"
        manifest.write_text(
            f"Manifest-Version: 1.0\n"
            f"Main-Class: {main_class}\n"
            f"Class-Path: elevator1.jar\n"
            f"Created-By: Auto JAR Builder\n"
        )
        subprocess.run(
            ['jar', 'cvfm', str(jar_path), str(manifest), '-C', str(classes_dir), '.'],
            check=True,
            capture_output=True,
            text=True
        )
    finally:
        if manifest is not None:
            manifest.unlink()


def process_zip(zip_path, output_dir):
    extract_dir = output_dir / f"temp_{zip_path.stem}"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    src_dir = extract_dir / "src"
    if not src_dir.exists():
        src_dir = extract_dir
    classes_dir = extract_dir / "classes"
    classes_dir.mkdir(exist_ok=True)
    java_files = list(src_dir.glob("**/*.java"))
    if not java_files:
        raise ValueError(f"没有找到Java文件: {zip_path.name}")
    compile_result = subprocess.run(
        ['javac', '-d', str(classes_dir), '-encoding', 'UTF-8', '-cp', str(dependency_jar)] + [str(f) for f in
                                                                                               java_files],
        capture_output=True,
        text=True
    )
    if compile_result.returncode != 0:
        error_msg = f"编译失败: {zip_path.name}\n{compile_result.stderr}"
        raise RuntimeError(error_msg)
    jar_path = output_dir / f"{zip_path.stem}.jar"
    if jar_path.exists():
        jar_path.unlink()
    create_executable_jar(classes_dir, jar_path)
    shutil.copy2(dependency_jar, output_dir)
    print(f"成功生成: {jar_path.name}")
    shutil.rmtree(extract_dir)


if __name__ == "__main__":
    zip_files = list(current_dir.glob("*.zip"))
    if zip_files:
        for zip_file in zip_files:
            try:
                print(f"\n正在处理: {zip_file.name}")
                process_zip(zip_file, out_dir)
            except Exception as e:
                print(f"处理失败: {zip_file.name}")
                print(f"错误详情: {str(e)}")
                print("=" * 50)
