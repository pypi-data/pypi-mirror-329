# **XPM**
Xidware Python project Manager

## **Specification**

### **Development Environment**
- **Operating System**: Windows
- **Python Version**: Python 3.10.11
- **Editor**: Visual Studio Code (VSCode)

### **Supported Environments**
- **Operating Systems**: Windows, Linux, macOS
- **Python Version**: Python 3.9.7+
- **Editor**: Any editor (VSCode, PyCharm, etc.)

## **Manual**

### **Installation**
To install `xpm`, use the following pip command:
```cmd
pip install xid-xpm
```


1. 패키지 `pip install xid-xpm` 혹은 CLI 프로그램 설치. `xid-xpm`
2. 환경 변수 등록. `PATH=...`
3. 프로젝트를 구축. `xpm new`
	- Windows: xpm.bat, project.xml
	- Linux/MacOS: xpm.sh, project.xml
4. xml 편집.
5. 프로젝트를 재구축. `xpm update`
	- Windows: project.bat, project.xml
	- Linux/MacOS: project.sh, project.xml
4. 프로젝트를 생성된 스크립트로 제어.
	- Windows: project venvUpdate
	- Linux/MacOS: ./project.sh venvUpdate
5. 바이너리 빌드.
	- Windows: project buildExecutable
	- Linux/MacOS: ./project.sh buildExecutable
6. 라이브러리 빌드.
	- Windows: project buildLibrary
	- Linux/MacOS: ./project.sh buildLibrary

```xml
<XPM Project="">
	<Project Name="" Version="" />
</XPM>
```