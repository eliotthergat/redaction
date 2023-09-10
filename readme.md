<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>redaction
</h1>
<h3>◦ Unlocking the Power of Collaboration</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/SVG-FFB13B.svg?style&logo=SVG&logoColor=black" alt="SVG" />
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style&logo=Streamlit&logoColor=white" alt="Streamlit" />
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style&logo=OpenAI&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style&logo=Docker&logoColor=white" alt="Docker" />
</p>
<img src="https://img.shields.io/github/languages/top/eliotthergat/redaction?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/eliotthergat/redaction?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/eliotthergat/redaction?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/eliotthergat/redaction?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

The codebase located at https://github.com/eliotthergat/redaction is a web application designed to enhance the quality of articles by providing various functionalities. It includes features such as article scraping from URLs, data cleaning, text analysis, text summarization, generation of better titles, fact-checking, and bolding keywords. The project aims to streamline the article creation process, improve the accuracy and reliability of content, and provide user-friendly options for article generation and enhancement. The use of technologies such as Streamlit, BeautifulSoup, OpenAI, PIL, and Markdownify adds value to the project by ensuring a smooth and efficient user experience.

---

## ⚙️ Features

| Feature                | Description                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| **⚙️ Architecture**     | The codebase is organized into modular components that use Streamlit and OpenAI APIs. It follows a client-server architectural pattern, with the Streamlit app serving as the frontend and the OpenAI APIs as backend services.                                             |
| **📖 Documentation**   | The codebase lacks extensive documentation. Some functions have descriptive docstrings, but an overall improvement in documentation is needed for better understanding and maintainability. |
| **🔗 Dependencies**    | The codebase relies on external libraries such as Streamlit, BeautifulSoup, OpenAI, and PIL for web and text processing, as well as Docker for containerization.      |
| **🧩 Modularity**      | The codebase demonstrates modularity by dividing the system's functionalities into separate components, allowing for easier code maintenance and reusability.                                                                |
| **✔️ Testing**          | The codebase does not mention specific testing strategies or tools. Incorporating automated tests would enhance the reliability and stability of the system.                                                                        |
| **⚡️ Performance**      | The codebase does not have performance optimizations mentioned explicitly. However, the system's efficiency could depend on the responsiveness and accuracy of the OpenAI APIs and the network's speed.                    |
| **🔐 Security**        | The codebase does not explicitly address security measures. It may require implementation of security practices such as input validation, authentication, and secure storage for sensitive data.                      |
| **🔀 Version Control** | The codebase uses Git for version control. The repository on GitHub allows for branching, merging, and tracking of changes, facilitating collaborative development and code management.                                        |
| **🔌 Integrations**    | The system directly integrates with OpenAI APIs for text generation, analysis, and fact-checking. It also utilizes external libraries like BeautifulSoup and PIL for web scraping and image processing, respectively.        |
| **📶 Scalability**     | The scalability of the system depends on the scalability of the external services it relies on, such as the OpenAI APIs. The codebase itself does not implement specific measures for handling high load or scaling the infrastructure.   |

---


## 📂 Project Structure




---

## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                                         | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                          | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [home.py](https://github.com/eliotthergat/redaction/blob/main/home.py)       | This code is a web application that helps in generating better quality articles. It uses various functionalities, such as scrapping articles from URLs, data cleaning, analyzing article content, generating summaries, writing articles based on provided title, plan, and keywords, fact-checking, suggesting title improvements, and bolding keywords. It also includes user-friendly features like sidebar, toggles, and download options. The code makes use of packages like Streamlit, BeautifulSoup, OpenAI, PIL, and Markdownify. |
| [Dockerfile](https://github.com/eliotthergat/redaction/blob/main/Dockerfile) | This Dockerfile sets up a Python 3.9 slim container. It installs necessary dependencies, copies the files, installs required Python packages, exposes port 8080, adds a health check, and starts the Streamlit app at port 8080 with the entrypoint command.                                                                                                                                                                                                                                                                               |

</details>

<details closed><summary>Components</summary>

| File                                                                                    | Summary                                                                                                                                                                                                                                                                                                      |
| ---                                                                                     | ---                                                                                                                                                                                                                                                                                                          |
| [sidebar.py](https://github.com/eliotthergat/redaction/blob/main/components/sidebar.py) | This code implements a Streamlit app for a text generation tool called Khontenu. It allows users to enter an OpenAI API key, select text inputs, provide a title and plan, input keywords, and choose various options for generating text. The app also displays information about the tool and its credits. |

</details>

<details closed><summary>Functions</summary>

| File                                                                                                             | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                                              | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [concurrent_analyzer.py](https://github.com/eliotthergat/redaction/blob/main/functions/concurrent_analyzer.py)   | This code defines a function called `concurrent_analyzer` that conducts text analysis using OpenAI Chat Completion API. It handles various API errors, retries failed requests, and tracks usage statistics. The function takes in `text` and `plan` as input, and returns the generated response.                                                                                                                                                                                                                                         |
| [fact_check.py](https://github.com/eliotthergat/redaction/blob/main/functions/fact_check.py)                     | This code defines a function called "fact_check" that interacts with the OpenAI API to perform fact checking. It takes a text input, sends it as a message to the API, and receives a response. It handles various error scenarios, retries failed requests, and tracks usage statistics. The main goal is to provide accurate and reliable fact checking by leveraging the power of the OpenAI model.                                                                                                                                     |
| [better_titles.py](https://github.com/eliotthergat/redaction/blob/main/functions/better_titles.py)               | This code utilizes the OpenAI GPT-4 model to generate better titles for a given text and information. It handles various types of OpenAI API errors and retries the requests with a configured number of attempts. The function "better_titles" takes in the text and information as input and returns a generated title.                                                                                                                                                                                                                  |
| [markdown_generator.py](https://github.com/eliotthergat/redaction/blob/main/functions/markdown_generator.py)     | This code is a function that generates markdown text using the OpenAI ChatCompletion API. It takes in a user input, makes a request to the API, and returns the generated markdown text. The function also includes error handling for various API exceptions.                                                                                                                                                                                                                                                                             |
| [completer.py](https://github.com/eliotthergat/redaction/blob/main/functions/completer.py)                       | This code is a completer function that interacts with the OpenAI ChatCompletion API. It receives text, information, title, plan, and keywords as input and returns completion suggestions based on the given inputs. It handles various errors that may occur during the API request process and provides retry functionality.                                                                                                                                                                                                             |
| [parser.py](https://github.com/eliotthergat/redaction/blob/main/functions/parser.py)                             | This code is a web scraping tool that parses a given HTML page and removes unnecessary elements such as images, scripts, links, and styling classes. It then extracts the main content of the page and converts it into Markdown text.                                                                                                                                                                                                                                                                                                     |
| [bolder_keywords.py](https://github.com/eliotthergat/redaction/blob/main/functions/bolder_keywords.py)           | The code is a Python script that uses OpenAI's ChatCompletion model to highlight keywords in a given text. It takes in a text input, sends it to the OpenAI API, and retrieves the response. The response is then processed to extract the important keywords and format them in bold using the Markdown format. The script also handles various error scenarios and retries the API calls if necessary. The code relies on the OpenAI Python library, as well as other dependencies like Streamlit, requests, Beautiful Soup, and dotenv. |
| [concurrent_sumerizer.py](https://github.com/eliotthergat/redaction/blob/main/functions/concurrent_sumerizer.py) | This code defines a function called `concurrent_summarizer` that uses the OpenAI API to generate a summary of given input text. It handles various exceptions and retries in case of API errors. The function takes three responses as input and combines them into a single list. The generated summary is returned as the output.                                                                                                                                                                                                        |
| [writer.py](https://github.com/eliotthergat/redaction/blob/main/functions/writer.py)                             | This code is a writer function that uses the OpenAI Chat Completion model to generate text based on given information, title, plan, and keywords. It handles various errors that may occur during the API request, retries if necessary, and keeps track of usage statistics.                                                                                                                                                                                                                                                              |
| [define_client.py](https://github.com/eliotthergat/redaction/blob/main/functions/define_client.py)               | Prompt exceeds max token limit: 4713.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

</details>

---

## 🚀 Getting Started

### ✔️ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - `ℹ️ Requirement 1`
> - `ℹ️ Requirement 2`
> - `ℹ️ ...`

### 📦 Installation

1. Clone the redaction repository:
```sh
git clone https://github.com/eliotthergat/redaction
```

2. Change to the project directory:
```sh
cd redaction
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using redaction

```sh
python main.py
```

### 🧪 Running Tests
```sh
pytest
```

---


## 🗺 Roadmap

> - [X] `ℹ️  Task 1: Implement X`
> - [ ] `ℹ️  Task 2: Refactor Y`
> - [ ] `ℹ️ ...`


---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 📄 License

This project is licensed under the `ℹ️  INSERT-LICENSE-TYPE` License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional info.

---

## 👏 Acknowledgments

> - `ℹ️  List any resources, contributors, inspiration, etc.`

---
