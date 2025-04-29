# features/environment.py

import time
from datadog import initialize, statsd
import os

# Initialize Datadog StatsD client
# The datadog-ci run command (added later to the workflow) will automatically
# configure the agent host and port via environment variables (DD_AGENT_HOST, DD_DOGSTATSD_PORT)
# If running locally without the wrapper, ensure DD_AGENT_HOST is set or DogStatsD is running on localhost:8125
options = {
    # Optional: Add default tags to all metrics sent from this environment
    # Example: Check for GitHub Actions environment variables
    "statsd_default_tags": [
        f"repository:{os.environ.get('GITHUB_REPOSITORY', 'unknown')}",
        f"workflow:{os.environ.get('GITHUB_WORKFLOW', 'unknown')}",
        f"run_id:{os.environ.get('GITHUB_RUN_ID', 'unknown')}",
        f"commit:{os.environ.get('GITHUB_SHA', 'unknown')}",
        f"branch:{os.environ.get('GITHUB_REF_NAME', 'unknown')}"
    ]
}
initialize(**options)

def before_all(context):
    """Set up test environment before all features.
    Initialize counters for custom metrics.
    """
    context.start_time = time.time()
    context.scenario_count = 0
    context.passed_scenarios = 0
    context.failed_scenarios = 0
    context.skipped_scenarios = 0
    context.tag_counts = {}

def before_scenario(context, scenario):
    """Set up before each scenario.
    Record scenario start time.
    """
    context.scenario_start_time = time.time()

def after_scenario(context, scenario):
    """Clean up after each scenario.
    Increment counters based on scenario status and send scenario duration.
    """
    context.scenario_count += 1
    scenario_duration_ms = (time.time() - context.scenario_start_time) * 1000

    # Common tags for scenario metrics
    scenario_tags = [
        f"feature:{scenario.feature.name}",
        f"scenario:{scenario.name}"
    ]
    scenario_tags.extend([f"tag:{tag}" for tag in scenario.tags])

    # Send scenario duration as a distribution metric
    statsd.distribution("behave.scenario.duration", scenario_duration_ms, tags=scenario_tags)

    # Increment status counters
    if scenario.status == "passed":
        context.passed_scenarios += 1
        statsd.increment("behave.scenario.passed", tags=scenario_tags)
    elif scenario.status == "failed":
        context.failed_scenarios += 1
        statsd.increment("behave.scenario.failed", tags=scenario_tags)
    elif scenario.status == "skipped":
        context.skipped_scenarios += 1
        statsd.increment("behave.scenario.skipped", tags=scenario_tags)
    else:
        # Handle other statuses if necessary (untested, etc.)
        statsd.increment("behave.scenario.other", tags=scenario_tags)

    # Count scenarios per tag
    for tag in scenario.tags:
        context.tag_counts[tag] = context.tag_counts.get(tag, 0) + 1

def after_all(context):
    """Clean up after all features.
    Send summary custom metrics to Datadog.
    """
    total_duration_s = time.time() - context.start_time

    # Send summary counts
    statsd.gauge("behave.run.total_scenarios", context.scenario_count)
    statsd.gauge("behave.run.passed_scenarios", context.passed_scenarios)
    statsd.gauge("behave.run.failed_scenarios", context.failed_scenarios)
    statsd.gauge("behave.run.skipped_scenarios", context.skipped_scenarios)

    # Send overall run duration
    statsd.gauge("behave.run.duration", total_duration_s)

    # Send counts per tag
    for tag, count in context.tag_counts.items():
        statsd.gauge(f"behave.run.tag.{tag}.count", count)

    print("\nCustom Datadog Metrics Sent:")
    print(f"- Total Scenarios: {context.scenario_count}")
    print(f"- Passed: {context.passed_scenarios}")
    print(f"- Failed: {context.failed_scenarios}")
    print(f"- Skipped: {context.skipped_scenarios}")
    print(f"- Run Duration: {total_duration_s:.2f}s")
    print(f"- Tag Counts: {context.tag_counts}")

    # Ensure all buffered metrics are sent
    statsd.flush()

