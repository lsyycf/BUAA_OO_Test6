import subprocess


def runner(name, os):
    input_path = rf"./datainput_student_linux_x86_64" if os == 'Linux' else rf"datainput_student_win64.exe"
    jar_path = rf"./JAR/{name}.jar" if os == 'Linux' else rf"JAR\{name}.jar"
    try:
        command = rf'{input_path} | java -jar {jar_path} > stdout.txt'
        subprocess.run(command, shell=True, check=True, timeout=90)
        return ''
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded!\n"


if __name__ == "__main__":
    runner("LHL", "Linux")
