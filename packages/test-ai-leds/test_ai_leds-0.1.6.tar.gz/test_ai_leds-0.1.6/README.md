*test-ai-leds is the python package that powers the [Test.AI](https://marketplace.visualstudio.com/items?itemName=GabrieldePaulaBrunetti.test-ai) VS code extension*

# Test.AI Extension for VS Code

Test.AI is a powerful Visual Studio Code extension designed to simplify the process of creating Behavior-Driven Development (BDD) tests for software. By leveraging generative AI and agents, Test.AI converts `.andes` files into Gherkin `.feature` files and auto-generates corresponding step definitions. This automation significantly reduces the time and effort required to develop comprehensive BDD tests.

## Features

- **Conversion of .andes Files to Gherkin**: Automatically transforms user stories described in `.andes` files into Gherkin `.feature` files.
- **Step Definition Generation**: Generates step definitions for the `.feature` files to streamline test development. Currently, step definitions are generated exclusively for **C#**, with plans to support additional languages in the future.
- **AI-Powered Automation**: Utilizes large language models (LLMs) to ensure high-quality and context-aware test generation.
- **Seamless Integration**: Works directly within Visual Studio Code, providing a smooth development experience.

## Installation

1. Open Visual Studio Code.
2. Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`.
3. Search for `Test.AI`.
4. Click `Install`.

## Getting Started

### Prerequisites
- Python
- Python package [test-ai-leds](https://pypi.org/project/test-ai-leds/)
- `.andes` files describing user cases in the expected format.
- An active internet connection for AI-based generation.
- A `.env` file in the root folder of your VS Code project containing the following variables:
  - `DTO_SOURCE`: The full path to the DTO files directory in your project.
  - `SWAGGER_PATH`: The full path to the Swagger document of your project.
  - `LLM_MODEL`: The AI model chosen by the user.
  - `API_KEY`: The API key for the AI model being used.


### Setup

**First you need to install test-ai-leds by running `pip install test-ai-leds` in the terminal.**
You can either install globally or in a virtual environment.

**It is also necessary to add the Python package scripts directory to the PATH environment variable. Below is an explanation of how to do this:**

- **Windows**:
  - Run `pip show test-ai-leds` in the terminal.
  - Some information will be returned, including the location of the installed packages. It will look something like:
    `C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages`
  - You just need to change the last directory from `site-packages` to `Scripts`. For example:
    `C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts`
  - Add this path to your environment variables.
  - **Note**: The same can be done using Python virtual environments if you do not want to install the library globally. In that case, the `Scripts` path will be relative to the venv folder.

- **Linux**:
  - Linux does not allow global installations of Python packages. Therefore, you need to create a virtual environment using the command:  
    `python -m venv <venv_name>`
  - Activate the venv with:  
    `source <path_to_venv>/bin/activate`
  - Run: `pip install test-ai-leds`
  - The scripts path on Linux is usually: `<path_to_venv>/bin`
  - Run: `nano ~/.bashrc`
    and add the following at the end of the file: `export PATH=$PATH:/<path_to_your_venv>/bin`
  - Finally, run: `source ~/.bashrc` to apply the changes.
  
### Usage
1. Open a `.andes` file in Visual Studio Code.
2. Right-click on the file and select **Generate BDD Tests with Test.AI**.
3. The extension will:
   - Create a corresponding `.feature` file in the same directory.
   - Generate step definitions and save them in a designated folder (`steps/` by default).
4. Review and refine the generated tests as needed.

## Example

### Input (`example.andes`):
```andes
[User Story]
As a user, I want to log in to my account so that I can access my dashboard.

[Acceptance Criteria]
- Given I am on the login page
- When I enter my username and password
- And I click the login button
- Then I should see the dashboard.
```

### Output (`features/example.feature`):
```gherkin
Feature: User Login

  Scenario: Successful login
    Given I am on the login page
    When I enter my username and password
    And I click the login button
    Then I should see the dashboard.
```

### Generated Step Definitions (`steps/exampleSteps.cs`):
```csharp
using TechTalk.SpecFlow;

[Binding]
public class ExampleSteps
{
    [Given("I am on the login page")]
    public void GivenIAmOnTheLoginPage()
    {
        // Add implementation here
    }

    [When("I enter my username and password")]
    public void WhenIEnterMyUsernameAndPassword()
    {
        // Add implementation here
    }

    [When("I click the login button")]
    public void WhenIClickTheLoginButton()
    {
        // Add implementation here
    }

    [Then("I should see the dashboard")]
    public void ThenIShouldSeeTheDashboard()
    {
        // Add implementation here
    }
}
```

Happy Testing! 🚀
