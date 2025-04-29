# Loyalty Program Application

This repository contains a simple Python application for managing airline loyalty points, along with a BDD test suite using Behave, Allure reporting, and Datadog CI Visibility integration.

## Application

The `app.py` file contains a `LoyaltyProgram` class that manages member points and tiers. It allows adding members, adding points, redeeming points, and checking member status (points and tier).

## BDD Tests (Behave)

The BDD tests are located in the `features/` directory:

*   `loyalty_program.feature`: Contains scenarios written in Gherkin syntax describing how the loyalty program functionality should behave.
*   `features/steps/loyalty_program_steps.py`: Contains the Python code (step definitions) that implements the steps defined in the feature file.
*   `features/environment.py`: Contains hooks that run before/after scenarios and features, used here to send custom metrics to Datadog.

### Tags

Scenarios are tagged for selective execution:

*   `@sanity`: Critical, fast-running checks.
*   `@critical`: Tests covering the most important functionality.
*   `@edgecase`: Tests for boundary conditions.
*   `@negative`: Tests for invalid inputs or expected failures.

## Running Tests Locally

1.  **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Behave tests (without Datadog):**
    ```bash
    behave features/
    ```

4.  **Run specific tags (without Datadog):**
    ```bash
    behave --tags=@sanity features/
    behave --tags="@critical and not @sanity" features/
    ```

## Datadog CI Visibility Integration

This project integrates with Datadog CI Visibility using a combination of methods:

1.  **Pipeline Visibility (via GitHub App):**
    *   Datadog automatically tracks the execution, status, and duration of your GitHub Actions workflows and jobs through the **Datadog GitHub App integration**.
    *   **Action Required:** You need to install and configure the Datadog GitHub App in your GitHub organization/repository and enable CI Visibility for the repository in your Datadog account settings. Follow the [Datadog documentation](https://docs.datadoghq.com/continuous_integration/pipelines/github/) for setup.

2.  **Test Results (via JUnit Upload):**
    *   The GitHub Actions workflow runs Behave tests with the `--junit` flag to generate JUnit XML reports.
    *   The `@datadog/datadog-ci` CLI tool is then used to upload these JUnit reports to Datadog.
    *   This populates the **CI > Tests** view in Datadog with individual test scenario results (pass/fail/skip, duration, errors).

3.  **Custom Metrics (via `environment.py`):**
    *   The `features/environment.py` file uses the `datadog` Python library (StatsD) to send custom metrics during the test run, including:
        *   `behave.scenario.duration` (distribution): Duration of each scenario.
        *   `behave.scenario.passed`, `behave.scenario.failed`, `behave.scenario.skipped` (counts): Status counts per scenario.
        *   `behave.run.total_scenarios`, `behave.run.passed_scenarios`, etc. (gauges): Summary counts for the entire run.
        *   `behave.run.duration` (gauge): Total duration of the test run.
        *   `behave.run.tag.<tag_name>.count` (gauges): Count of scenarios executed for each tag.
    *   These metrics provide additional insights beyond the standard JUnit results and can be used in Datadog dashboards and monitors.

### Running Locally with Datadog Integration

To send test results and custom metrics to Datadog when running locally:

1.  **Install Datadog Agent or DogStatsD:** Ensure you have the Datadog Agent running locally or DogStatsD available to receive custom metrics. Set the `DD_AGENT_HOST` environment variable if it's not running on `localhost`.

2.  **Install `datadog-ci` CLI:**
    ```bash
    npm install --global @datadog/datadog-ci
    ```

3.  **Set Environment Variables:**
    *   `DD_API_KEY`: Your Datadog API key. **Keep this secret.**
    *   `DD_SITE`: Your Datadog site (e.g., `datadoghq.eu`).
    *   `DD_ENV` (optional): Environment tag (e.g., `local`).
    *   `DD_SERVICE` (optional): Service name (e.g., `loyalty-program-tests`).

    Example (replace `<your_api_key>`):
    ```bash
    export DD_API_KEY=<your_api_key>
    export DD_SITE=datadoghq.eu
    export DD_ENV=local
    export DD_SERVICE=loyalty-program-tests
    # export DD_AGENT_HOST=<agent_hostname_if_not_localhost>
    ```

4.  **Run Tests and Upload:**
    ```bash
    # Run Behave with JUnit output
    behave --junit --junit-directory junit-results features/

    # Upload JUnit results
    datadog-ci junit upload --service $DD_SERVICE junit-results
    ```
    The custom metrics from `environment.py` will be sent automatically via DogStatsD during the `behave` run.

## Allure Reporting

Allure reporting can still be used alongside Datadog.

1.  **Run tests with Allure and JUnit formatters:**
    ```bash
    # Ensure Datadog environment variables are set if sending data locally
    behave --junit --junit-directory junit-results -f allure_behave.formatter:AllureFormatter -o allure-results features/
    ```

2.  **Upload JUnit to Datadog (Optional for local runs):**
    ```bash
    datadog-ci junit upload --service $DD_SERVICE junit-results
    ```

3.  **Generate and view the Allure HTML report:**
    ```bash
    allure serve allure-results/
    ```

## GitHub Actions

A GitHub Actions workflow is defined in `.github/workflows/run-tests.yml`. This workflow automatically:

*   Checks out the code.
*   Sets up Python and Node.js.
*   Installs Python dependencies and `@datadog/datadog-ci`.
*   Runs Behave tests, generating both JUnit XML and Allure results.
*   Uploads JUnit XML results to Datadog CI Visibility using `datadog-ci junit upload` (requires `DD_API_KEY` secret).
*   Sends custom metrics via DogStatsD (picked up automatically by the Agent configured by `datadog-ci`).
*   Generates an Allure report and deploys it to GitHub Pages.

**Note:**
*   You need to configure `DD_API_KEY` as a secret in your GitHub repository settings.
*   Ensure the Datadog GitHub App integration is configured for pipeline visibility.
